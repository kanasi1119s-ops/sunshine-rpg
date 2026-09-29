// 使い方: node tools/bgm-player/build.mjs [出力先.html] — ゲームの全BGM・効果音を聴けるBGMプレイヤー（1ファイルのHTML）を作る。
// 再生エンジンと曲データはゲーム本体のものをそのまま束ねる。出力: 既定は dist-bgm-player/index.html（gitには入れない）。
import { build } from "vite";
import fs from "fs";
import path from "path";

const root = new URL("../../", import.meta.url).pathname;
const out = path.resolve(process.argv[2] || root + "dist-bgm-player/index.html");
const result = await build({
  root, configFile: false, logLevel: "warn",
  build: { write: false, assetsInlineLimit: 100_000_000, minify: true, lib: { entry: root + "tools/bgm-player/entry.ts", name: "BgmPlayer", formats: ["iife"], fileName: "bgm" } },
});
const output = (Array.isArray(result) ? result[0] : result).output.find((o) => o.type === "chunk");
const js = output.code.replace(/<\/script/gi, "<\\/script");
const html = fs.readFileSync(root + "tools/bgm-player/template.html", "utf8").replace("/*BUNDLE*/", () => js);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log("書き出し:", out, (html.length / 1024).toFixed(0) + "KB");
