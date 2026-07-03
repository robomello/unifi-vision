/*
 * unifi-switch-card.js — near-photorealistic UniFi switch faceplate card
 * for Home Assistant Lovelace. Vanilla custom element, NO build step,
 * NO external imports. YAML-only configuration (no visual editor).
 *
 * Config:
 *   type: custom:unifi-switch-card
 *   entity: sensor.unifi_vision_shop_switch   # required (from unifi-vision poller)
 *   title: Shop Switch                        # optional; defaults to friendly_name
 *   show_poe: true                            # optional; default true — ⚡ N.NW badges
 *   led_mode: auto                            # optional; 'auto' (default: color+flash),
 *                                             # 'static' (color, no flash), 'off' (no LEDs)
 *
 * Entity contract (published by the unifi-vision poller via MQTT discovery):
 *   state: "14/26" (ports up / total)
 *   attributes: { model, mac, ports: [ { idx, name, up, speed, duplex,
 *                 poe_w, rx_bps, tx_bps, media } ], ts }   # ts = epoch seconds
 *
 * Traffic tiers (duplicated from poller config.py — keep in sync):
 *   max(rx_bps, tx_bps) < 1 KB/s  -> solid LED
 *   max(rx_bps, tx_bps) < 1 MB/s  -> slow flash (~1.2s)
 *   max(rx_bps, tx_bps) >= 1 MB/s -> fast flash (~0.3s)
 *
 * Staleness: (now - ts) > 20s -> desaturate + STALE ribbon.
 * Entity state "unavailable"/"unknown" (poller LWT) -> grey + OFFLINE ribbon.
 */
(() => {
  'use strict';

  // ---------------------------------------------------------------- constants
  const STALE_AFTER_S = 20;
  const TRAFFIC_LOW_BPS = 1024; // below: solid
  const TRAFFIC_HIGH_BPS = 1048576; // below: slow flash; at/above: fast flash

  const LED_DOWN = '#333333';
  const LED_FAST_ETH = '#f0a030'; // 10/100
  const LED_GIGABIT = '#30d158'; // 1000
  const LED_MULTI_GIG = '#4aa8ff'; // 2500/5000/10000 and SFP media

  // Shared port-geometry metrics (SVG user units)
  const RJ45_W = 34;
  const SFP_W = 40;
  const PORT_H = 46;
  const PITCH = 56; // column spacing
  const ROW_TOP_Y = 30;
  const ROW_BOT_Y = 84;
  const TWO_ROW_H = 150;

  // ------------------------------------------------------- geometry builders
  // UniFi numbering convention for two-row layouts: odd ports on the top row,
  // even ports on the bottom row, filling column by column left to right.
  function twoRowRj45(count, x0) {
    const out = [];
    const cols = Math.ceil(count / 2);
    for (let col = 0; col < cols; col += 1) {
      const x = x0 + col * PITCH;
      out.push({ idx: col * 2 + 1, x, y: ROW_TOP_Y, w: RJ45_W, h: PORT_H, type: 'rj45', badge: 'above' });
      if (col * 2 + 2 <= count) {
        out.push({ idx: col * 2 + 2, x, y: ROW_BOT_Y, w: RJ45_W, h: PORT_H, type: 'rj45', badge: 'below' });
      }
    }
    return out;
  }

  function singleRowRj45(count, x0, y) {
    const out = [];
    for (let i = 0; i < count; i += 1) {
      out.push({ idx: i + 1, x: x0 + i * PITCH, y, w: RJ45_W, h: PORT_H, type: 'rj45', badge: 'below' });
    }
    return out;
  }

  function sfpStack(idxTop, idxBottom, x) {
    return [
      { idx: idxTop, x, y: ROW_TOP_Y, w: SFP_W, h: PORT_H, type: 'sfp', badge: 'above' },
      { idx: idxBottom, x, y: ROW_BOT_Y, w: SFP_W, h: PORT_H, type: 'sfp', badge: 'below' },
    ];
  }

  // ------------------------------------------------------------ PORT_GEOMETRY
  // Keyed by UniFi `model` attribute. Unknown models fall through to
  // genericGeometry(ports.length) — never a blank card.
  const PORT_GEOMETRY = {
    // 24 RJ45 (2 rows of 12, odd top / even bottom) + 2 SFP cages (25/26), rack ears
    US24P250: {
      w: 1180, h: TWO_ROW_H, rackEars: true, label: 'US-24-250W',
      silkscreen: { x: 875, y: 75 },
      ports: [...twoRowRj45(24, 40), ...sfpStack(25, 26, 1060)],
    },
    // 8 RJ45 (2x4) + 2 SFP (9/10)
    US8P150: {
      w: 460, h: TWO_ROW_H, rackEars: false, label: 'US-8-150W',
      silkscreen: { x: 75, y: 75 },
      ports: [...twoRowRj45(8, 130), ...sfpStack(9, 10, 372)],
    },
    // 8 RJ45 (2x4), no SFP
    US8P60: {
      w: 410, h: TWO_ROW_H, rackEars: false, label: 'US-8-60W',
      silkscreen: { x: 75, y: 75 },
      ports: twoRowRj45(8, 130),
    },
    // USW Flex 5: 5 RJ45 in a single row
    USF5P: {
      w: 460, h: 112, rackEars: false, label: 'USW-FLEX-5',
      silkscreen: { x: 75, y: 56 },
      ports: singleRowRj45(5, 130, 32),
    },
    // USW-Lite-16-PoE: 16 RJ45 (2x8) only — no SFP on this model
    USL16LP: {
      w: 620, h: TWO_ROW_H, rackEars: false, label: 'USW-LITE-16-POE',
      silkscreen: { x: 75, y: 75 },
      ports: twoRowRj45(16, 130),
    },
    // UDM Pro: 8 RJ45 (1..8) + 2 SFP+ cages (9/10) + WAN RJ45 (11).
    // SFP/WAN silkscreen labels come from live port names when present.
    UDMPRO: {
      w: 560, h: TWO_ROW_H, rackEars: false, label: 'UDM-PRO',
      silkscreen: { x: 75, y: 75 },
      ports: [
        ...twoRowRj45(8, 130),
        ...sfpStack(9, 10, 372),
        { idx: 11, x: 442, y: 57, w: RJ45_W, h: PORT_H, type: 'wan', badge: 'below' },
      ],
    },
  };

  function genericGeometry(portCount) {
    const n = Number.isFinite(portCount) && portCount > 0 ? Math.floor(portCount) : 0;
    const cols = Math.max(1, Math.ceil(n / 2));
    return {
      w: 130 + cols * PITCH + 24,
      h: TWO_ROW_H,
      rackEars: false,
      label: `${n}-PORT`,
      silkscreen: { x: 75, y: 75 },
      ports: n > 0 ? twoRowRj45(n, 130) : [],
    };
  }

  // ------------------------------------------------------------------ helpers
  function esc(value) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return String(value).replace(/[&<>"']/g, (ch) => map[ch]);
  }

  function truncate(text, max) {
    return text.length > max ? `${text.slice(0, max - 1)}…` : text;
  }

  function fmtSpeed(speed) {
    const table = {
      10: '10 Mbps', 100: '100 Mbps', 1000: '1 Gbps',
      2500: '2.5 Gbps', 5000: '5 Gbps', 10000: '10 Gbps',
    };
    return table[speed] ?? `${speed} Mbps`;
  }

  function fmtBps(value) {
    const v = Number.isFinite(value) && value > 0 ? value : 0;
    if (v < 1024) return `${v} B/s`;
    if (v < 1048576) return `${(v / 1024).toFixed(1)} KB/s`;
    if (v < 1073741824) return `${(v / 1048576).toFixed(1)} MB/s`;
    return `${(v / 1073741824).toFixed(2)} GB/s`;
  }

  function ledColor(port) {
    if (port.up !== true) return LED_DOWN;
    const media = String(port.media ?? '').toUpperCase();
    if (media.includes('SFP')) return LED_MULTI_GIG;
    if (port.speed >= 2500) return LED_MULTI_GIG;
    if (port.speed >= 1000) return LED_GIGABIT;
    if (port.speed > 0) return LED_FAST_ETH;
    return LED_GIGABIT; // up but speed unreported — treat as generic link
  }

  function flashClass(port) {
    if (port.up !== true) return '';
    const peak = Math.max(port.rx_bps, port.tx_bps);
    if (peak < TRAFFIC_LOW_BPS) return '';
    if (peak < TRAFFIC_HIGH_BPS) return 'led-slow';
    return 'led-fast';
  }

  function normalizePorts(raw) {
    if (!Array.isArray(raw)) return [];
    const out = [];
    for (const entry of raw) {
      if (entry === null) continue;
      if (typeof entry !== 'object') continue;
      const idx = Number(entry.idx);
      if (!Number.isFinite(idx)) continue;
      out.push({
        idx,
        name: typeof entry.name === 'string' && entry.name.length > 0 ? entry.name : `Port ${idx}`,
        up: entry.up === true,
        speed: Number(entry.speed ?? 0),
        duplex: typeof entry.duplex === 'string' ? entry.duplex : '?',
        poe_w: Number(entry.poe_w ?? 0),
        rx_bps: Number(entry.rx_bps ?? 0),
        tx_bps: Number(entry.tx_bps ?? 0),
        media: typeof entry.media === 'string' ? entry.media : '',
      });
    }
    return out;
  }

  // --------------------------------------------------------------- SVG pieces
  // IDs below are scoped to this element's shadow root — no cross-card clashes.
  function svgDefs() {
    return `<defs>
      <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#45484e"/>
        <stop offset="0.08" stop-color="#393c42"/>
        <stop offset="0.5" stop-color="#2e3136"/>
        <stop offset="0.92" stop-color="#26282c"/>
        <stop offset="1" stop-color="#1d1f22"/>
      </linearGradient>
      <filter id="noiseF">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
        <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
      </filter>
      <filter id="ledGlow" x="-200%" y="-200%" width="500%" height="500%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>`;
  }

  function rackEarSvg(x, plateH) {
    return `<g>
      <rect x="${x}" y="8" width="26" height="${plateH - 16}" rx="3" fill="url(#metal)" stroke="#0a0a0b" stroke-width="1"/>
      <circle cx="${x + 13}" cy="28" r="5" fill="#101113" stroke="#000" stroke-width="1"/>
      <circle cx="${x + 13}" cy="${plateH - 28}" r="5" fill="#101113" stroke="#000" stroke-width="1"/>
    </g>`;
  }

  function plateSvg(geo) {
    const inset = geo.rackEars ? 30 : 0;
    const pw = geo.w - 2 * inset;
    const parts = [];
    if (geo.rackEars) {
      parts.push(rackEarSvg(0, geo.h));
      parts.push(rackEarSvg(geo.w - 26, geo.h));
    }
    parts.push(`<rect x="${inset}" y="0" width="${pw}" height="${geo.h}" rx="8" fill="url(#metal)" stroke="#0a0a0b" stroke-width="1.5"/>`);
    // bevel: top highlight, bottom shadow
    parts.push(`<rect x="${inset + 3}" y="2" width="${pw - 6}" height="2" rx="1" fill="rgba(255,255,255,0.10)"/>`);
    parts.push(`<rect x="${inset + 3}" y="${geo.h - 4}" width="${pw - 6}" height="2" rx="1" fill="rgba(0,0,0,0.45)"/>`);
    // subtle brushed-metal noise
    parts.push(`<rect x="${inset}" y="0" width="${pw}" height="${geo.h}" rx="8" filter="url(#noiseF)" opacity="0.55"/>`);
    return parts.join('');
  }

  function silkscreenSvg(geo, title) {
    const s = geo.silkscreen ?? { x: geo.w / 2, y: geo.h / 2 };
    return `<text x="${s.x}" y="${s.y - 5}" class="silk-name" text-anchor="middle">${esc(truncate(title, 18))}</text>
      <text x="${s.x}" y="${s.y + 13}" class="silk-model" text-anchor="middle">${esc(geo.label)}</text>`;
  }

  function portBodySvg(desc) {
    const bodyFill = desc.type === 'sfp' ? '#1b1d20' : '#141518';
    const parts = [];
    parts.push(`<rect x="${desc.x}" y="${desc.y}" width="${desc.w}" height="${desc.h}" rx="3" fill="${bodyFill}" stroke="#000" stroke-width="1"/>`);
    parts.push(`<rect x="${desc.x + 1.5}" y="${desc.y + 1}" width="${desc.w - 3}" height="1.5" fill="rgba(255,255,255,0.07)"/>`);
    if (desc.type === 'sfp') {
      // SFP cage: top vent + horizontal module slot
      parts.push(`<rect x="${desc.x + 3}" y="${desc.y + 4}" width="${desc.w - 6}" height="3" fill="#26292d"/>`);
      parts.push(`<rect x="${desc.x + 4}" y="${desc.y + desc.h / 2 - 4}" width="${desc.w - 8}" height="8" rx="1" fill="#0a0b0c" stroke="#2c2f33" stroke-width="0.8"/>`);
    } else {
      // RJ45: pin notch (top center) + contact-pins hint
      parts.push(`<rect x="${desc.x + desc.w / 2 - 7}" y="${desc.y + 2.5}" width="14" height="6" rx="1" fill="#0a0b0c"/>`);
      parts.push(`<rect x="${desc.x + 6}" y="${desc.y + 12}" width="${desc.w - 12}" height="2" fill="#26292d"/>`);
    }
    return parts.join('');
  }

  function portSvg(desc, port, cfg) {
    const lit = port !== undefined && port.up === true;
    const color = port !== undefined ? ledColor(port) : LED_DOWN;
    const flash = port !== undefined && cfg.led_mode === 'auto' ? flashClass(port) : '';
    const parts = [`<g class="port" data-idx="${desc.idx}">`];
    // enlarged transparent hit area (covers badge zone too)
    parts.push(`<rect x="${desc.x - 4}" y="${desc.y - 15}" width="${desc.w + 8}" height="${desc.h + 30}" fill="transparent"/>`);
    parts.push(portBodySvg(desc));
    parts.push(`<text x="${desc.x + desc.w / 2}" y="${desc.y + desc.h - 14}" class="port-num" text-anchor="middle">${desc.idx}</text>`);
    if (cfg.led_mode !== 'off') {
      const glow = lit ? ' filter="url(#ledGlow)"' : '';
      parts.push(`<rect class="led ${flash}" x="${desc.x + 5}" y="${desc.y + desc.h - 9.5}" width="${desc.w - 10}" height="4.5" rx="1.5" fill="${color}"${glow}/>`);
    }
    // badge slot: SFP/WAN get a silkscreen label (live port name when present);
    // RJ45 gets the PoE badge when drawing power.
    const badgeY = desc.badge === 'above' ? desc.y - 6 : desc.y + desc.h + 14;
    const isCage = desc.type === 'sfp' ? true : desc.type === 'wan';
    if (isCage) {
      const fallback = desc.type === 'wan' ? 'WAN' : 'SFP';
      const label = port !== undefined ? port.name : fallback;
      const shown = label.startsWith('Port ') ? fallback : label;
      parts.push(`<text x="${desc.x + desc.w / 2}" y="${badgeY}" class="silk-port" text-anchor="middle">${esc(truncate(shown, 10))}</text>`);
    } else if (cfg.show_poe && port !== undefined && port.poe_w > 0) {
      parts.push(`<text x="${desc.x + desc.w / 2}" y="${badgeY}" class="poe" text-anchor="middle">⚡${port.poe_w.toFixed(1)}W</text>`);
    }
    parts.push('</g>');
    return parts.join('');
  }

  function tipHtml(port) {
    const lines = [`<b>Port ${port.idx}</b> · ${esc(port.name)}`];
    if (port.up === true) {
      lines.push(`${esc(fmtSpeed(port.speed))} · ${esc(port.duplex)} duplex`);
    } else {
      lines.push('link down');
    }
    if (port.poe_w > 0) lines.push(`PoE ${port.poe_w.toFixed(1)} W`);
    lines.push(`RX ${fmtBps(port.rx_bps)} · TX ${fmtBps(port.tx_bps)}`);
    return lines.join('<br>');
  }

  // ---------------------------------------------------------------------- CSS
  const CARD_CSS = `
    :host { display: block; }
    ha-card, .card {
      display: block;
      position: relative;
      overflow: hidden;
      padding: 12px;
      color: var(--primary-text-color, #e8eaed);
      background: var(--card-background-color, var(--ha-card-background, #1c1c1e));
      border-radius: var(--ha-card-border-radius, 12px);
    }
    .title {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin: 0 2px 8px 2px;
      font-size: 15px;
      font-weight: 600;
      color: var(--primary-text-color, #e8eaed);
    }
    .upcount { font-size: 12px; font-weight: 500; opacity: 0.7; }
    .wrap { position: relative; }
    svg { display: block; width: 100%; height: auto; }
    .silk-name { font: 600 13px sans-serif; fill: #b7bcc2; letter-spacing: 0.06em; }
    .silk-model { font: 500 10px sans-serif; fill: #7d838a; letter-spacing: 0.14em; }
    .silk-port { font: 500 8.5px sans-serif; fill: #9aa0a6; }
    .port-num { font: 600 7px sans-serif; fill: rgba(255,255,255,0.38); pointer-events: none; }
    .poe { font: 600 9px sans-serif; fill: #ffd60a; }
    .port { cursor: pointer; }
    @keyframes led-slow-k { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
    @keyframes led-fast-k { 0% { opacity: 1; } 50% { opacity: 0.15; } 100% { opacity: 1; } }
    .led-slow { animation: led-slow-k 1.2s ease-in-out infinite; }
    .led-fast { animation: led-fast-k 0.3s linear infinite; }
    .stale .wrap svg { filter: saturate(0.2); }
    .offline .wrap svg { filter: grayscale(1) brightness(0.7); }
    .ribbon {
      display: none;
      position: absolute;
      top: 16px;
      right: -32px;
      transform: rotate(45deg);
      background: #c0392b;
      color: #fff;
      font: 700 10px/1.7 sans-serif;
      letter-spacing: 0.12em;
      padding: 1px 36px;
      z-index: 3;
      pointer-events: none;
    }
    .stale .ribbon, .offline .ribbon { display: block; }
    .stale .ribbon { background: #b7791f; }
    .tip {
      display: none;
      position: absolute;
      z-index: 4;
      max-width: 240px;
      background: rgba(18, 19, 22, 0.95);
      color: #e8eaed;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 6px 9px;
      font: 400 11px/1.55 sans-serif;
      pointer-events: none;
      white-space: nowrap;
    }
    .tip.show { display: block; }
    .missing { font: 400 13px/1.5 sans-serif; opacity: 0.8; padding: 8px; }
  `;

  // -------------------------------------------------------------- the element
  class UnifiSwitchCard extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this._config = null;
      this._renderKey = '';
      this._ts = 0;
      this._entityState = '';
      this._geoH = TWO_ROW_H;
      this._pinnedIdx = null;
      this._timer = null;
      this._portsByIdx = new Map();
    }

    setConfig(config) {
      const validEntity = typeof config?.entity === 'string' && config.entity.length > 0;
      if (!validEntity) {
        throw new Error('unifi-switch-card: "entity" is required (e.g. sensor.unifi_vision_shop_switch)');
      }
      this._config = {
        entity: config.entity,
        title: config.title ?? null,
        show_poe: config.show_poe ?? true,
        led_mode: config.led_mode ?? 'auto',
      };
      this._renderKey = ''; // force re-render on next hass set
    }

    set hass(hass) {
      if (this._config === null) return;
      const stateObj = hass?.states?.[this._config.entity] ?? null;
      if (stateObj === null) {
        if (this._renderKey !== 'missing') {
          this._renderKey = 'missing';
          this._renderMissing();
        }
        return;
      }
      const attrs = stateObj.attributes ?? {};
      const ports = normalizePorts(attrs.ports);
      const data = {
        state: String(stateObj.state ?? ''),
        title: this._config.title ?? attrs.friendly_name ?? this._config.entity,
        model: typeof attrs.model === 'string' ? attrs.model : '',
        ports,
      };
      this._ts = Number(attrs.ts ?? 0);
      this._entityState = data.state;
      // Re-render only when render-relevant data changed (ts excluded — the
      // freshness timer handles staleness without DOM thrash on every poll).
      const key = JSON.stringify([data.state, data.title, data.model, ports]);
      if (key !== this._renderKey) {
        this._renderKey = key;
        this._render(data);
      }
      this._updateFreshness();
    }

    connectedCallback() {
      if (this._timer === null) {
        this._timer = window.setInterval(() => this._updateFreshness(), 5000);
      }
    }

    disconnectedCallback() {
      if (this._timer !== null) {
        window.clearInterval(this._timer);
        this._timer = null;
      }
    }

    getCardSize() {
      return Math.max(2, Math.round(this._geoH / 50) + 1);
    }

    _renderMissing() {
      this.shadowRoot.innerHTML = `<style>${CARD_CSS}</style>
        <ha-card class="card"><div class="missing">unifi-switch-card: entity <b>${esc(this._config.entity)}</b> not found.</div></ha-card>`;
    }

    _render(data) {
      const geo = PORT_GEOMETRY[data.model] ?? genericGeometry(data.ports.length);
      this._geoH = geo.h;
      this._portsByIdx = new Map(data.ports.map((p) => [p.idx, p]));
      this._pinnedIdx = null;
      const portsMarkup = geo.ports
        .map((desc) => portSvg(desc, this._portsByIdx.get(desc.idx), this._config))
        .join('');
      const upBadge = /^\d+\/\d+$/.test(data.state) ? `${esc(data.state)} up` : '';
      this.shadowRoot.innerHTML = `<style>${CARD_CSS}</style>
        <ha-card class="card">
          <div class="title"><span>${esc(data.title)}</span><span class="upcount">${upBadge}</span></div>
          <div class="wrap">
            <svg viewBox="0 0 ${geo.w} ${geo.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(data.title)} faceplate">
              ${svgDefs()}
              ${plateSvg(geo)}
              ${silkscreenSvg(geo, data.title)}
              ${portsMarkup}
            </svg>
            <div class="tip"></div>
          </div>
          <div class="ribbon"></div>
        </ha-card>`;
      const wrap = this.shadowRoot.querySelector('.wrap');
      const tip = this.shadowRoot.querySelector('.tip');
      if (wrap !== null && tip !== null) this._attachEvents(wrap, tip);
      this._updateFreshness();
    }

    _attachEvents(wrap, tip) {
      wrap.addEventListener('mousemove', (ev) => {
        if (this._pinnedIdx !== null) return;
        const g = ev.target instanceof Element ? ev.target.closest('g.port') : null;
        if (g === null) {
          tip.classList.remove('show');
          return;
        }
        this._showTip(Number(g.getAttribute('data-idx')), ev.clientX, ev.clientY, wrap, tip);
      });
      wrap.addEventListener('mouseleave', () => {
        if (this._pinnedIdx === null) tip.classList.remove('show');
      });
      // tap-to-pin popup (mobile/touch); tap elsewhere or same port to dismiss
      wrap.addEventListener('click', (ev) => {
        const g = ev.target instanceof Element ? ev.target.closest('g.port') : null;
        if (g === null) {
          this._pinnedIdx = null;
          tip.classList.remove('show');
          return;
        }
        const idx = Number(g.getAttribute('data-idx'));
        if (this._pinnedIdx === idx) {
          this._pinnedIdx = null;
          tip.classList.remove('show');
          return;
        }
        this._pinnedIdx = idx;
        const r = g.getBoundingClientRect();
        this._showTip(idx, r.left + r.width / 2, r.top, wrap, tip);
      });
    }

    _showTip(idx, clientX, clientY, wrap, tip) {
      const port = this._portsByIdx.get(idx);
      if (port === undefined) {
        tip.classList.remove('show');
        return;
      }
      tip.innerHTML = tipHtml(port);
      tip.classList.add('show');
      const rect = wrap.getBoundingClientRect();
      const tw = tip.offsetWidth;
      const th = tip.offsetHeight;
      let x = clientX - rect.left + 14;
      let y = clientY - rect.top - th - 12;
      x = Math.min(Math.max(4, x), Math.max(4, rect.width - tw - 4));
      y = Math.min(Math.max(4, y), Math.max(4, rect.height - th - 4));
      tip.style.left = `${x}px`;
      tip.style.top = `${y}px`;
    }

    _updateFreshness() {
      const card = this.shadowRoot.querySelector('ha-card');
      const ribbon = this.shadowRoot.querySelector('.ribbon');
      if (card === null) return;
      if (ribbon === null) return;
      const offline = ['unavailable', 'unknown'].includes(this._entityState);
      const stale = !offline && this._ts > 0 && (Date.now() / 1000 - this._ts) > STALE_AFTER_S;
      card.classList.toggle('offline', offline);
      card.classList.toggle('stale', stale);
      ribbon.textContent = offline ? 'OFFLINE' : (stale ? 'STALE' : '');
    }
  }

  if (customElements.get('unifi-switch-card') === undefined) {
    customElements.define('unifi-switch-card', UnifiSwitchCard);
  }

  window.customCards = window.customCards ?? [];
  window.customCards.push({
    type: 'unifi-switch-card',
    name: 'UniFi Switch Card',
    description: 'Near-photorealistic UniFi switch faceplate with live per-port LEDs (unifi-vision poller).',
  });
})();
