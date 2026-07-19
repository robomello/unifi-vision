import { fileURLToPath } from "url";
import path from "path";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const puppeteer = require("/home/mello/.nvm/versions/node/v24.13.1/lib/node_modules/puppeteer");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PAGE = "file://" + path.join(__dirname, "index.html");
const CHROME = "/home/mello/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome";

let pass = 0, fail = 0;
const results = [];
function check(name, cond, detail = "") {
  if (cond) { pass++; results.push(`  ✓ ${name}`); }
  else { fail++; results.push(`  ✗ ${name}  ${detail}`); }
}

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 2 });

  // ---- trap every error channel ----
  const consoleErrors = [], pageErrors = [], failedReqs = [];
  page.on("console", m => { if (m.type() === "error") consoleErrors.push(m.text()); });
  page.on("pageerror", e => pageErrors.push(String(e)));
  page.on("requestfailed", r => failedReqs.push(`${r.url()} ${r.failure()?.errorText}`));

  const resp = await page.goto(PAGE, { waitUntil: "networkidle0" });

  // 1. HTTP + error channels
  check("navigation ok (non-error status)", resp.status() === 200 || resp.status() === 0, `status=${resp.status()}`);
  check("no page (JS runtime) errors", pageErrors.length === 0, JSON.stringify(pageErrors));
  check("no console.error output", consoleErrors.length === 0, JSON.stringify(consoleErrors));
  check("no failed subresource requests", failedReqs.length === 0, JSON.stringify(failedReqs));

  // 2. structure actually rendered (JS ran, not just static HTML)
  const dom = await page.evaluate(() => {
    const txt = el => (el ? el.textContent.trim() : null);
    return {
      kpiTiles: [...document.querySelectorAll("#kpiRow .tile")].map(t => ({
        label: txt(t.querySelector(".label")),
        value: txt(t.querySelector(".value")),
        foot:  txt(t.querySelector(".foot")),
      })),
      barRows: [...document.querySelectorAll("#bars .bar-row")].map(r => ({
        name: txt(r.querySelector(".bar-name")),
        width: r.querySelector(".bar-fill").style.width,
        val: txt(r.querySelector(".bar-val")),
      })),
      bodyRows: [...document.querySelectorAll("#tbody tr")].map(r =>
        [...r.querySelectorAll("td")].map(td => td.textContent.trim())),
      footRow: [...document.querySelectorAll("#tfoot td")].map(td => td.textContent.trim()),
      sampleBadgeVisible: (() => {
        const b = document.getElementById("sampleBadge");
        return b && getComputedStyle(b).display !== "none";
      })(),
    };
  });

  // KPI row
  check("4 KPI tiles rendered", dom.kpiTiles.length === 4, `got ${dom.kpiTiles.length}`);
  const kSaved = dom.kpiTiles.find(k => k.label === "Tokens saved");
  const kCost  = dom.kpiTiles.find(k => k.label === "Cost saved");
  const kUsage = dom.kpiTiles.find(k => k.label === "Total usage");
  const kRate  = dom.kpiTiles.find(k => k.label === "Compaction rate");
  check("KPI Tokens saved = 8.8M", kSaved?.value === "8.8M", JSON.stringify(kSaved));
  check("KPI Cost saved = $76.42", kCost?.value === "$76.42", JSON.stringify(kCost));
  check("KPI Total usage = 18.35M", kUsage?.value === "18.35M", JSON.stringify(kUsage));
  check("KPI Compaction rate = 21.4%", kRate?.value === "21.4%", JSON.stringify(kRate));
  check("KPI foot shows full token count", kSaved?.foot === "8,800,000 tokens", JSON.stringify(kSaved?.foot));

  // Bars
  check("4 bar rows rendered", dom.barRows.length === 4, `got ${dom.barRows.length}`);
  const opusBar = dom.barRows.find(b => b.name.includes("Opus 4.8"));
  check("Opus bar is 100% (max saved)", opusBar?.width === "100%", JSON.stringify(opusBar));
  const sonnetBar = dom.barRows.find(b => b.name.includes("Sonnet 5"));
  check("Sonnet bar width ~60.4%", sonnetBar && Math.abs(parseFloat(sonnetBar.width) - 60.465) < 0.1, JSON.stringify(sonnetBar));
  check("bar values are non-empty tokens", dom.barRows.every(b => /[0-9]/.test(b.val)), JSON.stringify(dom.barRows.map(b=>b.val)));

  // Table
  check("4 body rows rendered", dom.bodyRows.length === 4, `got ${dom.bodyRows.length}`);
  check("each row has 5 cells", dom.bodyRows.every(r => r.length === 5), JSON.stringify(dom.bodyRows.map(r=>r.length)));
  const opusRow = dom.bodyRows.find(r => r[0].includes("Opus 4.8"));
  check("Opus row: usage 8.9M / comp 2.1M / saved 4.3M / $64.50",
    opusRow && opusRow[1]==="8.9M" && opusRow[2]==="2.1M" && opusRow[3]==="4.3M" && opusRow[4]==="$64.50",
    JSON.stringify(opusRow));
  check("footer total row = Total / 18.35M / 3.93M / 8.8M / $76.42",
    dom.footRow[0]==="Total" && dom.footRow[1]==="18.35M" && dom.footRow[2]==="3.93M" && dom.footRow[3]==="8.8M" && dom.footRow[4]==="$76.42",
    JSON.stringify(dom.footRow));

  // Sample badge (DATA.live === false)
  check("sample-data badge is visible (not wired)", dom.sampleBadgeVisible === true);

  // 3. contrast / visibility sanity — text isn't invisible on its surface
  const vis = await page.evaluate(() => {
    const h1 = document.querySelector("h1");
    const cs = getComputedStyle(h1);
    return { color: cs.color, size: parseFloat(cs.fontSize) };
  });
  check("H1 has real color + size", vis.color !== "rgba(0, 0, 0, 0)" && vis.size >= 20, JSON.stringify(vis));

  // 4. no element overflows the viewport width (layout sanity)
  const overflow = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    let bad = [];
    for (const el of document.querySelectorAll("*")) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > vw + 1) bad.push(el.tagName + "." + (el.className||""));
    }
    return { vw, bad: bad.slice(0, 5), count: bad.length };
  });
  check("no horizontal overflow", overflow.count === 0, JSON.stringify(overflow));

  // screenshot light
  await page.screenshot({ path: path.join(__dirname, "shot-light.png"), fullPage: true });

  // 5. theme toggle → dark
  await page.click("#themeBtn");
  await new Promise(r => setTimeout(r, 250));
  const theme = await page.evaluate(() => {
    const t = document.documentElement.getAttribute("data-theme");
    const bg = getComputedStyle(document.querySelector(".viz-root")).backgroundColor;
    return { t, bg };
  });
  check("theme toggles to dark", theme.t === "dark", JSON.stringify(theme));
  check("dark surface applied (dark bg)", /rgb\(13, 13, 13\)|rgb\(26, 26, 25\)/.test(theme.bg), theme.bg);

  // regression guard: inherited text (h1, h2, tile values) must be LIGHT in dark mode,
  // not fall back to near-black. Parse luminance of each and require it bright.
  const darkInk = await page.evaluate(() => {
    const lum = el => {
      const [r,g,b] = getComputedStyle(el).color.match(/\d+/g).map(Number);
      return 0.2126*r + 0.7152*g + 0.0722*b; // 0..255
    };
    return {
      h1:    lum(document.querySelector("h1")),
      h2:    lum(document.querySelector(".section-h h2")),
      value: lum(document.querySelectorAll("#kpiRow .value")[2]), // "Total usage" (non-hero)
      td:    lum(document.querySelector("#tbody td")),
    };
  });
  check("dark: H1 inherits LIGHT ink (not black)", darkInk.h1 > 180, JSON.stringify(darkInk));
  check("dark: section heading LIGHT", darkInk.h2 > 180, JSON.stringify(darkInk));
  check("dark: KPI value LIGHT", darkInk.value > 180, JSON.stringify(darkInk));
  await page.screenshot({ path: path.join(__dirname, "shot-dark.png"), fullPage: true });

} finally {
  await browser.close();
}

console.log(results.join("\n"));
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
