---
name: Parallel Agent Invocations
description: Default to parallel agent operations when tasks are independent
type: feedback
---

# Parallel Agent Invocations

**Learning**: Roberto prefers using parallel agent invocations whenever possible to maximize performance. This should be the default approach for independent operations.

## Rule

When multiple independent agents or operations can execute in parallel:
- **Always batch them in a single Agent tool call** rather than sequential invocations
- Examples: research + planning, multiple tool invocations, parallel exploration, independent code analysis tasks

## When to Parallelize

✅ **DO parallelize**:
- Research agent + planning agent (independent work)
- Multiple code review agents (separate files/concerns)
- Exploration + analysis (don't wait for exploration to finish before starting analysis)
- Independent tool operations (Bash commands, file reads, etc.)

❌ **DON'T parallelize**:
- Sequential dependencies (output of task A feeds into task B)
- When later tasks depend on earlier results
- When coordination between agents is needed

## Benefits

- Faster turnaround (agents work simultaneously)
- Better resource utilization (human attention available sooner)
- Reduced wall-clock time for complex work

## Anti-Pattern

Sequential agent calls when they could run in parallel wastes time and reduces efficiency.
