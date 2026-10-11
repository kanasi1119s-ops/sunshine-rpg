/**
 * 世界のリズムの型（2026-10-11、docs/sound/scales-world-guide.md の提案 8、4-11 と 3-3 の型）。
 * ドラム（tom・kick・snare・hihat）やパートの `pattern` に名前で書くと、notes に展開される。
 * x＝打つ、X＝強く、o＝弱く、R＝休み。`cycle` は 1 周期の拍の数（合計）。
 */
export interface RhythmPattern {
  id: string;
  name: string;
  /** 1 周期の拍の数。 */
  cycle: number;
  /** 向く拍子（beats）。 */
  beats: number;
  notes: string;
  /** 向く楽器（目安）。 */
  use: string;
}

export const RHYTHM_PATTERNS: RhythmPattern[] = [
  { id: "son32", name: "3-2 ソン・クラーベ", cycle: 8, beats: 4, notes: "x:1.5 x:1.5 x:1 R:1 x:1 x:1 R:1", use: "tom・bell（ラテン）" },
  { id: "rumba32", name: "3-2 ルンバ・クラーベ", cycle: 8, beats: 4, notes: "x:1.5 x:2 x:0.5 R:1 x:1 x:1 R:1", use: "tom・bell（ラテン）" },
  { id: "tresillo", name: "トレシージョ（3+3+2）", cycle: 2, beats: 4, notes: "x:0.75 x:0.75 x:0.5", use: "kick・tom（ラテン・ダンス）" },
  { id: "bembe", name: "西アフリカの 12 拍の鈴", cycle: 6, beats: 6, notes: "x:1 x:1 x:0.5 x:1 x:1 x:1 x:0.5", use: "bell・kalimba（beats 6）" },
  { id: "soleaCompas", name: "フラメンコ 12 拍のアクセント", cycle: 12, beats: 6, notes: "o:1 o:1 X:1 o:1 o:1 X:1 o:1 X:1 o:1 X:1 o:1 X:1", use: "tom・snare（beats 6 × 2 小節）" },
  // 太鼓の二層（scales-world-guide 3-3）: 地打ち＝低く、拍の頭と 2 拍目だけ。表打ち＝高く、8 分の連打
  { id: "taikoJi", name: "太鼓の地打ち", cycle: 4, beats: 4, notes: "A2:1 A2:1 R:2", use: "tom（低い太鼓）" },
  { id: "taikoOmote", name: "太鼓の表打ち", cycle: 4, beats: 4, notes: "C4:0.5 C4:0.5 C4:0.5 C4:0.5 C4:0.5 C4:0.5 C4:0.5 C4:0.5", use: "tom（高い太鼓）" },
];

/** 名前で型を引く。"taiko2" は 地打ち＋表打ち の 2 パートに展開される（rhythmPatternParts）。 */
export function findRhythmPattern(id: string): RhythmPattern | undefined {
  return RHYTHM_PATTERNS.find((p) => p.id === id);
}

/** 1 つの名前が展開されるパターン（"taiko2" だけ 2 層）。 */
export function rhythmPatternLayers(id: string): RhythmPattern[] {
  if (id === "taiko2") return ["taikoJi", "taikoOmote"].map((x) => findRhythmPattern(x)!);
  const p = findRhythmPattern(id);
  return p ? [p] : [];
}

/**
 * 型の notes を、楽器に合わせて書き換える。ドラムの音（x）はそのまま。タムの音名つき（A2 など）の型はドラムでもそのまま、
 * 音程のある楽器では x・X・o を note（既定 C5）にして、X は `!`、o は `,` を付ける。
 */
export function realizeRhythm(p: RhythmPattern, drum: boolean, note = "C5"): string {
  if (drum) return p.notes;
  return p.notes
    .split(" ")
    .map((t) => {
      const [n, d] = t.split(":");
      if (n === "R") return t;
      if (/^[A-G]/.test(n)) return t;
      return `${note}:${d}${n === "X" ? "!" : n === "o" ? "," : ""}`;
    })
    .join(" ");
}
