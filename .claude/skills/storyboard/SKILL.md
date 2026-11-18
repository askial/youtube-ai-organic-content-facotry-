---
name: storyboard
description: Turn a story concept into a machine-readable shot list (storyboard.json) with character reference prompts, per-shot keyframe image prompts, motion prompts, durations, captions, and a music prompt — ready for Higgsfield rendering. Use after story-concept or when the user wants to plan shots.
argument-hint: "<production slug>"
---

# Storyboard

Inputs: `channel.yaml`, `productions/<slug>/concept.md`, `references/style-guide.md`.
Output: `productions/<slug>/storyboard.json` matching the schema below.

## Rules
- 8–12 shots (`format.shots_per_story`), each 3–6 s; total ≈ `format.target_seconds`
  and ≤ `format.max_seconds`.
- One action per shot. Vary framing: wide establishing → medium → close-up on faces and
  the symbolic object → wide reveal at the payoff.
- **Every keyframe prompt is self-contained**: restate the style block, the setting, the
  lighting, and each visible character's full visual description (same wording every
  time — consistency comes from repetition plus the character reference images).
- Motion prompts describe only movement and camera (e.g. "slow push-in, he looks up,
  rain falling, umbrella opens"), not appearance — the keyframe carries the look.
- No readable text in prompts except short signs that matter to the story (≤ 3 words,
  in quotes). Never brand names or logos.
- Captions: only the payoff lines (`format.captions`). Leave `caption` null elsewhere.

## Schema
```json
{
  "slug": "lantern-keeper-returns",
  "title": "Working title",
  "aspect_ratio": "9:16",
  "style": "<style block from style-guide.md, adapted to the setting>",
  "characters": [
    {
      "id": "boy_young",
      "description": "10-year-old boy, messy black hair, oversized black hoodie, white sneakers",
      "ref_prompt": "Character reference sheet ... full body, front view, neutral pose, plain background, <style>"
    }
  ],
  "shots": [
    {
      "id": "s01",
      "beat": "HOOK",
      "duration": 4,
      "characters": ["boy_young", "old_man"],
      "keyframe_prompt": "<style>. <setting/light>. <framing>. <full descriptions of visible characters>. <action frozen at start>.",
      "motion_prompt": "<camera move + character motion + ambient motion>",
      "caption": null
    }
  ],
  "music": {
    "prompt": "gentle emotional piano and soft strings, slow build to warm swell at the reveal, no vocals",
    "duration": 45
  }
}
```

After writing, print a compact table (id · beat · duration · one-line action) and total
runtime so the user can sanity-check.
