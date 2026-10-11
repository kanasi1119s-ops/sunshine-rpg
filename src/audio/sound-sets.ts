// サウンドセット: 「この音で作る」を1つ選ぶだけで、アンプ・パートごとの音量の目安・ミックス・ドラムの設定・使う音源（ベース・ドラム・ギター）をまとめて切りかえる。
// 作り方: 参考にした録音や、人間が「いい」と言った曲を、tools/audio-check/analyze.py・analyze-rhythm.py で測り、その数値（帯域・音量比・左右）から決める。
// 録音の音そのものは取り込まない（数値だけ）。名前はバンド名ではなく、音の特徴にする（CLAUDE.md 1-1）。
import { GENRE_SOUND_SETS } from "./genre-sound-sets";
import type { AmpSetting, Instrument, Score, Track } from "./score";

export interface PartMix {
  /** このパートの音量（0〜1）。曲の全パートの合計が 0.9 をこえないように、書き出しの前にそろえる（内部のリミッターでつぶれて割れるのを避ける）。 */
  volume?: number;
  amp?: AmpSetting;
  bright?: number;
  reverb?: number;
  chorus?: number;
  duck?: number;
  /** 左右の位置。同じ楽器が複数あるときは、元の左右の向きを保って、この大きさ（0〜1）に合わせる。 */
  panWidth?: number;
}
export interface SoundSet {
  id: string;
  label: string;
  /** どんな音か（人間向けの説明）。 */
  description: string;
  /** 元にした録音・曲のメモ（数値の出どころ）。音そのものは入っていない。 */
  source: string;
  /** 使う追加の音源（作曲ソフトの「ベース音源」「ドラム音源」「ギター音源」の id）。 */
  overlays: { bass: string; drums: string; guitar: string };
  tone?: Score["tone"];
  human?: number;
  /** 楽器ごとの設定。書いていない楽器の音量は 0.06 を上限にする。 */
  parts: Partial<Record<Instrument, PartMix>>;
  drumMix?: Score["drumMix"];
  /**
   * 書き出しのWAVの仕上げ。ゲーム中の再生には効かない。lufs＝大きさ、widen＝広がり、
   * preset＝仕上げのプリセット（--master-preset と同じ。tools/composer/master.mjs）、space・spaceWet＝共通の部屋（--space・--space-wet と同じ）。
   * 書き出しの引数を別に書けば、そちらが優先。
   */
  master?: { lufs: number; widen?: number; preset?: string; space?: "hall" | "room" | "plate"; spaceWet?: number };
  /** 目安のテンポ（BPM）。自動では変えない。 */
  tempoHint?: [number, number];
  /** 打ち込みの型の例（16分の格子。ドラムのパートに書く）。 */
  drumPatterns?: Record<string, string>;
}

export const SOUND_SETS: Record<string, SoundSet> = {
  "punk-run": {
    id: "punk-run",
    label: "疾走パンク（2ビート・ギター前）",
    description: "歪みギターを左右に振って前に出し、ベースとキックは控えめ。ドラムは2ビート（キックが表・スネアが裏）。メロディは生ギターのクリーン。",
    source: "参考録音5曲の楽器ごとの分析（analyze-stems.py：音量比・帯域・重心・左右の広がり。docs/sound/punk-guide.md §9）と、見本曲の調整（2026-10-11。見本曲は採用せず削除）。数字だけを使い、音は取り込んでいない",
    overlays: { bass: "pick", drums: "rock", guitar: "gretsch" },
    tone: "rock",
    human: 0.4,
    parts: {
      kick: { volume: 0.03 }, snare: { volume: 0.054 }, hihat: { volume: 0.045 }, crash: { volume: 0.055 }, tom: { volume: 0.033 },
      bass: { volume: 0.026, bright: 0.5, duck: 0.15 },
      distGuitar: { volume: 0.12, amp: { type: "punk" }, panWidth: 0.55 },
      crunch: { volume: 0.12, amp: { type: "punk" }, panWidth: 0.55 },
      leadGuitar: { volume: 0.09, amp: { type: "clean" }, reverb: 0.2 },
      echoGuitar: { volume: 0.06, amp: { type: "clean" }, reverb: 0.2, chorus: 0 },
    },
    drumMix: { hat: { level: 1.05, pan: -0.3, reverb: 0.05 }, snare: { level: 1.15, reverb: 0.15 }, tom: { spread: 0.6, reverb: 0.12, tune: -3 }, crash: { level: 1.0, pan: 0.3, reverb: 0.25 } },
    master: { lufs: -10 },
    tempoHint: [160, 210],
    drumPatterns: {
      "2beat-kick": "x...x...x...x...", "2beat-kick-b": "x...x...x..xx...", "2beat-snare": "..x...x...x...x.", "2beat-hat": "x.X.x.X.x.X.x.X.",
      "halftime-kick": "x.......x.......", "halftime-snare": "........x.......",
    },
  },
  "clear-guitar-rock": {
    id: "clear-guitar-rock",
    label: "透明感ギターロック（生ギター・自然な余韻）",
    description: "生ギターの自然な減り方を聴かせる。ビブラートや sustain で無理に鳴りを作らない。アコースティックはナイロン弦。タムは低め、クラッシュは余韻長め。",
    source: "人間が「いい」と言った通し（band-pedal-arpeggio）の設定（2026-10-11）。音は取り込んでいない",
    overlays: { bass: "finger", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    human: 0.45,
    parts: {
      kick: { volume: 0.09 }, snare: { volume: 0.065 }, hihat: { volume: 0.03 }, crash: { volume: 0.032 }, tom: { volume: 0.05 },
      bass: { volume: 0.095, bright: 0.2, duck: 0.2 },
      guitar: { volume: 0.2, amp: { type: "clean" }, chorus: 0, reverb: 0.15, panWidth: 0.5 },
      echoGuitar: { volume: 0.095, amp: { type: "clean" }, reverb: 0.2, chorus: 0, panWidth: 0.55 },
      leadGuitar: { volume: 0.09, amp: { type: "clean" }, reverb: 0.25 },
      bell: { volume: 0.05, reverb: 0.4 }, harp: { volume: 0.055, reverb: 0.4 }, strings: { volume: 0.06, reverb: 0.5 },
    },
    drumMix: { hat: { level: 0.62, pan: -0.35, reverb: 0.08 }, snare: { reverb: 0.2 }, tom: { spread: 0.7, reverb: 0.15, level: 0.9, tune: -4.5 }, crash: { level: 0.85, pan: 0.35, reverb: 0.25 } },
    tempoHint: [120, 160],
  },
  // ── ここから mix-patterns.md の型（M17〜M50 から代表）。数字は同書のもの。書き出しの引数も一緒に持つ ──
  "rock-4": {
    id: "rock-4",
    label: "ロックバンド（4人・ギター2本を左右）",
    description: "ドラム・ベース・ギター2本（左右）・リード。リズムギターは左右に開き、リードは中央で少し奥。低域は中央。",
    source: "docs/sound/mix-patterns.md M17（記事の方針をうちの道具に読み替えた推定。clear-guitar-rock の目盛り）",
    overlays: { bass: "rock", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    parts: {
      kick: { volume: 0.09 }, snare: { volume: 0.065, reverb: 0.15 }, hihat: { volume: 0.03 }, crash: { volume: 0.032 }, tom: { volume: 0.05 },
      bass: { volume: 0.09, bright: 0.2, duck: 0.25 },
      crunch: { volume: 0.13, panWidth: 0.8, reverb: 0.1, bright: -0.1 }, distGuitar: { volume: 0.13, panWidth: 0.8, reverb: 0.1, bright: -0.1 },
      leadGuitar: { volume: 0.1, reverb: 0.2 },
    },
    drumMix: { hat: { level: 0.7, pan: -0.3, reverb: 0.08 }, snare: { reverb: 0.15 }, tom: { spread: 0.6, reverb: 0.12 }, crash: { level: 0.9, pan: 0.3, reverb: 0.2 } },
    master: { lufs: -10, widen: 1.4, preset: "rock-clean", space: "room", spaceWet: 0.12 },
    tempoHint: [110, 170],
  },
  "pop-lead": {
    id: "pop-lead",
    label: "ポップ（リード＝歌が主役）",
    description: "リードを一番前に。伴奏は歌の席（1〜4kHz）を空けるため少し暗く、ドラムは小さめ。プレートの共通残響。",
    source: "docs/sound/mix-patterns.md M23（推定）",
    overlays: { bass: "finger", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    parts: {
      leadGuitar: { volume: 0.12, reverb: 0.2, chorus: 0.1 }, lead: { volume: 0.12, reverb: 0.2 },
      piano: { volume: 0.1, panWidth: 0.3, reverb: 0.2, bright: -0.1 }, guitar: { volume: 0.14, panWidth: 0.4, reverb: 0.15, bright: -0.1 },
      strings: { volume: 0.05, panWidth: 0.3, reverb: 0.35, bright: -0.1 }, bell: { volume: 0.04, panWidth: 0.5, reverb: 0.4 },
      bass: { volume: 0.085, duck: 0.25 }, kick: { volume: 0.08 }, snare: { volume: 0.06, reverb: 0.2 }, hihat: { volume: 0.028 }, crash: { volume: 0.03 },
    },
    drumMix: { hat: { level: 0.6, pan: 0.3, reverb: 0.08 }, snare: { reverb: 0.2 }, tom: { spread: 0.5 }, crash: { level: 0.8, pan: -0.3 } },
    master: { lufs: -11, widen: 1.5, preset: "pop", space: "plate", spaceWet: 0.12 },
    tempoHint: [90, 150],
  },
  "jpop-bright": {
    id: "jpop-bright",
    label: "J-POP／アニソン（明るく・歌が最大）",
    description: "リードが最大で、サビで全員が上がる。ストリングスは高い音域で歌の隙間を埋める。明るめで広い。",
    source: "docs/sound/mix-patterns.md M24（数値の載る記事が無く推定が多い）",
    overlays: { bass: "jpop", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    parts: {
      leadGuitar: { volume: 0.12, reverb: 0.22, bright: 0.1 }, lead: { volume: 0.12, reverb: 0.22 },
      guitar: { volume: 0.12, panWidth: 0.5, reverb: 0.15 }, crunch: { volume: 0.09, panWidth: 0.7, reverb: 0.1 },
      strings: { volume: 0.05, panWidth: 0.3, reverb: 0.4 }, piano: { volume: 0.07, panWidth: 0.3, reverb: 0.25 },
      bass: { volume: 0.085, bright: 0.25, duck: 0.2 }, kick: { volume: 0.08 }, snare: { volume: 0.06, reverb: 0.2 }, hihat: { volume: 0.028 }, crash: { volume: 0.03 }, tom: { volume: 0.04 },
      bell: { volume: 0.04, panWidth: 0.6, reverb: 0.35 },
    },
    drumMix: { hat: { level: 0.65, pan: -0.3 }, snare: { reverb: 0.2 }, crash: { level: 0.85, pan: 0.3, reverb: 0.2 } },
    master: { lufs: -10, widen: 1.6, preset: "pop", space: "plate", spaceWet: 0.14 },
    tempoHint: [120, 190],
  },
  "ballad-piano-strings": {
    id: "ballad-piano-strings",
    label: "バラード（ピアノ＋弦）",
    description: "ピアノが主役、弦は右奥。ドラムは極小。曲には dynamics:\"natural\" をつけて起伏を残す。ホールの残響。",
    source: "docs/sound/mix-patterns.md M26（推定）",
    overlays: { bass: "finger", drums: "jazz", guitar: "gretsch" },
    tone: "rock",
    parts: {
      piano: { volume: 0.16, panWidth: 0.2, reverb: 0.25, bright: -0.1 }, strings: { volume: 0.08, panWidth: 0.3, reverb: 0.45, bright: -0.2, chorus: 0.2, duck: 0.25 },
      leadGuitar: { volume: 0.09, reverb: 0.25 }, bass: { volume: 0.06, bright: -0.1, duck: 0.1 },
      kick: { volume: 0.05, reverb: 0.2 }, snare: { volume: 0.03, reverb: 0.3 }, hihat: { volume: 0.012 },
    },
    drumMix: { kick: { level: 0.7 }, snare: { level: 0.7, reverb: 0.3 }, hat: { level: 0.45, reverb: 0.1 } },
    master: { lufs: -15, widen: 1.2, preset: "solo", space: "hall", spaceWet: 0.2 },
    tempoHint: [60, 90],
  },
  "jazz-trio": {
    id: "jazz-trio",
    label: "ジャズトリオ（ピアノ・ベース・ドラム）",
    description: "ピアノを左、ベースをわずかに右。圧縮はごく軽く、残響は短い部屋。ドラムは小さく、ライドを控えめに。",
    source: "docs/sound/mix-patterns.md M27（推定）",
    overlays: { bass: "jazz", drums: "jazz", guitar: "hofner" },
    tone: "rock",
    parts: {
      piano: { volume: 0.16, panWidth: 0.3, reverb: 0.12 }, bass: { volume: 0.13, bright: -0.1, reverb: 0.04 },
      kick: { volume: 0.05 }, snare: { volume: 0.04, reverb: 0.1 }, hihat: { volume: 0.025, panWidth: 0.2 }, crash: { volume: 0.02, panWidth: 0.3, reverb: 0.15 },
    },
    drumMix: { kick: { level: 0.7 }, snare: { level: 0.8, reverb: 0.1 }, hat: { level: 0.6, pan: -0.25 }, crash: { level: 0.7, pan: 0.3, reverb: 0.15 }, tom: { spread: 0.7 } },
    master: { lufs: -16, preset: "jazz", space: "room", spaceWet: 0.15 },
    tempoHint: [90, 220],
  },
  "funk-bass": {
    id: "funk-bass",
    label: "ファンク（ベースが主役）",
    description: "ベースがキックより大きい主役。ギターは細かい16分で高域、鍵盤とブラスは右寄り。",
    source: "docs/sound/mix-patterns.md M29（推定）",
    overlays: { bass: "finger", drums: "muldjord", guitar: "std" },
    tone: "rock",
    parts: {
      bass: { volume: 0.13, bright: 0.3, duck: 0.15 }, guitar: { volume: 0.12, panWidth: 0.6, bright: 0.2, reverb: 0.05 },
      keys: { volume: 0.09, panWidth: 0.5 }, brass: { volume: 0.09, panWidth: 0.2, reverb: 0.1 },
      kick: { volume: 0.085 }, snare: { volume: 0.07, reverb: 0.1 }, hihat: { volume: 0.035, panWidth: 0.3 },
    },
    drumMix: { kick: { level: 1.0 }, snare: { level: 1.05, reverb: 0.1 }, hat: { level: 0.75, pan: -0.3 }, tom: { spread: 0.5 } },
    master: { lufs: -11, widen: 1.2, preset: "pop" },
    tempoHint: [95, 125],
  },
  "house-duck": {
    id: "house-duck",
    label: "ハウス（キックでパッドが凹む）",
    description: "キックが低域を取り、ベースは100Hz以上で性格を出す。パッドとキーは duck で呼吸する。明るく広い。",
    source: "docs/sound/mix-patterns.md M33（推定）",
    overlays: { bass: "std", drums: "std", guitar: "std" },
    tone: "rock",
    parts: {
      kick: { volume: 0.1, bright: 0.2 }, bass: { volume: 0.08, duck: 0.4, bright: 0.15 }, snare: { volume: 0.06, reverb: 0.18 }, hihat: { volume: 0.028, panWidth: 0.3 }, crash: { volume: 0.02, panWidth: 0.3, reverb: 0.15 },
      pad: { volume: 0.05, panWidth: 0.3, chorus: 0.4, duck: 0.4, reverb: 0.35, bright: -0.2 }, keys: { volume: 0.07, panWidth: 0.4, duck: 0.3 }, lead: { volume: 0.07, panWidth: 0.2, reverb: 0.2 },
    },
    drumMix: { kick: { level: 1.2 }, snare: { level: 0.8, reverb: 0.18 }, hat: { level: 0.6, pan: 0.3 } },
    master: { lufs: -9, widen: 1.6, preset: "edm", space: "plate", spaceWet: 0.1 },
    tempoHint: [118, 130],
  },
  "ambient-wide": {
    id: "ambient-wide",
    label: "アンビエント（広い・静か）",
    description: "2つのパッドを左右反対に。低域を空け、残響を多めに。ドラムなし。起伏は音のオン・オフで作る。",
    source: "docs/sound/mix-patterns.md M38（推定）",
    overlays: { bass: "std", drums: "std", guitar: "std" },
    tone: "rock",
    parts: {
      pad: { volume: 0.09, panWidth: 0.4, chorus: 0.35, reverb: 0.55, bright: -0.2 }, strings: { volume: 0.06, reverb: 0.5 },
      bell: { volume: 0.04, panWidth: 0.5, reverb: 0.6 }, leadGuitar: { volume: 0.05, reverb: 0.5 }, bass: { volume: 0.06, bright: -0.2 },
    },
    master: { lufs: -18, widen: 1.8, preset: "ambient", space: "hall", spaceWet: 0.3 },
    tempoHint: [50, 90],
  },
  "orchestra-depth": {
    id: "orchestra-depth",
    label: "オーケストラ（手前から奥へ）",
    description: "弦が手前（残響少なめ）、管がその後ろ、打楽器が最後方。弦を左右に分ける。ホールの共通残響。",
    source: "docs/sound/mix-patterns.md M39（推定）",
    overlays: { bass: "std", drums: "std", guitar: "std" },
    tone: "rock",
    parts: {
      strings: { volume: 0.08, panWidth: 0.4, reverb: 0.25 }, bass: { volume: 0.07, bright: -0.2, reverb: 0.2 }, brass: { volume: 0.09, panWidth: 0.2, reverb: 0.4, bright: -0.1 },
      choir: { volume: 0.07, reverb: 0.4 }, harp: { volume: 0.05, panWidth: 0.5, reverb: 0.35 }, tom: { volume: 0.05, reverb: 0.5, bright: -0.1 }, kick: { volume: 0.05, reverb: 0.45 },
    },
    drumMix: { kick: { level: 0.8, reverb: 0.45 }, tom: { spread: 0.7, reverb: 0.4, level: 0.9 }, crash: { level: 0.7, reverb: 0.4 } },
    master: { lufs: -16, widen: 1.3, preset: "orch", space: "hall", spaceWet: 0.22 },
    tempoHint: [60, 140],
  },
  "game-battle": {
    id: "game-battle",
    label: "ゲーム：戦闘",
    description: "ドラムとベースが核、ギターは左右。効果音（1〜4kHz）の席を空けるためギターを少し暗く。仕上げは戦闘用（低域だけ圧縮・-14.5LUFS）。",
    source: "docs/sound/mix-patterns.md M45 と mastering-guide §3-1 #13",
    overlays: { bass: "rock", drums: "supra", guitar: "std" },
    tone: "rock",
    parts: {
      kick: { volume: 0.09 }, snare: { volume: 0.075, reverb: 0.12 }, hihat: { volume: 0.035 }, crash: { volume: 0.035 }, tom: { volume: 0.055 },
      bass: { volume: 0.09, bright: 0.3, duck: 0.3 }, distGuitar: { volume: 0.11, panWidth: 0.75, bright: -0.1 }, crunch: { volume: 0.11, panWidth: 0.75, bright: -0.1 },
      leadGuitar: { volume: 0.1, reverb: 0.15 }, strings: { volume: 0.06, reverb: 0.25 },
    },
    drumMix: { kick: { level: 1.1 }, snare: { level: 1.1, reverb: 0.12 }, hat: { level: 0.7, pan: -0.3 }, crash: { level: 0.85, pan: 0.3, reverb: 0.2 }, tom: { spread: 0.6 } },
    master: { lufs: -14.5, widen: 1.2, preset: "game-battle", space: "room", spaceWet: 0.1 },
    tempoHint: [140, 190],
  },
  "game-boss": {
    id: "game-boss",
    label: "ゲーム：ボス戦",
    description: "戦闘より一段厚い。ブラスと合唱は同じ席（500〜2kHz）なので片方を休符で抜く。ホールを少し。",
    source: "docs/sound/mix-patterns.md M46 と mastering-guide §3-1 #14",
    overlays: { bass: "rock", drums: "supra", guitar: "std" },
    tone: "rock",
    parts: {
      kick: { volume: 0.1, bright: 0.2 }, snare: { volume: 0.075, reverb: 0.15 }, tom: { volume: 0.07, reverb: 0.2 }, crash: { volume: 0.035 },
      bass: { volume: 0.1, bright: 0.3, duck: 0.3 }, distGuitar: { volume: 0.11, panWidth: 0.8 }, crunch: { volume: 0.11, panWidth: 0.8 },
      brass: { volume: 0.09, panWidth: 0.2, reverb: 0.25 }, choir: { volume: 0.06, reverb: 0.4 }, strings: { volume: 0.06, reverb: 0.3 },
    },
    drumMix: { kick: { level: 1.15 }, snare: { level: 1.1, reverb: 0.15 }, tom: { spread: 0.6, reverb: 0.2 }, crash: { level: 0.85, pan: 0.3, reverb: 0.25 } },
    master: { lufs: -14.5, widen: 1.4, preset: "game-boss", space: "hall", spaceWet: 0.1 },
    tempoHint: [120, 180],
  },
  "game-town": {
    id: "game-town",
    label: "ゲーム：町",
    description: "生ギターが主役で、低い楽器は少なめ。人の声（会話・市場の効果音）が重なるので1〜4kHzを控えめに。",
    source: "docs/sound/mix-patterns.md M47 と mastering-guide §3-1 #12",
    overlays: { bass: "finger", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    parts: {
      guitar: { volume: 0.18, panWidth: 0.35, reverb: 0.15 }, lead: { volume: 0.1, reverb: 0.25 }, leadGuitar: { volume: 0.1, reverb: 0.25 },
      harp: { volume: 0.07, panWidth: 0.4, reverb: 0.3 }, strings: { volume: 0.04, reverb: 0.4 }, bass: { volume: 0.06, duck: 0.1 }, kick: { volume: 0.03 }, hihat: { volume: 0.012, panWidth: 0.3 },
    },
    drumMix: { kick: { level: 0.6 }, hat: { level: 0.4, pan: 0.3 } },
    master: { lufs: -16.5, widen: 1.2, preset: "game-field", space: "room", spaceWet: 0.15 },
    tempoHint: [80, 130],
  },
  "game-dungeon": {
    id: "game-dungeon",
    label: "ゲーム：ダンジョン",
    description: "暗いパッドと弦、疎らなベル。足音や水滴の効果音が聞こえるよう2〜4kHzを空ける。広いホールで静かに。",
    source: "docs/sound/mix-patterns.md M48 と mastering-guide §3-1 #15",
    overlays: { bass: "std", drums: "std", guitar: "std" },
    tone: "rock",
    parts: {
      pad: { volume: 0.09, panWidth: 0.3, bright: -0.35, reverb: 0.5, chorus: 0.1 }, strings: { volume: 0.07, panWidth: 0.3, bright: -0.3, reverb: 0.5 },
      bass: { volume: 0.08, bright: -0.2 }, bell: { volume: 0.035, panWidth: 0.6, reverb: 0.6 }, tom: { volume: 0.05, reverb: 0.5, bright: -0.2 }, wind: { volume: 0.03, reverb: 0.4 },
    },
    drumMix: { tom: { spread: 0.6, reverb: 0.5 }, kick: { level: 0.6, reverb: 0.5 } },
    master: { lufs: -18, widen: 1.4, preset: "game-dungeon", space: "hall", spaceWet: 0.3 },
    tempoHint: [50, 100],
  },
};

Object.assign(SOUND_SETS, GENRE_SOUND_SETS);
export const SOUND_SET_IDS = Object.keys(SOUND_SETS);

/**
 * 曲にサウンドセットを当てはめる（元の曲は変えず、新しい曲を返す）。何度当てても同じ結果になる（音量は目標の値に置きかえる）。
 * 音量: セットに書かれた楽器は目標の音量に、書かれていない楽器は 0.06 を上限に。最後に、合計が 0.9 をこえたら全体を同じ比率で下げる。
 */
export function applySoundSet(score: Score, set: SoundSet): Score {
  const tracks: Track[] = score.tracks.map((t) => {
    const inst = t.instrument;
    const mix = inst ? set.parts[inst] : undefined;
    if (!mix) return { ...t, volume: Math.min(t.volume, 0.06) };
    const next: Track = { ...t, volume: mix.volume ?? t.volume };
    if (mix.amp) next.amp = { ...mix.amp };
    if (mix.bright !== undefined) next.bright = mix.bright;
    if (mix.reverb !== undefined) next.reverb = mix.reverb;
    if (mix.chorus !== undefined) next.chorus = mix.chorus;
    if (mix.duck !== undefined) next.duck = mix.duck;
    if (mix.panWidth !== undefined && t.pan !== undefined && t.pan !== 0) next.pan = Math.sign(t.pan) * mix.panWidth;
    return next;
  });
  const sum = tracks.reduce((a, t) => a + t.volume, 0);
  if (sum > 0.9) for (const t of tracks) t.volume = Math.round((t.volume * 0.9) / sum * 10000) / 10000;
  const out: Score = { ...score, tracks };
  if (set.tone) out.tone = set.tone;
  if (set.human !== undefined) out.human = set.human;
  if (set.drumMix) out.drumMix = { ...(score.drumMix ?? {}), ...set.drumMix };
  return out;
}

/**
 * 場面（フィールド・戦闘・ボス・町・ダンジョン・タイトル）から、サウンドセットと書き出しのプリセットを選ぶ表。
 * 作曲ソフトで場面を選ぶと、パートの初期値（セット）と書き出しの引数（プリセット）が入る、という使い方（mix-patterns 提案 12）。
 */
export const SCENE_SETS: Record<string, { sound: string; preset: string; label: string }> = {
  field: { sound: "game-town", preset: "game-field", label: "フィールド（探索）" },
  town: { sound: "game-town", preset: "game-field", label: "町" },
  battle: { sound: "game-battle", preset: "game-battle", label: "戦闘" },
  boss: { sound: "game-boss", preset: "game-boss", label: "ボス戦" },
  dungeon: { sound: "game-dungeon", preset: "game-dungeon", label: "ダンジョン" },
  title: { sound: "orchestra-depth", preset: "game-boss", label: "タイトル画面" },
};

/**
 * 音づくりの型（sound-design-basics 提案 8）。パートの PartMix を、役割の名前で選ぶ。名前は音の特徴にしてある。
 * 使うとき: `{ ...track, ...PART_RECIPES["soft-pad"].mix }` のように、volume・reverb・bright などを当てる。
 */
export const PART_RECIPES: Record<string, { label: string; instruments: Instrument[]; mix: PartMix }> = {
  "soft-pad": { label: "やわらかい弦パッド（遅い立ち上がり・広い・凹む）", instruments: ["strings", "pad", "choir"], mix: { volume: 0.06, reverb: 0.5, bright: -0.25, chorus: 0.2, duck: 0.25, panWidth: 0.4 } },
  "pluck-arp": { label: "プラックのアルペジオ（明るく短い・左右に）", instruments: ["harp", "guitar", "keys", "piano"], mix: { volume: 0.07, reverb: 0.3, bright: 0, duck: 0, panWidth: 0.5 } },
  "bell-accent": { label: "ベル系の飾り（小さく・遠く・暗め）", instruments: ["bell", "chime"], mix: { volume: 0.04, reverb: 0.6, bright: -0.3, panWidth: 0.5 } },
};

/**
 * 1〜4kHz を担うパート（リード・ギター・ベルなど）を db だけ下げ、ほかの伴奏を少し暗くする（ゲーム用の席空け）。元の曲は変えない。
 * 実体は mix-tools.ts の applyGameDuck。ここは「サウンドセットをゲーム版にする」入り口。
 */
export { applyGameDuck } from "./mix-tools";
