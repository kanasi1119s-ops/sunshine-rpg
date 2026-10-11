// ジャンル別の仕上がりの目標（日本一フリーBGM の測定値から。docs/sound/nihonichi-genre-analysis.md §7 の提案 1〜5）。
//   resolveGenre(名前)              … 作曲ソフトのスタイル名（rock・battle・ballad・game-field…）→ 目標の表（p10/中央値/p90）
//   genreTargets(名前, {bpm})       … LRA・PLR・頭・余韻・corr・flat・空気の目標の幅。BPM があれば LRA・PLR をテンポに合わせてずらす
//   genreJudge(測定値, 名前, {bpm}) … ○／要直し の行（gate.mjs の judge と同じ形）
//   tempoShift(指標, bpm, 基準bpm)  … テンポ表（by_tempo）から LRA・PLR の中央値のずれ
// 数字だけを使う（音・旋律・和音は入っていない）。AI生成曲の統計なので「出発点の目安」で、最後は耳で決める。mix-targets.json（帯域の目標）は別のまま。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
export const DATA_DIR = path.join(ROOT, "docs", "sound", "data");

/** 測定値のキー → 目標の表のキー。 */
export const METRIC_KEYS = { lra: "LRA", plr: "PLR", corr: "corr", flat: "flat", head: "頭", tail: "余韻", air: "帯域_air" };

/** 作曲ソフトのスタイル名 → 目標の表。group＝スタイル別(genre-targets-nihonichi.json の groups)、site＝サイトのジャンル別。conf=low は元の曲が少ない（目安が粗い）。 */
const G = (group, conf = "ok", note = "") => ({ kind: "group", key: group, conf, note });
const S = (site, conf = "ok", note = "") => ({ kind: "site", key: site, conf, note });
export const STYLE_MAP = {
  // ゲーム
  "game-battle": G("ボス/戦闘"), battle: G("ボス/戦闘"), boss: G("ボス/戦闘"), "game-boss": G("ボス/戦闘"),
  "game-field": G("フィールド/町/ダンジョン"), field: G("フィールド/町/ダンジョン"), "game-town": G("フィールド/町/ダンジョン"), "game-dungeon": G("フィールド/町/ダンジョン"),
  horror: G("ホラー/ダーク"), dark: G("ホラー/ダーク"),
  // バンド系（ロックは元の曲が 92、パンク・メタルもここに含まれる）
  rock: G("ロック/パンク/メタル", "low", "AI生成のロックは音量が控えめ（−13LUFS前後）。人間の録音のロックは別に決める"), "rock-clean": G("アコースティック/フォーク"), hardrock: G("ロック/パンク/メタル", "low"),
  punk: G("ロック/パンク/メタル", "low"), metal: G("ロック/パンク/メタル", "low"),
  // ポップ系・R&B・ヒップホップ・EDM（元の曲が足りない。全体か近いスタイルで代用）
  pop: G("(全体)", "low", "ポップスの元データが無いので全体の分布で代用"), jpop: G("(全体)", "low", "J-POP の元データが無いので全体の分布で代用"), vocaloid: G("エレクトロニック/シンセ", "low", "速いポップの元データが無いので電子系で代用"),
  hiphop: G("エレクトロニック/シンセ", "low", "ヒップホップの元データが無いので電子系で代用"), rnb: G("ジャズ/ファンク/ボサノバ", "low", "R&B の元データが無いのでジャズ・ファンク系で代用"), trap: G("エレクトロニック/シンセ", "low"),
  edm: G("エレクトロニック/シンセ"), house: G("エレクトロニック/シンセ"), disco: G("エレクトロニック/シンセ"), dnb: G("エレクトロニック/シンセ"), dubstep: G("エレクトロニック/シンセ"),
  retro: G("チップチューン/8bit"), chiptune: G("チップチューン/8bit"), "8bit": G("チップチューン/8bit"),
  // 静かな系
  jazz: G("ジャズ/ファンク/ボサノバ"), funk: G("ジャズ/ファンク/ボサノバ"), bossa: G("ジャズ/ファンク/ボサノバ"), reggae: G("ジャズ/ファンク/ボサノバ", "low", "レゲエの元データが無いのでジャズ・ファンク系で代用"), dembow: G("エレクトロニック/シンセ", "low"),
  solo: G("ピアノ独奏"), piano: G("ピアノ独奏"), acoustic: G("アコースティック/フォーク"), folk: G("アコースティック/フォーク"),
  ballad: G("バラード/子守歌"), lofi: S("Lo-Fi", "low", "Lo-Fi は 50曲測定の結果がある場合だけ。なければバラード系を使う"), lullaby: G("バラード/子守歌"),
  ambient: G("アンビエント/ドローン"), orch: G("オーケストラ/シネマ"), orchestra: G("オーケストラ/シネマ"), cinematic: G("オーケストラ/シネマ"), wafu: G("和風"),
};
const FALLBACKS = { lofi: "ballad" };

let cache = null;
/** 目標の表を読む。nihonichi（スタイル別）と、あれば site50（ジャンル別50曲測定）。 */
export function loadTargets(dir = DATA_DIR) {
  if (cache && cache.dir === dir) return cache.data;
  const rd = (f) => { try { return JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); } catch { return null; } };
  const data = { nihonichi: rd("genre-targets-nihonichi.json"), site50: rd("genre-targets-site50.json") };
  cache = { dir, data };
  return data;
}
export const clearTargetCache = () => { cache = null; };

/** サイト50の表を使う最低曲数。これ未満なら使わない。 */
export const SITE_MIN_N = 15;

/**
 * スタイル名から目標の表を探す。日本語のスタイル名（"ボス/戦闘"）、サイトのジャンル名（"game-bgm"）、作曲ソフトの名前（STYLE_MAP）のどれでもよい。
 * 戻り値: { name, label, source, n, stats, conf, note } または null
 */
export function resolveGenre(name, { data = loadTargets() } = {}) {
  if (!name) return null;
  const raw = String(name).trim();
  const lower = raw.toLowerCase();
  const nih = data.nihonichi, s50 = data.site50;
  const make = (label, source, entry, conf = "ok", note = "") => entry && entry.LRA ? { name: raw, label, source, n: entry.n, stats: entry, conf, note } : null;
  const trySite = (key) => {
    // 1000曲の表（曲数が多い）にあればそちら。なければ50曲測定の表（曲数が SITE_MIN_N 以上のとき）
    const e = nih?.by_site_genre?.[key];
    if (e) return make(key, "nihonichi-site", e);
    const e50 = s50?.groups?.[key];
    return e50 && e50.n >= SITE_MIN_N ? make(key, "site50", e50) : null;
  };
  let m = STYLE_MAP[lower] ?? STYLE_MAP[raw];
  if (!m && FALLBACKS[lower]) m = STYLE_MAP[FALLBACKS[lower]];
  if (m) {
    if (m.kind === "site") {
      const r = trySite(m.key);
      if (r) return { ...r, conf: m.conf === "low" ? "low" : r.conf, note: m.note };
      const fb = FALLBACKS[lower];
      return fb ? resolveGenre(fb, { data }) : null;
    }
    const r = make(m.key, "nihonichi", nih?.groups?.[m.key], m.conf, m.note);
    if (r) return r;
  }
  if (nih?.groups?.[raw]) return make(raw, "nihonichi", nih.groups[raw]);
  return trySite(raw);
}

/** 対応しているスタイル名の一覧（エラーメッセージ用）。 */
export const listGenreNames = (data = loadTargets()) => [...new Set([...Object.keys(STYLE_MAP), ...Object.keys(data.nihonichi?.groups ?? {}), ...Object.keys(data.site50?.groups ?? {})])];

// ---- テンポ ----
const BIN_CENTERS = [["0-80", 65], ["80-100", 90], ["100-120", 110], ["120-140", 130], ["140-160", 150], ["160-300", 190]];

/** テンポ表の中央値を、BPM に合わせて線形補間で返す（範囲の外は端の値）。指標は LRA・PLR など。 */
export function tempoMedian(metric, bpm, data = loadTargets()) {
  const bt = data.nihonichi?.by_tempo;
  if (!bt || !Number.isFinite(bpm)) return NaN;
  const pts = BIN_CENTERS.map(([k, c]) => [c, bt[k]?.[metric]?.med]).filter(([, v]) => Number.isFinite(v));
  if (!pts.length) return NaN;
  if (bpm <= pts[0][0]) return pts[0][1];
  if (bpm >= pts[pts.length - 1][0]) return pts[pts.length - 1][1];
  for (let i = 1; i < pts.length; i++) {
    if (bpm <= pts[i][0]) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i]; return y0 + ((y1 - y0) * (bpm - x0)) / (x1 - x0); }
  }
  return NaN;
}

/** そのスタイルの代表的なテンポ（中央値）。なければ 100。 */
export const refBpm = (entry) => (Number.isFinite(entry?.bpm?.med) ? entry.bpm.med : 100);

/** 曲の BPM に合わせた LRA／PLR の中央値のずれ（スタイルの代表テンポ → 曲の BPM での差。BPM が上がるほどマイナス）。 */
export function tempoShift(metric, bpm, baseBpm = 100, data = loadTargets()) {
  const a = tempoMedian(metric, bpm, data), b = tempoMedian(metric, baseBpm, data);
  return Number.isFinite(a) && Number.isFinite(b) ? a - b : 0;
}

const r1 = (x, d = 1) => Number(x.toFixed(d));

/** 頭の大きさの型（最初の5秒 − いちばん大きい5秒、dB）。 */
export function headStyle(med) {
  if (!Number.isFinite(med)) return { label: "不明", text: "" };
  if (med >= -4.5) return { label: "すぐ全開", text: "頭からほぼ全開（目安 −3〜−4dB）" };
  if (med <= -7) return { label: "小さく始める", text: "小さく始めて育てる（目安 −7〜−8dB）" };
  return { label: "中間", text: "やや小さめに始める（目安 −5〜−6dB）" };
}
/** 余韻の型。 */
export function tailStyle(med) {
  if (!Number.isFinite(med)) return { label: "不明", text: "" };
  if (med >= 2.0) return { label: "長い", text: "長く消える（目安 2秒以上。reverb・space-wet を多めに）" };
  if (med <= 1.0) return { label: "短い", text: "すぐ切れる（目安 1秒以下。残響は控えめ）" };
  return { label: "中くらい", text: "1〜1.5秒ほどで消える" };
}

/**
 * ジャンルの目標。戻り値: { label, source, n, conf, note, bpm, shift, ranges: { lra: {lo, med, hi}, ... }, head, tail }
 * bpm があれば LRA・PLR の幅をテンポに合わせてずらす（そのスタイルの代表テンポとの差）。
 */
export function genreTargets(name, { bpm = NaN, data = loadTargets() } = {}) {
  const g = resolveGenre(name, { data });
  if (!g) return null;
  const shift = { LRA: 0, PLR: 0 };
  const useBpm = Number.isFinite(bpm) && bpm > 0;
  if (useBpm) for (const k of Object.keys(shift)) shift[k] = tempoShift(k, bpm, refBpm(g.stats), data);
  const ranges = {};
  for (const [key, mk] of Object.entries(METRIC_KEYS)) {
    const s = g.stats[mk];
    if (!s || !Number.isFinite(s.med)) continue;
    const d = shift[mk] ?? 0;
    let lo = s.p10 + d, hi = s.p90 + d, med = s.med + d;
    if (mk === "LRA") { lo = Math.max(0.5, lo); hi = Math.max(lo + 0.5, hi); med = Math.max(0.5, med); }
    ranges[key] = { lo: r1(lo, 2), med: r1(med, 2), hi: r1(hi, 2) };
  }
  return { label: g.label, source: g.source, n: g.n, conf: g.conf, note: g.note, bpm: useBpm ? bpm : null, shift, ranges, head: headStyle(g.stats["頭"]?.med), tail: tailStyle(g.stats["余韻"]?.med) };
}

const HINTS = {
  lra: (v, t) => v < t.lo ? "起伏が小さい。セクション表の強さ差を広げる・dynamics: \"natural\"・サビ前に引く。" : "起伏が大きすぎる。静かな所を持ち上げるか、山を少し下げる。",
  plr: (v, t) => v < t.lo ? "潰れ気味。圧縮・リミッターを浅く、パートの足しすぎをやめる。" : "ピークだけ突き出ている。リミッターを少し効かせるか、突き出る音（スネア・キック）を下げる。",
  corr: (v, t) => v > t.hi ? "モノ寄り。和音の楽器を左右に振る（pan）・--widen。" : "左右がばらけすぎ。低音とリードは中央に。",
  flat: (v, t) => v < t.lo ? "2〜8kHzのざらつき（シンバル・ハイハットの高域・空気・残響）が少ない。hat の level・space（プレート系）を足す。" : "ざらつきが多すぎる（歪み・ノイズ・シンバルの出しすぎ）。hat・crash を下げる。",
  air: (v, t) => v < t.lo ? "8kHz以上の空気が少ない。hat・シェイカー・高いきらめき・残響の高域を足す（--lpf を上げる）。" : "8kHz以上が多すぎる。hat・crash を下げる。reverb を減らす。",
  head: (v, t) => v > t.hi ? "頭が最大より大きすぎる（全開すぎ）。導入の volume を下げて小さく始める。" : "頭が小さすぎる。導入を少し上げる（最初の5秒が静かすぎる）。",
  tail: (v, t) => v < t.lo ? "余韻が短い。space-wet・reverb を増やす／--loop-tail を使う前に尾を伸ばす。" : "余韻が長すぎる。space-wet を減らす。",
};
const LABELS = { lra: "ラウドネスレンジ", plr: "PLR（ピーク−ラウドネス）", corr: "左右の相関", flat: "ざらつき flat（2〜8kHz）", air: "空気（8kHz以上）", head: "頭の大きさ（最初の5秒−最大の5秒）", tail: "余韻（−20→−50dBの秒数）" };
const UNITS = { lra: "LU", plr: "dB", corr: "", flat: "", air: "dB", head: "dB", tail: "秒" };
const DIGITS = { lra: 1, plr: 1, corr: 2, flat: 2, air: 1, head: 1, tail: 2 };
export const GENRE_ROW_KEYS = ["lra", "plr", "head", "tail", "corr", "flat", "air"];

/**
 * ジャンル別の合否の行。m は measureWav の戻り値（lra・plr・corr・flat・air・intro・tail。無いものは飛ばす）。
 * 行は gate.mjs の judge と同じ形（key・label・value・unit・goal・ok・hint）。
 */
export function genreJudge(m, name, { bpm = NaN, data = loadTargets() } = {}) {
  const t = genreTargets(name, { bpm, data });
  if (!t) return null;
  const vals = { lra: m.lra, plr: m.plr, corr: m.corr, flat: m.flat, air: m.air, head: m.intro ?? m.headVsMax, tail: m.tail };
  const rows = [];
  for (const key of GENRE_ROW_KEYS) {
    const r = t.ranges[key];
    if (!r) continue;
    const v = vals[key];
    const d = DIGITS[key];
    const known = Number.isFinite(v);
    const ok = known ? v >= r.lo && v <= r.hi : true;
    let goal = `${r1(r.lo, d)}〜${r1(r.hi, d)}（中央 ${r1(r.med, d)}）`;
    if (key === "head") goal += `　${t.head.text}`;
    if (key === "tail") goal += `　${t.tail.text}`;
    rows.push({ key, label: LABELS[key], value: known ? r1(v, d) : null, unit: UNITS[key], goal, ok, hint: ok ? "" : HINTS[key](v, r) });
  }
  return { target: t, rows };
}

/** 目標の説明（1ジャンル分）を日本語で。 */
export function describeGenre(name, { bpm = NaN } = {}) {
  const t = genreTargets(name, { bpm });
  if (!t) return `ジャンル「${name}」の目標がありません（使える名前: ${listGenreNames().join("・")}）`;
  const d = (k) => { const r = t.ranges[k]; return r ? `${r.lo}〜${r.hi}（中央 ${r.med}）` : "-"; };
  const out = [`■ ジャンル目標「${t.label}」（元の曲 ${t.n}、出どころ ${t.source}${t.conf === "low" ? "、目安が粗い" : ""}${t.bpm ? `、BPM ${t.bpm} に合わせて LRA ${t.shift.LRA >= 0 ? "+" : ""}${t.shift.LRA.toFixed(1)}・PLR ${t.shift.PLR >= 0 ? "+" : ""}${t.shift.PLR.toFixed(1)}` : ""}）`];
  out.push(`  LRA ${d("lra")} / PLR ${d("plr")} / corr ${d("corr")} / flat ${d("flat")} / 空気 ${d("air")}`);
  out.push(`  頭 ${d("head")} dB … ${t.head.label}型。${t.head.text}`);
  out.push(`  余韻 ${d("tail")} 秒 … ${t.tail.label}。${t.tail.text}`);
  if (t.note) out.push(`  注意: ${t.note}`);
  return out.join("\n");
}
