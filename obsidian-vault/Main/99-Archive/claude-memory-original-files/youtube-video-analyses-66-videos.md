---
name: YouTube Video Analyses (66 videos)
description: 66 YouTube video analyses at /home/mello/commander/projects/youtube-analyses/. Top channels: Cole Medin (12), Simon Scrapes (8), Nate Herk (7). Served by yt-analyses container.
type: project
---

## YouTube Video Analyses (66 videos analyzed)

**Location:** /home/mello/commander/projects/youtube-analyses/
**Output format:** Markdown files named YYYY-MM-DD_channel-name_video-title-slug.md
**Analysis tool:** youtube-analyzer skill at /home/mello/skills/youtube-analyzer/
**Extraction script:** /home/mello/skills/youtube-analyzer/scripts/yt_extract.py
**Serving:** Container yt-analyses (nginx:alpine), static files at /data/sites/yt-analyses, manifest.json

### Each analysis contains:
- Metadata table (channel, published date, duration, views, likes, URL)
- Original description
- Timestamped content breakdown merging transcript + visual frame analysis
- Visual elements catalog
- Key takeaways
- Full transcript in collapsible section

### Top channels analyzed (by frequency):
| Channel | # Analyses | Primary Topics |
|---------|-----------|----------------|
| Cole Medin | 12 | Claude Code, agent teams, subagents, harnesses |
| Simon Scrapes | 8 | Claude Code skills, tips, OpenClaw comparison |
| Nate Herk | 7 | Claude Code workflows, Seedance video, subagents, LLM wikis |
| Jack Roberts | 5 | Claude Code, NotebookLM, Antigravity, Stitch 2.0 |
| Mark Kashef | 4 | Obsidian second brain, Fable mindset, agentic OS |
| Fahd Mirza | 2 | IBM Granite local models |
| Chloe vs History | 1 | AI-generated historical vlogging (1.25M views) |
| Systems by Vic | 1 | Claude skill replacing Higgsfield (78K views) |
| Kun Chen | 1 | L8 Principal engineer agentic workflow (29K views) |
| Jordan Urbs | 1 | AI harness engineering (27K views) |
| Sean Kochel | 1 | 5 vibe coding repos (8K views) |
| IndyDevDan | 1 | Fable 5 banned model analysis |
| Apple Developer | 1 | WWDC26 MLX distributed inference |
| OpenAI | 1 | Codex earnings analysis demo |
| Others | 11 | Etsy, POD, ComfyUI, OCR, Kiraa, video editing |

### Notable high-view videos analyzed:
- Chloe vs History 'Tudor London 1536' — 1,251,036 views (research for time-travel franchise)
- Systems by Vic 'Cancelled Higgsfield' — 78,078 views
- Nate Herk 'Seedance 2.0 + Claude Code' — 76,523 views
- Nate Herk 'Fable 5 + Karpathy LLM Wiki' — 45,872 views
- Kun Chen 'L8 Principal Agentic Workflow' — 29,317 views
- Jordan Urbs 'AI Harness Engineering' — 27,027 views
- Patrick Dang 'Sign First Client with Claude' — 9,822 views
- Sean Kochel '5 NEW Vibe Coding Repos' — 8,205 views

### Skill eval results:
- Baseline: 26/30 assertions passed (86.7%)
- After improvement: 29/30 (96.7%)
- Eval files: /home/mello/skills/youtube-analyzer/evals/evals.json

Why: 66 video analyses represent a significant knowledge base extracted from YouTube. Not documented in memory before.

How to apply: When referencing insights from these videos, check youtube-analyses/ first. The yt-intel system auto-analyzes new videos from tracked channels.
