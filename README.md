# YouTube AI Organic Content Factory

Claude Code skills that turn an idea into upload-ready, 3D-animated, emotional
"twist ending" YouTube Shorts using the **Higgsfield MCP** for images, video and music.

Inspired by the format of a viral animated reel (wordless story → time jump → heartfelt
payoff). The skills copy the *formula*, never the characters or plot.

## Setup
1. Connect the **Higgsfield** connector in claude.ai (Settings → Connectors) and make
   sure you have credits.
2. Edit `channel.yaml` (channel name, niche, style, models, budget).
3. `ffmpeg` + Python 3 are needed for assembly (pre-installed in Claude Code cloud sessions).

## Usage
In Claude Code, inside this repo:

```
/shorts-factory 3
/shorts-factory 1 a lighthouse keeper and a lost puppy
```

Or run stages individually:

| Command | Does |
|---|---|
| `/story-concept [theme]` | Original concept + beat sheet → `concept.md` |
| `/storyboard <slug>` | Shot list with prompts → `storyboard.json` |
| `/higgsfield-render <slug>` | Character refs → keyframes → clips → music → `manifest.json` |
| `/assemble-short <slug>` | ffmpeg edit → `final.mp4` |
| `/shorts-metadata <slug>` | Titles, description, tags → `metadata.md` |

You approve: the loglines, the estimated credit cost, the character designs, and the
keyframes before video is generated — the expensive step.

## Layout
```
channel.yaml                 channel profile
.claude/skills/              the pipeline skills
productions/<slug>/          one folder per short
```

## Notes
- Mark uploads as "Altered or synthetic content" in YouTube Studio.
- If the content is primarily directed at children, YouTube requires "Made for kids".
