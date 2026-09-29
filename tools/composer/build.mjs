// 使い方: node tools/composer/build.mjs [出力先.html] — 実楽器の音で鳴らして作曲・編集できる作曲ソフト（1ファイルのHTML）を作る。
// 再生エンジンと曲データはゲーム本体のものをそのまま束ねる。出力: 既定は dist-composer/index.html（gitには入れない）。
import { build } from "vite";
import fs from "fs";
import path from "path";

const root = new URL("../../", import.meta.url).pathname;
const out = path.resolve(process.argv[2] || root + "dist-composer/index.html");
// 無料のアンプシミュレーター（NAM）のワークレットとWASMを、データURLにして埋め込む
const nam = await build({
  root, configFile: false, logLevel: "silent",
  build: { write: false, minify: true, lib: { entry: root + "src/audio/nam/nam-processor.ts", name: "NamProcessor", formats: ["es"], fileName: "nam" } },
});
const namCode = (Array.isArray(nam) ? nam[0] : nam).output.find((o) => o.type === "chunk").code;
const namWasm = fs.readFileSync(root + "node_modules/@opendaw/nam-wasm/dist/nam.wasm");
const result = await build({
  root, configFile: false, logLevel: "warn",
  define: {
    __NAM_PROCESSOR__: JSON.stringify("data:text/javascript;base64," + Buffer.from(namCode).toString("base64")),
    __NAM_WASM__: JSON.stringify(namWasm.toString("base64")),
  },
  build: { write: false, assetsInlineLimit: 100_000_000, minify: true, lib: { entry: root + "tools/composer/entry.ts", name: "Composer", formats: ["iife"], fileName: "bgm" } },
});
const output = (Array.isArray(result) ? result[0] : result).output.find((o) => o.type === "chunk");
const js = output.code.replace(/<\/script/gi, "<\\/script");
const html = fs.readFileSync(root + "tools/composer/template.html", "utf8").replace("/*BUNDLE*/", () => js);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log("書き出し:", out, (html.length / 1024).toFixed(0) + "KB");
