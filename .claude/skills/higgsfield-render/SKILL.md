---
name: higgsfield-render
description: Render a storyboard.json into character reference images, per-shot keyframes, image-to-video clips, and a music track using the Higgsfield MCP tools, recording every job in manifest.json. Use after storyboard (and after the user approved the cost) or to re-render specific shots.
argument-hint: "<production slug> [shot ids to (re)render]"
---

# Higgsfield Render

Requires the Higgsfield MCP connector (`mcp__Higgsfield__*`). If the tools are missing,
stop and tell the user to connect Higgsfield in their claude.ai connector settings.

Inputs: `channel.yaml` (`higgsfield.*` models), `productions/<slug>/storyboard.json`.
Output: `productions/<slug>/manifest.json` (create or update — never discard existing
job ids; they make reruns resumable and cheap).

## 0. Preflight
- Model constraints change: call `mcp__Higgsfield__models_explore` with `action: "get"`
  for the image, video, and music models to confirm supported `aspect_ratio`, `duration`
  values, and `medias[].roles` (e.g. the role name for a start-frame image). Snap shot
  durations to allowed values.
- Call `get_preferences` once; if it says to auto-create projects, call
  `create_project` named after the slug and pass its `default_folder_id` as
  `folder_id` on **every** generation below.
- The cost gate in `shorts-factory` must already be passed. If running standalone,
  estimate and ask first.
- Never set `use_unlim` yourself. If a response contains `unlim_choice`, ask the user,
  then repeat with their answer.

## 1. Character references
For each `characters[]` entry without a `manifest.characters[id].job_id`:
`generate_image_batch` (≤ 12 per call) with `model = higgsfield.image_model`,
`prompt = ref_prompt`, `aspect_ratio: "9:16"`. Wait with `jobs_wait` (repeat until
`all_terminal`), then show them with one `show_generation_by_ids`. **Pause and ask the
user to approve the characters** — everything downstream depends on them.

## 2. Keyframes
For each shot: `generate_image_batch` items with `prompt = keyframe_prompt`,
`aspect_ratio: "9:16"`, and `medias` = the job ids of the characters in
`shot.characters` (use the reference role reported by `models_explore`).
Wait, display, and let the user flag shots to redo before spending on video.

## 3. Video clips
For each shot: `generate_video_batch` items with `model = higgsfield.video_model`,
`prompt = motion_prompt`, `duration = shot.duration` (snapped), `aspect_ratio: "9:16"`,
`medias = [{ value: <keyframe job id>, role: <start-image role> }]`.
Disable or omit native audio unless the model needs it; music is added in assembly.
Wait in groups of ≤ 12; record `video_url` for each terminal job.

## 4. Music
One `generate_audio` with `model = higgsfield.music_model`, `prompt = music.prompt`,
`duration` = total runtime rounded up (integer, Suno: 15–360), instrumental.
Record `music.url`.

## manifest.json
```json
{
  "folder_id": "…",
  "characters": { "boy_young": { "job_id": "…", "url": "…" } },
  "shots": {
    "s01": { "keyframe_job": "…", "keyframe_url": "…", "video_job": "…", "video_url": "…", "status": "completed" }
  },
  "music": { "job_id": "…", "url": "…" },
  "credits_spent": 0
}
```
Write the manifest after **each** stage, so an interrupted run can resume.

## Failures
- `failed` / `nsfw` / `ip_detected`: tell the user the reason, soften the prompt (remove
  anything resembling existing IP or brands), and retry that shot only.
- Transport timeout on submit: do NOT resubmit blindly; check the returned job ids first.
- Inconsistent character in a clip: regenerate the keyframe with stronger reference
  wording before regenerating video.
