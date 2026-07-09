---
name: Muse Studio — Replacing OpenAI/Anthropic SDK with claude --print CLI
description: Muse Studio migration plan: rip openai/anthropic SDK across Python backend + Next.js frontend; simulated streaming (claude --print returns full response); model name mapping; preserve Ollama + LM Studio providers
type: project
---

# Muse Studio — OpenAI/Anthropic SDK → `claude --print` CLI

Muse Studio currently uses `from openai import AsyncOpenAI` and direct `https://api.openai.com/v1` calls across both Python backend and Next.js frontend. Roberto's NON-NEGOTIABLE: NEVER `import openai`, `OPENAI_API_KEY`, `import anthropic`, `ANTHROPIC_API_KEY`, `ChatAnthropic`. **All Claude calls must go through `claude --print --model <model>` via subprocess.**

Project path: `/home/mello/Muse-Studio/`

## Streaming Architecture

`claude --print` does NOT support streaming. The current app uses SSE for real-time text display. Strategy:

- **Backend (Python)**: `claude --print` returns full response at once. `generate_stream()` runs the subprocess, collects full output, then yields a single `LLMChunk(text=full_output, is_final=True)`. Existing SSE infrastructure passes through transparently.
- **Frontend (Next.js)**: Replace `streamOpenAICompat()` in `route.ts` (which calls OpenAI/Anthropic with streaming) with a function that shells out to `claude --print` via Node `child_process`, collects output, and **simulates streaming by splitting into ~20-word chunks with 50ms delays** for UX. No frontend hook changes.

## Package Changes

| Package | Action |
|---|---|
| `openai` (pip) | REMOVE from `requirements.txt` |
| `langchain-openai` | KEEP — still needed for LM Studio provider |
| `langchain-anthropic` | REMOVE |
| `claude` CLI | Required on PATH in host + backend env |

Pre-check: `which claude && claude --version && echo Hello | claude --print --model haiku`

## Backend: Rewrite `muse_backend/app/providers/llm/claude_provider.py`

Current: 124 lines, uses `from openai import AsyncOpenAI` pointed at Anthropic endpoint.

```python
import asyncio, shutil
from app.providers.base import LLMProvider, LLMChunk

CHUNK_SIZE = 80  # chars per simulated stream chunk
MODEL_MAP = {
    "haiku": "haiku",
    "sonnet": "sonnet",
    "opus": "opus",
    "claude-haiku-3-5": "haiku",
    "claude-sonnet-4-6": "sonnet",
    "claude-opus-4-6": "opus",
}
DEFAULT_MODEL = "sonnet"

class ClaudeProvider(LLMProvider):
    provider_id = "claude"
    display_name = "Claude (CLI)"
    provider_type = "api"

    def is_available(self) -> bool:
        return shutil.which("claude") is not None

    async def generate_stream(self, task, prompt, context, params):
        model = MODEL_MAP.get(params.get("claude_model", ""), DEFAULT_MODEL)
        system_prompt = SYSTEM_PROMPTS.get(task, SYSTEM_PROMPTS["default"])
        user_message = prompt
        if context:
            ctx = "\n".join(f"{k}: {v}" for k, v in context.items())
            user_message = f"Context:\n{ctx}\n\nRequest:\n{prompt}"

        proc = await asyncio.create_subprocess_exec(
            "claude", "--print", "--model", model,
            "--system-prompt", system_prompt,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=user_message.encode()),
            timeout=120,
        )
        # yield as simulated stream
        ...
```

- Remove `ANTHROPIC_API_KEY` requirement entirely
- `is_available()` checks `shutil.which("claude")`
- Timeout 120 seconds via `asyncio.wait_for`

## Frontend `route.ts` (Next.js)

Replace `streamOpenAICompat()` direct API call with Node `child_process.spawn("claude", ["--print", "--model", model, "--system-prompt", systemPrompt])`. Pipe user message to stdin, collect stdout, then emit as SSE events in ~20-word chunks with 50ms delays.

## Preserve

- Ollama provider (untouched)
- LM Studio provider (`langchain-openai` kept just for it)
- All non-LLM code paths

See [[obsidian]] and `context.md` for the broader Claude-CLI-only rule.
