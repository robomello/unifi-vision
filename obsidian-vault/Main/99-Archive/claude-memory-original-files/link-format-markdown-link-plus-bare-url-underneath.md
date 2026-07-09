---
name: Link format: markdown link plus bare URL underneath
description: When sending links in the terminal, output a markdown link then the raw URL on the next line
type: feedback
---

When sending a link in the Claude Code terminal, use the "both lines" format: a markdown link, then the bare URL on its own line directly underneath.

Example:
[Define 7 XL build (galvesribeiro)](https://forum.level1techs.com/t/threadripper-7980x-asus-pro-ws-trx50-sage-wifi-build/210550)
https://forum.level1techs.com/t/threadripper-7980x-asus-pro-ws-trx50-sage-wifi-build/210550

**Why:** On his GNOME Terminal both mechanisms then apply at once. The markdown link is OSC 8 ctrl-clickable (but hides the URL); the bare URL is auto-highlighted by GNOME Terminal/VTE and shows the full, copyable address. Both lines = clickable AND visible AND copyable.

**How to apply:** For every link sent to Roberto, emit `[text](url)` followed by the plain `https://...` on the next line. Applies to citations, sources, and any URL in chat.
