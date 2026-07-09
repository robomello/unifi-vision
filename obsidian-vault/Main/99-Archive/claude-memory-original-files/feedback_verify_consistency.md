---
name: Verify Consistency Properly
description: When checking UI consistency across pages, compare actual content not just visual impressions
type: feedback
originSessionId: <REDACTED-UUID-18>
---
When verifying that multiple pages have the same header/nav/footer, don't just look at screenshots and declare "consistent." Extract the actual HTML and compare programmatically.

**Why:** Declared 3 pages "consistent" from screenshots when h1 text, CSS properties, and element structure were all different. User caught it.

**How to apply:** Before claiming UI consistency, compare the actual DOM/HTML of the shared element across pages. Use browser-agent's cross-page comparison, or at minimum grep the source files and diff the header blocks side by side.
