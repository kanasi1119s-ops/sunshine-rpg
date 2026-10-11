import { makeRng, type EnvSpec, type FilterSpec, type NoiseColor, type Wave } from "./synth-dsp";
import type { FmLayer, Layer, NoiseLayer, SeKind, SfxRecipe, ToneLayer } from "./sfx-synth";

/**
 * 純合成の効果音のレシピ 58 種（docs/sound/synth-sfx-guide.md §5。2026-10-11）。
 * 数字はガイドの表のまま（出発点。耳で直す）。音程の組は独自に選んだもので、既存のゲームの効果音と同じ 2 音・同じ形にしていない。
 * ※調 の層は tune:true（tuneSe が BGM の調の音階へ寄せる）。
 */

type E = [number, number, number, number];
const env = (e: E, hold = 0): EnvSpec => ({ a: e[0], d: e[1], s: e[2], r: e[3], ...(hold ? { hold } : {}) });

interface Opt {
  at?: number; db?: number; hold?: number; tune?: boolean; f1?: number; glide?: number; detunes?: number[];
  filter?: FilterSpec[]; am?: { hz: number; depth: number; shape?: "sine" | "square" }; fpath?: [number, number][];
}
const tone = (wave: Wave, f0: number, e: E, o: Opt = {}): ToneLayer => ({
  kind: "tone", wave, f0, at: o.at ?? 0, db: o.db ?? 0, env: env(e, o.hold), ...(o.f1 ? { f1: o.f1 } : {}), ...(o.glide ? { glide: o.glide } : {}),
  ...(o.detunes ? { detunes: o.detunes } : {}), ...(o.filter ? { filter: o.filter } : {}), ...(o.am ? { am: o.am } : {}), ...(o.tune ? { tune: true } : {}), ...(o.fpath ? { fpath: o.fpath } : {}),
});
const noise = (color: NoiseColor, e: E, o: Opt = {}): NoiseLayer => ({
  kind: "noise", color, at: o.at ?? 0, db: o.db ?? 0, env: env(e, o.hold), ...(o.filter ? { filter: o.filter } : {}), ...(o.am ? { am: o.am } : {}),
});
const fm = (fc: number, ratio: number, i0: number, i1: number, sweep: number, e: E, o: Opt = {}): FmLayer => ({
  kind: "fm", fc, ratio, i0, i1, sweep, at: o.at ?? 0, db: o.db ?? 0, env: env(e, o.hold), ...(o.filter ? { filter: o.filter } : {}), ...(o.tune ? { tune: true } : {}),
});
const lp = (f0: number, o: Partial<FilterSpec> = {}): FilterSpec => ({ type: "lp", f0, ...o });
const hp = (f0: number, o: Partial<FilterSpec> = {}): FilterSpec => ({ type: "hp", f0, ...o });
const bp = (f0: number, o: Partial<FilterSpec> = {}): FilterSpec => ({ type: "bp", f0, ...o });
/** 周波数の並びを step 秒ずつずらして、同じ形の層を並べる。 */
const seq = (freqs: number[], step: number, make: (f: number, at: number, i: number) => Layer, at0 = 0): Layer[] => freqs.map((f, i) => make(f, at0 + i * step, i));

const R = (id: string, group: string, name: string, kind: SeKind, lengthSec: number, layers: Layer[], extra: Partial<SfxRecipe> = {}): SfxRecipe => ({ id, group, name, kind, lengthSec, layers, ...extra });

// 足音（石）の 1 歩。stairs でも使う。k＝フィルター中心の倍率
const stoneStep = (at: number, k = 1, db = 0): Layer[] => [
  noise("white", [0.001, 0.03, 0, 0.01], { at, db, filter: [hp(1500 * k), bp(3000 * k, { q: 2 })] }),
  tone("sine", 160, [0.001, 0.04, 0, 0.01], { at, db: db - 12, f1: 90, glide: 0.03 }),
];
// 斬撃（切る音）。会心の一撃でも使う
const slash = (): Layer[] => [
  noise("white", [0.01, 0.1, 0, 0.03], { filter: [bp(1500, { f1: 6000, sweep: 0.12, q: 1.2 })] }),
  noise("white", [0.001, 0.04, 0, 0.02], { at: 0.1, db: -3, filter: [hp(3000)] }),
  tone("sine", 200, [0.001, 0.08, 0, 0.03], { at: 0.1, db: -4, f1: 90, glide: 0.08 }),
];
// 扉のきしみ。f0→f1 へ glide 秒
const creak = (at: number, f0: number, f1: number, glide: number, db = 0, cutoff = 1200): Layer[] => [
  tone("sawtooth", f0, [0.05, 0.5, 0.5, 0.2], { at, db, f1, glide, hold: 0.05, filter: [lp(cutoff, { q: 2 })], am: { hz: 35, depth: 0.6, shape: "square" } }),
  noise("pink", [0.05, 0.5, 0.5, 0.2], { at, db: db - 20, filter: [lp(400)] }),
];
// ランダムな時刻の短い層（きらめき・泡・パチパチ）を作る。種は固定
const scatter = (n: number, span: [number, number], seed: number, make: (at: number, r: () => number) => Layer): Layer[] => {
  const r = makeRng(seed);
  return Array.from({ length: n }, () => make(span[0] + r() * (span[1] - span[0]), r)).sort((a, b) => a.at - b.at);
};
// ブラス風（のこぎり波＋フィルター包絡）
const brass = (f: number, at: number, hold: number, db = 0, tune = false): Layer =>
  tone("sawtooth", f, [0.01, 0.1, 0.7, 0.2], { at, db, hold, tune, filter: [lp(800, { f1: 3000, sweep: 0.15, q: 1.2 })] });

const ID = (n: number): number[] => Array.from({ length: n }, (_, i) => i);

export const SFX_RECIPES: SfxRecipe[] = [
  // ───── メニュー・画面（14） ─────
  R("cursor", "メニュー・画面", "カーソル移動", "ui", 0.05, [
    tone("triangle", 1320, [0.001, 0.03, 0, 0.01]), tone("sine", 2640, [0.001, 0.02, 0, 0.01], { db: -12 }),
  ], { vary: { pitch: 0.02, gainDb: 0.5 }, throttleMs: 40 }),
  R("confirm", "メニュー・画面", "決定", "ui", 0.25, [
    tone("triangle", 880, [0.003, 0.06, 0.3, 0.04], { tune: true }),
    tone("triangle", 1319, [0.003, 0.12, 0.2, 0.08], { at: 0.06, tune: true }), tone("sine", 2638, [0.002, 0.1, 0, 0.05], { at: 0.06, db: -10, tune: true }),
  ]),
  R("cancel", "メニュー・画面", "キャンセル", "ui", 0.2, [
    tone("triangle", 1568, [0.003, 0.05, 0.3, 0.03]), tone("triangle", 1047, [0.003, 0.1, 0.1, 0.07], { at: 0.06 }),
  ], { filter: [lp(3000)] }),
  R("error", "メニュー・画面", "ブブー（使えない）", "notice", 0.35, [
    ...[0, 0.16].flatMap((at) => [tone("square", 150, [0.005, 0.1, 0.6, 0.02], { at }), tone("square", 157, [0.005, 0.1, 0.6, 0.02], { at })]),
  ], { filter: [lp(1200)], peakDb: -8, duck: "none" }),
  R("menu-open", "メニュー・画面", "メニューを開く", "ui", 0.25, [
    ...seq([1047, 1319, 1568], 0.04, (f, at) => tone("triangle", f, [0.002, 0.05, 0.2, 0.05], { at })),
    noise("white", [0.01, 0.1, 0, 0.05], { db: -18, filter: [bp(2000, { f1: 5000, sweep: 0.15, q: 1 })] }),
  ]),
  R("menu-close", "メニュー・画面", "メニューを閉じる", "ui", 0.22, [
    ...seq([1568, 1319, 1047], 0.04, (f, at) => tone("triangle", f, [0.002, 0.05, 0.2, 0.05], { at })),
    noise("white", [0.01, 0.1, 0, 0.05], { db: -18, filter: [bp(5000, { f1: 2000, sweep: 0.15, q: 1 })] }),
  ]),
  R("text-tick", "メニュー・画面", "文字送り", "ui", 0.02, [tone("square", 900, [0.001, 0.012, 0, 0.005], { db: -14 })], { vary: { pitch: 0.05 }, throttleMs: 60, peakDb: -12 }),
  R("page", "メニュー・画面", "ページめくり", "ui", 0.15, [noise("white", [0.01, 0.1, 0, 0.03], { filter: [bp(3000, { f1: 1500, sweep: 0.12, q: 0.7 })] })], { peakDb: -9 }),
  R("click", "メニュー・画面", "ボタンクリック", "ui", 0.04, [
    noise("white", [0.001, 0.008, 0, 0.005], { filter: [hp(2000)] }), tone("sine", 1800, [0.001, 0.025, 0, 0.01], { db: -3, f1: 1200, glide: 0.02 }),
  ]),
  R("switch-on", "メニュー・画面", "スイッチ ON", "ui", 0.08, [tone("pulse25", 700, [0.002, 0.05, 0, 0.03], { f1: 1000, glide: 0.04 })]),
  R("switch-off", "メニュー・画面", "スイッチ OFF", "ui", 0.08, [tone("pulse25", 1000, [0.002, 0.05, 0, 0.03], { f1: 650, glide: 0.05 })]),
  R("save", "メニュー・画面", "セーブ", "notice", 0.9, [
    ...seq([523, 659, 784, 1047], 0.07, (f, at) => tone("triangle", f, [0.003, 0.15, 0.2, 0.2], { at, tune: true })),
    fm(1568, 3.5, 3, 0, 0.4, [0.002, 0.5, 0, 0.6], { at: 0.21, db: -10, tune: true }),
  ]),
  R("shop", "メニュー・画面", "買い物（お金）", "notice", 0.35, [
    tone("square", 1175, [0.002, 0.04, 0, 0.02]), tone("square", 1760, [0.002, 0.25, 0, 0.2], { at: 0.05 }), tone("sine", 3520, [0.002, 0.25, 0, 0.2], { at: 0.05, db: -14 }),
  ], { peakDb: -8 }),
  R("equip", "メニュー・画面", "装備する", "ui", 0.2, [
    tone("sine", 180, [0.001, 0.1, 0, 0.03], { f1: 90, glide: 0.08 }), fm(2400, 3.5, 2, 0, 0.06, [0.001, 0.06, 0, 0.04], { at: 0.03, db: -6 }),
    noise("white", [0.001, 0.01, 0, 0.01], { db: -8, filter: [hp(3000)] }),
  ]),
  // ───── フィールド（15） ─────
  R("step-grass", "フィールド", "足音（草）", "impact", 0.08, [
    noise("white", [0.003, 0.05, 0, 0.02], { filter: [bp(1200, { q: 0.8 })] }), tone("sine", 110, [0.001, 0.04, 0, 0.01], { db: -10, f1: 70, glide: 0.04 }),
  ], { vary: { pitch: 0.05, filter: 0.15, gainDb: 1 }, throttleMs: 120, peakDb: -12 }),
  R("step-stone", "フィールド", "足音（石）", "impact", 0.06, stoneStep(0), { vary: { pitch: 0.05, filter: 0.15, gainDb: 1 }, throttleMs: 120, peakDb: -12 }),
  R("step-wood", "フィールド", "足音（木の床）", "impact", 0.1, [
    tone("sine", 220, [0.001, 0.07, 0, 0.02], { f1: 110, glide: 0.06 }), noise("white", [0.001, 0.05, 0, 0.02], { db: -6, filter: [bp(700, { q: 3 })] }),
  ], { vary: { pitch: 0.05, filter: 0.15, gainDb: 1 }, throttleMs: 120, peakDb: -12 }),
  R("door-open", "フィールド", "扉を開ける（きしみ）", "impact", 0.8, creak(0, 180, 260, 0.4), { peakDb: -8, soft: true }),
  R("door-close", "フィールド", "扉を閉める", "impact", 0.3, [
    noise("brown", [0.001, 0.15, 0, 0.05], { filter: [lp(300, { f1: 120, sweep: 0.15 })] }), tone("sine", 90, [0.001, 0.15, 0, 0.05], { db: -3, f1: 50, glide: 0.15 }),
    noise("white", [0.001, 0.01, 0, 0.005], { db: -10, filter: [hp(2000)] }),
  ]),
  R("locked", "フィールド", "鍵がかかっている", "impact", 0.5, [
    ...[0, 0.12].flatMap((at) => [tone("sine", 160, [0.001, 0.05, 0, 0.02], { at, f1: 100, glide: 0.04 }), noise("white", [0.001, 0.02, 0, 0.01], { at, db: -6, filter: [bp(1500)] })]),
    noise("white", [0.002, 0.1, 0, 0.05], { at: 0.28, db: -10, filter: [bp(2500, { q: 5 })], am: { hz: 40, depth: 0.9, shape: "square" } }),
  ]),
  R("chest-open", "フィールド", "宝箱を開ける", "magic", 1.5, [
    noise("white", [0.001, 0.01, 0, 0.005], { filter: [hp(3000)] }),
    ...creak(0.05, 150, 300, 0.3, -6),
    ...seq([1319, 1760, 2349, 2794, 3136], 0.05, (f, at, i) => tone(i % 2 ? "triangle" : "sine", f, [0.003, 0.4, 0, 0.4], { at, db: -8 }), 0.4),
    fm(2093, 3.5, 3, 0, 0.5, [0.002, 0.8, 0, 0.8], { at: 0.6, db: -12 }),
  ], { peakDb: -6 }),
  R("item-get", "フィールド", "アイテム入手", "notice", 0.5, [
    tone("triangle", 1047, [0.003, 0.07, 0.2, 0.05], { tune: true }), tone("triangle", 1568, [0.003, 0.3, 0.2, 0.2], { at: 0.07, tune: true }),
    tone("sine", 3136, [0.002, 0.2, 0, 0.1], { at: 0.07, db: -12, tune: true }),
  ]),
  R("stairs", "フィールド", "階段", "impact", 0.8, [0, 1, 2, 3].flatMap((i) => stoneStep(i * 0.18, 1.08 ** i, -3 * i)), { peakDb: -12 }),
  R("warp", "フィールド", "ワープ", "magic", 1.6, [
    tone("sawtooth", 200, [0.1, 0.6, 0.6, 0.2], { f1: 2000, glide: 0.8, hold: 0.1, detunes: [-12, 0, 12], filter: [lp(400, { f1: 6000, sweep: 0.8, q: 2 })] }),
    noise("white", [0.2, 0.6, 0.3, 0.2], { db: -8, filter: [bp(500, { f1: 5000, sweep: 0.8, q: 1.5 })] }),
    fm(2637, 2.76, 4, 0, 0.5, [0.002, 0.7, 0, 0.7], { at: 0.8, db: -10 }),
  ], { soft: true }),
  R("jump", "フィールド", "ジャンプ", "impact", 0.15, [tone("pulse25", 330, [0.002, 0.12, 0, 0.04], { f1: 660, glide: 0.1 })]),
  R("splash", "フィールド", "水しぶき", "impact", 0.5, [
    noise("white", [0.005, 0.25, 0, 0.15], { filter: [bp(2500, { q: 0.7 })] }),
    ...scatter(5, [0, 0.3], 26, (at) => tone("sine", 400, [0.002, 0.06, 0, 0.02], { at, db: -10, f1: 1200, glide: 0.05 })),
  ]),
  R("alarm", "フィールド", "警報（警告）", "notice", 1.0, [
    ...[0, 0.2, 0.4].flatMap((at) => [
      tone("square", 660, [0.003, 0.1, 0.8, 0.01], { at }), tone("square", 1320, [0.003, 0.1, 0.8, 0.01], { at, db: -6 }), tone("square", 1980, [0.003, 0.1, 0.8, 0.01], { at, db: -10 }),
    ]),
  ], { duck: "warning", peakDb: -4.5 }),
  R("rumble", "フィールド", "地響き", "magic", 1.6, [
    noise("brown", [0.2, 0, 1, 0.6], { hold: 0.8, filter: [lp(90, { q: 1 })] }), tone("sine", 40, [0.2, 0, 1, 0.6], { hold: 0.8, db: -3, f1: 30, glide: 1.5 }),
  ], { am: { hz: 8, depth: 0.4 }, soft: true }),
  R("bump", "フィールド", "壁にぶつかる", "impact", 0.12, [
    tone("sine", 130, [0.001, 0.1, 0, 0.03], { f1: 70, glide: 0.08 }), noise("white", [0.001, 0.05, 0, 0.02], { db: -6, filter: [bp(400)] }),
  ]),
  // ───── 戦闘（8） ─────
  R("encounter", "戦闘", "敵と遭遇", "impact", 0.6, [
    tone("sawtooth", 1200, [0.002, 0.3, 0.1, 0.1], { f1: 200, glide: 0.35, filter: [lp(3000)] }), noise("white", [0.001, 0.25, 0, 0.1], { db: -8, filter: [hp(4000)] }),
    tone("square", 110, [0.005, 0.2, 0.4, 0.15], { at: 0.3, db: -6 }),
  ]),
  R("slash", "戦闘", "斬撃", "impact", 0.3, slash()),
  R("hit", "戦闘", "打撃・ダメージ", "impact", 0.25, [
    tone("sine", 180, [0.001, 0.12, 0, 0.04], { f1: 50, glide: 0.12 }), noise("white", [0.001, 0.1, 0, 0.03], { db: -3, filter: [lp(3000, { f1: 300, sweep: 0.1 })] }),
    noise("white", [0.001, 0.01, 0, 0.005], { db: -8, filter: [hp(2000)] }),
  ]),
  R("critical", "戦闘", "会心の一撃", "impact", 0.7, [
    ...slash(), tone("sawtooth", 400, [0.002, 0.15, 0, 0.05], { db: -8, f1: 1600, glide: 0.15 }),
    fm(2200, 2.76, 5, 0, 0.3, [0.001, 0.4, 0, 0.3], { at: 0.1, db: -10 }), tone("sine", 100, [0.001, 0.4, 0, 0.1], { at: 0.1, f1: 40, glide: 0.4 }),
  ]),
  R("miss", "戦闘", "ミス（かわされた）", "impact", 0.2, [noise("white", [0.02, 0.1, 0, 0.05], { filter: [bp(800, { f1: 2500, sweep: 0.15, q: 1 })] })], { peakDb: -8 }),
  R("guard", "戦闘", "防御", "impact", 0.25, [
    noise("white", [0.001, 0.02, 0, 0.01], { filter: [bp(2000, { q: 4 })] }), fm(1200, 3.5, 3, 0, 0.1, [0.001, 0.15, 0, 0.1], { db: -3 }),
    tone("sine", 150, [0.001, 0.08, 0, 0.03], { db: -6, f1: 100, glide: 0.05 }),
  ]),
  R("ally-damage", "戦闘", "味方がダメージを受ける", "impact", 0.35, [
    tone("sawtooth", 300, [0.002, 0.2, 0, 0.08], { f1: 90, glide: 0.2, filter: [lp(1500)] }), tone("sawtooth", 318, [0.002, 0.2, 0, 0.08], { db: -6, f1: 95, glide: 0.2, filter: [lp(1500)] }),
    noise("white", [0.001, 0.15, 0, 0.05], { db: -4, filter: [lp(2000, { f1: 400, sweep: 0.15 })] }), tone("sine", 120, [0.001, 0.1, 0, 0.03], { db: -4, f1: 60, glide: 0.1 }),
  ]),
  R("enemy-defeat", "戦闘", "敵を倒した", "impact", 0.7, [
    tone("sawtooth", 600, [0.002, 0.5, 0, 0.1], { f1: 60, glide: 0.5, filter: [lp(3000, { f1: 300, sweep: 0.5 })] }),
    noise("white", [0.001, 0.5, 0, 0.1], { db: -3, filter: [lp(6000, { f1: 300, sweep: 0.5 })] }),
  ], { am: { hz: 20, depth: 0.3 } }),
  // ───── 魔法・状態（14） ─────
  R("charge", "魔法・状態", "詠唱・チャージ", "magic", 1.2, [
    tone("sawtooth", 220, [0.8, 0, 1, 0.1], { hold: 0.3, f1: 880, glide: 1.0, detunes: [-20, -10, 0, 10, 20], filter: [lp(500, { f1: 5000, sweep: 1.0, q: 2 })] }),
    tone("sine", 1760, [0.8, 0, 1, 0.1], { hold: 0.3, db: -12, am: { hz: 6, depth: 0.5 } }),
  ], { soft: true }),
  R("fire", "魔法・状態", "炎", "magic", 0.9, [
    noise("pink", [0.05, 0.5, 0.3, 0.3], { filter: [bp(600, { f1: 2500, sweep: 0.5, q: 0.8 })] }),
    ...scatter(24, [0.05, 0.85], 39, (at, r) => noise("white", [0.0005, 0.003, 0, 0.002], { at, db: -10 - r() * 6, filter: [hp(2000)] })),
    tone("sine", 80, [0.01, 0.5, 0, 0.2], { db: -4, f1: 50, glide: 0.5 }),
  ], { soft: true }),
  R("ice", "魔法・状態", "氷", "magic", 0.8, [
    fm(2637, 2.76, 4, 0, 0.5, [0.001, 0.5, 0, 0.5]),
    ...scatter(5, [0, 0.4], 40, (at, r) => tone("sine", 3000 + r() * 3000, [0.001, 0.2, 0, 0.2], { at, db: -10 })),
    noise("white", [0.001, 0.1, 0, 0.1], { db: -18, filter: [hp(6000)] }),
  ]),
  R("thunder", "魔法・状態", "雷", "magic", 1.1, [
    noise("white", [0, 0.03, 0, 0.02], { filter: [hp(3000)] }), tone("sawtooth", 3000, [0.001, 0.08, 0, 0.02], { db: -6, f1: 200, glide: 0.08 }),
    noise("brown", [0.05, 0.6, 0.2, 0.5], { at: 0.05, db: -2, filter: [lp(200)] }), tone("sawtooth", 60, [0.05, 0.6, 0.2, 0.5], { at: 0.05, db: -6, filter: [lp(150)] }),
  ]),
  R("wind", "魔法・状態", "風", "magic", 0.9, [
    noise("pink", [0.2, 0, 1, 0.3], { hold: 0.4, filter: [bp(400, { path: [[0, 400], [0.4, 1200], [0.8, 600]], q: 1.2, lfo: { hz: 1.2, depth: 0.3 } })] }),
  ], { soft: true, peakDb: -9 }),
  R("light", "魔法・状態", "光", "magic", 1.2, [
    ...seq([1319, 1760, 2349, 3136], 0.06, (f, at) => tone("sine", f, [0.003, 0.3, 0, 0.3], { at, tune: true })),
    ...[2093, 2100, 2087].map((f) => tone("triangle", f, [0.1, 0.4, 0.3, 0.5], { hold: 0.1, db: -8, tune: true })), fm(3136, 3.5, 3, 0, 0.5, [0.001, 0.8, 0, 0.8], { db: -12, tune: true }),
  ], { filter: [hp(500)], soft: true }),
  R("dark", "魔法・状態", "闇", "magic", 1.2, [
    tone("sawtooth", 110, [0.05, 0.5, 0.3, 0.4], { f1: 55, glide: 0.6, hold: 0.25, detunes: [-25, 0, 25], filter: [lp(600, { f1: 200, sweep: 0.8 })] }),
    tone("sine", 55, [0.05, 0.5, 0.3, 0.4], { hold: 0.25, db: -3 }), noise("brown", [0.3, 0.4, 0, 0.3], { db: -6, filter: [lp(150)] }), tone("sine", 117, [0.05, 0.5, 0.3, 0.4], { hold: 0.25, db: -8 }),
  ], { soft: true }),
  R("heal", "魔法・状態", "回復", "magic", 1.0, [
    ...seq([523, 659, 784, 1047, 1319], 0.07, (f, at) => tone("triangle", f, [0.003, 0.5, 0, 0.3], { at, tune: true })),
    tone("sine", 1047, [0.2, 0.4, 0.3, 0.5], { db: -8, tune: true }), tone("sine", 1319, [0.2, 0.4, 0.3, 0.5], { db: -8, tune: true }),
  ], { filter: [hp(400)], soft: true }),
  R("buff", "魔法・状態", "能力アップ", "magic", 0.4, [
    ...seq([440, 554, 659, 880], 0.05, (f, at) => tone("square", f, [0.002, 0.05, 0, 0.03], { at })), tone("sine", 880, [0.01, 0.3, 0, 0.1], { db: -8, f1: 1760, glide: 0.3 }),
  ], { peakDb: -6 }),
  R("debuff", "魔法・状態", "能力ダウン", "magic", 0.4, [
    ...seq([880, 659, 554, 440], 0.05, (f, at) => tone("square", f, [0.002, 0.05, 0, 0.03], { at })), tone("sine", 880, [0.01, 0.3, 0, 0.1], { db: -8, f1: 440, glide: 0.3 }),
  ], { filter: [lp(2000)], peakDb: -7 }),
  R("poison", "魔法・状態", "毒", "magic", 0.7, [
    ...scatter(4, [0, 0.6], 48, (at) => tone("sine", 150, [0.002, 0.08, 0, 0.03], { at, f1: 250, glide: 0.08 })),
    tone("sawtooth", 98, [0.1, 0, 0.6, 0.2], { hold: 0.4, db: -6, filter: [lp(400)] }), tone("sawtooth", 103, [0.1, 0, 0.6, 0.2], { hold: 0.4, db: -6, filter: [lp(400)] }),
    noise("white", [0.1, 0, 0.6, 0.2], { hold: 0.4, db: -14, filter: [bp(500, { q: 2 })] }),
  ], { soft: true }),
  R("sleep", "魔法・状態", "眠り", "magic", 1.0, [
    ...seq([523, 440, 349], 0.25, (f, at) => tone("sine", f, [0.02, 0.3, 0.3, 0.3], { at, am: { hz: 4, depth: 0.4 }, filter: [lp(1200)] })),
    noise("pink", [0.3, 0, 1, 0.4], { hold: 0.3, db: -20, filter: [lp(500)] }),
  ], { soft: true }),
  R("paralysis", "魔法・状態", "麻痺", "magic", 0.45, [
    tone("sawtooth", 120, [0.01, 0.3, 0.5, 0.1], { am: { hz: 50, depth: 0.8 }, filter: [bp(1000, { q: 3 })] }),
    noise("white", [0.01, 0.3, 0.5, 0.1], { db: -6, filter: [bp(3000, { q: 4 })], am: { hz: 33, depth: 1, shape: "square" } }),
  ]),
  R("revive", "魔法・状態", "復活", "magic", 1.6, [
    ...[262, 330, 392].map((f) => tone("sawtooth", f, [0.4, 0, 0.8, 0.5], { hold: 0.3, tune: true, filter: [lp(1500)] })),
    tone("sine", 1047, [0.002, 0.8, 0, 0.8], { at: 0.6, tune: true }), tone("sine", 2093, [0.002, 0.8, 0, 0.8], { at: 0.6, tune: true }),
    ...scatter(4, [0.6, 1.0], 51, (at, r) => tone("sine", 2500 + r() * 2500, [0.002, 0.3, 0, 0.3], { at, db: -10 })),
  ], { soft: true }),
  // ───── ファンファーレ・節目（7） ─────
  R("level-up", "ファンファーレ・節目", "レベルアップ", "fanfare", 1.4, [
    ...seq([523, 659, 784, 988], 0.09, (f, at) => brass(f, at, 0, 0, true)),
    brass(1319, 0.36, 0.5, 0, true), brass(988, 0.36, 0.5, -4, true), brass(784, 0.36, 0.5, -4, true),
    tone("sine", 2638, [0.01, 0.1, 0.7, 0.2], { at: 0.36, hold: 0.5, db: -8, tune: true }), fm(2093, 3.5, 3, 0, 0.5, [0.002, 0.8, 0, 0.6], { at: 0.36, db: -12, tune: true }),
  ]),
  R("victory", "ファンファーレ・節目", "勝利", "fanfare", 3.0, [
    ...[0, 0.1, 0.19, 0.27, 0.34, 0.4, 0.45, 0.49].map((at, i) => noise("white", [0.001, 0.05, 0, 0.02], { at, db: -8 + i * 0.5, filter: [bp(1500)] })),
    brass(392, 0.55, 0), brass(523, 0.7, 0), brass(659, 0.85, 0), brass(784, 1.0, 1.2), brass(523, 1.0, 1.2, -4), brass(659, 1.0, 1.2, -4),
    tone("sine", 100, [0.002, 0.3, 0, 0.2], { at: 1.0, f1: 55, glide: 0.3 }), noise("white", [0.003, 1.2, 0, 0.8], { at: 1.0, db: -6, filter: [hp(6000)] }),
  ], { soft: true }),
  R("game-over", "ファンファーレ・節目", "ゲームオーバー", "fanfare", 3.5, [
    ...seq([220, 175, 147], 0.6, (f, at, i) => tone("sawtooth", f, [0.1, 0, 0.8, i === 2 ? 2 : 0.4], { at, hold: i === 2 ? 0.2 : 0.3, filter: [lp(3000, { f1: 400, sweep: 2.5 })] })),
    ...seq([220, 175, 147], 0.6, (f, at, i) => tone("triangle", f, [0.1, 0, 0.8, i === 2 ? 2 : 0.4], { at, hold: i === 2 ? 0.2 : 0.3, db: -3 })),
  ], { reverb: { decay: 2, mix: 0.3 }, soft: true }),
  R("key-item", "ファンファーレ・節目", "重要アイテム", "fanfare", 1.2, [
    ...seq([523, 659, 784], 0.1, (f, at) => brass(f, at, 0, 0, true)), brass(1047, 0.3, 0.4, 0, true), tone("sine", 2093, [0.01, 0.1, 0.7, 0.2], { at: 0.3, hold: 0.4, db: -8, tune: true }),
  ]),
  R("count-tick", "ファンファーレ・節目", "経験値・お金のカウント", "ui", 0.4, [
    ...ID(10).map((i) => tone("square", 1200 * 1.02 ** i, [0.001, 0.03, 0, 0.01], { at: i * 0.04, db: -10 })),
  ], { throttleMs: 0, peakDb: -10 }),
  R("boss-hit", "ファンファーレ・節目", "ボス登場（シネマティック・ヒット）", "fanfare", 3.0, [
    noise("white", [0.8, 0, 1, 0.01], { db: -10, filter: [hp(1000)] }),
    tone("sine", 60, [0.005, 1.5, 0, 0.5], { at: 0.8, f1: 30, glide: 1.5 }), noise("brown", [0.01, 1.2, 0, 0.8], { at: 0.8, db: -3, filter: [lp(200)] }),
    ...[65, 82, 98].map((f) => tone("sawtooth", f, [0.05, 1, 0, 1], { at: 0.8, db: -8, filter: [lp(500)] })),
  ], { soft: true, reverb: { decay: 1.2, mix: 0.2 } }),
  R("transition", "ファンファーレ・節目", "場面転換（スウッシュ）", "fanfare", 1.1, [
    noise("white", [0.8, 0, 1, 0.05], { hold: 0.2, filter: [bp(200, { f1: 8000, sweep: 1.0, q: 1.5 })] }), tone("sine", 100, [0.8, 0, 1, 0.05], { hold: 0.2, db: -12, f1: 800, glide: 1.0 }),
  ], { soft: true }),
];

export const SFX_BY_ID: Record<string, SfxRecipe> = Object.fromEntries(SFX_RECIPES.map((r) => [r.id, r]));
