---
name: Docker: mount ~/.claude dir, never the single .credentials.json file
description: Containerized claude CLI 401s on a stale single-file ~/.claude/.credentials.json bind mount; fix = mount the whole ~/.claude dir (rw). Hit garden-telegram + dreamvault-gen, fixed 2026-06-21.
type: reference
---

**Symptom:** a containerized `claude` CLI returns `401 Invalid authentication credentials` while the exact same call works on the host.

**Root cause:** Docker bind-mounts a *single file* by inode. When the host `claude` refreshes its OAuth token it writes a new file and atomically renames it over the old one (new inode). A container that bind-mounts the single file `/home/mello/.claude/.credentials.json` stays pinned to the ORIGINAL inode and keeps reading the stale, now-expired token, so it 401s. The host is unaffected, and it can sit broken for days until the container is recreated.

**Diagnose (compare inodes + token expiry):**
- host: `stat -c %i ~/.claude/.credentials.json`
- container: `docker exec <c> stat -c %i /home/mello/.claude/.credentials.json`
- Different inode = stale. Token expiry is the `claudeAiOauth.expiresAt` field (epoch ms).

**Fix:** mount the whole directory instead of the file, so path resolution happens per-open and rotations are visible. Replace the `.credentials.json` single-file volume line with:
`- /home/mello/.claude:/home/mello/.claude:rw`
(rw also lets the in-container CLI refresh+persist the token itself.)

**Audit every running container for the bad pattern:**
`for c in $(docker ps --format '{{.Names}}'); do docker inspect $c --format '{{range .Mounts}}{{.Destination}}{{"\n"}}{{end}}' | grep -q '/.claude/.credentials.json$' && echo "VICTIM: $c"; done`

**History:** bit `garden-telegram` and `dreamvault-gen`; both fixed 2026-06-21 by swapping to the dir mount. `image-telegram` and most other claude containers already mount the dir and were unaffected. Recreate after editing compose (`docker stop && rm && compose up -d`) since the mount only re-resolves on container creation.
