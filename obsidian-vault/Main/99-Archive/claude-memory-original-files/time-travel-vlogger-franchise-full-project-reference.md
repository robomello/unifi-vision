---
name: Time-Travel Vlogger Franchise — full project reference
description: Three channels (Save/Fail/Become), public viewer, Telegram bot, pipeline, downstream stack.
type: project
---

**Time-Travel Vlogger Franchise — single source of truth.** Three AI-vlogger YouTube channels in a shared universe. The vloggers don't know each other exist; edits leak between timelines as audience-decoded Easter eggs.

### Channels (renamed 2026-05-11 to "I Made History" trio)

| code | channel | vlogger | premise | tone | launch |
|---|---|---|---|---|---|
| `save` | **I Saved History** | Joel | prevents disaster; alt-present rarely better | hope_then_regret | Q2 2026 |
| `fail` | **I Lost History** | Cintia | tries, fails, watches it happen | meditative_melancholy | Q4 2026 |
| `become` | **I Made History** | Claudio | slowly realizes he IS the cause — the channel name is the payoff | slow_burn_horror | Q1 2027 |

`channel_code` (save/fail/become) is the immutable key everywhere in code and NocoDB; only `channel_name` was renamed.

### Public viewer — https://franchise.synai.ai

Read-only nginx, no auth, public internet. Backed by `franchise-viewer` Docker service (nginx:1.27-alpine), config at `/home/mello/commander/projects/franchise-viewer/nginx.conf`. Cloudflare tunnel `<REDACTED-UUID-2>` (Robomello79@gmail.com account — same tunnel running n8n/nocodb/cmd/comfyui).

| URL path | contents |
|---|---|
| `/` | landing page with channel index |
| `/bible/` | franchise.json, channels.json, vloggers.json, background_chars.json, manifest.json |
| `/stories/` | one dir per story_id with 7 role outputs + merged.json |
| `/hero_refs/` | per-vlogger anchor reference images |
| `/runs/` | per-run artifacts under `<run_id>/` |

### Telegram operator — @Commander_Mello_bot

Container `image-telegram` (service name kept for `TELEGRAM_IMAGE_TOKEN` env-var continuity). `bot.py` locks every `claude --print` call's cwd to the franchise project. Commands: `/channels /status /smoke /run /story /viewer /stop /new /model /end /sessions`. Shortcuts: `!cmd` (bash), `>path` (read), `?pat` (grep), `@haiku|sonnet|opus msg` (one-shot model override). Plain text routes to Claude with the franchise dir as cwd.

### Code layout

```
/home/mello/commander/projects/time-travel-franchise/
  bible/        SHA-256 locked franchise canon (manifest.json)
  factory/      orchestrator, claude_client, persistence, schemas, validators
  runner/       runner.run_generation CLI
  prompts/      9 role prompts
  .state/       stories/, hero_refs/, runs/, current_run_id.txt
  scripts/      maintenance helpers
  tests/        pytest suite
```

### Pipeline

7 roles per story (channels parallel via ThreadPoolExecutor(3), episodes sequential within channel):
```
showrunner -> writer -> casting -> prompt_engineer -> copywriter
                                                   -> sensitivity
                                                   -> viral_hook (3-strike retry)
                                                   -> merged.json
```
Bible integrity enforced at runner start. To re-lock after intentional bible edits:
```python
from pathlib import Path
from factory.persistence import write_bible_manifest
write_bible_manifest(Path("bible"))
```

### Downstream stack (not yet wired)

| stage | tool |
|---|---|
| hero refs (3 vlogger anchors) | Flux 2 Dev local via ComfyUI |
| scene plates (~180 / story) | MyDesigns Dream AI |
| video (character consistency) | HappyHorse via Fal.ai |
| voice | ElevenLabs (no `elevenlabs_voice_id` cast yet) |

### Status (as of 2026-05-11)

Phases 0-3 complete. Smoke3 PASSED (viral_hook 88/100, title "I Saved All 146. The Safety Laws Died With Them.", Triangle Shirtwaist Fire 1911). NocoDB blocker resolved — `.state/nocodb_ids.json` written, all 7 tables created. Phase 4 (full 30-story run) unblocked.

**Why:** Roberto's brain is Obsidian — project knowledge accumulates here, not in per-project CLAUDE.md files. CLAUDE.md in the project dir is kept minimal (just load-bearing facts the bot's `claude --print` needs from cwd).

**How to apply:** When asked about the franchise — channels, viewer, bot, pipeline, status — pull from this entry first. Update this entry when adding pieces, don't sprawl docs across the repo.
