---
name: CodeForge Arena
description: LLM benchmarking platform at arena.synai.ai -- tests models generating working apps, 3 benchmark types, Next.js dashboard
type: project
---

## CodeForge Arena -- LLM Code Generation Benchmark

- **Location**: `/home/mello/commander/projects/codeforge-arena/`
- **Port**: 9099, domain: arena.synai.ai
- **Container**: `bench-dashboard` on n8n-net
- **Stack**: Python (harness) + Next.js 14 (dashboard)

**What it does**: Tests LLMs' ability to generate working applications from a single prompt. Models produce code, which gets Docker-built, deployed, and validated against automated test suites. Scored on correctness, completeness, and speed.

### Benchmark Types (3 tabs on dashboard)

| Type | Tab | Tests | What it builds | Results dir |
|------|-----|-------|---------------|-------------|
| Full-Stack | `/` | 13 HTTP tests | E-commerce site (Node.js) | `results/` |
| Coding | `/coding` | External | Coding challenges | External (`glm-bench/`) |
| Agent | `/agent` | 50 queries | AI agent service (FastAPI + 8 tools) | `results-agent/` |

### Key Components

- `config.py` -- Model registry (16+ models), `Model` dataclass, port mapping 9101-9116
- `harness.py` -- CLI: `--model KEY`, `--all`, `--dashboard`, `--agent-model`, `--agent-all`
- `llm_client.py` -- Async LLM calls (Claude CLI, Ollama, llama-cpp, Z.ai)
- `builder.py` / `agent_bench/builder.py` -- Docker build/deploy per model
- `validator.py` / `agent_bench/validator.py` -- Automated test suites
- `scorer.py` / `agent_bench/scorer.py` -- Score calculation

### Port Map

| Range | Purpose |
|-------|---------|
| 9099 | Dashboard |
| 9101-9116 | E-commerce benchmark containers |
| 9200 | bench-image-api |
| 9201 | bench-tool-server (Agent Bench mock data) |
| 9301-9316 | Agent benchmark containers |

### Timeline

- Pre-2026-04-05: Full-Stack and Coding benchmarks operational
- 2026-04-05: Nemotron Cascade 2 30B added (port 9116), dashboard brought live for VP presentation
- 2026-04-06: Agent Bench integrated (50 tests, 8 scoring categories, `agent_bench/` package)
- 2026-04-07: VP presentation delivered
- 2026-04-08: Active benchmarking continues (16+ bench containers running concurrently)

### Agent Bench Scoring Categories (100 pts)

tool_selection (20), parameter_correctness (15), multi_tool_orchestration (15), hallucination_resistance (15), rag_synthesis (10), conversation_context (10), error_recovery (8), action_confirmation (7)

**Why:** Showcases LLM capabilities for Mercedes leadership. VP presentation delivered 2026-04-07.

**How to apply:** Run benchmarks via `cd /home/mello/commander/projects/codeforge-arena && python harness.py --model <key>`. Dashboard rebuild: `python harness.py --dashboard`.
