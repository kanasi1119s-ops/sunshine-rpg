// 使い方: node tools/composer/build.mjs [出力先.html] — 実楽器の音で鳴らして作曲・編集できる作曲ソフト（1ファイルのHTML）を作る。
// 再生エンジンと曲データはゲーム本体のものをそのまま束ねる。出力: 既定は dist-composer/index.html（gitには入れない）。
import { build } from "vite";
import fs from "fs";
import path from "path";

const root = new URL("../../", import.meta.url).pathname;
const argv = process.argv.slice(2);
const desktop = argv.includes("--desktop");
// 環境変数 COMPOSER_SOUNDFONT=<.sf2/.sf3のパス> で、作曲ソフトだけ別の録音音源に差し替えられる（ゲームの game.sf3 は変えない）
const altSoundfont = process.env.COMPOSER_SOUNDFONT ? path.resolve(process.env.COMPOSER_SOUNDFONT) : null;
const out = path.resolve(argv.find((a) => !a.startsWith("--")) || root + "dist-composer/index.html");
// 無料のアンプシミュレーター（NAM）のワークレットとWASMを、データURLにして埋め込む
const nam = await build({
  root, configFile: false, logLevel: "silent",
  build: { write: false, minify: true, lib: { entry: root + "src/audio/nam/nam-processor.ts", name: "NamProcessor", formats: ["es"], fileName: "nam" } },
});
const namCode = (Array.isArray(nam) ? nam[0] : nam).output.find((o) => o.type === "chunk").code;
const namWasm = fs.readFileSync(root + "node_modules/@opendaw/nam-wasm/dist/nam.wasm");
// 同梱のNAMモデル（MIT。assets-src/nam-models/README.md）
const NAM_MODELS = { "builtin:highgain-a": ["ハイゲインアンプA", "highgain-a.nam"], "builtin:highgain-b": ["ハイゲインアンプB", "highgain-b.nam"], "builtin:bass-preamp": ["ベース用プリアンプ", "bass-preamp.nam"] };
const namModels = Object.fromEntries(Object.entries(NAM_MODELS).map(([k, [label, file]]) => [k, { label, json: fs.readFileSync(root + "assets-src/nam-models/" + file, "utf8") }]));
// 見本のアンプ定義（assets-src/amp-plugins/）
const ampDir = root + "assets-src/amp-plugins/";
const ampSamples = fs.readdirSync(ampDir).filter((f) => f.endsWith(".sunshine-amp.json")).map((f) => JSON.parse(fs.readFileSync(ampDir + f, "utf8")));
const result = await build({
  root, configFile: false, logLevel: "warn",
  resolve: altSoundfont ? { alias: [{ find: /^.*\/soundfont\/game\.sf3\?url$/, replacement: altSoundfont + "?url" }] } : undefined,
  define: {
    __NAM_PROCESSOR__: JSON.stringify("data:text/javascript;base64," + Buffer.from(namCode).toString("base64")),
    __NAM_WASM__: JSON.stringify(namWasm.toString("base64")),
    __NAM_MODELS__: JSON.stringify(namModels),
    __AMP_SAMPLES__: JSON.stringify(ampSamples),
  },
  build: { write: false, assetsInlineLimit: 100_000_000, minify: true, lib: { entry: root + "tools/composer/entry.ts", name: "Composer", formats: ["iife"], fileName: "bgm" } },
});
const output = (Array.isArray(result) ? result[0] : result).output.find((o) => o.type === "chunk");
const js = output.code.replace(/<\/script/gi, "<\\/script");
// アイコン（desktop/build/icon.svg）を、左上のロゴに使う
const icon = "data:image/svg+xml;base64," + fs.readFileSync(root + "desktop/build/icon.svg").toString("base64");
let html = fs.readFileSync(root + "tools/composer/template.html", "utf8").replace("/*ICON*/", () => `'${icon}'`).replace("/*BUNDLE*/", () => js);
if (desktop) {
  // デスクトップ版: 外への通信は画面からはしない（AIとのやりとりは本体の側）。読み込めるものを、埋め込んだ部品と文字のフォントだけにする
  const csp = "default-src 'none'; script-src 'unsafe-inline' data: 'wasm-unsafe-eval'; worker-src data: blob:; style-src 'unsafe-inline'; font-src data:; img-src data: blob:; media-src data: blob:; connect-src data: blob:";
  // 文字のフォントは、外から読み込まずに同梱する（OFLライセンス）。日本語はパソコンに入っている文字（游ゴシック・ヒラギノなど）を使う
  const face = (family, pkg, file, weight) => `@font-face{font-family:"${family}";font-weight:${weight};font-style:normal;font-display:swap;src:url(data:font/woff2;base64,${fs.readFileSync(root + "node_modules/@fontsource/" + pkg + "/files/" + file).toString("base64")}) format("woff2")}`;
  const fonts = [face("Orbitron", "orbitron", "orbitron-latin-500-normal.woff2", 500), face("Orbitron", "orbitron", "orbitron-latin-700-normal.woff2", 700), face("Orbitron", "orbitron", "orbitron-latin-800-normal.woff2", 800), face("JetBrains Mono", "jetbrains-mono", "jetbrains-mono-latin-400-normal.woff2", 400), face("JetBrains Mono", "jetbrains-mono", "jetbrains-mono-latin-600-normal.woff2", 600)].join("");
  html = html.replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>/, () => `<style>${fonts}</style>`);
  html = html.replace('<meta charset="utf-8">', `<meta charset="utf-8">\n<meta http-equiv="Content-Security-Policy" content="${csp}">`);
}
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log("書き出し:", out, (html.length / 1024).toFixed(0) + "KB");
