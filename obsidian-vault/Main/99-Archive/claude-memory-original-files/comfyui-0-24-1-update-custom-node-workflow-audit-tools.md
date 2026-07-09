---
name: ComfyUI 0.24.1 update + custom-node/workflow audit tools
description: ComfyUI bumped 0.22.0->0.24.1 for Ideogram 4; pin lifted; backup image + two audit tools added; 23 packs + 12 workflows pruned
type: project
---

ComfyUI was updated 0.22.0 -> 0.24.1 (2026-06-07) to get the Ideogram 4 core nodes (Ideogram4Scheduler, DualModelGuider, CFGOverride), which did not exist in 0.22.0.

Build/deploy: image `comfyui:local` builds from context /home/mello/ComfyUI (official comfyanonymous/ComfyUI repo). The repo was on a deliberately pinned branch `master-pinned @ bb560036` (v0.22.0+77). Now checked out to branch `pinned-v0.24.1` (tag v0.24.1). Local patch reapplied: comfy_api/latest/_input_impl/video_types.py adds `torch.nan_to_num(...).clamp(-1,1)` on the audio waveform before AudioFrame.from_ndarray.

ROLLBACK: backup image tagged `comfyui:local-bak-0.22.0-bb560036`; git rollback `git checkout master-pinned` (bb560036) then rebuild. To apply changes use compose recreate (a PreToolUse hook blocks `docker restart`): `docker compose -f /home/mello/docker-compose.yml up -d --force-recreate comfyui`.

New reusable tools in commander/tools/: `comfyui_node_usage.py` (which custom-node packs are used vs dumpable) and `comfyui_workflow_audit.py` (broken/stale workflows). Both have a quarantine/archive mode and write a markdown report to /tmp.

GOTCHA: ComfyUI /object_info `python_module` is UNRELIABLE on this box - the pack `comfyui-workflow-encrypt` hooks node registration and mis-attributes other packs' nodes (VHS, IPAdapter, etc.) to itself. Attribute node->pack by STATICALLY parsing each pack's NODE_CLASS_MAPPINGS instead.

Cleanup applied: 23 unused/broken packs renamed `*.disabled` (incl. a duplicate comfyui-logic/ComfyUI-Logic, and broken VSRFI-ComfyUI[needs cupy]/ComfyUI_IndexTTS[transformers drift]). 12 workflows (5 broken + 7 stale >120d) moved to /home/mello/comfyui-workflows-archive/ (restore manifest at .manifest.tsv). Result: node types 5054 -> 4753, 110 active / 25 disabled packs, 108 live workflows. All reversible.
