---
name: sofia.synai.ai is the AI Psychologist public route - down again 2026-07-09
description: sofia.synai.ai fronts the ai-psychologist app; brought up 2026-07-07, but container gone and HTTP 530 as of 2026-07-09
type: project
---

`sofia.synai.ai` is the public Cloudflare route for the [AI Psychologist](ai-psychologist.md) app ("Sofia" persona: TTS voice ref `/data/sites/ai-psychologist/voices/sofia.wav`, portrait `sofia.png`, per docker-compose.yml). Brought up and browser-verified in the 2026-07-07 session ("make it 100% functional").

**Status 2026-07-09 (verified):** DOWN. `https://sofia.synai.ai/` returns HTTP 530, `ai-psychologist` container absent from `docker ps -a`, port 3021 unreachable. The container documented as "running, healthy" on Jul 5 no longer exists — needs `docker compose up -d` (not restart) to come back.

Route standard: [synai.ai services CF Access standard](synai-ai-services-always-use-the-cf-access-standard.md).
