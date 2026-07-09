---
name: SSH idle drops fixed via ClientAliveInterval
description: SSH sessions to home server dropped when idle (no server-side trace); root cause was ClientAliveInterval 0 + tunneled traffic getting silently reaped; fixed by enabling keepalive probes in sshd_config
type: project
---

Root cause: sshd_config had ClientAliveInterval 0 (disabled, default) — the server never sent keepalive probes during idle periods. SSH access to this box goes through the cloudflared tunnel (172.18.0.68 in logs), and an idle TCP stream through that path was getting silently reaped by an intermediate timeout with zero trace in sshd logs (no broken pipe, no timeout entries — nothing, because the server never even checked). Confirmed via: 22h of journalctl -u ssh showed no abnormal disconnects tied to the mello account, cloudflared had 0 restarts/errors (tunnel itself stable), NIC drop rate negligible — ruling those out left the missing-keepalive explanation as the only one consistent with 'drops only when idle, no server-side evidence.'

Fix applied 2026-07-04: set ClientAliveInterval 30 and ClientAliveCountMax 3 in /etc/ssh/sshd_config, then 'systemctl reload ssh' (reload only restarts the listener, doesn't kill existing sessions). This makes sshd send a periodic null packet during idle, generating real traffic that keeps the tunnel/NAT mapping alive and lets the server actually detect a truly dead peer instead of hanging silently.

Note: the frequent short-lived SSH sessions from 172.18.0.68 seen in logs (every ~2min, key fingerprint /3usoydy...) are NOT related to this bug — that's an automated job (likely one of the n8n-claude-cli authorized_keys entries) doing one-shot commands through the tunnel, not a dropped interactive session. Don't mistake that traffic for the drop issue again.
