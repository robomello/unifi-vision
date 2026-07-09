---
name: Meituan LongCat-2.0 (open-source 1.6T MoE model)
description: Meituan released LongCat-2.0 open-source: 1.6T MoE, 48B active/token, 1M context, trained fully on domestic Chinese chips
type: reference
---

Meituan released LongCat-2.0 on 2026-06-29/30. Verified via VentureBeat, SiliconANGLE, The Decoder, SCMP, and official LongCat AI benchmarks page.

Confirmed specs:
- 1.6 trillion parameters, MoE architecture, 48B active per token (dynamic 33B-56B range)
- 1 million token context window
- Trained fully (pretraining + inference) on 50,000+ domestic Chinese chips (Huawei cluster), zero NVIDIA hardware -- first trillion-param model claimed to do both stages on domestic silicon (DeepSeek-V4 was inference-only on domestic chips)
- Purpose-built for agentic coding
- Benchmarks: SWE-bench Pro 59.5 (vs GPT-5.5's 58.6), Terminal-Bench 2.1 70.8, SWE-bench Multilingual 77.3

Backstory: the model was anonymously topping OpenRouter charts under the codename "Owl Alpha" (11T monthly token throughput, 200% growth) before being unmasked as LongCat-2.0-Preview.

Caveat as of verification: model weights listed as "coming soon" on the official site -- announcement/benchmarks are out, weights not yet downloadable.

Relevance: notable for local-model / self-hosted LLM evaluation given the home server's no-NVIDIA-API-dependency stance is more about avoiding OpenAI/Gemini cloud APIs than chip origin, but worth tracking if a strong open-weight agentic-coding model becomes downloadable and runnable on local GPU (GPU 1, RTX PRO 6000 96GB) once weights ship -- 1.6T total params won't fit locally, but distilled/smaller variants may follow.
