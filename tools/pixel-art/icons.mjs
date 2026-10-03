// アイテム・装備・ジョブ・特技・灯貨の16×16アイコン70個（assets-src/pixel-practice/r21-icons/、エージェントが一から作成）。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/r21-icons/", import.meta.url);
export const ICON_NAMES = fs.readdirSync(ROOT).filter((f) => f.endsWith(".txt")).map((f) => f.replace(".txt", "")).sort();
function piece(name) {
  const rows = fs.readFileSync(new URL(`${name}.txt`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = JSON.parse(fs.readFileSync(new URL(`pal-${name}.json`, ROOT), "utf8"));
  const keys = Object.keys(pal);
  return {
    name: `I-${name}`,
    pal: keys.map((k) => [k, pal[k]]),
    build() {
      const g = Array.from({ length: 16 }, () => Array(16).fill(-1));
      rows.forEach((r, y) => [...r].forEach((ch, x) => { const k = keys.indexOf(ch); if (k >= 0 && y < 16 && x < 16) g[y][x] = k; }));
      return g;
    },
  };
}
export const PIECES = ICON_NAMES.map(piece);
