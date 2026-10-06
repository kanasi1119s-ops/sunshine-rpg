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
  props: [1, { "P1-木": "prop:tree", "P2-家": "prop:house", "P3-家青": "prop:house-blue", "P4-家緑": "prop:house-green", "P5-岩": "prop:rock", "P6-茂み": "prop:bush", "P7-屋敷": "prop:manor", "P8-屋敷青": "prop:manor-blue", "P9-屋敷緑": "prop:manor-green", "P50-白い家": "prop:house-white", "P10-雪の木": "prop:tree-snow", "P51-針葉樹": "prop:tree-pine", "P11-枯れ木": "prop:tree-dead", "P12-雪の岩": "prop:rock-snow", "P13-雪の茂み": "prop:bush-snow", "P14-ヤシ": "prop:palm", "P15-サボテン": "prop:cactus", "P16-樽": "prop:barrel", "P17-街灯": "prop:lamp", "P18-井戸": "prop:well", "P19-道しるべ": "prop:signpost", "P20-木箱の山": "prop:crates", "P21-花壇": "prop:flowerbed", "P22-アイコンport": "prop:icon-port", "P23-アイコンvillage": "prop:icon-village", "P24-アイコンlake": "prop:icon-lake", "P25-アイコンmine": "prop:icon-mine", "P26-アイコンcastle": "prop:icon-castle", "P27-アイコンtents": "prop:icon-tents", "P28-アイコンtemple": "prop:icon-temple", "P29-アイコンsnowtown": "prop:icon-snowtown", "P30-アイコンsky": "prop:icon-sky", "P31-アイコンpalace": "prop:icon-palace" }],
  icons: [1, Object.fromEntries(fs.readdirSync(new URL("../../assets-src/pixel-practice/r21-icons/", import.meta.url)).filter((f) => f.endsWith(".txt")).map((f) => f.replace(".txt", "")).map((n) => [`I-${n}`, `icon:${n}`]))],
  party: [1, { "C1-ユーリ": "char:ユーリ", "C2-レト": "char:レト", "C3-ミナ": "char:ミナ", "C4-コハク": "char:コハク", "C5-オルカ": "char:オルカ" }],
};
for (const [i, n] of ["ruin", "shrine", "cave", "stones", "bigtree", "vortex"].entries()) SETS.props[1][`P${40 + i}-アイコン${n}`] = `prop:icon-${n}`;
SETS.props[1]["P46-アイコンvolcano"] = "prop:icon-volcano";
SETS.props[1]["P47-アイコンdive"] = "prop:icon-dive";
SETS.props[1]["P48-教会"] = "prop:church";
SETS.props[1]["P49-教会の中"] = "prop:church-interior";
SETS.props[1]["P50-船大工の小屋"] = "prop:icon-hut";
SETS.props[1]["P51-芯環塔"] = "prop:icon-core-spire";
SETS.props[1]["P52-アイコンvillage-mist"] = "prop:icon-village-mist";
SETS.props[1]["P53-アイコンtents-grass"] = "prop:icon-tents-grass";
SETS.props[1]["P54-アイコンmineshaft"] = "prop:icon-mineshaft";
for (const n of fs.readdirSync(new URL("../../assets-src/pixel-practice/r20-props/", import.meta.url)).filter((f) => f.endsWith(".txt")).map((f) => f.replace(".txt", ""))) {
  SETS.props[1][`R20-${n}`] = `prop:${n}`;
}
for (const n of fs.readdirSync(new URL("../../assets-src/pixel-practice/r22-vehicles/", import.meta.url)).filter((f) => f.endsWith(".txt") && !f.startsWith("whirlpool") && !f.startsWith("airship")).map((f) => f.replace(".txt", ""))) {
  SETS.props[1][`R22-${n}`] = n === "spire" || n.startsWith("islet-") ? `prop:icon-${n}` : `prop:${n}`;
}
for (const n of fs.readdirSync(new URL("../../assets-src/pixel-practice/r24-airship/", import.meta.url)).filter((f) => f.startsWith("airship-") && f.endsWith(".txt") && !f.includes("showcase")).map((f) => f.replace(".txt", ""))) {
  SETS.props[1][`R24-${n}`] = `prop:${n}`;
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
  // 全体フィールドの地形テクスチャ（ai-gen/world_tiles.py で作る world-terrain.json）
  const world = new URL("./world-terrain.json", import.meta.url);
  if (fs.existsSync(world)) Object.assign(all, JSON.parse(fs.readFileSync(world, "utf8")));
  // 全体フィールドの地面（草原・丘・道・砂・雪・荒れ地・灰の地）を、光と細かな模様のある絵に（assets-src/pixel-practice/r17-polish/ground_tex.py で作る ground-terrain.json。2026-10-06）
  const ground = new URL("./ground-terrain.json", import.meta.url);
  if (fs.existsSync(ground)) Object.assign(all, JSON.parse(fs.readFileSync(ground, "utf8")));
  // 町の草むら（terrain:forest）を、立体の茂みの絵に（assets-src/pixel-practice/r17-polish/canopy3d.py で作る canopy-terrain.json。2026-10-06）
  const canopy = new URL("./canopy-terrain.json", import.meta.url);
  if (fs.existsSync(canopy)) Object.assign(all, JSON.parse(fs.readFileSync(canopy, "utf8")));
  // 敵の絵（ai-gen/monster_batch.py export で作る enemy-art.json。雑魚は enemy:<id> 96×96、ボスは boss:<id> を置きかえる）
  const enemyArt = new URL("./enemy-art.json", import.meta.url);
  if (fs.existsSync(enemyArt)) Object.assign(all, JSON.parse(fs.readFileSync(enemyArt, "utf8")));
  // 幻想の禁域の地面（assets-src/pixel-practice/r33-illusion/illusion_tex.py。128×128、つながる模様。2026-10-06）
  for (const name of ["illusion-void", "illusion-floor", "illusion-rune", "illusion-wall", "illusion-hidden"]) {
    const base = new URL("../../assets-src/pixel-practice/r33-illusion/", import.meta.url);
    const rows = fs.readFileSync(new URL(`${name}.txt`, base), "utf8").split("\n").filter((l) => l);
    const pal = JSON.parse(fs.readFileSync(new URL(`${name}-pal.json`, base), "utf8"));
    const syms = Object.keys(pal);
    const g = rows.map((r) => [...r].map((ch) => syms.indexOf(ch)));
    all[`terrain:${name}`] = { size: rows.length, palette: syms.map((k) => pal[k]), rle: encode(g, syms.length > 26) };
  }
  // 隠しボス「機械の悪神巨人兵」（assets-src/monsters/mecha-god-giant/ の 256×256・40色。人間がプッシュした絵を使う。2026-10-06）
  for (const [key, dir, name] of [["boss:arbiter", "mecha-god-giant", "final"]]) {
    const base = new URL(`../../assets-src/monsters/${dir}/`, import.meta.url);
    const rows = fs.readFileSync(new URL(`${name}.txt`, base), "utf8").split("\n").filter((l) => l);
    const pal = JSON.parse(fs.readFileSync(new URL(`${name}.json`, base), "utf8"));
    const syms = Object.keys(pal);
    const g = rows.map((r) => [...r].map((ch) => (ch === "." ? -1 : syms.indexOf(ch))));
    all[key] = { size: rows.length, palette: syms.map((k) => pal[k]), rle: encode(g, syms.length > 26) };
  }
  // コスモリングライトをまとった2頭身ユーリ（50×50の待機・攻撃態勢）と、追尾砲台（assets-src/pixel-practice/r31-cosmo/。2026-10-06）
  {
    const base = new URL("../../assets-src/pixel-practice/r31-cosmo/", import.meta.url);
    const pal = JSON.parse(fs.readFileSync(new URL("pal-cosmo.json", base), "utf8"));
    const syms = Object.keys(pal);
    for (const [key, name] of [["cosmo:idle", "yuri2-cosmo-idle"], ["cosmo:attack", "yuri2-cosmo-attack"], ["cosmo:pod", "cosmo-pod"]]) {
      const rows = fs.readFileSync(new URL(`${name}.txt`, base), "utf8").split("\n").filter((l) => l);
      const size = Math.max(rows.length, ...rows.map((r) => r.length));
      // 正方形にそろえ、下そろえ・左そろえ（ほかの絵と同じ形）
      const g = Array.from({ length: size }, (_, y) => {
        const r = rows[y - (size - rows.length)] ?? "";
        return Array.from({ length: size }, (_, x) => (r[x] && r[x] !== "." ? syms.indexOf(r[x]) : -1));
      });
      all[key] = { size, palette: syms.map((k) => pal[k]), rle: encode(g, syms.length > 26) };
    }
  }
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
