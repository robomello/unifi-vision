# Registering the unifi-switch-card Lovelace resource

The card is a **single file**: `card/unifi-switch-card.js`. No build step, no second
resource, no load-order concerns (the optional `port-geometry.js` split was not needed —
the card is well under the 800-line limit).

## 1. Deploy the file to Home Assistant

Copy the card to the Home Assistant config share using Samba, SSH, or your
preferred deployment method:

```
/config/www/unifi-vision/unifi-switch-card.js
```

`/config/www/` is served by HA at `/local/`. Create the `unifi-vision` subfolder if it
does not exist. If `/config/www/` itself did not exist before, restart Home Assistant
once (HA only starts serving `/local/` after the folder exists at boot).

## 2. Register the resource

### Via UI (default, storage-mode dashboards)
1. Settings -> Dashboards -> three-dot menu (top right) -> **Resources**.
   (The Resources menu only appears with **Advanced Mode** enabled on your user profile.)
2. **Add resource**:
   - URL: `/local/unifi-vision/unifi-switch-card.js?v=1`
   - Resource type: **JavaScript module**
3. Save, then hard-refresh the browser (Ctrl+Shift+R).

### Via YAML (only if the dashboard is YAML-mode)
```yaml
lovelace:
  mode: yaml
  resources:
    - url: /local/unifi-vision/unifi-switch-card.js?v=1
      type: module
```

## 3. Cache-busting (`?v=`) — required on EVERY redeploy

Browsers and the HA companion apps cache `/local/` resources aggressively. After every
copy of a new `unifi-switch-card.js` to `/config/www/unifi-vision/`:

1. Edit the resource URL and **bump the version query**: `?v=1` -> `?v=2` -> `?v=3` ...
2. Hard-refresh the browser (Ctrl+Shift+R). In the companion app:
   Settings -> Companion App -> Debugging -> **Reset frontend cache**.

If you skip the `?v=` bump, the browser may serve the previous card version.
Bump first, verify second.

## 4. Add the dashboard view

Paste `deploy/network-view.yaml` as a new view in the dashboard raw configuration
editor (one `custom:unifi-switch-card` per switch). If the card
shows a red "Custom element doesn't exist: unifi-switch-card" box, the resource is not
loaded yet — re-check step 2 and hard-refresh.
