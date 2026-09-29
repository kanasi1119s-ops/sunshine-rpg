import type { Instrument, Score, Track, Waveform } from "./score";

/**
 * ゲームによくある効果音の一式。すべてオリジナルの合成音（音声ファイルは使わない）。
 * 拍のテンポを240BPM（1拍＝0.25秒）にそろえてあり、"音名:拍数" で長さを書く。
 * 打撃・ノイズ系（impact・swoosh・hihat・snare）の音名は、音の明るさ（高いほど明るく鋭い）を決める。
 */

function parse(spec: string): Track["notes"] {
  return spec.split(" ").map((token) => {
    const [name, beats] = token.split(":");
    return { note: name, durationBeats: Number(beats) };
  });
}
function part(instrument: Instrument | null, waveform: Waveform, volume: number, spec: string): Track {
  return { waveform, instrument: instrument ?? undefined, volume, notes: parse(spec) };
}
function se(...tracks: Track[]): Score {
  return { tempoBpm: 240, loop: false, tracks };
}
const sq = (v: number, s: string): Track => part(null, "square", v, s);
const tri = (v: number, s: string): Track => part(null, "triangle", v, s);

export interface SeEntry {
  id: string;
  name: string;
  group: string;
  score: Score;
}

export const SE_LIBRARY: SeEntry[] = [
  // ── メニュー・画面まわり ──
  { id: "cursor", group: "メニュー", name: "カーソル移動", score: se(sq(0.16, "E6:0.2")) },
  { id: "confirm", group: "メニュー", name: "決定", score: se(sq(0.18, "E6:0.25 A6:0.5")) },
  { id: "cancel", group: "メニュー", name: "キャンセル", score: se(sq(0.16, "A5:0.25 E5:0.5")) },
  { id: "error", group: "メニュー", name: "ブブー（使えない）", score: se(part(null, "sawtooth", 0.15, "E3:0.4 R:0.15 E3:0.5")) },
  { id: "menu-open", group: "メニュー", name: "メニューを開く", score: se(part("sfxUp", "square", 0.12, "C5:0.6")) },
  { id: "menu-close", group: "メニュー", name: "メニューを閉じる", score: se(part("sfxDown", "square", 0.12, "G5:0.6")) },
  { id: "page", group: "メニュー", name: "ページめくり", score: se(part("swoosh", "sine", 0.16, "C4:0.5")) },
  { id: "text-blip", group: "メニュー", name: "文字送り", score: se(sq(0.08, "B5:0.1")) },
  { id: "save", group: "メニュー", name: "セーブ", score: se(part("chime", "sine", 0.2, "C6:0.4 E6:0.4 G6:0.4 C7:1")) },
  { id: "equip", group: "メニュー", name: "装備する", score: se(part("impact", "sine", 0.22, "A3:0.3"), part("chime", "sine", 0.14, "R:0.3 E6:0.6")) },
  { id: "buy", group: "メニュー", name: "買い物（お金）", score: se(part("chime", "sine", 0.2, "B6:0.25 E7:0.9")) },
  { id: "sell", group: "メニュー", name: "売る", score: se(part("chime", "sine", 0.2, "E7:0.25 B6:0.9")) },
  // ── フィールド ──
  { id: "footstep", group: "フィールド", name: "足音", score: se(part("impact", "sine", 0.1, "G3:0.25")) },
  { id: "door", group: "フィールド", name: "扉を開ける", score: se(part("swoosh", "sine", 0.14, "A3:0.8"), part("impact", "sine", 0.18, "R:0.6 D3:0.4")) },
  { id: "door-locked", group: "フィールド", name: "扉が開かない", score: se(part("impact", "sine", 0.2, "F3:0.2 R:0.2 F3:0.2")) },
  { id: "chest", group: "フィールド", name: "宝箱を開ける", score: se(part("impact", "sine", 0.2, "C3:0.3"), part("chime", "sine", 0.2, "R:0.4 G6:0.3 C7:0.3 E7:0.3 G7:1")) },
  { id: "item-get", group: "フィールド", name: "アイテム入手", score: se(sq(0.16, "G5:0.25 C6:0.25 E6:0.25 G6:1")) },
  { id: "stairs", group: "フィールド", name: "階段", score: se(part("impact", "sine", 0.1, "E3:0.2 R:0.1 E3:0.2 R:0.1 E3:0.2 R:0.1 E3:0.2")) },
  { id: "warp", group: "フィールド", name: "ワープ", score: se(part("sfxUp", "sine", 0.18, "C4:2"), part("swoosh", "sine", 0.14, "C5:2")) },
  { id: "bump", group: "フィールド", name: "壁にぶつかる", score: se(part("impact", "sine", 0.16, "D3:0.2")) },
  { id: "jump", group: "フィールド", name: "ジャンプ", score: se(part("sfxUp", "square", 0.12, "E4:0.5")) },
  { id: "splash", group: "フィールド", name: "水しぶき", score: se(part("swoosh", "sine", 0.18, "F5:0.8"), part("impact", "sine", 0.1, "R:0.2 A4:0.4")) },
  { id: "alarm", group: "フィールド", name: "警報", score: se(sq(0.14, "A5:0.5 E5:0.5 A5:0.5 E5:0.5 A5:0.5 E5:0.5")) },
  { id: "quake", group: "フィールド", name: "地響き", score: se(part("impact", "sine", 0.3, "D2:2 R:0.3 C2:2")) },
  { id: "mystery", group: "フィールド", name: "不思議な気配", score: se(part("bell", "sine", 0.12, "B5:0.5 F6:2"), part("pad", "sine", 0.1, "E3:4")) },
  // ── 戦闘 ──
  { id: "encounter", group: "戦闘", name: "敵と遭遇", score: se(part("sfxDown", "sawtooth", 0.16, "A5:1.5"), part("impact", "sine", 0.24, "R:1 C3:0.5"), part("swoosh", "sine", 0.14, "C4:1.5")) },
  { id: "battle-start", group: "戦闘", name: "戦闘開始", score: se(part("crash", "sine", 0.16, "C5:0.5"), part("impact", "sine", 0.26, "E3:0.5 R:0.5 A3:0.5")) },
  { id: "attack", group: "戦闘", name: "斬撃", score: se(part("swoosh", "sine", 0.2, "C5:0.4"), part("impact", "sine", 0.24, "R:0.3 G3:0.3")) },
  { id: "hit", group: "戦闘", name: "ダメージ（命中）", score: se(part("impact", "sine", 0.3, "A3:0.4"), part("sfxDown", "square", 0.1, "R:0.05 A4:0.4")) },
  { id: "critical", group: "戦闘", name: "会心の一撃", score: se(part("crash", "sine", 0.2, "C5:0.5"), part("impact", "sine", 0.34, "E3:0.5"), part("sfxUp", "sawtooth", 0.12, "C5:0.3 G5:0.5")) },
  { id: "miss", group: "戦闘", name: "ミス（かわされた）", score: se(part("swoosh", "sine", 0.16, "G5:0.6")) },
  { id: "guard", group: "戦闘", name: "防御", score: se(part("impact", "sine", 0.2, "D4:0.3"), part("chime", "sine", 0.14, "R:0.05 A5:0.4")) },
  { id: "player-damage", group: "戦闘", name: "味方がダメージを受ける", score: se(part("impact", "sine", 0.28, "F3:0.4"), part("sfxDown", "sawtooth", 0.1, "R:0.05 E4:0.6")) },
  { id: "magic-charge", group: "戦闘", name: "魔法の詠唱", score: se(part("sfxUp", "triangle", 0.14, "C4:2.5"), part("swoosh", "sine", 0.1, "E4:2.5")) },
  { id: "fire", group: "戦闘", name: "炎の術", score: se(part("swoosh", "sine", 0.22, "D4:1"), part("impact", "sine", 0.3, "R:0.7 C4:1.3")) },
  { id: "ice", group: "戦闘", name: "氷の術", score: se(part("chime", "sine", 0.18, "E7:0.15 B6:0.15 G7:0.15 D7:0.15 B7:0.8"), part("swoosh", "sine", 0.1, "G6:1.2")) },
  { id: "thunder", group: "戦闘", name: "雷の術", score: se(part("sfxDown", "sawtooth", 0.2, "A6:0.5"), part("impact", "sine", 0.36, "R:0.2 C3:1.5")) },
  { id: "wind", group: "戦闘", name: "風の術", score: se(part("swoosh", "sine", 0.24, "E3:1.8")) },
  { id: "heal", group: "戦闘", name: "回復", score: se(part("chime", "sine", 0.18, "C6:0.3 E6:0.3 G6:0.3 C7:0.3 E7:1"), part("sfxUp", "sine", 0.06, "C5:1.5")) },
  { id: "buff", group: "戦闘", name: "能力アップ", score: se(part("sfxUp", "square", 0.13, "C5:0.5 E5:0.5 G5:0.7")) },
  { id: "debuff", group: "戦闘", name: "能力ダウン", score: se(part("sfxDown", "square", 0.13, "G5:0.5 E5:0.5 C5:0.7")) },
  { id: "poison", group: "戦闘", name: "毒", score: se(part("sfxDown", "sawtooth", 0.14, "E4:0.6 D4:0.6 C4:0.8")) },
  { id: "sleep", group: "戦闘", name: "眠り", score: se(part("bell", "sine", 0.14, "G5:0.6 E5:0.6 C5:1.2")) },
  { id: "status-recover", group: "戦闘", name: "状態異常が治る", score: se(part("chime", "sine", 0.16, "G6:0.3 C7:0.3 E7:0.9")) },
  { id: "revive", group: "戦闘", name: "復活", score: se(part("chime", "sine", 0.18, "C5:0.4 E5:0.4 G5:0.4 C6:0.4 E6:0.4 G6:1.4"), part("sfxUp", "sine", 0.06, "C4:3")) },
  { id: "flee", group: "戦闘", name: "走り去る（逃げる）", score: se(part("impact", "sine", 0.13, "G3:0.5 G3:0.5 G3:0.5 G3:0.5 G3:0.5 G3:0.5 G3:0.5 G3:0.5"), part("swoosh", "sine", 0.16, "C4:4")) },
  { id: "flee-fail", group: "戦闘", name: "逃げられない", score: se(part("impact", "sine", 0.14, "G3:0.5 G3:0.5 G3:0.5"), part("sfxDown", "square", 0.12, "R:1.5 E4:0.8")) },
  { id: "enemy-down", group: "戦闘", name: "敵を倒した", score: se(part("sfxDown", "sawtooth", 0.16, "A4:1.5"), part("impact", "sine", 0.2, "R:0.2 C3:1")) },
  { id: "boss-appear", group: "戦闘", name: "ボス登場", score: se(part("impact", "sine", 0.34, "C2:2 R:0.5 C2:2"), part("swoosh", "sine", 0.16, "C3:3"), part("crash", "sine", 0.18, "R:2.5 C5:1")) },
  { id: "level-up", group: "戦闘", name: "レベルアップ", score: se(sq(0.16, "C5:0.5 E5:0.5 G5:0.5 C6:0.5 R:0.25 G5:0.5 C6:1.5"), tri(0.2, "C4:0.5 E4:0.5 G4:0.5 C5:0.5 R:0.25 E4:0.5 G4:1.5")) },
  { id: "victory", group: "戦闘", name: "勝利のファンファーレ", score: se(sq(0.16, "C5:0.5 C5:0.5 C5:0.5 C5:1 G4:1 A4:1 C5:0.5 A4:0.5 C5:3"), tri(0.2, "C4:0.5 C4:0.5 C4:0.5 C4:1 E3:1 F3:1 F3:0.5 F3:0.5 C4:3")) },
  { id: "defeat", group: "戦闘", name: "全滅", score: se(tri(0.24, "E4:1.5 D4:1.5 C4:1.5 B3:4"), part("sfxDown", "sawtooth", 0.1, "R:1 E3:5")) },
  { id: "exp-gain", group: "戦闘", name: "経験値・お金を得る", score: se(sq(0.13, "E6:0.15 E6:0.15 E6:0.15 E6:0.15 E6:0.15 G6:0.6")) },
];
