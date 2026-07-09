---
name: YouTube Intel Monitoring (yt-intel)
description: YouTube channel monitor at /home/mello/commander/projects/yt-intel/. 6 tracked channels (Simon Scrapes, Nate Herk, Jack Roberts, Mark Kashef, Ryan Hogue, Cole Medin). Auto-analyzes new videos.
type: project
---

## YouTube Intel Monitoring System (yt-intel)

**Location:** /home/mello/commander/projects/yt-intel/
**Settings:** /home/mello/commander/projects/yt-intel/data/settings.json
**Video cache:** /home/mello/commander/projects/yt-intel/data/video_cache/ (7 channel JSON files)
**Status:** Active monitoring system

### What It Does
aiohttp web server (yt_monitor.py) that monitors YouTube channels on configurable intervals, auto-detects new videos via yt-dlp --flat-playlist, extracts transcripts + frames via yt_extract.py, analyzes frames using QwenVL 8B via ComfyUI, and runs Claude (configurable: haiku/sonnet/opus) to produce analysis markdown.

### 6 Actively Tracked Channels:
| Handle | Channel Name | Auto-Analyze | Model | Check Interval |
|--------|-------------|--------------|-------|----------------|
| @SimonScrapes | Simon Scrapes | YES | opus | 6 hours |
| @nateherk | Nate Herk | NO | opus | 3 hours |
| @Itssssss_Jack | Jack Roberts | YES | opus | 6 hours |
| @Mark_Kashef | Mark Kashef | NO | opus | 12 hours |
| @RyanHoguePassiveIncome | Ryan Hogue | NO | sonnet | 6 hours |
| @ColeMedin | Cole Medin | YES | sonnet | 6 hours |

### Cached channel data:
@Chase-H-AI.json, @ColeMedin.json, @Itssssss_Jack.json, @Mark_Kashef.json, @nateherk.json, @RyanHoguePassiveIncome.json, @SimonScrapes.json

### Pipeline:
1. yt-dlp --flat-playlist detects new videos
2. yt_extract.py downloads metadata + transcript + frames (5s intervals)
3. QwenVL 8B via ComfyUI analyzes frames for visual descriptions
4. Claude (haiku/sonnet/opus) produces merged analysis markdown
5. Results stored in manifest + copied to yt-analyses nginx-served directory

Why: yt-intel is the automated YouTube monitoring system that feeds the youtube-analyses/ directory. Not documented in memory.

How to apply: When adding new channels to monitor, edit data/settings.json. Auto-analyze channels get full analysis; others just get cached metadata.
