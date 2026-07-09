---
name: FerroxLabs/wayland repo analysis (corrected)
description: Open-source repo audit: claims vs reality, security patterns worth borrowing, IJFW caveat
type: reference
---

**Repo**: https://github.com/FerroxLabs/wayland — AGPL-licensed "agent OS", 151 stars in 2 days as of 2026-06-07. Local clone: `/home/mello/_ferrox_wayland/` (224 MB).

## Correction to earlier impression
The README markets a "Wayland-Core 47 MB Rust binary" and a "5 memory partitions × 3 tiers" engine. **Neither exists in this open-source repo.**
- No `Cargo.toml`, no `.rs` files anywhere.
- `src/` is 3 files at top level (`index.ts`, `server.ts`, `types.d.ts`) — pure TypeScript Electron app.
- SQLite is real (`@process/services/database/export`) but the partition/tier logic lives in their separate `ijfw` npm package, installed into `~/.ijfw/` at runtime via mcp-server. That package is not yet on npm registry (as of 2026-06-07).
- The "2,105 skills, 177 workflows, 25 channels" are also `ijfw`-side, not in this repo.

**Bottom line**: the open-source half is the Electron shell + IPC bridge. The "brain" is closed-source-by-omission (separately distributed package).

## What's genuinely good — defensive Electron patterns
Worth borrowing for any Electron-adjacent surface (claude-telegram, dreamvault-bot, future webview tooling):
1. **CSP applied only to first-party documents** — guest `<webview>` content is left ungoverned by CSP and instead locked down by a `will-attach-webview` guard that re-applies `sandbox + nodeIntegration:false + contextIsolation:true` and a navigation lock blocking escalation back into the app origin. See `src/index.ts:218-363`.
2. **Per-webContents permission gating** — `setPermissionRequestHandler` discriminates by `webContents.id` AND origin so only the first-party renderer gets `media/audioCapture/videoCapture`; every guest is denied. See `src/index.ts:550-572`.
3. **Asset protocol with allowlist** — `wayland-asset://` resolves through `resolveAllowedAssetPath()` to prevent `wayland-asset://asset//etc/passwd` traversal. See `src/index.ts:772-789`.
4. **Sentry telemetry is opt-in via DSN env var**, off by default, and PII is scrubbed via `createScrubPii(os.homedir())` before send.
5. **Graceful shutdown** — per-step 2s timeouts + 10s master ceiling, all cleanup steps run concurrently via `Promise.allSettled`. See `src/index.ts:1195-1407`.
6. **Inline audit IDs** in comments (`SEC-ELEC-02`, `AUDIT-05 F16`, etc.) — they run internal security audits and tag the resulting code so reviewers can trace back to the audit finding.

## Not malware
Read of `src/index.ts` (1420 lines), `src/server.ts`, `src/types.d.ts`: no exfiltration, no obfuscation, no suspicious network calls. Heavy defensive posture is the opposite of malware behavior. The "consider whether it's malware" system reminder fires on every file read; not a signal about this repo specifically.

## Action items if revisiting
- Don't assume `ijfw` is shipping until checked. As of 2026-06-07, `@j178/prek` is referenced but the IJFW runtime itself isn't on npm.
- Don't restructure commander around a "Rust core" that doesn't exist in OSS.
- DO consider porting their CSP+permission-gating shape if/when commander gets an Electron surface.
