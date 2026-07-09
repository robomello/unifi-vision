---
name: OTTO Server
description: Mercedes-Benz W138 AI server -- hardware, architecture, projects, team, infrastructure
type: reference
---

# OTTO Server (Mercedes-Benz W138 Tuscaloosa)

Full knowledge export at: `~/ottos_data/otto-knowledge.tar.gz`

## What OTTO Is

Operational Task & Troubleshooting Orchestrator -- AI assistant for factory engineers.
- Breakdown analysis (production KPIs, downtime)
- RAG-powered troubleshooting (SOPs, manuals, tribal knowledge)
- PLC/SCADA code generation (Siemens, Rockwell, Ignition)
- Real-time factory system integration (iPortal MES, Ignition SCADA)

## Hardware

- CPU: AMD Ryzen 9950X3D
- GPU: NVIDIA RTX 5090 (32GB VRAM)
- OS: Ubuntu 24.04
- Planned upgrade: Threadripper PRO 9985WX (128C/256T), 4x RTX PRO 6000 (384GB VRAM total)

## Key Infrastructure

- **Ollama**: port 11435 (NOT 11434), all inference local
- **Docker compose**: `mercedes-docker-compose.yml`
- **Corporate proxy**: cntlm on localhost:3128, Docker builds have NO proxy (wheel dance)
- **GenAI Nexus**: corporate Claude API gateway (`genai-nexus.api.corpinter.net`) for Haiku/Sonnet/Opus
- **Access**: `https://otto.us138.corpintra.net` or `https://53.68.46.101`

## Services (Docker)

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432, 5433 | n8n backend + RAG/pgvector |
| n8n | 5678 | Workflow orchestration |
| Qdrant | 6333/6334 | Vector embeddings |
| Jupyter | 8888 | Dev notebooks (GPU) |
| OTTO | 443 (HTTPS) | Main app (FastAPI + auth) |
| Docling | 5001 | Document processing |
| ComfyUI | 8188 | Image generation |
| FileBrowser | 8080 | Web file management |
| Torque Redis | 6379 | Hot buffer for sensor data |
| CVAT | 8085 | Image annotation (v2.61.0) |
| QuestDB | 9000/9009/8812 | Time-series for CNN Inspection |

## Active Models (Ollama)

| Model | Role |
|-------|------|
| qwen3:4b | Classifier, Direct LLM, Summarizer |
| qwen3-vl:32b | PRIMARY: KPI Agent, vision |
| qwen3-vl:8b | FALLBACK: lightweight vision |
| qwen3:14b | iPortal Agent |
| qwen3:8b | Default model |
| ministral-3 | Response validation (critic) |
| Claude Haiku 4.5 | Query routing via GenAI Nexus |

## Query Flow

```
User Query -> Classifier (qwen3:4b) -> [direct_llm | iportal | ignition] -> Validation (ministral-3) -> Response
```

## Active Projects on OTTO

| Project | Location | Status |
|---------|----------|--------|
| OTTO v2 | /home/mbot/otto/ | Phase 2 done, Phase 3 waiting |
| CNN Inspection | /home/mbot/projects/cnn_inspection/ | Phase 1 in progress, 29 sensors, 101K+ rows |
| Torque Vision | /home/mbot/torque-vision/ | Dashboard live at /torque/, vision pipeline pending |
| MARCO | /home/mbot/marco/ | Phase 0 complete, needs webcam for Phase 1 |
| Bedrock Chat | /home/mbot/projects/bedrock-chat/ | v0.1.0 public (FastAPI + React + AWS Bedrock) |

## Factory Systems

- **iPortal MES**: 463 KPIs, shops MO (Assembly), OF (Paint), RB (Body)
- **Ignition SCADA**: MCP tools for tags, alarms, historian
- **Plant MQTT**: 53.68.128.46:1883 (adhesive + robot status topics)

## Multi-Engineer Team

5 engineers sharing Claude Code via `/opt/claude-shared/`:
- romello (Roberto, project lead)
- gilliab (Brad Gilliam)
- brperry (Brett Perry)
- jgoncy7 (Jeff Goncy)
- dabboua (Abdul Dabboua)
- Andy (cybersecurity team, security testing)

Shared rules symlinked, per-user prefs, coordination daemon on port 9091.

## Key Differences from Mello Home Server

| Aspect | Mello (home) | OTTO (Mercedes) |
|--------|-------------|-----------------|
| GPU | RTX 3080 Ti + RTX PRO 6000 96GB | RTX 5090 32GB |
| LLM | Claude CLI (--print) | Ollama local + GenAI Nexus |
| Network | Cloudflare tunnels, public | Corporate proxy, air-gapped builds |
| Images | ComfyUI (local only) | ComfyUI (local only) |
| Users | mello only | 5+ engineers |
| Domain | synai.ai subdomains | us138.corpintra.net |
