---
name: pxpipe-recall-bench
description: Recall benchmark tool at /home/mello/commander/projects/pxpipe-recall-bench/. Tests context compression accuracy with independent measurement and needle verification.
type: project
---

## pxpipe-recall-bench (2026-07-04)

**Location:** /home/mello/commander/projects/pxpipe-recall-bench/
**Status:** Active testing as of Jul 4

### What It Is
Recall benchmark/testing tool for context compression evaluation. Tests how well different compression strategies preserve information retrieval accuracy.

### Structure
- pxbench/ (core benchmark code)
- tests/ (test suite with coverage)
- config/ (benchmark configurations)
- scripts/ (helper scripts)
- results/ (benchmark outputs)
- systemd/ (service definitions)

### Context
Part of the ongoing evaluation of context compression tools (headroom, etc.). Roberto flagged shallow testing patterns — this is the proper benchmarking approach with:
- Independent measurement (not trusting tool's own numbers)
- Needle planting for correctness verification
- Real code path testing (not README evaluation)

Why: Recent project (Jul 4) not in memory. Related to context compression evaluation work mentioned in lessons.md.

How to apply: When evaluating context compression or recall accuracy, use this benchmark suite. Results in results/ directory.
