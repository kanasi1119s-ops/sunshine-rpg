// 使い方: node export-game-data.mjs — 地形・ボス・登場人物のドット絵を、ゲームが読み込める形式（色番号のRLE）に書き出す。
// 出力: src/game/art/sprite-data.generated.ts（手で編集しない。元データは terrain.mjs / bosses.mjs / characters.mjs）
import fs from "fs";

async function build(setName, scale, keyMap) {
  process.env.SCALE = String(scale);
  const mod = await import(`./${setName}.mjs`);
  const out = {};
  for (const p of mod.PIECES) {
    const key = keyMap[p.name];
    if (!key) continue;
    const g = p.build();
    out[key] = { size: g.length, palette: p.pal.map((x) => x[1]), rle: encode(g) };
  }
  return out;
}
/** 色番号A〜Z＋透明(_)を、続く同じ値の数（36進数の小文字）つきで並べる。1個のときは数を省く。 */
function encode(g) {
  let s = "", prev = null, n = 0;
  const flush = () => { if (prev === null) return; s += prev + (n > 1 ? n.toString(36) : ""); };
  for (const row of g) for (const k of row) {
    const ch = k < 0 || Number.isNaN(k) ? "_" : String.fromCharCode(65 + k);
    if (ch === prev) n++; else { flush(); prev = ch; n = 1; }
  }
  flush();
  return s;
}

const SETS = {
  terrain: [2, { "T1-草地A": "terrain:grass-a", "T7-草地B": "terrain:grass-b", "T2-土の道": "terrain:dirt", "T3-水面": "terrain:water", "T5-深い森": "terrain:forest", "T4-崖の壁": "terrain:cliff", "T6-岸辺": "terrain:bank" }],
  bosses: [4, { "B1-水涸れの歪み": "boss:mugikano-yugami", "B2-積荷の歪み": "boss:garasuko-yugami", "B3-実験の歪み": "boss:tetsukusari-yugami", "B4-砂嵐の歪み": "boss:sanone-yugami", "B5-予言の歪み": "boss:kiri-yugami", "B6-試作機の歪み": "boss:shimohara-yugami" }],
  characters: [4, { "C1-ユーリ": "char:ユーリ", "C2-レト": "char:レト", "C3-ミナ": "char:ミナ", "C4-ガイド": "char:ガイド", "C5-オルカ": "char:オルカ" }],
};
// 倍率（SCALE）はモジュールの読み込み時に決まるため、セットごとに別のプロセスで実行する（node export-game-data.mjs → 自動で分けて実行）。
const [mode, tmpDir] = process.argv.slice(2);
if (mode && mode !== "merge") {
  const [scale, keyMap] = SETS[mode];
  fs.writeFileSync(`${tmpDir}/${mode}.json`, JSON.stringify(await build(mode, scale, keyMap)));
} else if (mode === "merge") {
  const all = {};
  for (const name of Object.keys(SETS)) Object.assign(all, JSON.parse(fs.readFileSync(`${tmpDir}/${name}.json`, "utf8")));
  // ぴぽや素材（import-pipoya.mjs で作る pipoya-terrain.json）があれば、同名の地形テクスチャを置き換える
  const pipoya = new URL("./pipoya-terrain.json", import.meta.url);
  if (fs.existsSync(pipoya)) Object.assign(all, JSON.parse(fs.readFileSync(pipoya, "utf8")));
  const body = Object.entries(all).map(([k, v]) => `  ${JSON.stringify(k)}: { size: ${v.size}, palette: ${JSON.stringify(v.palette)}, rle: ${JSON.stringify(v.rle)} },`).join("\n");
  fs.writeFileSync(new URL("../../src/game/art/sprite-data.generated.ts", import.meta.url), `// 自動生成: tools/pixel-art/export-game-data.mjs（手で編集しない）
import type { SpriteData } from "./sprite";

export const SPRITE_DATA: Record<string, SpriteData> = {
${body}
};
`);
  console.log("書き出し:", Object.keys(all).length, "点");
} else {
  const { execFileSync } = await import("child_process");
  const os = await import("os");
  const tmp = fs.mkdtempSync(os.tmpdir() + "/sprite-");
  for (const name of Object.keys(SETS)) execFileSync("node", [new URL(import.meta.url).pathname, name, tmp], { stdio: "inherit", env: { ...process.env, SCALE: String(SETS[name][0]) } });
  execFileSync("node", [new URL(import.meta.url).pathname, "merge", tmp], { stdio: "inherit" });
}
