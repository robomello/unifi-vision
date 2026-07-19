import { createRequire } from "module";
const require = createRequire(import.meta.url);
const puppeteer = require("/home/mello/.nvm/versions/node/v24.13.1/lib/node_modules/puppeteer");

const CHROME = "/home/mello/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome";
const URL_LOCAL = "http://127.0.0.1:8098/";
const OUT = "/home/mello/tokens-savings/shot-live.png";

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 2 });
  const resp = await page.goto(URL_LOCAL, { waitUntil: "networkidle0", timeout: 30000 });
  console.log("status:", resp.status());
  // let the timeseries chart's own fetch()+render complete after networkidle0
  await page.waitForSelector("#tsChart .ts-bar", { timeout: 10000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: OUT, fullPage: true });
  console.log("saved:", OUT);

  // dark theme too
  await page.click("#themeBtn");
  await new Promise(r => setTimeout(r, 400));
  const OUT_DARK = OUT.replace(/\.png$/, "-dark.png");
  await page.screenshot({ path: OUT_DARK, fullPage: true });
  console.log("saved:", OUT_DARK);
} finally {
  await browser.close();
}
