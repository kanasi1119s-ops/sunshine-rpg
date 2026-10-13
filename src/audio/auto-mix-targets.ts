/**
 * 自動ミックスの目標値（2026-10-14）。調整しやすいよう、数字はすべてこのファイルに集める（実装側には数字を書かない）。
 * 各値に出典の印を付ける:
 *   【出】… 実際の録音の測定、または公開の記事の数字を、そのまま（または単純に計算して）使ったもの
 *   【推】… 出典がない部分を、近い資料の数字から決めた出発点。耳で確かめて変えてよい
 * 出典の一覧と、数字の導き方は docs/sound/band-ensemble/auto-mix.md。
 * 「ラウドネス」は、鳴っている間の力（左右の平均の RMS、dB）を リード = 0 として比べた値。
 */
import type { BandId } from "./auto-mix";

export type MixRole =
  | "lead" | "leadDouble" | "counter"
  | "kick" | "snare" | "hihat" | "cymbal" | "tom"
  | "bass" | "guitarRhythm" | "guitarClean" | "keys" | "strings" | "brass" | "other";

export type MixGroup = "lead" | "double" | "counter" | "drums" | "bass" | "guitar" | "keys" | "strings" | "brass" | "other";

export const GROUP_LABEL: Record<MixGroup, string> = {
  lead: "リード", double: "リードの重ね", counter: "合いの手・対旋律", drums: "ドラム全体", bass: "ベース", guitar: "ギター全体", keys: "鍵盤", strings: "弦・パッド", brass: "ブラス（伴奏）", other: "その他",
};

/** グループ全体の、リード = 0 としたときの大きさ（dB）と、許す幅。 */
export const GROUP_TARGETS: Record<MixGroup, { relDb: number; tolDb: number; source: string }> = {
  lead: { relDb: 0, tolDb: 0, source: "基準" },
  double: { relDb: -4, tolDb: 3.5, source: "【推】リードと同じ旋律を重ねるパート（ソロの重ね等）は、リードより 4dB 下（重ねは足し算で聞こえるので）" },
  counter: { relDb: -5, tolDb: 3.5, source: "【推】合いの手・対旋律はリードより 4〜6dB 下（mix-patterns.md §5 の「リード = 1」に対する脇役の比）" },
  drums: { relDb: -0.8, tolDb: 3, source: "【出】punk-guide.md §9: 録音5曲を Demucs で分けた share_dB の平均 ドラム −6.9 − ボーカル −6.1" },
  bass: { relDb: -1.1, tolDb: 3, source: "【出】同上: ベース −7.2 − ボーカル −6.1（範囲 −5.8〜−8.6）" },
  guitar: { relDb: -2.2, tolDb: 3, source: "【出】同上: ギター −8.3 − ボーカル −6.1（範囲 −7.8〜−8.8）。歌のない曲では「歌」をリード楽器に読みかえる【推】" },
  keys: { relDb: -3, tolDb: 3.5, source: "【推】mix-patterns.md §5 ロック5人 M18 の鍵盤 0.7（= −3dB）。volume の比なので出発点" },
  strings: { relDb: -6, tolDb: 4, source: "【推】mix-patterns.md §5 ポップ M23 の弦/パッド 0.42（−7.5dB）とバラード 0.89（−1dB）の間" },
  brass: { relDb: -4, tolDb: 3.5, source: "【推】mix-patterns.md §5 ファンク M29 の brass 0.69（−3dB）。伴奏のブラスとして" },
  other: { relDb: -6, tolDb: 4, source: "【推】役割が決まらないパートは、リードより 6dB 下" },
};

export interface RoleSpec {
  label: string;
  group: MixGroup;
  /** グループの中での、他の役割との差（dB。グループ内の基準 = 0）。同じ役割が複数あれば、力を等分する。 */
  withinDb: number;
  source: string;
  /** パンの目安: center = 中央（|pan| ≤ centerMax）、spread = 同じ役割が 2 つ以上なら左右に（|pan| ≥ spreadMin） */
  pan?: "center" | "spread" | "free";
  /** 聞こえやすさ（他のパート全部に対する差）を見る帯域と、許す最低値（中央値、dB） */
  clarity?: { bands: BandId[]; minMedianDb: number };
  /** 低域（Sub+Bass）が要らない役割: 自分の力のうち Sub+Bass がこれより多ければ HPF を提案する（dB、自分の全体を 0 として）。hpfHz は提案するカット周波数 */
  lowCut?: { maxLowShareDb: number; hpfHz: number; source: string };
  /** 濁り（200-500Hz）の削りの候補になる優先度（大きいほど先に削る。0 = 削らない） */
  mudCutPriority: number;
  /** 削るときの中心周波数 */
  mudCutHz?: number;
  /** 音量の調整のしかた: drum = volume（ドラムは gainDb が効かない）、gain = gainDb（音色を変えずに音量だけ動かす） */
  levelBy: "volume" | "gain";
}

export const ROLE_SPECS: Record<MixRole, RoleSpec> = {
  lead: { label: "リード", group: "lead", withinDb: 0, source: "基準", pan: "center", clarity: { bands: ["mid", "presence"], minMedianDb: -3 }, lowCut: { maxLowShareDb: -20, hpfHz: 100, source: "【出】rock-metal.md §3.1: リードギターは 100Hz 以下カット" }, mudCutPriority: 1, mudCutHz: 320, levelBy: "gain" },
  leadDouble: { label: "リードの重ね（ソロの同じ旋律など）", group: "double", withinDb: 0, source: "【推】リードと同じ旋律を重ねるパートは、リードより 4dB 下", pan: "free", lowCut: { maxLowShareDb: -20, hpfHz: 100, source: "【推】リードと同じ" }, mudCutPriority: 1, mudCutHz: 320, levelBy: "gain" },
  counter: { label: "合いの手・対旋律", group: "counter", withinDb: 0, source: "【推】対旋律・合いの手はリードより 4〜6dB 下", pan: "free", lowCut: { maxLowShareDb: -18, hpfHz: 100, source: "【推】" }, mudCutPriority: 1, mudCutHz: 320, levelBy: "gain" },
  kick: { label: "キック", group: "drums", withinDb: 0, source: "【出】Point Prime「Volume Balancing Cheat Sheet」(fundamentals.md 出49): キックを基準にする", pan: "center", clarity: { bands: ["sub", "bass"], minMedianDb: -6 }, mudCutPriority: 2, mudCutHz: 300, levelBy: "volume" },
  snare: { label: "スネア", group: "drums", withinDb: -1.5, source: "【出】同上: キックの −1〜−2dB", pan: "center", mudCutPriority: 2, mudCutHz: 400, levelBy: "volume" },
  tom: { label: "タム", group: "drums", withinDb: -4, source: "【推】mix-patterns.md M17: タム 0.5／キック 0.9（−5dB）", pan: "free", lowCut: { maxLowShareDb: -10, hpfHz: 60, source: "【出】rock-metal.md §3.1: タムは 60Hz 以下カット" }, mudCutPriority: 0, levelBy: "volume" },
  hihat: { label: "ハイハット", group: "drums", withinDb: -9, source: "【出】Point Prime: ハイハットはキックの −8〜−10dB", pan: "free", lowCut: { maxLowShareDb: -25, hpfHz: 250, source: "【出】rock-metal.md §3.1: ハイハット・シンバルは 200〜500Hz 以下をカット" }, mudCutPriority: 0, levelBy: "volume" },
  cymbal: { label: "シンバル（クラッシュ・ライド）", group: "drums", withinDb: -9, source: "【推】mixing-guide.md §ドラム慣例値: オープンハット・ライド −12〜−16dB（キック = 0）、クラッシュは打点で大きいので −9", pan: "free", lowCut: { maxLowShareDb: -25, hpfHz: 250, source: "【出】rock-metal.md §3.1" }, mudCutPriority: 0, levelBy: "volume" },
  bass: { label: "ベース", group: "bass", withinDb: 0, source: "【出】punk-guide.md §9 の録音（ベースはほぼ Bass 帯域だけ）", pan: "center", clarity: { bands: ["bass", "lowmid"], minMedianDb: -4 }, mudCutPriority: 2, mudCutHz: 220, levelBy: "gain" },
  guitarRhythm: { label: "リズムギター（歪み・刻み）", group: "guitar", withinDb: 0, source: "【出】punk-guide.md §9: ギターは左右に広く（広がり 0.74〜1.09）、1〜4kHz が主", pan: "spread", lowCut: { maxLowShareDb: -14, hpfHz: 100, source: "【出】rock-metal.md §3.1: リズムギターの HPF 80〜100Hz（標準 E）。アンプが既に切っている分は測定で見分ける" }, mudCutPriority: 3, mudCutHz: 350, levelBy: "gain" },
  guitarClean: { label: "クリーンギター（きらめき・アルペジオ）", group: "guitar", withinDb: -6, source: "【推】歪みのリズムギターの 6dB 下（M17 の craft: 主役のリズムを邪魔しない）", pan: "free", lowCut: { maxLowShareDb: -16, hpfHz: 120, source: "【推】jpop-clean-guitar-guide.md: クリーンは 100Hz 以下を切る" }, mudCutPriority: 2, mudCutHz: 350, levelBy: "gain" },
  keys: { label: "ピアノ・鍵盤", group: "keys", withinDb: 0, source: "【推】M18", pan: "free", lowCut: { maxLowShareDb: -12, hpfHz: 80, source: "【推】fundamentals.md: 鍵盤の左手はベースと席を分ける" }, mudCutPriority: 2, mudCutHz: 300, levelBy: "gain" },
  strings: { label: "弦・パッド", group: "strings", withinDb: 0, source: "【推】", pan: "free", lowCut: { maxLowShareDb: -12, hpfHz: 200, source: "【出】mixing-guide.md §パッド: 200〜300Hz でハイパス" }, mudCutPriority: 2, mudCutHz: 300, levelBy: "gain" },
  brass: { label: "ブラス（伴奏）", group: "brass", withinDb: 0, source: "【推】", pan: "free", lowCut: { maxLowShareDb: -14, hpfHz: 100, source: "【推】" }, mudCutPriority: 1, mudCutHz: 320, levelBy: "gain" },
  other: { label: "その他", group: "other", withinDb: 0, source: "【推】", pan: "free", mudCutPriority: 0, levelBy: "gain" },
};

/** 調整の決まり。 */
export const MIX_RULES = {
  /** この dB より差が小さければ動かさない */
  deadbandDb: 2,
  /** 1 回の反復で動かす最大（dB） */
  maxStepDb: 6,
  /** 目標との差のうち、1 回で動かす割合（行き過ぎ防止。--loop で収束させる） */
  damping: 0.8,
  /** gainDb の範囲（ai-song.ts の仕様） */
  gainDbRange: [-12, 18] as [number, number],
  /** ドラムなど volume で動かすときの範囲（ai-song.ts: 0.02〜0.5） */
  volumeRange: [0.02, 0.5] as [number, number],
  /**
   * volume を 1 倍→r 倍にしたときの大きさの変化 ≈ 40·log10(r) dB。
   * SoundFont の velocity→減衰の決まり（2 乗則）から。録音音源の標準。実測で合わないときはここを変える。
   */
  volumeDbPerDecade: 40,
  /** EQ の削りの合計上限（dB）。mixing-guide.md: 減算は合計 3dB 程度まで */
  eqCutLimitDb: 3,
  /** 濁り（200-500Hz の割合）の目標（全体に対する dB）。mix-targets の lowmid 250-1k を ≈-6〜-5dB とし、250-500 はその約半分（1 オクターブ中の 1 オクターブ）なので -9 を出発点にした【推】 */
  mudShareTargetDb: -9,
  /** 濁りの削りを提案する超過量（dB）。これ未満なら削らない */
  mudExcessActDb: 1.5,
  /** ぐじゃぐじゃ指数の判定（推）。0〜25 すっきり／25〜50 やや混む／50 以上 混んでいる */
  messWarn: 25,
  messBad: 50,
  /** キック・ベースの重なりがこの % 以上なら、ベースに duck を提案する */
  kickBassClosePct: 40,
  /** 中域（500-2k）が混んでいる（3 パート以上が同じ強さ）窓の割合がこれ以上なら警告 */
  midCrowdWarnPct: 35,
  /** 左右バランスのずれ（dB）がこれを超えたら警告（全体） */
  balanceWarnDb: 1.5,
  /** 低域の左右の相関がこれ未満なら警告（モノで低音が痩せる）。analyze.py --mono-low と同じ 0.9 */
  lowCorrWarn: 0.9,
};

/** 全体の仕上げ（マスター）の目標。ジャンルの家族別。数字は docs/sound/data/mix-targets.json（mix-patterns.md §3.0）と mastering-guide.md。 */
export interface MasterFamily {
  label: string;
  /** mix-targets.json の家族名 */
  mixTargetFamily: string;
  /** 勧める master-preset */
  preset: string;
  /** つぶれ気味のときに替える preset */
  presetLighter: string;
  /** 目標の大きさ（LUFS）の幅 */
  lufs: [number, number];
  /** PLR（真のピーク − 統合LUFS）の目安 */
  plr: [number, number];
  /** 左右の相関の目安（genre-targets / analyze.py: 0.4〜0.88） */
  corr: [number, number];
}
export const MASTER_FAMILIES: Record<string, MasterFamily> = {
  rock: { label: "ロック／ポップ", mixTargetFamily: "rock", preset: "rock-clean", presetLighter: "rock-open", lufs: [-11, -9], plr: [9, 14.5], corr: [0.4, 0.88] },
  punk: { label: "パンク／メタル", mixTargetFamily: "punk", preset: "punk", presetLighter: "rock-open", lufs: [-10.5, -9], plr: [8.5, 14.5], corr: [0.3, 0.85] },
  jazz: { label: "ジャズ／アコースティック", mixTargetFamily: "jazz", preset: "jazz", presetLighter: "solo", lufs: [-18, -14], plr: [11, 16], corr: [0.5, 0.92] },
  game: { label: "ゲーム（フィールド）", mixTargetFamily: "rock", preset: "game-field", presetLighter: "game-field", lufs: [-17.5, -15], plr: [10, 16], corr: [0.4, 0.9] },
};
