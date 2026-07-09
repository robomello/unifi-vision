---
name: seo-writer Skill (Julian Goldie SEO Method, Claude-First)
description: Adapt Julian Goldie's video #5nWeSkOn13c SEO method as a Claude Code seo-writer skill at /home/mello/skills/seo-writer/; SOP-template prompt, 6-field output schema, no schema-injector/EMD/n8n in this scope
type: project
---

# seo-writer Skill — Julian Goldie SEO Method Ported to Claude

Source: Julian Goldie's video <https://youtu.be/5nWeSkOn13c> ("ChatGPT 5.5 AI SEO: How to Rank #1 on Autopilot!", 24 Apr 2026, GoldieAgencySEO). Frame-by-frame analysis showed the **video itself is a Claude vs ChatGPT A/B test** — Goldie's own pick on camera was Opus 4.6 ("I'm still going to go with Opus 4.6. I still think that's better for creating content"). The clickbait title sells GPT-5.5; the actual content shows Claude winning. His paid Skool community ("AI Profit Boardroom") has sidebar trainings dominated by Claude.

## What's in the Video (5 methods)

| # | Method | Goldie's tool | Mello equivalent |
|---|---|---|---|
| 1 | SEO blog writer | Claude Opus 4.6 Extended (winning side of A/B) | `claude --print --model opus`, `copywriting`/`humanizer`/`content-idea-generator` skills, `roberto-voice.md` |
| 2 | EMD landing pages | ChatGPT Codex single-file `index.html` | Claude Code + `frontend-design` skill (Codex's twin) |
| 3 | AI SEO tools (calculator) | Codex with SKILL.md for Frontend Design + SEO Fundamentals via `skillboss` | Claude Code already has `~/.claude/skills/` |
| 4 | Schema injection | Codex follow-up: "add technical SEO schema + relevant entities" → FAQ + Article + Breadcrumb schema | `geo-audit-agent` audits but doesn't inject — gap |
| 5 | Workspace agents (24/7) | ChatGPT Workspace Agents "OpenClaw SEO Publisher", "Skool Growth Operator", "AI News SEO Writer" → Google Doc with 6-field schema | n8n at `n8n.synai.ai` + `/loop` skill + Commander cron + `claude --print` |

## The SOP Prompt (visible on screen — not paywalled)

```
Create an SEO optimized article for this:
Keyword = {KEYWORD}
Content Outline = {HEADINGS + OUTLINE}

For content creation, do this:
- SOURCE CONTEXT: Write as {AUTHOR PERSONA — credentials, business, audience}
- {INTERNAL LINK 1 — community/lead magnet}
- {INTERNAL LINK 2 — strategy session/CTA}

Style:
- Easy to read + feels conversational
- UK grammar
- Add FAQs
```

That's the entire "secret prompt" — a templated SOP, easy to clone with Roberto's voice + brands.

## EMD Landing-Page Tactic (visible, working)

Short generic domain + literal keyword as `<title>` and `<h1>`, with FAQ + Schema markup. Goldie's example: `enterpriseseroicalculator.com` ranks #1 for "enterprise seo roi calculator". That's the whole ranking trick.

## Final Scope Decided (after Roberto's call)

Build ONE thing: **`seo-writer` skill** at `/home/mello/skills/seo-writer/`. Skip schema injector, EMD reference, and n8n template for now. Why a skill: writing an SEO article needs interactive steering (per-section review, voice tweaks, outline approval) and orchestrates multiple existing skills — textbook skill case per `skill-vs-agent.md`.

## Skill Layout

```
/home/mello/skills/seo-writer/
├── SKILL.md                            # entry point + workflow
├── learnings.md                        # populated over time
├── references/
│   ├── sop-template.md                 # Goldie's prompt shape, voice-agnostic
│   ├── output-schema.md                # 6 fields: Title/Meta/Primary kw/Secondary kw/Slug/Body
│   └── seo-checklist.md                # FAQ, EEAT, internal links, headings
└── evals/
    └── evals.json                      # 3 keywords, binary asserts on schema fields
```

## SKILL.md Activation Logic

1. Read `learnings.md`
2. Inputs (ask if missing): `KEYWORD` (required), `OUTLINE` (optional — generate via `content-idea-generator` if absent), `BRAND` (optional — if set, read `~/.claude/brand-context/{brand}/brand.md`; always read `~/.claude/brand-context/shared/roberto-voice.md`)
3. **Outline phase** — produce H2/H3 outline + FAQ list (5+), present to Roberto for review/edits
4. **Draft phase** — `claude --print --model opus` with SOP template populated. UK grammar, conversational, ≥1500 words, FAQ at end
5. **Humanize phase** — pipe draft through existing `humanizer` skill
6. **Schema phase** — wrap in 6-field output schema, write to `/home/mello/commander/projects/seo-articles/{date}_{slug}.md` with frontmatter
7. **Quality gate** — Haiku-cheap pass: keyword in H1, FAQ section present, ≥1500 words, no AI tells (`furthermore`, `delve`, `landscape`, em-dashes), at least one internal link slot

## Output 6-Field Schema (Goldie's frame 44)

`Title | Meta description | Primary keyword | Secondary keywords (5–6) | URL slug | Blog post body`

## Reuse — no new code where possible

- Voice → `~/.claude/brand-context/shared/roberto-voice.md`
- Humanization → existing `humanizer` skill (chained)
- Outline brainstorm → existing `content-idea-generator` skill (chained)
- Quality pass → `claude --print --model haiku` per `performance.md` (cheap models for frequent calls)

## Eval (3 keywords, binary asserts)

| Keyword | Asserts |
|---|---|
| "AI SEO calculator" | 6 fields, body ≥1500 words, FAQ ≥5, keyword in H1 |
| "claude code skills" | same + ≥1 internal link slot |
| "drinkware printing" (drinkwaretrove) | same + voice match against `roberto-voice.md` via Haiku grader |

## Explicitly NOT This Skill

- No publishing (output is markdown; user decides where it goes)
- No image generation (could be `local-image-gen` add later)
- No web research (outline phase asks for source links; doesn't crawl — Goldie's "source context" is just author bio)

## Deferred (Roberto rejected for now)

- Schema injector (HTML in → HTML+JSON-LD out for FAQ/Article/Breadcrumb/Organization)
- EMD landing-page reference (hero/H1/FAQ/schema/footer authority pattern)
- n8n scheduled-content workflow with Drive write emitting 6-field schema

Easy adds once `seo-writer` is in place — flag them if Roberto comes back asking to "publish" or "rank" the output.

## Surprise from Visuals (not in transcript)

Codex calls SKILL.md files via a `skillboss` guidance system (frame 28) — same pattern Roberto already runs in `~/.claude/skills/`. **Roberto already has this primitive.** The whole video is essentially demoing what Claude Code + skills already does on Mello's home server.
