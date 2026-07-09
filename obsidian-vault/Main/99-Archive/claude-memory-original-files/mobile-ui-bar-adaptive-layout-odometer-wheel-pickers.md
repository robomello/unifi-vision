---
name: Mobile UI bar: adaptive layout + odometer wheel pickers
description: iPhone-friendly means adaptive card layout (no horizontal scroll) + odometer-style wheel pickers for numbers
type: feedback
---

Roberto's bar for 'iPhone-friendly' web UIs (from mellos.synai.ai build, 2026-06-10):

**Why:** First mobile pass (wheel picker only) wasn't enough — he flagged that the wide table still required sideways scrolling on iPhone.

**How to apply:**
- Mobile-friendly = the LAYOUT adapts (cards/stacked instead of wide tables), not just input widgets. No horizontal scrolling, ever.
- Desktop keeps dense tables; phone gets cards. Same page detects via media query, no separate URL.
- For number entry on mobile he loves iOS-style odometer wheel pickers: endless digit drums that carry/borrow across places (rolling ones past 9 ticks tens up; 300 minus one notch on ones = 299 with hundreds drum dropping to 2), with tick sound per notch.
- Verify mobile UI in a real phone-sized viewport with touch emulation (pointer: coarse), including checking scrollWidth <= viewport width.
