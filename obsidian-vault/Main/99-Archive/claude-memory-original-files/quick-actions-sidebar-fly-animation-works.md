---
name: Quick Actions sidebar: fly animation works
description: User confirmed the 600ms portal-clone fly animation for pinning chat prompts to OTTO's Quick Actions sidebar feels right
type: feedback
---

On 2026-04-28 Roberto called the chat-prompt-to-Quick-Actions fly animation "awesome".

Pattern that worked:
- Source: getBoundingClientRect() of the chat user-message bubble.
- Destination: the dashed `+` tile (data-quick-actions-add-target) inside the panel marked with data-quick-actions-widget.
- Animation: a transient clone rendered into a portal at document.body, fixed-positioned at the source rect. After two requestAnimationFrame ticks (so the start frame paints), apply transform: translate(dx, dy) scale(0.18) and opacity 0.05 with a 600ms cubic-bezier(0.4, 0.0, 0.2, 1) transition. Then emit a `quickaction:pin-resolve` window event so the panel persists the action and shows a brief cyan ring pulse on the new entry.

**Why:** users dismissed the prior plain "click button to send" UX as static. The fly + pulse gives a clear cause/effect chain ("I clicked Pin -> the prompt physically arrived in the panel"), which is what made it feel premium.

**How to apply:** when porting interactions where one surface "claims" content from another (drag-to-pin, save-to-collection, drop-into-bucket), prefer a portal-clone fly with these timings rather than a fade-in/slide. Don't skip the double-rAF — without it the start frame doesn't paint and you get an instant teleport instead of an animation.
