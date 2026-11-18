---
name: shorts-factory
description: End-to-end pipeline that turns an idea (or nothing) into finished, upload-ready 9:16 animated story Shorts using the Higgsfield MCP — concept, storyboard, character refs, keyframes, video clips, music, assembly, and YouTube metadata. Use when the user asks to "make a short", "make N videos", "run the factory", or gives a reference video/screenshot to emulate.
argument-hint: "[count] [optional theme or reference]"
---

# Shorts Factory (orchestrator)

Produces original, family-friendly, wordless-or-near-wordless 3D-animated micro-stories
(~35–50 s) with an emotional twist ending — the format of the reference reel this repo
was built from (see `story-concept/references/formulas.md`).

## Inputs
- `$ARGUMENTS`: optional count (default `posting.shorts_per_batch` from `channel.yaml`),
  optional theme, optional path to a reference video/image.
- Always read `channel.yaml` first. All skills obey it.

## Pipeline (run in order, one production folder per short)

| # | Stage | Skill | Output in `productions/<slug>/` |
|---|-------|-------|------------------------------|
| 0 | Analyse reference (only if given) | this skill, step 0 | `reference-notes.md` |
| 1 | Concept | `story-concept` | `concept.md` |
| 2 | Storyboard | `storyboard` | `storyboard.json` |
| 3 | **Cost gate** | this skill | user approval |
| 4 | Render | `higgsfield-render` | `manifest.json` |
| 5 | Assemble | `assemble-short` | `final.mp4` |
| 6 | Metadata | `shorts-metadata` | `metadata.md` |

### Step 0 — reference analysis (optional)
If the user supplies a video: `ffprobe` it, then extract a contact sheet
(`ffmpeg -i in.mp4 -vf "fps=1,scale=160:-1,tile=12x6" -frames:v 1 sheet.jpg`) and Read it.
Write `reference-notes.md`: runtime, shot count, avg shot length, beat structure, style,
caption usage, CTA. **Extract the formula, never the characters, names, or plot.**

### Step 1–2
Generate all N concepts first and show the user the loglines in one short list before
storyboarding, so they can veto weak ones cheaply. Then storyboard each approved concept.

### Step 3 — cost gate (mandatory)
Before any generation, call `mcp__Higgsfield__balance` and price one representative
image, video shot, and music track with `estimate_image_cost` / `estimate_video_cost` /
`estimate_audio_cost`. Multiply by the counts in the storyboards and present:
`N shorts × (chars + keyframes + clips + music) ≈ X credits (balance Y)`.
Proceed only if the user approves, or if the total is under
`higgsfield.max_credits_per_short × N` and that value is > 0.
Never set `use_unlim` on your own; if a tool returns `unlim_choice`, ask the user.

### Step 4–6
Run `higgsfield-render`, then `assemble-short`, then `shorts-metadata` for each short.
Batch generations across shorts where possible (batch tools take up to 12 jobs).

## Finish
Report per short: logline, `final.mp4` path + duration, title, and credits spent.
Offer to commit the production folders (media files are git-ignored).

## Guardrails
- Original characters, names, and stories only. No real people, brands, or existing IP.
- Kid-safe: no violence, injury, romance, or scary content; sadness resolves to warmth.
- Do not claim the video will "go viral"; no misleading titles.
- Disclose AI generation: YouTube requires the "Altered or synthetic content" toggle
  for realistic synthetic media — remind the user in the final report.
