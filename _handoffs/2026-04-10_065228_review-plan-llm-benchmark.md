# Handoff: review_plan.sh Pipeline Upgrade — LLM Benchmark Complete

**Date**: 2026-04-10 06:52:28 (UTC-6)
**Project**: Mello Home Server (`~/.claude/`)
**Branch**: N/A (not a git repo at `/home/mello`)
**Session Summary**: Benchmarked 12 LLMs (cloud + local Ollama) to pick the best 4-model combo for the `review_plan.sh` plan-review hook. User needs to select a pipeline option (A/B/C) before the plan gets written and ExitPlanMode is called.

## Completed This Session
- Ran 12-model benchmark against `~/.claude/plans/cuddly-rolling-scott.md` (skill-improver-agent upgrade plan, 11KB). All outputs saved to `/tmp/llm_benchmark/`.
- Identified that bigger ≠ better: Devstral-2 123B (74GB) underperformed Qwen3-Coder-Next Q4 (51GB).
- Discovered GLM-4.7-Flash Q8 > GLM-4.7-Flash BF16 for instruction-following on this task (quantization helped).
- Confirmed Sonnet 4.6 is uniquely valuable because it checks the actual current implementation state vs. plan claims (caught that cuddly-rolling-scott was already 447 lines, not 405).
- Presented 3 recommended pipeline combinations (Option A/B/C) to the user.

## In Progress
- [ ] **Waiting on user choice**: Option A (Max Quality), Option B (Balanced), or Option C (Fast + Cheap). Last assistant message: "Which option do you want? I'll write the plan for the `review_plan.sh` upgrade around that choice."

## Pending (Not Started)
- [ ] Write the plan file to `~/.claude/plans/tingly-hugging-ullman.md` (this is the plan slug for the current plan-mode session — still empty).
- [ ] Call `ExitPlanMode` once plan is written and approved.
- [ ] Implement the actual `review_plan.sh` edit: replace MiniMax M2.5 (OpenRouter) and GLM-5 (Z.ai API) with 2 local Ollama models per the chosen option.
- [ ] Verify pipeline still runs in both phases (independent reviews + consensus votes).
- [ ] Clean up `/tmp/llm_benchmark/` after implementation is verified.

## Blockers
- None. Just waiting on the user to pick A/B/C.

## Key Decisions Made
- **Decision**: Keep Sonnet 4.6 + Gemini 3.1 Pro as the 2 cloud models in Options A and B (Haiku 4.5 only in C).
  **Reasoning**: Sonnet was the only benchmarked model that actually inspected the current code state instead of reviewing the plan in isolation. Gemini 3.1 Pro gave the most structured critique.
- **Decision**: Use Qwen3-Coder-Next as the primary local model across all 3 options.
  **Reasoning**: Top-scoring local model in the benchmark (A- tier). Q8 at 84GB for max quality, Q4 at 51GB when pairing with a second local model under the 96GB VRAM budget.
- **Decision**: Drop MiniMax M2.5 and GLM-5 (Z.ai API) from the pipeline.
  **Reasoning**: Local models now match/exceed their output quality and avoid external API cost + latency.

## Known Issues
- Devstral-2 123B produced only 615 words despite being the largest model tested. Not recommended for this pipeline.
- GLM-4.7-Flash BF16 version is WORSE than Q8 version on this task — if using GLM-4.7-Flash, must specify Q8.

## Next Steps (Priority Order)
1. **Ask user to select Option A, B, or C** — nothing else moves until this is decided.
2. **Write plan** to `~/.claude/plans/tingly-hugging-ullman.md` with the chosen pipeline. Plan must include `## Team Structure` as the last section (per planning.md rule).
3. **Let consensus review hook fire** automatically on the plan write (do NOT bypass per `feedback_plan_agent_flow.md`).
4. **Incorporate review feedback** then call `ExitPlanMode`.
5. **Implement the hook edit** on `~/.claude/hooks/review_plan.sh`. This is a single-file change touching both Phase 1 (parallel reviews) and Phase 2 (consensus votes).
6. **Test with a throwaway plan write** to confirm all 4 models respond and the consensus phase still works.

## Files Actively Being Edited
- `~/.claude/plans/tingly-hugging-ullman.md` — empty, needs to be written with the chosen pipeline plan.
- `~/.claude/hooks/review_plan.sh` — not yet touched this session. Will be modified in the implementation phase.

## Context for Next Session

### Pipeline Options On The Table

**Option A: Max Quality** (~200s total)
- Sonnet 4.6 + Gemini 3.1 Pro (cloud, parallel)
- Qwen3-Coder-Next Q8 (84GB) + Nemotron-3-Super 120B (86GB)
- Locals run SEQUENTIALLY (can't fit both in 96GB VRAM)

**Option B: Balanced** (~197s total)
- Sonnet 4.6 + Gemini 3.1 Pro (cloud, parallel)
- Qwen3-Coder-Next Q4 (51GB) + GLM-4.7-Flash Q8 (31GB)
- Locals fit PARALLEL at 82GB total VRAM

**Option C: Fast + Cheap** (~98s total)
- Haiku 4.5 (instead of Sonnet) + Gemini 3.1 Pro (cloud, parallel)
- Qwen3-Coder-Next Q4 + GLM-4.7-Flash Q8 (parallel, 82GB)
- 10x cheaper on the cloud side; loses Sonnet's code-state awareness

### Benchmark Top Scores (12 models tested)
- **Sonnet 4.6**: 197s, 1553 words, A+ (checked actual code state)
- **Haiku 4.5**: 98s, 2460 words, A (most thorough, best pseudocode)
- **Gemini 3.1 Pro**: (cloud) A (most structured critique)
- **Qwen3-Coder-Next Q8**: 53s, 1433 words, A- (best local)
- **Nemotron-3-Super 120B**: 108s, 1387 words, A- (self-correcting reasoning)
- **Qwen3-Coder-Next Q4**: A- (tier-matched Q8 for this task)
- **GLM-4.7-Flash Q8**: B+
- **GLM-4.7-Flash BF16**: B (worse than Q8)
- **Devstral-2 123B**: 91s, 615 words, B- (disappointing for size)

### Current Hook Architecture (for the implementation phase)
- Location: `~/.claude/hooks/review_plan.sh`
- Trigger: PostToolUse on Write/Edit matching `**/plans/**.md`
- Wired at: `~/.claude/settings.local.json` line 299
- Phase 1: 4 LLMs independently review the plan (parallel)
- Phase 2: Same 4 LLMs vote on consensus based on each other's reviews
- Currently uses: MiniMax M2.5 (OpenRouter), Gemini 3.1, Sonnet 4.6, GLM-5 (Z.ai)
- Target: Replace MiniMax M2.5 and GLM-5 with 2 local Ollama models

### Benchmark Artifacts (preserve until implementation verified)
- `/tmp/llm_benchmark/` — all 12 model outputs, named per model
- `/tmp/review_benchmark.sh` — the benchmark script used
- Test input plan: `~/.claude/plans/cuddly-rolling-scott.md`

## Git State
- Not a git repository. No commits possible.
- Handoff saved but NOT committed.
