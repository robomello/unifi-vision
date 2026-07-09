---
name: synai.ai personal blog (Astro)
description: synai.ai apex serves Roberto's Astro blog; container synai-blog:8068; publish = add md + npm run build; Obsidian pipeline still TODO
type: project
---

Roberto's personal blog went LIVE 2026-06-07 at https://synai.ai (apex) and https://www.synai.ai.

Stack: Astro static "blog" starter, dark GitHub-style theme (accent #79c0ff, canvas #0d1117). Project at /home/mello/commander/projects/synai-blog. Served by docker service "synai-blog" (nginx:alpine, network n8n-net, host 127.0.0.1:8068) from .../synai-blog/dist. Public + indexed: RSS at /rss.xml, sitemap, OpenGraph.

Routing (via the EXISTING CF tunnel, added by cloudflare-agent): ingress synai.ai + www.synai.ai -> http://synai-blog:80, plus a proxied apex CNAME synai.ai -> <tunnel-id>.cfargotunnel.com (CNAME flattening; MX/email left intact). Brand/title = "Roberto de Mello".

Publishing TODAY = add a markdown file under src/content/blog/ (frontmatter: title, description, pubDate, tags, draft) then run `npm run build`. nginx serves the bind-mounted dist/, so rebuilds go live immediately, no container restart.

NOT yet built: the Obsidian -> Astro authoring pipeline + one-command publish (the chosen long-term workflow). Header/footer currently have only an RSS link (real social handles TBD). Favicon still Astro default. First post slug: harness-design-long-running-agents (summary of Anthropic's "Harness design for long-running application development").
