import { chromium } from "playwright-core";
import fs from "fs";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage();
await p.goto("http://localhost:5231/", { waitUntil: "domcontentloaded" });
const data = await p.evaluate(async () => {
  const m = await import("/src/render/logo-pixel.ts");
  const c = m.getPixelLogo("Ringlight Chronicle");
  return c ? c.toDataURL("image/png") : null;
});
fs.writeFileSync(process.argv[2], Buffer.from(data.split(",")[1], "base64"));
await b.close();
