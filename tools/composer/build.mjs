// 使い方: node tools/composer/build.mjs [出力先.html] — 実楽器の音で鳴らして作曲・編集できる作曲ソフト（1ファイルのHTML）を作る。
// 再生エンジンと曲データはゲーム本体のものをそのまま束ねる。出力: 既定は dist-composer/index.html（gitには入れない）。
import { build } from "vite";
import fs from "fs";
import path from "path";

const root = new URL("../../", import.meta.url).pathname;
const out = path.resolve(process.argv[2] || root + "dist-composer/index.html");
const result = await build({
  root, configFile: false, logLevel: "warn",
  build: { write: false, assetsInlineLimit: 100_000_000, minify: true, lib: { entry: root + "tools/composer/entry.ts", name: "Composer", formats: ["iife"], fileName: "bgm" } },
});
const output = (Array.isArray(result) ? result[0] : result).output.find((o) => o.type === "chunk");
const js = output.code.replace(/<\/script/gi, "<\\/script");
const html = fs.readFileSync(root + "tools/composer/template.html", "utf8").replace("/*BUNDLE*/", () => js);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log("書き出し:", out, (html.length / 1024).toFixed(0) + "KB");
