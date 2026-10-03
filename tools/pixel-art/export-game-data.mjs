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
    out[key] = { size: g.length, palette: p.pal.map((x) => x[1]), rle: encode(g, p.pal.length > 26) };
  }
  return out;
}
/** 色番号A〜Z＋透明(_)を、続く同じ値の数（36進数の小文字）つきで並べる。1個のときは数を省く。 */
function encode(g, wide = false) {
  if (wide) {
    // 色が27色以上のとき: 「色番号:続く数」をカンマでつなぐ。先頭の「~」が目印（透明は -1）
    const toks = []; let prev = null, n = 0;
    for (const row of g) for (const k of row) { const v = k < 0 || Number.isNaN(k) ? -1 : k; if (v === prev) n++; else { if (prev !== null) toks.push(prev + ":" + n); prev = v; n = 1; } }
    if (prev !== null) toks.push(prev + ":" + n);
    return "~" + toks.join(",");
  }
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
  bosses: [4, { "B1-水涸れの歪み": "boss:mugikano-yugami", "B2-積荷の歪み": "boss:garasuko-yugami", "B3-実験の歪み": "boss:tetsukusari-yugami", "B4-砂嵐の歪み": "boss:sanone-yugami", "B5-予言の歪み": "boss:kiri-yugami", "B6-試作機の歪み": "boss:shimohara-yugami", "B7-浮嶼の歪み": "boss:fushima-yugami", "B8-灯芯都の歪み": "boss:toushin-yugami", "B9-虚灯宮の歪み": "boss:kyotoukyu-yugami" }],
  guardians: [4, { "G1-恵みの残照": "boss:god-1", "G2-理不尽の羽音": "boss:god-2", "G3-坩堝の顎": "boss:god-3", "G4-在らざる歌": "boss:god-4", "G5-透き徹る誓い": "boss:god-5", "G6-不敗の咎人": "boss:god-6", "G7-境界を見ぬ者": "boss:god-7", "G8-無音の弔鐘": "boss:god-8", "M1-塔の守り（2層）": "boss:tower2-guard", "M2-塔の守り（3層）": "boss:kanou3-guard", "M3-灯りの番人": "boss:tower3-guard", "M4-深部3層の歪み": "boss:deep3-yugami", "M5-全観": "boss:zenkan" }],
  mobs: [1, { "MB1-こうもり": "mob:bat", "MB2-虫": "mob:beetle", "MB3-結晶": "mob:shard", "MB4-しずく": "mob:drop", "MB5-かげ": "mob:ghost", "MB6-ねずみ": "mob:rat", "MB7-サソリ": "mob:scorpion", "MB8-め": "mob:eye" }],
  props: [1, { "P1-木": "prop:tree", "P2-家": "prop:house", "P3-家青": "prop:house-blue", "P4-家緑": "prop:house-green", "P5-岩": "prop:rock", "P6-茂み": "prop:bush", "P7-屋敷": "prop:manor", "P8-屋敷青": "prop:manor-blue", "P9-屋敷緑": "prop:manor-green", "P10-雪の木": "prop:tree-snow", "P11-枯れ木": "prop:tree-dead", "P12-雪の岩": "prop:rock-snow", "P13-雪の茂み": "prop:bush-snow", "P14-ヤシ": "prop:palm", "P15-サボテン": "prop:cactus", "P16-樽": "prop:barrel", "P17-街灯": "prop:lamp", "P18-井戸": "prop:well", "P19-道しるべ": "prop:signpost", "P20-木箱の山": "prop:crates", "P21-花壇": "prop:flowerbed", "P22-アイコンport": "prop:icon-port", "P23-アイコンvillage": "prop:icon-village", "P24-アイコンlake": "prop:icon-lake", "P25-アイコンmine": "prop:icon-mine", "P26-アイコンcastle": "prop:icon-castle", "P27-アイコンtents": "prop:icon-tents", "P28-アイコンtemple": "prop:icon-temple", "P29-アイコンsnowtown": "prop:icon-snowtown", "P30-アイコンsky": "prop:icon-sky", "P31-アイコンpalace": "prop:icon-palace" }],
  party: [1, { "C1-ユーリ": "char:ユーリ", "C2-レト": "char:レト", "C3-ミナ": "char:ミナ", "C4-ガイド": "char:ガイド", "C5-オルカ": "char:オルカ" }],
};
for (const [i, n] of ["ruin", "shrine", "cave", "stones", "bigtree", "vortex"].entries()) SETS.props[1][`P${40 + i}-アイコン${n}`] = `prop:icon-${n}`;
for (const n of fs.readdirSync(new URL("../../assets-src/pixel-practice/r20-props/", import.meta.url)).filter((f) => f.endsWith(".txt")).map((f) => f.replace(".txt", ""))) {
  SETS.props[1][`R20-${n}`] = `prop:${n}`;
}
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
