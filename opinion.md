# Opinion

My standing opinions and convictions, written in my own voice so Claude Code knows where I actually stand before it talks to me. Load this at session start. It is opinion, not law: argue with me when I'm wrong, and tell me to update it when it drifts.

> **Provenance (v2, 2026-06-21):** v1 was a bootstrap seed assembled from working context. v2 is grounded against my Obsidian second brain — `00-Advisor/advisor-rules.md`, `00-Advisor/mercedes-context.md`, `00-Advisor/financial-state.md`, `00-Advisor/strategic-decisions-log.md`, and the consolidated `50-Reference/claude-code-memory.md`. Lines marked **[confirmed]** are backed by the vault. Lines marked **[unverified]** still need a pass. The vault is the source of truth; if this file and the vault disagree, the vault wins.

No fluff, no flattery. I asked for honesty over comfort. Don't mirror my excitement — pressure-test it.

---

## Industrial automation & controls

### Skip the PLC when the problem allows it **[confirmed]**
I'd rather integrate at the edge (SIM2000 + Node-RED) than reach for a PLC by reflex. PLCs earn their place in safety and hard-real-time determinism, not as the default glue for every data path. The honest version: edge-first for data paths, PLC-first where safety or determinism is on the line. The discipline is knowing which is which.

### Cameras should learn and flag, not just record **[confirmed]**
A vision system that only stores frames is a liability, not an asset. The value is judgment at the edge. A camera building an archive someone reviews after the fact is doing the wrong job. (This is the VIQA/MARCO thesis: zero-shot and trained inspection at the edge, not a DVR.)

### AI/ML only where it produces measurable ROI **[confirmed]**
I don't deploy models for novelty. If I can't point to takt time, scrap rate, downtime, or labor hours, it doesn't ship. *Self-check:* the real belief is "no production deploy without ROI." Don't let that kill the exploratory work that finds the ROI before it's measurable. Killing slop is good; killing discovery is not.

### SICK over Keyence — for the ecosystem, not the optics **[confirmed]**
The preference is web UI, tooling, and edge capability, not raw sensor quality. A tooling judgment, not a permanent verdict. Re-check as edge stories evolve.

### Verify a tool before judging it **[confirmed]**
I don't dismiss tools on reputation or vibe. Run it first, then have the opinion.

### OTTO is the platform, not a hobby **[confirmed]**
OTTO is my factory AI assistant deployed on corpintra at MBUSI — direct iPortal integration, sub-second latency against PowerBI's 2-day lag, a real user base, a 5-engineer team around it. Mercedes never asked me to build it. I build it because it's right and everyone grows with it. *The advisor's standing job:* that exact frame ("I do it because I love it and it's easy") is also the one that lets the work go uncompensated. Name it when it shows up in a career context.

---

## AI, agents & tooling

### Agent actions are proposals until they clear a gate **[confirmed]**
Autonomous work is governed, not trusted. Every consequential agent action is a proposal until it passes a trust-gate (observe → verify → test → operate). Auto-push without a gate is how you earn a 2am incident. *(The principle is real; I have not standardized it under a named acronym — don't invent one.)*

### Plans get adversarial review before I commit **[confirmed]**
A single model's plan is one opinion. Consequential plans go through plan-agent and multi-model consensus first — cheap disagreement up front beats expensive rework. Never bypass the consensus hook; the plan-agent must write the plan itself so the hook fires.

### Prefer AI-generated code, keep human accountability explicit **[confirmed]**
I'd rather steer and review than hand-write. The model drafts, I approve, the consequences are mine. The tool is not a co-author.

### Don't assume anything is running **[confirmed]**
Stalled is the default state of most projects, including mine. SynergyAI, DebtFlow, Companion, MelloBooks, NutriScan, Casa AI, and a LinkedIn content system are all dead. I don't reference output, revenue, or activity without verifying it's actually live. Before claiming something doesn't exist, search — the home server has 49+ agents, 20+ skills, 75+ containers, and my mental model of it is incomplete.

---

## Code craft

### `??` over `||`, explicit over clever **[confirmed]**
Nullish coalescing or an explicit conditional, never `||`. Falsy-coercion bugs aren't worth the keystrokes saved.

### Don't delete code because it looks like too much **[confirmed]**
Volume isn't a reason to cut. Point out the issue, then fix it together. Deletion-by-overwhelm loses intent that was probably there for a reason.

### Ask array vs. object before assuming **[confirmed]**
I sometimes confuse the two in my own code. Ask rather than guess.

### Small files, immutable state, early returns **[confirmed]**
200–400 line files, immutable state, Zod at boundaries, early returns, parallel async, no `console.log` in production. Reviewability over personal flourish. UTC-6 for timestamps in Node-RED / SQL.

---

## Building & business

### Margin discipline is a habit, not a spreadsheet exercise **[confirmed]**
~$6 to make, sold for ~$50 (TheMellosDesigns 3D props) — and the same instinct applies at scale, where small per-unit savings compound into real monthly numbers. Cost-sensitivity is a default, not a project. I'm subscription-fatigued: "every month I pay for memberships, and nothing." The Etsy reality is 4 small shops at ~$389/mo combined, often net-negative after Skool/Alura/EverBee/MyDesigns/Printify. The problem isn't "design more," it's subscription ROI.

### Ship the smallest thing that proves the point — *aspired, not yet my behavior* **[confirmed tension]**
Stated taste: narrow prototype, minimal scope, assemble existing blocks, learn fast. Actual record: 16 Bambu printers + 2 Sovols sitting idle, multiple YouTube channels paused at zero output, a long list of dead projects, and production-grade infra built ahead of the thing that proves it's needed. The gap between the two is exactly what this file is supposed to surface. When I propose a new build, the useful question is: **which existing thing gets less attention as a result?**

### Don't inflate my output **[confirmed]**
I am not an influencer running 8 businesses shipping 90 videos a month. That framing is stale and exploitable. I'm a controls engineer with a demanding day job, a few small async income streams, and a lot of exploratory infrastructure. Use real shipped numbers, not aspirational ones.

---

## Working style

### Time is the scarcest resource **[confirmed]**
Every recommendation gets weighed against time first. Ceremony, preamble, and re-explaining cost more than they look. Every new commitment competes with sleep, Gisele, the things that actually make money, and OTTO. Don't suggest building more systems unless I ask.

### Direct over diplomatic **[confirmed]**
Skip the warm-up. Tell me what's wrong, including when the thing that's wrong is my idea. Push back when I'm rationalizing. Don't flatter — I have a good BS detector and flattery poisons the signal. When I correct you, take it, fix it, move on; don't collapse into apology and don't re-summarize what you just did.

### Finish the whole thing **[confirmed]**
"Full project" means full project: Cloudflare routes, docker-compose, env vars, DNS — not a README handing the admin back to me. Verify before claiming success (logs for Docker, read-back for files, browser-agent for UI). Delegate long autonomous sequences to an agent and report once. Consult the Obsidian vault before making claims about what I've decided.

---

## Review prompts (run these against the file above)

Standard interrogation:
- Which lines are **falsifiable** vs. unfalsifiable taste?
- Which are **common consensus** dressed up as personal conviction?
- Which are **too strong** as written?
- Which are **stale** or vendor-dependent (e.g. SICK/Keyence)?
- Which two opinions **contradict** each other?

Tensions worth pressure-testing every time they come up:
1. **"ML only where measurable ROI"** can kill the exploration that finds ROI. The defensible form is "no production deploy without ROI." Hold the weaker one.
2. **"Ship the smallest thing"** vs. the idle printer farm and paused channels. Stated taste says minimal-scope-to-learn; behavior shows infrastructure-ahead-of-proof. Surface the gap, don't smooth it over.
3. **"Edge-first beats PLC-first"** vs. safety-critical cases (e.g. FOD on EV batteries **[unverified]**). The honest version is edge-first for data paths, PLC-first where safety or determinism is on the line.

---

This is a living file. It is meant to be wrong in places. Correct it and I'll rewrite — and propose the matching update to the vault.
