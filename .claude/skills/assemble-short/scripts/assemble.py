#!/usr/bin/env python3
"""Assemble a production folder into final.mp4 (1080x1920, <= max seconds).

Usage: assemble.py productions/<slug> [--no-music] [--no-captions]
                   [--xfade 0.25] [--music-volume 0.6] [--max-seconds 59]
Standard library only; needs ffmpeg and ffprobe on PATH.
"""
import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

W, H, FPS = 1080, 1920, 30


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")
    return r.stdout


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)])
    return float(out.strip())


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "shorts-factory/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def find_existing(folder, stem):
    hits = sorted(folder.glob(f"{stem}.*")) if folder.exists() else []
    return hits[0] if hits else None


def ass_time(t):
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(path, events):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,80,80,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{txt.upper()}"
             for a, b, txt in events]
    path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--xfade", type=float, default=0.25)
    ap.add_argument("--music-volume", type=float, default=0.6)
    ap.add_argument("--max-seconds", type=float, default=59)
    a = ap.parse_args()

    prod = Path(a.production).resolve()
    board = json.loads((prod / "storyboard.json").read_text())
    mpath = prod / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    shots = board["shots"]
    clips_dir, norm_dir, audio_dir = prod / "clips", prod / "clips" / "norm", prod / "audio"
    norm_dir.mkdir(parents=True, exist_ok=True)

    # 1. collect clips
    missing = []
    for s in shots:
        if find_existing(clips_dir, s["id"]):
            continue
        url = manifest.get("shots", {}).get(s["id"], {}).get("video_url")
        if not url:
            missing.append(s["id"])
            continue
        print(f"downloading {s['id']} ...")
        try:
            download(url, clips_dir / f"{s['id']}.mp4")
        except Exception as e:  # network policy / expired URL
            print(f"  failed: {e}")
            missing.append(s["id"])
    if missing:
        sys.exit("missing clips for shots: " + ", ".join(missing) +
                 f"\nRe-render them, or place files at {clips_dir}/<shot>.mp4")

    # 2. normalise
    norm = []
    for s in shots:
        src = find_existing(clips_dir, s["id"])
        dst = norm_dir / f"{s['id']}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                    f"crop={W}:{H},fps={FPS},format=yuv420p,setsar=1",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(dst)])
        norm.append((s, dst, duration(dst)))

    # 3. timeline + concat with crossfades
    xf = max(a.xfade, 0)
    starts, t = [], 0.0
    for i, (_, _, d) in enumerate(norm):
        starts.append(t)
        t += d - (xf if i < len(norm) - 1 else 0)
    total = min(t, a.max_seconds)

    inputs, filt = [], []
    for _, p, _ in norm:
        inputs += ["-i", str(p)]
    if xf > 0 and len(norm) > 1:
        prev = "[0:v]"
        for i in range(1, len(norm)):
            out = f"[v{i}]"
            filt.append(f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:"
                        f"offset={starts[i]:.3f}{out}")
            prev = out
        vlabel = prev
    else:
        filt.append("".join(f"[{i}:v]" for i in range(len(norm))) +
                    f"concat=n={len(norm)}:v=1:a=0[vc]")
        vlabel = "[vc]"

    # 4. captions
    if not a.no_captions:
        events = []
        for i, (s, _, d) in enumerate(norm):
            if s.get("caption"):
                events.append((starts[i] + 0.2, starts[i] + d - 0.2, s["caption"]))
        if events:
            write_ass(prod / "captions.ass", events)
            filt.append(f"{vlabel}subtitles=captions.ass[vs]")
            vlabel = "[vs]"

    # 5. music
    music = None
    if not a.no_music:
        music = find_existing(audio_dir, "music")
        url = manifest.get("music", {}).get("url")
        if not music and url:
            ext = Path(url.split("?")[0]).suffix or ".mp3"
            music = audio_dir / f"music{ext}"
            print("downloading music ...")
            try:
                download(url, music)
            except Exception as e:
                print(f"  music download failed ({e}); continuing without music")
                music = None
    amap = []
    if music:
        idx = len(norm)
        inputs += ["-i", str(music)]
        fade_st = max(total - 1.5, 0)
        filt.append(f"[{idx}:a]atrim=0:{total:.3f},volume={a.music_volume},"
                    f"afade=t=out:st={fade_st:.3f}:d=1.5,loudnorm=I=-14:TP=-1.5[a]")
        amap = ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]

    out = prod / "final.mp4"
    run(["ffmpeg", "-y", "-v", "error", *inputs,
         "-filter_complex", ";".join(filt), "-map", vlabel, *amap,
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], cwd=prod)
    print(f"wrote {out} ({duration(out):.1f}s, {len(norm)} shots)")


if __name__ == "__main__":
    main()
