---
name: UniFi: commander_unifi has Super Admin on all apps
description: Credential commander_unifi (in ~/.env as UNIFI_USER/UNIFI_PASS) is Super Admin role on UDM Pro 192.168.2.1 with admin permissions on every UniFi service
type: reference
---

The local UniFi account `commander_unifi` is **Super Admin**, NOT Protect-only as I previously assumed. Verified via `GET /api/users/self`:

- Role: Super Admin (group: MelloHome)
- Permissions (14 services, all `admin`):
  - access · calculus · connect · drive · fabric · innerspace · led
  - network · olympus · protect · talk · talk-relay
  - system.management.location · system.management.user

Console: UDM Pro at `192.168.2.1`, firmware UDMPRO.al324.v5.1.12.a10f0a5 (beta channel), owner Roberto De Mello (sso_uuid `<REDACTED-UUID-36>`). UNVR for Protect cameras at `192.168.2.169`.

**API gotcha (UDM 5.x):** even with Super Admin, the legacy controller paths return 404 or HTML SPA fallback. Audit/login-history endpoints are NOT exposed via REST in this firmware. What works for sure: `/api/users/self`, `/api/system`, `/proxy/network/api/s/default/stat/sysinfo`, `/proxy/network/api/s/default/self`. To pull actual login/audit logs requires either SSH on the UDM (currently disabled), the cloud-side `account.ui.com` Owner session, or capturing the SPA's internal XHRs.

Use this credential before guessing what it can do.
