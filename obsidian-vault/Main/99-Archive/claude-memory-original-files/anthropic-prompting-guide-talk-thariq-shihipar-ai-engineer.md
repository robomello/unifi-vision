---
name: Anthropic Prompting Guide Talk (Thariq Shihipar, AI Engineer)
description: Anthropic official prompting guide for Claude/Claude Code, broken down by Thariq at AI Engineer; via Andros Wong LinkedIn clip
type: reference
---

Source: Andros Wong LinkedIn post (video, ~4 min) sharing Thariq Shihipar's AI Engineer talk on Anthropic's official prompting guide for Claude/Claude Code.
- Post URL: https://www.linkedin.com/posts/andros-wong-2b066943_anthropic-just-dropped-their-official-prompting-ugcPost-7481039587058941953-ZBks/
- Local video: /home/mello/anthropic_fable5_prompting_andros_wong.mp4 (720p, 58MB, EN captions)

Thesis: the frontier model is undertrained by your harness, not its weights ("capability overhang"). Four moves:
1. Unhobble it - shrink the system prompt (they cut 80% of Claude Code's own), use all effort levels (medium beats old-model xhigh), give it tools, state boundaries explicitly since it takes initiative.
2. Find your unknowns - ask for a "blind spot pass", request 4 divergent designs instead of a spec, have it interview you, give references over descriptions, quiz yourself before merging.
3. Scaffold for long runs - ground every claim in tool-output evidence, give the WHY not just WHAT, dispatch parallel subagents, build a persistent memory that compounds on your codebase.
4. Be less reasonable - good/fast/cheap is now pick-three; Thariq built his whole deck in 4 hours.

Punchline: "Building is easier, but generating value is still hard. The bottleneck shifted from execution to knowing what's worth building." Aligns with opinion.md.

Retrieval note: linkedin-agent was fully blocked (Apify+ScrapingDog 403, cookie gate refused). yt-dlp (python3 -m yt_dlp) pulled the LinkedIn video + verbatim caption + captions directly. Use that fallback for LinkedIn video posts.
