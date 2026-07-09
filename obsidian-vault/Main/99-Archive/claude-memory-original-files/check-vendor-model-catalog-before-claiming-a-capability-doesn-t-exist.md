---
name: Check vendor model catalog before claiming a capability doesn't exist
description: Before saying a kie.ai/fal.ai/replicate model lacks a capability, WebFetch the vendor catalog page first.
type: feedback
---

When a user provides a URL pointing to a vendor model catalog (e.g. kie.ai/<slug>?model=<id> or docs.kie.ai/market/<vendor>/<endpoint>), fetch it before claiming a model lacks a capability. Specifically for kie.ai: model cards live at https://kie.ai/<slug>-1-0?model=<vendor>%2F<endpoint> and full API docs live at https://docs.kie.ai/market/<vendor>/<endpoint>. Both can be fetched with WebFetch.

Why: 2026-05-11, I claimed HappyHorse had no classic image-to-video endpoint after seeing only the Fal.ai reference-to-video agent and the kie.ai text-to-video docs. Roberto corrected me with the kie.ai/happyhorse-1-0?model=happyhorse%2Fimage-to-video URL. The endpoint exists; I had not checked the kie.ai model catalog before answering. This violated rules/agent-behavior.md Rule 6 (verify before asserting non-existence).

How to apply: any time about to say 'X doesn't have Y capability' for a model/vendor in the kie.ai catalog, first WebFetch the kie.ai pricing/model page or docs.kie.ai/market/... — both routes are cheap and reliable. Same principle for fal.ai (fal.ai/models/<slug>) and replicate (replicate.com/<owner>/<model>).
