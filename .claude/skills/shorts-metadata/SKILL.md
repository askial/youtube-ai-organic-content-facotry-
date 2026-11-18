---
name: shorts-metadata
description: Write YouTube Shorts upload metadata for a finished production — title options, description, tags, hashtags, pinned comment, thumbnail frame pick, and posting checklist — into metadata.md. Use after assemble-short or when the user needs titles/descriptions.
argument-hint: "<production slug>"
---

# Shorts Metadata

Inputs: `channel.yaml`, `productions/<slug>/concept.md`, `storyboard.json`, `final.mp4`.
Output: `productions/<slug>/metadata.md`.

## Rules
- **Titles** (give 3, ≤ 60 chars, best first): curiosity about the payoff without
  spoiling it, emotional and honest. Patterns: "He never forgot what she did…",
  "She gave him an umbrella. 10 years later…". No ALL CAPS clickbait, no false claims.
- **Description**: 1–2 sentence hook + one line inviting comments (a question about the
  story), then hashtags: `posting.hashtags_base` + 2–3 story-specific ones. ≤ 5 hashtags
  total is plenty.
- **Tags**: 10–15 short phrases (theme, format, emotion).
- **Pinned comment**: a question that sparks replies ("What would you have done?").
- **Cover frame**: name the timestamp of the most emotional close-up (check frames with
  ffmpeg + Read) — Shorts lets you pick a frame from the video.
- **Posting checklist** (include verbatim):
  - [ ] Mark "Altered or synthetic content" = Yes in YouTube Studio
  - [ ] Set the audience honestly: if the video is primarily directed at children, YouTube (COPPA) requires "Made for kids"
  - [ ] Watch the full video once on a phone before publishing
  - [ ] Schedule; space uploads ≥ 3 h apart

## Template
```markdown
# <slug> — upload metadata
**File:** productions/<slug>/final.mp4 (<duration> s)

## Title options
1. ...
2. ...
3. ...

## Description
...

## Tags
tag, tag, ...

## Pinned comment
...

## Cover frame
<mm:ss> — <what's in it>

## Posting checklist
...
```
