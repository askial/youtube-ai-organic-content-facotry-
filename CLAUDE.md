# YouTube AI Organic Content Factory

Produces original 9:16 animated micro-story Shorts with the Higgsfield MCP.

- Channel settings live in `channel.yaml` — read it before any content work.
- Skills (in `.claude/skills/`): `shorts-factory` (orchestrator) → `story-concept` →
  `storyboard` → `higgsfield-render` → `assemble-short` → `shorts-metadata`.
- Each short lives in `productions/<slug>/` (concept.md, storyboard.json, manifest.json,
  metadata.md are committed; clips/audio/mp4 are git-ignored).
- Never spend Higgsfield credits without the cost gate in `shorts-factory` (estimate, then user approval).
- Original characters and stories only; kid-safe; no real brands, people, or existing IP.
