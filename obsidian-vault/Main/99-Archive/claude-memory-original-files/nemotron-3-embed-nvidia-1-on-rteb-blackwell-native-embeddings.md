---
name: Nemotron-3-Embed (NVIDIA) - #1 on RTEB, Blackwell-native embeddings
description: NVIDIA Nemotron-3-Embed embedding models top RTEB; NVFP4 variant is Blackwell-native, relevant to Qdrant/vector memory
type: reference
---

NVIDIA Nemotron-3-Embed (released 2026-07-16, https://huggingface.co/blog/nvidia/nemotron-3-embed-wins-rteb). Open, commercially available text embedding models that top the RTEB retrieval leaderboard (incl. RTEB Multilingual). Multilingual + code retrieval.

Repos / variants:
- `nvidia/Nemotron-3-Embed-8B-BF16` - 8.0B params, 4096-dim. RTEB 78.5% (NDCG@10), ranked #1. MMTEB Retrieval 75.5%.
- `nvidia/Nemotron-3-Embed-1B-BF16` - 1.14B params, 2048-dim. RTEB 72.4% (27% error-rate reduction vs predecessor). MMTEB Retrieval 71.0%.
- `nvidia/Nemotron-3-Embed-1B-NVFP4` - 1.14B, 2048-dim, quantized. Retains 99%+ of BF16 retrieval accuracy, ~2x throughput on Blackwell.

Specs: max seq length 32k, mean pooling, input prefixes `query:` / `document:`. Matryoshka not mentioned. License name not stated in article (just "open and commercially available").

1B derived from Ministral-3-3B, distilled via NVIDIA ModelOpt NAS (3B->2B->1.14B); QAD quantization for NVFP4. 8B: contrastive pre-train on web+synthetic pairs, fine-tuned on curated multilingual sets (legal/finance/medical/business/education).

Run via: SentenceTransformers, Transformers, vLLM (weights on HF), NVIDIA NIM at build.nvidia.com. Partners: Baseten, DeepInfra, OpenRouter.

Why it matters for the home server: NVFP4 is Blackwell-native (both cards here are Blackwell - RTX 5090 32GB + RTX PRO 6000 96GB), so the 1B-NVFP4 runs cheap/fast locally and the 8B fits with room to spare. Candidate upgrade for the Qdrant vector-memory / semantic-memory embedding layer. Not yet benchmarked or deployed here.
