// 配布物に入れるライセンス文をそろえる（録音音源・再生ライブラリ・NAM・AIのSDK）。
import fs from "fs";
import path from "path";

const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(here, "..");
const out = path.join(here, "licenses");
fs.mkdirSync(out, { recursive: true });
for (const f of fs.readdirSync(path.join(root, "public/licenses"))) fs.copyFileSync(path.join(root, "public/licenses", f), path.join(out, f));
for (const [pkg, name] of [["orbitron", "Orbitron-OFL.txt"], ["jetbrains-mono", "JetBrainsMono-OFL.txt"]]) {
  const f = path.join(root, "node_modules/@fontsource", pkg, "LICENSE");
  if (fs.existsSync(f)) fs.copyFileSync(f, path.join(out, name));
}
// MP3 の部品（LAME / lamejs、LGPL-3.0）の表示とライセンス文
for (const f of ["LGPL-3.0.txt", "GPL-3.0.txt"]) fs.copyFileSync(path.join(here, "legal", f), path.join(out, f));
const lameNotice = path.join(here, "node_modules/@breezystack/lamejs/LICENSE");
fs.writeFileSync(path.join(out, "LAME-NOTICE.txt"), [
  "このソフトの MP3 の書き出しには、LAME（https://lame.sourceforge.net/ ）を JavaScript にしたもの",
  "（lamejs、https://github.com/zhuker/lamejs ／配布パッケージ @breezystack/lamejs 1.2.7、https://github.com/shijinyu/lamejs ）を、改変せずに使っています。",
  "ライセンス: GNU Lesser General Public License version 3（LGPL-3.0。本文は LGPL-3.0.txt と GPL-3.0.txt）。",
  "この部品は、本体と別のファイルとして入っています（インストール先の resources/app.asar.unpacked/node_modules/@breezystack/lamejs）。",
  "LGPL にもとづき、利用者はこの部品を、互換のある別の版に差し替えて使えます。部品のソースコードは、上の入手先から手に入ります。",
  "",
  ...(fs.existsSync(lameNotice) ? ["--- 部品に付いている説明（原文） ---", fs.readFileSync(lameNotice, "utf8")] : []),
].join("\n"));
const sdk = path.join(here, "node_modules/@anthropic-ai/sdk/LICENSE");
if (fs.existsSync(sdk)) fs.copyFileSync(sdk, path.join(out, "anthropic-sdk-typescript-LICENSE.txt"));
fs.writeFileSync(path.join(out, "README.txt"), [
  "サンシャイン作曲ソフト（© サンシャインソフトウェア）で使っている部品のライセンス",
  "",
  "- Fluid (R3) GM SoundFont（© Frank Wen、Mono版 © Michael Cowgill）: MIT",
  "- spessasynth: Apache-2.0",
  "- Neural Amp Modeler Core と見本のアンプモデル（© Steven Atkinson）: MIT",
  "- Anthropic TypeScript SDK: MIT（AI作曲の通信）",
  "- 文字のフォント Orbitron・JetBrains Mono: SIL Open Font License 1.1",
  "- MP3 の変換 LAME（lamejs）: LGPL-3.0（LAME-NOTICE.txt。別のファイルとして入っていて、差し替えられます）",
  "- Electron / Chromium: 本体のフォルダの LICENSE.electron.txt・LICENSES.chromium.html",
  "",
].join("\n"));
console.log("ライセンス文をそろえました:", out);
