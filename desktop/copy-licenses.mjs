// 配布物に入れるライセンス文をそろえる（録音音源・再生ライブラリ・NAM・AIのSDK）。
import fs from "fs";
import path from "path";

const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(here, "..");
const out = path.join(here, "licenses");
fs.mkdirSync(out, { recursive: true });
for (const f of fs.readdirSync(path.join(root, "public/licenses"))) fs.copyFileSync(path.join(root, "public/licenses", f), path.join(out, f));
const sdk = path.join(here, "node_modules/@anthropic-ai/sdk/LICENSE");
if (fs.existsSync(sdk)) fs.copyFileSync(sdk, path.join(out, "anthropic-sdk-typescript-LICENSE.txt"));
fs.writeFileSync(path.join(out, "README.txt"), [
  "サンシャイン作曲ソフト（© サンシャインソフトウェア）で使っている部品のライセンス",
  "",
  "- Fluid (R3) GM SoundFont（© Frank Wen、Mono版 © Michael Cowgill）: MIT",
  "- spessasynth: Apache-2.0",
  "- Neural Amp Modeler Core と見本のアンプモデル（© Steven Atkinson）: MIT",
  "- Anthropic TypeScript SDK: MIT（AI作曲の通信）",
  "- Electron / Chromium: 本体のフォルダの LICENSE.electron.txt・LICENSES.chromium.html",
  "",
].join("\n"));
console.log("ライセンス文をそろえました:", out);
