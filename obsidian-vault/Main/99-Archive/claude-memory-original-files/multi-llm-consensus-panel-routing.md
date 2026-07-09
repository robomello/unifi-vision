---
name: Multi-LLM consensus panel routing
description: How to reach each non-Claude LLM for consensus panels: GPT via codex CLI, Kimi via OpenRouter, GLM via glm-agent
type: reference
---

For multi-LLM "consensus panel" discussions, reach each model via its sanctioned path (no banned OpenAI/Gemini direct APIs):

- **Claude (Haiku/Sonnet/Opus)**: `claude --print --model haiku|sonnet|opus` (or claude-llm-agent).
- **GLM (Z.ai)**: `glm-agent` — curl to `open.bigmodel.cn/api/paas/v4`, key `ZAI_API_KEY` in `/home/mello/.env`. Default model `glm-5.2`.
- **Kimi (Moonshot)**: via **OpenRouter** — `curl https://openrouter.ai/api/v1/chat/completions`, key `OPENROUTER_API_KEY` in `/home/mello/.env`, model `moonshotai/kimi-k2`.
- **GPT (OpenAI, e.g. GPT-5.5)**: Roberto's instruction — use the **codex CLI**, NOT OpenRouter, NOT the OpenAI API directly. Non-interactive: `codex exec -m gpt-5.5 --skip-git-repo-check "<prompt>"`. Reads prompt from stdin if `-` or piped.

**Why:** Roberto convenes 4-6 LLMs to critique plans/strategy (mirrors OTTO's plan-consensus hook). Each provider has one correct access path; GPT specifically goes through codex per his explicit preference (set 2026-06-21).
