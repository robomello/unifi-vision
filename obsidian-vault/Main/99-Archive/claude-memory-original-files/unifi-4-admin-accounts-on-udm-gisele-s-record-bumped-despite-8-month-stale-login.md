---
name: UniFi: 4 admin accounts on UDM, Gisele's record bumped despite 8-month-stale login
description: UDM has 4 Super Admin/Owner accounts. May 2026 incident: repeated verify-identity prompts traced to giseledutrasantos@hotmail.com record updating without successful login
type: project
---

UDM Pro at 192.168.2.1 has **4 admin accounts** (queried via `GET /proxy/users/api/v2/users/admin/uos`):

| Account | Type | Role |
|---|---|---|
| `mello_roberto@hotmail.com` | Ubiquiti SSO | **Owner** |
| `commander_unifi` | Local | Super Admin (used by this server) |
| `giseledutrasantos@hotmail.com` | Ubiquiti SSO | Super Admin (Gisele) |
| `HomeAssistant` | Local | Super Admin (HA integration) |

**Why:** May 2026 — Roberto was getting repeated "verify identity" mobile-app prompts. Investigation found Gisele's account `login_time` was Sept 2025 (8 months stale) but `update_time` bumped to the current second. That field moves on failed auth attempts / 2FA challenges, not just successful logins.

**How to apply:** If repeated UniFi verify prompts come back, FIRST check `/proxy/users/api/v2/users/admin/uos` for any admin whose `update_time` is recent but `login_time` is old — that's the account being targeted. Owner's phone receives 2FA pushes for any SSO admin on the console, so a brute force on a less-used account still wakes the Owner.

**Mitigation playbook:** account.ui.com → Active Sessions → Sign out all → rotate password → enable TOTP 2FA. Then UDM Console Settings → demote any unused admin to Limited Admin or remove entirely to shrink attack surface.
