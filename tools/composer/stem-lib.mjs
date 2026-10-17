// パート別の書き出し（自動ミックスの解析用）。作曲ソフト（1ファイルのHTML）をヘッドレスのブラウザで開き、
// 1 回の描き出しで「全体の音」と「パートごとの測定結果」を取り出す（entry.ts の renderStems）。
// 共有の dist-composer/index.html は、他の作業と同時に作り直されることがあるので、自動ミックスは自分用のコピーを作って使う。
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { loadPlaywright, ROOT } from "./song-lib.mjs";

/** src/audio と entry.ts・template.html のいちばん新しい更新時刻 */
function newestSource() {
  const files = ["tools/composer/entry.ts", "tools/composer/template.html"];
  const walk = (dir) => {
    for (const f of fs.readdirSync(path.join(ROOT, dir), { withFileTypes: true })) {
      if (f.isDirectory()) walk(path.join(dir, f.name));
      else if (/\.(ts|json)$/.test(f.name) && !f.name.endsWith(".test.ts")) files.push(path.join(dir, f.name));
    }
  };
  walk("src/audio");
  // 音源（.sf3）を直したときも作り直す（2026-10-17: 直す前の音源で点検していた）
  for (const f of fs.readdirSync(path.join(ROOT, "assets-src/soundfont/extra"))) if (f.endsWith(".sf3")) files.push(path.join("assets-src/soundfont/extra", f));
  for (const f of fs.readdirSync(path.join(ROOT, "tools/composer"))) if (f.endsWith(".ts")) files.push(path.join("tools/composer", f));
  return Math.max(...files.map((f) => fs.statSync(path.join(ROOT, f)).mtimeMs));
}

/** 自分用の作曲ソフト HTML を用意する（古ければ作り直す。約 1〜2 分）。 */
export function ensureComposerHtml(html) {
  fs.mkdirSync(path.dirname(html), { recursive: true });
  if (!fs.existsSync(html) || fs.statSync(html).mtimeMs < newestSource()) {
    execSync(`node ${JSON.stringify(path.join(ROOT, "tools/composer/build.mjs"))} ${JSON.stringify(html)}`, { stdio: "ignore", maxBuffer: 1 << 28 });
  }
  return html;
}

/** ブラウザを 1 つ開いておき、何度かパート別の描き出しをする。 */
export async function openStemSession(html, { soundfont = "game", bass = "std", drums = "std", guitar = "std", orchestra = "std", piano = "std" } = {}) {
  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required", "--disable-gpu"] });
  const page = await browser.newPage({ viewport: { width: 320, height: 240 } });
  await page.goto("file://" + html, { timeout: 240000 });
  await page.addStyleTag({ content: "*,*::before,*::after{animation:none!important;transition:none!important}" });
  await page.waitForFunction(() => "__composer" in window, undefined, { timeout: 240000 });
  await page.evaluate(([b, d, g, o, p]) => window.__composer.setOverlays(b, d, g, o, p), [bass, drums, guitar, orchestra, piano]);
  if (soundfont === "gu") await page.evaluate(() => window.__composer.setSoundfont("gu"));
  return {
    /** score（stemKey 付き）を描いて測る。busFile を渡せば全体の WAV をそこへ書く。 */
    async render(score, edition, { windowSec = 0.25, busFile = null, fixedGainDb, timeoutMs = 600000, keepStems = false } = {}) {
      // 1 回の描き出しが固まったときに、いつまでも待たない（ブラウザのメモリ不足などで止まることがある）
      let timer;
      const limit = new Promise((_, rej) => { timer = setTimeout(() => rej(new Error(`描き出しが ${Math.round(timeoutMs / 1000)} 秒で終わりませんでした（ブラウザが止まった可能性）`)), timeoutMs); });
      let r;
      try {
        r = await Promise.race([page.evaluate(([s, e, o]) => window.__composer.renderStems(s, e, o), [score, edition, { windowSec, wantBus: !!busFile, fixedGainDb, keepStems }]), limit]);
      } finally { clearTimeout(timer); }
      if (busFile && r.busWav) fs.writeFileSync(busFile, Buffer.from(r.busWav, "base64"));
      delete r.busWav;
      return r;
    },
    /** render（keepStems: true）のあと、パートの音を WAV のファイルに書く（楽器ごとの点検用） */
    async writeStem(key, file) {
      const b64 = await page.evaluate((k) => window.__composer.stemWav(k), key);
      if (!b64) return false;
      fs.writeFileSync(file, Buffer.from(b64, "base64"));
      return true;
    },
    close: () => browser.close(),
  };
}
