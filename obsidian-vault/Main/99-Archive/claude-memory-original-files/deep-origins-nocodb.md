---
name: Deep Origins NocoDB
description: Deep Origins NocoDB base pjf6dzz40r87uqh — table ids, exact column-name oddities, internal URL gotcha
type: reference
---

**Base Id**: `pjf6dzz40r87uqh`
**UI**: https://nocodb.synai.ai/dashboard/#/nc/base/pjf6dzz40r87uqh
**Container-internal URL**: `http://nocodb:8080` (public is CF-Access gated; server-to-server MUST use internal)
**Auth**: `xc-token: $NOCODB_API`

## Tables

| Title | Id | Purpose | Natural key |
|---|---|---|---|
| Video Project | `myrvllg0hjmee1o` | Per-animal project metadata + Evolution JSON | `Title` |
| Evolution Other Scenes | `msixny7e4dyqq8q` | Opening/closing, blog (8 sections), YouTube metadata | `animal` |
| Generation | `mgj4hikjt6f4th8` | One row per species. Replace-not-append per `Animal Name` | `Specie #` + `Animal Name` |
| Description | `mkqt2tld00spvp6` | YouTube view/like stats — separate flow |
| Extra Videos | `mqo2wzhxowtiegf` | Auxiliary scene clips |
| Pre-Production Scoring | `mz53w61gnushmg1` | Content planning |
| (3 car tables) | — | Unrelated car-evolution sister project |

## Column-name gotchas (case + whitespace sensitive)

- `Specie #` (with space) — NOT `Specie#`
- `folder-name` (lowercase, hyphen) — NOT `Folder` or `folder_name`
- `Evolution JSON` (with space) — NOT `Evolution_JSON`
- `Project Name` (Video Project) vs `project name` (Generation, lowercase)
- `Lenght` (typo) — preserved deliberately, do NOT "fix" to Length
- `Weight` Decimal kg, `Lenght` Decimal meters

No relation/link fields — tables linked via TEXT fields (`Animal Name`, `project name`, `Record ID`).

## Wired into pipeline

`deep_origins/tools/research/step_10_nocodb.py` does the persistence. Re-run in isolation:

```bash
docker exec deep-origins python3 -m deep_origins.tools.research.pipeline \
  --job-dir /data/sites/deep-origins/jobs/<id> \
  --animal "<name>" --depth standard --orientation portrait \
  --from 10
```

## Why this memory exists

Roberto pointed out on 2026-04-25 that this base "has been there for weeks" but I had no memory of it. n8n workflow originally used Airtable; NocoDB equivalent was set up later but never recorded.
