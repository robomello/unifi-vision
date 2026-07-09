---
name: gemma4-coder (Gemma 4 12B GGUF) — local install, run recipe, gotchas, eval
description: Download/run/test recipe for yuxinlu1 gemma-4-12B coder GGUF in ollama; gotchas (needs ollama>=0.30.8 gemma4_unified arch, never send think:true=HTTP400), aliased gemma4-coder Q8 ~87 tok/s, eval results, for OTTO/baby-otto replication
type: reference
---

**Model:** `hf.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF` — Gemma 4 12B Python-coding fine-tune (base `google/gemma-4-12B-it`), GGUF, `gemma4_unified` arch, native thinking channel. Distilled from execution-verified Composer 2.5 + Fable 5 chain-of-thought. Python/algorithmic specialist, English-centric, NOT safety-aligned (reduced refusals), max ctx 131K. License: Gemma.

**Quants:** Q2_K 4.83 GB · Q4_K_M 7.38 GB (card's recommended) · Q6_K 9.79 GB · Q8_0 12.67 GB (≈ full quality).

**Installed at home (2026-06-14):** pulled Q8_0 into the `ollama` container, aliased **`gemma4-coder`**. Run: `docker exec -it ollama ollama run gemma4-coder`. API server-side on :11434 (internal only). ~16 GB VRAM on the RTX 5090, ~26 GB on the RTX PRO 6000; 60-87 tok/s; loads ~35 s. GPU context: see [home GPU layout](home-gpu-layout-2026-06-14-rtx-5090-rtx-pro-6000-600w.md).

**Download:** `ollama pull hf.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF:Q8_0` (stored with lowercase tag `:q8_0`). For small GPUs use `:Q4_K_M`.

**Gotchas (learned the hard way):**
1. Needs **ollama >= 0.30.8** — this is the `gemma4_unified` arch; older builds fail to load it. Containerized: `docker pull ollama/ollama:latest` then recreate the container. (Home host ollama 0.20.2 was too old; the container at 0.30.8 worked.)
2. **Never send `"think": true`** to the API — this raw HF GGUF is not registered thinking-capable, so ollama returns HTTP 400 "does not support thinking". It still reasons natively; the CoT comes back in the response `thinking` field automatically. Just omit the flag.
3. Coding tests: `options {"temperature": 0, "num_predict": 4096}` (temp 0 = deterministic code; num_predict must cover thinking + answer or it truncates). Card's recommended creative sampling is temp 1.0 / top_p 0.95 / top_k 64.

**Test method:** EXECUTE the generated code (the model was trained on execution-verified data, so actually run what it writes). Example task: ask for `evaluate(expr)` arithmetic parser (+ - * /, parentheses, unary minus, ValueError on malformed, no `eval()`); run against `1+2*3=7`, `(1+2)*3=9`, `10/4=2.5`, `2*-(3+1)=-8`, `"1 +"` → ValueError, `"(1 + 2"` → ValueError.

**Eval results (home, Q8):** LIS textbook algorithm 7/7 (correct O(n log n) patience sort). Expression evaluator: correct recursive-descent parser but **dropped division on first pass (6/8)**; handed the failure back → **fixed to 8/8 first try** with accurate root-cause. Smoke-test palindrome correct.

**Verdict:** Usable for real Python at a "strong junior you code-review" level. Picks right patterns (recursive descent, bisect), reasons in the open, debugs accurately from feedback. Makes 12B-class slips (drops a spec item like a whole operator), so workflow = write → run/test → feed failures back; do not merge unreviewed. Don't rely on it for non-Python or factual recall.

**For OTTO / baby-otto:** baby-otto has the 96 GB RTX PRO 6000 Max-Q, so Q8 fits easily — replicate with the download + gotchas + test method above. Expect a possible first-pass miss that fixes cleanly when the failure is handed back (that is normal, not a broken download). Smaller cards: drop to `:Q4_K_M` (~7 GB).
