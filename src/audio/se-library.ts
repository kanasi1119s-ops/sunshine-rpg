import { midiToName } from "./compose";
import type { Instrument, Score, Track, Waveform } from "./score";

/**
 * ゲームによくある効果音の一式（53種、それぞれ約2〜4秒）。
 * 録音音源（GMの楽器: ティンパニ・ハープ・ビブラフォン・合唱・ブラス・ドラムなど）と、ノイズの合成音（風切り・打撃・足音）を重ねて作る。
 * 録音音源の準備ができていないときは、同じ譜面を合成音で鳴らす（`gm`つきのパートには、代わりの`instrument`を持たせてある）。
 * 拍のテンポは240BPM（1拍＝0.25秒）にそろえ、"音名:拍数" で書く。最後に無音の「間」を足して、余韻（残響）まで含めた長さにする。
 * ダメージ系（斬撃・ダメージ・会心・被ダメージ）には、打撃音のあとに「鋭く刺さる高音」（pierce）をつけてある。
 * 勝利・レベルアップのファンファーレは、既存作品の有名な勝利曲に似ないよう、独自の楽句で作った（D長調・E長調、同音連打で始めない）。
 * 打楽器（gmDrum）の「音名」は、GMドラムのキー番号（例: 36=バスドラム、38=スネア、49=クラッシュ、47=タム）を音名にしたもの。
 */

function parse(spec: string): Track["notes"] {
  return spec.split(" ").map((token) => {
    const [name, beats] = token.split(":");
    return { note: name, durationBeats: Number(beats) };
  });
}

/** 録音音源の楽器 → 準備中に鳴らす合成音の代わり。 */
const FALLBACK: Record<number, Instrument> = {
  8: "chime", 9: "bell", 11: "bell", 12: "keys", 14: "bell", 24: "guitar", 33: "bass", 44: "strings", 45: "guitar", 46: "guitar", 47: "impact", 48: "strings", 52: "pad", 53: "pad",
  55: "impact", 56: "lead", 61: "lead", 89: "pad", 91: "pad", 96: "pad", 98: "chime", 99: "pad", 100: "chime", 101: "pad", 102: "pad", 103: "sfxUp", 115: "impact",
  116: "impact", 119: "swoosh", 120: "swoosh", 121: "wind", 122: "wind", 126: "swoosh",
};
/** 録音音源の楽器（GMの番号）で鳴らすパート。 */
const gm = (program: number, volume: number, spec: string, waveform: Waveform = "triangle"): Track => ({
  waveform, instrument: FALLBACK[program], gm: program, volume, notes: parse(spec),
});
/** 録音音源のドラム（音名＝GMドラムのキー番号）。準備中は `fallback` の合成音で鳴らす。 */
const dr = (volume: number, fallback: Instrument, spec: string): Track => ({
  waveform: "sine", instrument: fallback, gm: 0, gmDrum: true, volume, notes: parse(spec),
});
/** 合成音のパート（ノイズの打撃・風切りなど）。 */
const syn = (instrument: Instrument, waveform: Waveform, volume: number, spec: string): Track => ({
  waveform, instrument, volume, notes: parse(spec),
});
const k = (n: number): string => midiToName(n);
/** 全体の長さ（秒）を決める無音のパート。余韻（残響）が消えるまでを含める。 */
const spacer = (secs: number): Track => ({ waveform: "sine", volume: 0, notes: [{ note: "R", durationBeats: secs * 4 }] });
function E(id: string, group: string, name: string, secs: number, ...tracks: Track[]): SeEntry {
  return { id, group, name, score: { tempoBpm: 240, loop: false, tracks: [...tracks, spacer(secs)] } };
}

export interface SeEntry {
  id: string;
  name: string;
  group: string;
  score: Score;
}

// 打楽器のキー番号
const KICK = k(36), SNARE = k(38), CRASH = k(49), CRASH2 = k(57), TOM_H = k(50), TOM_M = k(47), TOM_L = k(43), SIDE = k(37), CLAP = k(39);

export const SE_LIBRARY: SeEntry[] = [
  // ── メニュー・画面まわり ──
  E("cursor", "メニュー", "カーソル移動", 2.2, gm(8, 0.34, "E6:0.5"), gm(11, 0.06, "E6:4")),
  E("confirm", "メニュー", "決定", 2.4, gm(8, 0.22, "E6:0.5 A6:1"), gm(11, 0.06, "A5:6")),
  E("cancel", "メニュー", "キャンセル", 2.2, gm(12, 0.22, "A4:0.5 E4:1.5"), gm(89, 0.05, "E3:6")),
  E("error", "メニュー", "ブブー（使えない）", 2.2, gm(33, 0.3, "E2:1 R:0.5 E2:2"), syn("lead", "sawtooth", 0.06, "E3:1 R:0.5 E3:2"), syn("wind", "sine", 0.03, "C3:6")),
  E("menu-open", "メニュー", "メニューを開く", 2.4, gm(46, 0.2, "C5:0.25 E5:0.25 G5:0.25 C6:0.25 E6:1.5"), gm(11, 0.05, "C6:6")),
  E("menu-close", "メニュー", "メニューを閉じる", 2.4, gm(46, 0.2, "E6:0.25 C6:0.25 G5:0.25 E5:0.25 C5:1.5"), gm(89, 0.05, "C4:6")),
  E("page", "メニュー", "ページめくり", 2.0, syn("swoosh", "sine", 0.14, "C5:1"), gm(45, 0.12, "A5:0.25"), syn("wind", "sine", 0.02, "C5:6")),
  E("text-blip", "メニュー", "文字送り", 2.0, gm(115, 0.2, "C6:0.25"), gm(8, 0.04, "C7:0.25 E7:0.25")),
  E("save", "メニュー", "セーブ", 3.4, gm(46, 0.2, "C5:0.5 E5:0.5 G5:0.5 C6:0.5 E6:0.5 G6:2"), gm(52, 0.08, "C5:8"), gm(11, 0.06, "G6:8")),
  E("equip", "メニュー", "装備する", 2.6, syn("impact", "sine", 0.22, "A3:0.5"), syn("chime", "sine", 0.14, "R:0.5 E6:1"), gm(11, 0.1, "R:0.5 E6:6")),
  E("buy", "メニュー", "買い物（お金）", 2.4, gm(9, 0.22, "B6:0.25 E7:1"), gm(11, 0.08, "E6:6")),
  E("sell", "メニュー", "売る", 2.4, gm(9, 0.22, "E7:0.25 B6:1"), gm(11, 0.08, "B5:6")),
  // ── フィールド ──
  E("footstep", "フィールド", "足音", 2.2, syn("impact", "sine", 0.12, "G3:0.25 R:1.75 F3:0.25 R:1.75 G3:0.25 R:1.75 F3:0.25 R:1.75"), syn("wind", "sine", 0.02, "C5:8")),
  E("door", "フィールド", "扉を開ける", 2.8, syn("swoosh", "sine", 0.12, "A3:6"), gm(33, 0.1, "A1:4"), syn("impact", "sine", 0.2, "R:6 D3:0.5"), dr(0.2, "kick", `R:6 ${KICK}:0.5`)),
  E("door-locked", "フィールド", "扉が開かない", 2.4, syn("impact", "sine", 0.2, "F3:0.25 R:1 F3:0.25 R:1 F3:0.25 R:1"), dr(0.2, "snare", `${SIDE}:0.25 R:1 ${SIDE}:0.25 R:1 ${SIDE}:0.25 R:1`), gm(115, 0.1, "E5:0.25")),
  E("chest", "フィールド", "宝箱を開ける", 3.2, syn("impact", "sine", 0.18, "C3:0.5"), gm(46, 0.3, "R:1 G5:0.5 C6:0.5 E6:0.5 G6:0.5 C7:2"), gm(52, 0.07, "R:1 C5:8"), gm(11, 0.06, "R:2 G6:8")),
  E("item-get", "フィールド", "アイテム入手", 2.8, gm(9, 0.22, "G5:0.5 C6:0.5 E6:0.5 G6:2"), gm(46, 0.12, "C5:0.5 E5:0.5 G5:0.5 C6:2"), gm(11, 0.06, "C6:8")),
  E("stairs", "フィールド", "階段", 2.4, syn("impact", "sine", 0.1, "E3:0.25 R:0.75 E3:0.25 R:0.75 E3:0.25 R:0.75 E3:0.25 R:0.75"), gm(115, 0.06, "C5:0.25 R:0.75 D5:0.25 R:0.75 E5:0.25 R:0.75 F5:0.25")),
  E("warp", "フィールド", "ワープ", 3.6, syn("sfxUp", "sine", 0.16, "C4:6"), syn("swoosh", "sine", 0.14, "C5:8"), gm(98, 0.16, "C4:10"), gm(53, 0.07, "C5:10")),
  E("bump", "フィールド", "壁にぶつかる", 2.2, syn("impact", "sine", 0.16, "D3:0.25"), gm(47, 0.2, "D2:0.5"), syn("wind", "sine", 0.02, "C3:6")),
  E("jump", "フィールド", "ジャンプ", 2.2, syn("sfxUp", "square", 0.1, "E4:0.5"), gm(12, 0.16, "E4:0.25 A4:0.25 E5:1"), syn("impact", "sine", 0.1, "R:2 G3:0.25")),
  E("splash", "フィールド", "水しぶき", 2.8, syn("swoosh", "sine", 0.18, "F5:2"), syn("impact", "sine", 0.1, "R:0.5 A4:0.5"), gm(122, 0.12, "C4:8")),
  E("alarm", "フィールド", "警報", 3.4, gm(14, 0.24, "A5:1 R:1 E5:1 R:1 A5:1 R:1 E5:1 R:1 A5:1 R:1 E5:1"), syn("lead", "square", 0.06, "A4:1 R:1 E4:1 R:1 A4:1 R:1 E4:1 R:1 A4:1 R:1 E4:1")),
  E("quake", "フィールド", "地響き", 3.8, syn("impact", "sine", 0.3, "D2:2 R:0.3 C2:2"), gm(47, 0.24, "D2:1 D2:1 D2:1 D2:1 C2:1 C2:1 C2:1 C2:1"), syn("wind", "sine", 0.1, "D2:14")),
  E("mystery", "フィールド", "不思議な気配", 3.8, gm(14, 0.14, "B5:1 F6:2"), gm(91, 0.1, "E3:12"), gm(98, 0.06, "B4:12")),
  // ── 戦闘 ──
  E("encounter", "戦闘", "敵と遭遇", 2.8, syn("sfxDown", "sawtooth", 0.16, "A5:2"), gm(47, 0.28, "R:1.5 C2:1 C2:1"), gm(55, 0.22, "R:2 C3:1"), syn("swoosh", "sine", 0.12, "C4:3"), dr(0.2, "crash", `R:2 ${CRASH}:1`)),
  E("battle-start", "戦闘", "戦闘開始", 3.2, dr(0.3, "crash", `${CRASH}:1`), gm(116, 0.3, "C2:0.5 C2:0.5 G2:1 C2:0.5 C2:0.5 G2:1"), gm(55, 0.25, "C3:1"), dr(0.2, "kick", `${KICK}:0.5 R:1.5 ${KICK}:0.5`)),
  E("attack", "戦闘", "斬撃", 2.2, syn("swoosh", "sine", 0.22, "C5:1"), syn("impact", "sine", 0.24, "R:0.8 G3:0.5"), syn("pierce", "sawtooth", 0.2, "R:0.85 E7:0.75"), dr(0.16, "crash", `R:0.8 ${CRASH2}:1`), gm(45, 0.14, "R:0.8 E6:0.5")),
  E("hit", "戦闘", "ダメージ（命中）", 2.4, syn("impact", "sine", 0.3, "A3:0.5"), syn("pierce", "sawtooth", 0.24, "R:0.4 A6:1"), syn("pierce", "sawtooth", 0.12, "R:1.2 A6:0.5"), dr(0.28, "snare", `${SNARE}:0.5`), gm(47, 0.22, "A2:0.5"), syn("sfxDown", "square", 0.08, "R:0.2 A4:1")),
  E("critical", "戦闘", "会心の一撃", 2.8, dr(0.22, "crash", `${CRASH}:1`), syn("impact", "sine", 0.34, "E3:0.5"), syn("pierce", "sawtooth", 0.28, "R:0.4 E7:1.25"), syn("pierce", "sawtooth", 0.16, "R:1.6 B6:0.75"), gm(55, 0.28, "E3:1"), syn("sfxUp", "sawtooth", 0.12, "C5:1 G5:1"), gm(47, 0.24, "E2:0.5")),
  E("miss", "戦闘", "ミス（かわされた）", 2.2, syn("swoosh", "sine", 0.18, "G5:2"), gm(120, 0.1, "C4:2"), syn("wind", "sine", 0.03, "G4:6")),
  E("guard", "戦闘", "防御", 2.4, syn("impact", "sine", 0.2, "D4:0.5"), gm(14, 0.16, "D5:0.5"), dr(0.18, "snare", `${SIDE}:0.5`), gm(11, 0.06, "A5:6")),
  E("player-damage", "戦闘", "味方がダメージを受ける", 2.6, syn("impact", "sine", 0.28, "F3:0.5"), syn("pierce", "sawtooth", 0.24, "R:0.4 F#6:1"), gm(47, 0.24, "F2:0.5"), syn("sfxDown", "sawtooth", 0.1, "R:0.2 E4:2"), gm(33, 0.14, "F1:2")),
  E("magic-charge", "戦闘", "魔法の詠唱", 3.2, syn("sfxUp", "triangle", 0.14, "C4:8"), syn("swoosh", "sine", 0.1, "E4:8"), gm(98, 0.16, "C5:10"), gm(53, 0.08, "C4:10")),
  E("fire", "戦闘", "炎の術", 3.2, syn("swoosh", "sine", 0.22, "D4:3"), syn("impact", "sine", 0.3, "R:2.5 C4:2"), gm(47, 0.2, "R:2.5 C2:1"), gm(100, 0.1, "R:1 C4:8"), dr(0.16, "crash", `R:2.5 ${CRASH2}:1`)),
  E("ice", "戦闘", "氷の術", 3.4, gm(9, 0.2, "E7:0.5 B6:0.5 G7:0.5 D7:0.5 B7:2"), gm(98, 0.16, "E5:10"), syn("swoosh", "sine", 0.1, "G6:5"), gm(11, 0.08, "B6:10")),
  E("thunder", "戦闘", "雷の術", 3.4, syn("sfxDown", "sawtooth", 0.2, "A6:2"), syn("impact", "sine", 0.36, "R:1 C3:3"), dr(0.24, "crash", `R:1 ${CRASH}:1`), gm(47, 0.28, "R:1 C2:1 C2:1 C2:1")),
  E("wind", "戦闘", "風の術", 3.4, syn("swoosh", "sine", 0.24, "E3:6"), syn("wind", "sine", 0.14, "E3:12"), gm(122, 0.1, "C4:12")),
  E("heal", "戦闘", "回復", 3.6, gm(46, 0.2, "C5:0.5 E5:0.5 G5:0.5 C6:0.5 E6:0.5 G6:0.5 C7:2"), gm(52, 0.1, "C5:12"), gm(8, 0.12, "R:1 E6:1 G6:1 C7:2"), gm(11, 0.05, "C6:12")),
  E("buff", "戦闘", "能力アップ", 2.8, gm(9, 0.2, "C5:0.5 E5:0.5 G5:0.5 C6:2"), syn("sfxUp", "square", 0.08, "C5:2"), gm(61, 0.1, "R:1.5 G5:2")),
  E("debuff", "戦闘", "能力ダウン", 2.8, gm(9, 0.18, "C6:0.5 G5:0.5 E5:0.5 C5:2"), syn("sfxDown", "square", 0.08, "G5:2"), gm(33, 0.14, "R:1.5 C2:3")),
  E("poison", "戦闘", "毒", 3.0, syn("sfxDown", "sawtooth", 0.14, "E4:2 D4:2 C4:3"), gm(33, 0.2, "E2:2 D2:2 C2:3"), gm(101, 0.1, "E3:8")),
  E("sleep", "戦闘", "眠り", 3.6, gm(9, 0.16, "G5:1 E5:1 C5:3"), gm(89, 0.1, "C4:14"), gm(8, 0.08, "R:2 E5:1 G5:1 C6:3")),
  E("status-recover", "戦闘", "状態異常が治る", 2.8, gm(46, 0.18, "G5:0.5 C6:0.5 E6:0.5 G6:2"), gm(11, 0.08, "C6:8"), gm(52, 0.06, "G4:8")),
  E("revive", "戦闘", "復活", 3.8, gm(46, 0.2, "C5:0.5 E5:0.5 G5:0.5 C6:0.5 E6:0.5 G6:1"), gm(52, 0.14, "C4:14"), gm(48, 0.1, "C4:12"), gm(9, 0.14, "R:3 C7:3"), syn("sfxUp", "sine", 0.05, "C4:10")),
  E("flee", "戦闘", "走り去る（逃げる）", 2.8, syn("impact", "sine", 0.13, "G3:0.25 R:0.25 F3:0.25 R:0.25 G3:0.25 R:0.25 F3:0.25 R:0.25 G3:0.25 R:0.25 F3:0.25 R:0.25 G3:0.25 R:0.25 F3:0.25 R:0.25 G3:0.25 R:0.25 F3:0.25 R:0.25"), syn("swoosh", "sine", 0.16, "D4:10"), syn("wind", "sine", 0.05, "C4:10"), gm(115, 0.05, "C5:0.25 R:0.25 D5:0.25 R:0.25 C5:0.25 R:0.25 D5:0.25 R:0.25")),
  E("flee-fail", "戦闘", "逃げられない", 2.6, syn("impact", "sine", 0.14, "G3:0.25 R:0.25 G3:0.25 R:0.25 G3:0.25"), syn("sfxDown", "square", 0.12, "R:3 E4:2"), gm(47, 0.2, "R:3 E2:1"), gm(33, 0.14, "R:3 E1:3")),
  E("enemy-down", "戦闘", "敵を倒した", 3.0, syn("sfxDown", "sawtooth", 0.16, "A4:3"), syn("impact", "sine", 0.2, "R:0.5 C3:2"), gm(55, 0.16, "R:0.5 C3:1"), gm(53, 0.08, "A3:10")),
  E("boss-appear", "戦闘", "ボス登場", 3.9, gm(47, 0.3, "C2:1 C2:1 C2:1 C2:1 C2:0.5 C2:0.5 C2:0.5 C2:0.5 C2:1"), dr(0.22, "crash", `R:8 ${CRASH}:1`), gm(55, 0.28, "R:8 C3:2"), gm(119, 0.16, "C4:8"), gm(52, 0.12, "C3:14"), syn("swoosh", "sine", 0.14, "C3:8")),
  E("level-up", "戦闘", "レベルアップ", 3.6, gm(46, 0.24, "E4:0.5 B4:0.5 E5:0.5 G#5:0.5 B5:0.5 E6:2.5"), gm(61, 0.16, "R:2.5 B5:1 E6:5"), gm(8, 0.16, "R:1 E6:0.5 G#6:0.5 B6:0.5 E7:3"), gm(47, 0.22, "E2:0.5 R:1.5 B2:0.5 R:0.5 E3:3"), dr(0.16, "crash", `R:2.5 ${CRASH}:1`), gm(11, 0.06, "B5:14")),
  // 勝利: 拍を刻む太鼓のうなり → 低く始まる金管の上昇（二度の駆け上がり）→ 高い音で長く伸ばし、ハープが駆け上がって合唱とシンバルが開く。
  // 「同じ音の連打で始まって短い下降で受ける」型を避け、D長調（ミクソリディアからの上昇）で作った完全に独自の楽句
  E("victory", "戦闘", "勝利のファンファーレ", 4.0, gm(47, 0.24, "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 A2:1 D3:3"), gm(61, 0.22, "R:1 D5:1 F#5:1 A5:1 F#5:1 G5:1 B5:1 D6:5"), gm(56, 0.14, "R:1 B4:1 D5:1 F#5:1 D5:1 E5:1 G5:1 B5:5"), gm(46, 0.2, "R:8 D5:0.25 F#5:0.25 A5:0.25 D6:0.25 F#6:0.25 A6:0.25 D7:2"), dr(0.22, "crash", `R:8 ${CRASH}:1`), gm(52, 0.1, "R:8 D4:8"), gm(9, 0.1, "R:9 A6:0.5 D7:0.5 F#7:3")),
  E("defeat", "戦闘", "全滅", 4.0, gm(48, 0.2, "E3:2 D3:2 C3:2 B2:8"), gm(47, 0.22, "E2:1 R:1 D2:1 R:1 C2:1 R:1 B1:5"), gm(53, 0.08, "E4:2 D4:2 C4:2 B3:8"), syn("sfxDown", "sawtooth", 0.08, "R:3 E3:8")),
  E("exp-gain", "戦闘", "経験値・お金を得る", 2.4, gm(9, 0.2, "E6:0.25 E6:0.25 E6:0.25 E6:0.25 E6:0.25 G6:1.5"), gm(11, 0.06, "G6:6")),
];
// 打楽器のキー番号の定数を使わないと未使用エラーになるものを、明示的に参照
void [TOM_H, TOM_M, TOM_L, CLAP];
