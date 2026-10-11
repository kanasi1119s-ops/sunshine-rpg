// コード進行の選択ツール（docs/sound/chord-theory-deep.md の提案 7）。作曲の前に、場面に合って、直近の曲と違う進行の候補を出す。
//   node tools/composer/chord-pick.mjs --scene battle [--avoid-last 3] [--key random|G|Em] [--count 3] [--seed 1] [--last 曲名,曲名] [--allow-overused]
// 場面: field town battle boss dungeon sad ending event mystery sky night（docs/sound/data/chord-recipes.json の scenes）。
// 出すのは「型とコード名の候補」だけ。旋律・リズム・コードの長さは、自分で決める（毎回同じ Am F C G を止めるための道具）。
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { loadRecipes, realize, pcName, useFlats } from "./chord-recipes.mjs";
import { signature, similarity, recipeOf, parseChord } from "./chord-variety.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));

function mulberry32(a) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** 直近の曲（ファイルの更新が新しい順。names を渡せばその曲だけ）。 */
export function recentSongs(dir, n, names) {
  if (!fs.existsSync(dir)) return [];
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => ({ name: f.replace(/\.json$/, ""), t: fs.statSync(path.join(dir, f)).mtimeMs }));
  const pick = names?.length ? files.filter((f) => names.includes(f.name)) : files.sort((a, b) => b.t - a.t).slice(0, n);
  const out = [];
  for (const f of pick) {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, `${f.name}.json`), "utf8"));
      if (typeof d.chords === "string") out.push({ name: f.name, chords: d.chords });
    } catch { /* 読めない曲は飛ばす */ }
  }
  return out;
}

/** 候補を選ぶ。recent は [{name, chords}]。戻り値は [{ id, name, scenes, roman, tonic, chords(コード名の配列) , text }]。 */
export function pickRecipes({ scene, recent = [], count = 3, key = "random", seed = Date.now(), allowOverused = false } = {}) {
  const rng = mulberry32(Number(seed) || 1);
  const { recipes } = loadRecipes();
  const recentSigs = recent.map((s) => ({ name: s.name, seq: signature(s.chords).seq, id: recipeOf(s.chords)?.id, tonic: parseChord(String(s.chords).split(/[\s|]+/)[0] ?? "")?.root }));
  const cands = recipes.filter((r) => {
    if (scene && !r.scenes.includes(scene)) return false;
    if (r.overused && !allowOverused) return false;
    const sig = signature(realize(r.roman, 0, { minor: r.mode === "minor" }).join(" ")).seq;
    return !recentSigs.some((s) => s.id === r.id || similarity(sig, s.seq) >= 0.7);
  });
  const shuffled = cands.map((r) => ({ r, k: rng() })).sort((a, b) => a.k - b.k).map((x) => x.r);
  const usedTonics = new Set(recentSigs.map((s) => s.tonic).filter((x) => x !== undefined));
  const out = [];
  const keyPc = key && key !== "random" ? parseChord(key)?.root : undefined;
  if (key && key !== "random" && keyPc === undefined) throw new Error(`--key が読めません（${key}）。random か G・Em のような主音で`);
  for (const r of shuffled.slice(0, count)) {
    const minor = r.mode === "minor";
    let tonic = keyPc;
    if (tonic === undefined) {
      const pool = [...Array(12).keys()].filter((p) => p !== 0 && !usedTonics.has(p));
      tonic = pool[Math.floor(rng() * pool.length)];
    }
    const chords = realize(r.roman, tonic, { minor, flats: useFlats(tonic, minor) });
    out.push({ id: r.id, name: r.name, scenes: r.scenes, roman: r.roman, tonic: pcName(tonic, useFlats(tonic, minor)) + (minor ? "m" : ""), chords, text: chords.join(" ") });
  }
  return out;
}

function main() {
  const args = process.argv.slice(2);
  const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
  if (args.includes("--help") || !args.length) {
    console.log("使い方: node tools/composer/chord-pick.mjs --scene <場面> [--avoid-last 3] [--key random|G|Em] [--count 3] [--seed N] [--last 曲名,曲名] [--allow-overused]\n場面: " + Object.entries(loadRecipes().scenes).map(([k, v]) => `${k}(${v})`).join(" "));
    return;
  }
  const dir = path.join(ROOT, "assets-src", "ai-songs");
  const recent = recentSongs(dir, Number(opt("--avoid-last", 3)), opt("--last")?.split(","));
  const res = pickRecipes({ scene: opt("--scene"), recent, count: Number(opt("--count", 3)), key: opt("--key", "random"), seed: opt("--seed", Date.now()), allowOverused: args.includes("--allow-overused") });
  console.log(`避けた直近の曲: ${recent.map((s) => s.name).join("・") || "なし"}`);
  if (!res.length) console.log("条件に合う型がありません（--scene を変えるか、--avoid-last を減らす）");
  res.forEach((c, i) => console.log(`\n候補${i + 1}: ${c.name}（${c.id}）　主音 ${c.tonic}　度数 ${c.roman}\n  chords: ${c.text}`));
  if (res.length) console.log("\n※ 型の骨組みです。コードの長さ（Am*2）・転回・7th・借用を1〜2か所入れて、description に型名を書く。");
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main();
