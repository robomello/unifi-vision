---
name: GSPOC AI Visual Inspection — vlm-inspect + Web App Plan
description: Mercedes final-assembly visual inspection POC: VLM home-server testing + GSPOC web app plan (FastAPI monolith, Ollama, SSE+polling fallback, Cloudflare Access, CLIP zone classification + zone-aware VLM inspection)
type: project
---

# GSPOC — AI Visual Inspection System for Mercedes-Benz Final Assembly

**Owner**: Roberto de Mello, Central Standards Team, MBUSI Tuscaloosa (US138).

Replaces manual barcode scanning on the final assembly line with AI visual inspection. Operator sweeps iPhone camera across vehicle interior; VLM on MacBook Pro confirms correct parts installed within ~37 s (assembly takt = 70 s).

## Why It Matters

- Barcodes confirm part was DELIVERED, not INSTALLED CORRECTLY
- One quality escape costs more than entire POC budget
- Zero cloud dependency — all data on-prem, all inference local

## Production Architecture (Target)

```
iPhone 17 Pro (camera) --WiFi 7 6GHz--> MacBook Pro M5 Max 128GB (VLM brain) --results--> iPad Pro / iPhone (operator display)
[MacBook] --TB5--> [CalDigit TS5 Plus] --Cat6a 10GbE--> [USW-Pro-XG-8-PoE] --PoE--> [U7 Pro Outdoor AP IP67] --WiFi 7--> [iPhones / iPad]
                                          ↘ HDMI → [LG 34" Ultrawide PBP]
```

## Operator Workflow

```
T=0s:     Scan VIN barcode → PLUS system returns expected parts list → Visual RAG retrieves reference images
T=0-15s:  Right side video scan (5 keyframes extracted)
T=15-20s: Right side pass/fail on iPad
T=17-32s: Left side scan
T=32-37s: Combined pass/fail + defect locations | 33s remaining in takt
```

## VLM Stack

- **POC current**: Qwen2.5-VL-7B-Instruct via Ollama (`qwen3.5:35b-a3b`) — fastest, ~4 s/zone with CLIP-zoned prompts
- **Production target**: Qwen2.5-VL-72B-Instruct-AWQ (4-bit, fits 128GB), ~2-4 s/frame on M5 Max
- **Learning**: few-shot in-context (1-3 golden reference images) + Visual RAG (CLIP embeddings in FAISS) + optional LoRA fine-tuning. F1=0.950 with 1 reference on MVTec AD.

## CLIP Zone Classification Pipeline (2026-03-09 breakthrough)

The original single-pass VLM ("identify what area + inspect in one call") caused hallucination spirals (8B listing "door window washer fluid reservoir control indicator haptic feedback...") and all-LOW-CONFIDENCE hedging.

**Solution**: separate classification from inspection.

```
./vlm.sh extract           # FFmpeg frame extraction
./vlm.sh classify          # CLIP ViT-L-14 (~92ms/frame) → *_zones_latest.json
./vlm.sh inspect-zoned     # Ollama qwen3.5:35b-a3b zone-specific prompts (~4s/zone)
./vlm.sh results           # Structured PASS/FAIL per zone
# Or: ./vlm.sh pipeline    (all three at once)
```

**10 zones**: door_left, door_right, front_seats, rear_seats, dashboard, center_console, trunk, exterior, b_pillar, headliner. Each has 3-5 text prompts for accuracy.

**Benchmark (24 frames, 7 videos, 19 zones)**:
- CLIP: 2.2 s total (92ms/frame)
- VLM zoned: 75 s total (4s/zone via Ollama)
- Result: 9 PASS | 9 FAIL | 1 INCONCLUSIVE

Compare old pipeline: 4 frames took 254s on 32B transformers with hallucinations.

| Model | Method | Avg/frame | Quality |
|---|---|---|---|
| Qwen2.5-VL-7B | transformers | 12s | Low (hedging, no verdicts) |
| Qwen3-VL-8B | transformers | 18.6s | Medium (hallucination loops) |
| Qwen3-VL-32B | transformers | 52.7s | High |
| Qwen3.5-35B-A3B | ollama | 8.3s | High (best speed/quality) |
| Qwen3.5-35B-A3B + CLIP zones | ollama | 4s/zone | Highest (zone prompts eliminate hallucination) |

**CLIP limitations**: door_left vs door_right scores within 0.001 (unreliable for L/R). IMG_1655 undercarriage misclassified as center_console/trunk (no undercarriage prompts). All frames have low blur scores (<100) due to iPhone video motion blur — blur threshold may need lowering for video vs photos. CLIP confidence ranges 0.21-0.27 but zone ranking is correct.

## GSPOC Web App Plan (for the POC demo at Mercedes)

Single-page tool. FastAPI monolith + vanilla HTML/CSS/JS frontend (NOT casa-ai-style split). Container `gspoc`, port 3600, `gspoc.synai.ai` behind **Cloudflare Access** restricted to Roberto's email (prevents anonymous uploads burning GPU time on shared Ollama).

### Architecture Decisions (all consensus-driven from 4-reviewer pass)

1. **Background queue, never block event loop**: bounded `asyncio.Queue` (depth = MAX_CONCURRENT_SESSIONS=2), single async consumer worker for extract → blur → inspect
2. **State persisted to `meta.json` per pipeline step** (queued, extracting, filtering, inspecting frame N, complete, error). On startup, scan `/app/data/sessions/` to rebuild in-memory state — mid-processing sessions become `"interrupted"`, retryable via `POST /api/session/{id}/retry`
3. **SSE with `: ping` heartbeat every 15 s** + `Last-Event-ID` resume + **polling fallback** (`GET /api/session/{id}/status`) after 3 missed heartbeats (Mobile Safari background + aggressive proxies eat SSE)
4. **Upload validation**: max 500 MB (`Content-Length` + streaming counter), max 120 s duration (ffprobe), allowed MIME types validated by magic bytes (`video/mp4`, `video/quicktime`, `video/x-msvideo`)
5. **Path-traversal guards**: server-generated UUID session IDs validated by `^[a-f0-9-]{36}$`, ffmpeg-generated filenames validated by `^frame_\d{4}\.jpg$`, `os.path.commonpath()` on the final resolved path
6. **Concurrency guard**: queue full → 429
7. **Ollama fault isolation**: 60 s `httpx` timeout per frame, mark errored frames `"status": "error"` and continue. Abort session at 3 consecutive Ollama failures (`"status": "error_ollama"`)
8. **Hourly cleanup**: deletes sessions older than `SESSION_RETENTION_HOURS` (default 168 = 7 days)
9. **Ollama params**: `model=qwen3.5:35b-a3b`, `stream=False`, `think=False`, `keep_alive=-1` (no cold start), `options.num_predict=2048` (matches benchmark.py)
10. **Structured-JSON verdict prompt** → `parse_verdict()` extracts PASS/FAIL from JSON block first, falls back to regex, defaults to `INCONCLUSIVE` (not silent default)
11. **Blur detection**: OpenCV Laplacian variance, threshold ~100 (tunable). Blurry frames flagged but still shown (grayed out, not silently deleted)
12. **Frame extraction**: fps=1.0 default, max 30/video, 1920px wide, JPEG quality 85

### Compose Block

```yaml
gspoc:
  build: { context: ./commander/projects/gspoc }
  image: gspoc:latest
  container_name: gspoc
  environment:
    OLLAMA_URL: http://ollama:11434
    OLLAMA_MODEL: qwen3.5:35b-a3b
    MAX_UPLOAD_MB: 500
    MAX_CONCURRENT_SESSIONS: 2
    SESSION_RETENTION_HOURS: 168
  ports: ["3600:3600"]
  volumes: [/data/gspoc:/app/data]
  networks: [n8n-net]
  healthcheck: { test: ["CMD", "curl", "-f", "http://localhost:3600/api/health"] }
```

No GPU reservation needed — Ollama has its own GPU.

### Session Layout

```
sessions/{session_id}/
  video.mp4                  # original upload
  meta.json                  # status, timestamps, config (persisted every step)
  frames/frame_NNNN.jpg
  results.json
```

### Endpoints

- `POST /api/upload` → 413 (size), 422 (format/duration), 429 (queue full)
- `GET /api/session/{id}/status` (polling fallback)
- `GET /api/session/{id}/stream` (SSE w/ heartbeat + Last-Event-ID)
- `GET /api/session/{id}/results`
- `GET /api/session/{id}/frame/{filename}` (path traversal guarded)
- `POST /api/session/{id}/retry` (re-enqueue interrupted/errored)
- `GET /api/sessions`
- `GET /api/health`

### UI

Mobile-first dark theme (#1a1a2e bg, #c0c0c0 silver text, #00d4aa pass green, #ff4757 fail red). Three views: upload (large tap target, drag-drop on desktop), processing (progress + current frame thumb + step indicator), results (scrollable frame grid w/ pass/fail badges, expandable analysis).

## Test Folder Structure (`/home/mello/vlm-inspect/`)

```
vlm.sh              # CLI wrapper (run from host)
videos/             # iPhone MOV/mp4
frames/{video}/     # extracted JPEGs
scripts/
  extract_frames.py
  classify_zones.py    # CLIP ViT-L-14 (NEW)
  inspect_zoned.py     # Zone-aware Ollama (NEW)
  inspect.py           # Original generic
  benchmark.py
reference/          # Golden reference images
results/
  *_zones_latest.json    # Zone lookup bridge
  *_zones_<TS>.json      # Full classification details
  *_zoned_*.json         # Zone-aware results
  *_general_*.json       # Old-style generic
```

Container path: `/app/vlm-inspect/`. Scripts run inside `comfyui` container (CUDA, PyTorch 2.10, transformers).

## Hardware Shopping List ($13,587 with 9% AL tax + 10% supplier fee)

MacBook Pro 16" M5 Max 128GB/2TB nano $5,994 | iPhone 17 Pro 512GB ×2 $3,115 | iPad Pro 11" M5 1TB nano $2,037 | Apple Pencil Pro $155 | OtterBox Defender ×2 $156 | SEYMAC rugged $48 | Belkin USB-C 2.5GbE $42 | LG 34" UW $396 | USW-Pro-XG-8-PoE $598 | U7 Pro Outdoor $335 | CalDigit TS5 Plus $540 | TB4 cable $36 | Cat6a STP 35ft ×2 $36 | Apple Dev Org $99.

MacBook ships ~April 1 (3 week lead time).

## Key Design Decisions

1. MacBook Pro 16" 128GB over Mac Studio — mobility + same inference + WiFi 7 built-in
2. Wireless last mile only — everything wired except iPhone/iPad to AP
3. Network.framework + Bonjour (Apple DTS recommends for video, NOT MultipeerConnectivity)
4. JPEG @ 1080p 1-5fps (not continuous 4K) — bandwidth-efficient, takt time allows it
5. Video scan (10s sweep) over single photo — better coverage
6. Few-shot ICL + Visual RAG over fine-tuning — no training data needed to start
7. U7 Pro Outdoor IP67 — factory dust/humidity proof, directional antenna
8. USW-Pro-XG-8-PoE — production-grade Layer 3, 10GbE
9. iPad Pro 1TB over 2TB — same 10-core/16GB CPU upgrade, saves $400
10. LG 34" Ultrawide w/ PBP — split-view dashboard (camera left, results right)
11. ComfyUI container for testing — reuse existing CUDA/PyTorch stack, no new Docker builds

## Status (Mar 2026)

- VLM testing on home server: ACTIVE (first batch running)
- 7 iPhone videos, 24 frames extracted, results saving to `/app/vlm-inspect/results/*.json`
- Hardware procurement: justification pending manager approval
- Swift app development: waiting on MacBook arrival
- PLUS API integration (VIN → BOM): designed not coded
