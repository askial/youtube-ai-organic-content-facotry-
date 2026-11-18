---
name: assemble-short
description: Assemble rendered Higgsfield clips into a final 1080x1920 YouTube Short — download clips, normalise, concatenate in storyboard order with short crossfades, mix music, burn in payoff captions, enforce the ≤ 59 s limit. Use after higgsfield-render or whenever clips need re-cutting.
argument-hint: "<production slug>"
---

# Assemble Short

Requires `ffmpeg`/`ffprobe` and Python 3 (standard library only).

```bash
python3 .claude/skills/assemble-short/scripts/assemble.py productions/<slug>
```

Options: `--no-music`, `--no-captions`, `--xfade 0.25` (seconds; 0 = hard cuts),
`--music-volume 0.6`, `--max-seconds 59`.

What it does:
1. Reads `storyboard.json` + `manifest.json`.
2. Downloads each `video_url` to `clips/<shot>.mp4` (skips ones already present; you can
   also drop files there manually if the CDN host is blocked by the network policy).
3. Normalises every clip to 1080x1920, 30 fps, no audio.
4. Joins them in shot order (crossfades of `--xfade` s).
5. Burns captions from `shot.caption` as bold centred ASS subtitles in the lower third
   during that shot.
6. Adds `audio/music.*` (downloaded from `manifest.music.url`), fades out the last 1.5 s,
   loudness-normalises to −14 LUFS.
7. Trims to `--max-seconds` and writes `final.mp4`; prints duration.

After it runs: extract 3 frames (start, middle, end) and Read them to check visually,
then report the path and duration. If any clip is missing, the script lists the shots
to re-render with `higgsfield-render`.
