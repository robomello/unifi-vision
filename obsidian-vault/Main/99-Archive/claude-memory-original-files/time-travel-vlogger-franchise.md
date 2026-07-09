---
name: Time-Travel Vlogger Franchise
description: Three-channel AI YouTube franchise (Joel/Cintia/Claudio) generating 30 viral stories via 7-role Claude CLI pipeline into NocoDB. Active build at /home/mello/commander/projects/time-travel-franchise/
type: project
---

**Status (2026-05-10):** Phase 0-3 complete, Phase 4 (full 30-story run) gated on smoke3 quality + NocoDB base creation by Roberto.

**Concept:** Three YouTube channels, each starring one AI vlogger time-traveler. They don't know each other exist; their edits leak between timelines; recurring background characters appear across channels as audience-decoded Easter eggs.
- **The Save (Joel):** prevents disasters, alt-present is rarely better
- **The Fail (Cintia):** tries, fails, watches it happen
- **Become (Claudio):** slowly realizes he IS the cause of every disaster

**Pipeline:** 7 role-specialized Claude CLI calls per story (showrunner sonnet → writer sonnet → casting haiku → prompt_engineer sonnet → copywriter sonnet → sensitivity haiku → viral_hook sonnet w/ 3-strike retry). 30 stories total (10 per channel), 25-50 shots per story at 5-15s each. ~11-20 min per story, ~2 hr full run at 3-channels concurrent.

**Reference channel studied:** Chloe vs History (1.35M+ views on Titanic vlog). Style guides at `_research/chloe_style_guide.md` and `_research/chloe_shorts_guide.md`. Key insight: Jonathan Laramie (creator) starts from REAL historical source images (paintings, photos), image-to-image to photorealistic, composites Chloe in. Doesn't text-prompt history from scratch.

**Project paths:**
- Code: `/home/mello/commander/projects/time-travel-franchise/`
- Plan: `/home/mello/.claude/plans/time-travel-franchise.md`
- Handoff: `/home/mello/commander/projects/time-travel-franchise/HANDOFF.md`
- Smoke output: `/home/mello/commander/projects/time-travel-franchise/.state/stories/<story_id>/merged.json`

**Downstream stack (decided, not built):**
- Video: HappyHorse (Fal.ai, `happyhorse-agent` exists) for character consistency. Seedance 2.0 fallback (no agent yet).
- Image: Flux 2 Dev local for 3 vlogger hero refs. MyDesigns Dream AI (ChatGPT Image 2) for scene plates.
- Voice: ElevenLabs (voice_id null until cast).

**Outstanding blockers:** Roberto needs to create empty NocoDB base `time_travel_franchise` in the UI; token has no base-create permission. After that, `python -m factory.nocodb_bootstrap <base_id>` auto-creates all 7 tables.

**First smoke result (smoke2):** viral_hook score 88/100. Title "I Saved 146 Triangle Workers and Came Home to This" (Triangle Shirtwaist Factory fire 1911). Only 7 scenes — too few. **smoke3** in flight with Chloe-style edits + 25-50 shot output requirement.
