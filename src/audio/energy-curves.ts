import type { Section, SectionKind, Transition } from "./arrangement";

/**
 * エネルギー曲線の追加分（docs/sound/form-structure-guide.md §3 の20パターンのうち、scene.ts の既定の6つ以外）。
 * energy: "sawtooth" のように名前で書くと、セクション数に合わせて伸び縮みする（resampleEnergy）。
 * form: "sawtooth" のように曲線の名前を form に書くと、下の sections も一緒に入る（form-helper.ts）。
 * 強さは 1〜10。小節の合計と時間の例は form-structure-guide.md の表を参照。
 */
export interface CurveInfo {
  /** ガイドの表の番号。 */
  no: number;
  label: string;
  /** 向く場面。 */
  use: string;
  /** 「kind:小節」または「kind:小節/from」を空白でつないだもの。 */
  sections: string;
  energy: number[];
  /** ループ前提の曲か（false＝一度きり・場面が進む曲）。 */
  loop: boolean;
}

export const CURVE_TABLE = {
  classic: { no: 3, label: "定番（ラスサビ上げ）", use: "タイトル・主題曲", sections: "intro:4 verse:8 pre:4 chorus:8 interlude:4 verse:8 pre:4 chorus:8 bridge:8 chorus:8/stopBeat chorus:8 outro:4", energy: [2, 4, 6, 8, 4, 4, 6, 9, 3, 9, 10, 3], loop: false },
  dropChorus: { no: 4, label: "落ちサビ", use: "バラード・回想", sections: "intro:4 verse:8 pre:4 chorus:8 interlude:4 verse:8 pre:4 chorus:8 bridge:4 chorus:8 chorus:8 outro:4", energy: [2, 4, 6, 8, 4, 4, 6, 8, 2, 9, 10, 3], loop: false },
  gentleWave: { no: 6, label: "平らな波", use: "町・宿屋・ローファイ", sections: "verse:8 interlude:8 verse:8 bridge:8", energy: [4, 3, 4, 3], loop: true },
  highFlat: { no: 7, label: "高い平ら", use: "通常戦闘", sections: "verse:8 chorus:8", energy: [8, 9], loop: true },
  slowRise: { no: 9, label: "ゆっくり上る", use: "タイトル", sections: "intro:8 verse:8 pre:8 chorus:16 interlude:4 chorus:16 outro:4", energy: [3, 4, 6, 9, 5, 9, 3], loop: false },
  recall: { no: 10, label: "回想", use: "エンディング", sections: "intro:8 verse:8 pre:8 chorus:16 bridge:8 chorus:16 outro:8", energy: [2, 4, 7, 9, 2, 10, 2], loop: false },
  drone: { no: 11, label: "持続", use: "ダンジョン・洞窟", sections: "intro:4 verse:8 interlude:8 verse:8 bridge:8 outro:4", energy: [2, 3, 3, 2, 4, 1], loop: true },
  sawtooth: { no: 12, label: "のこぎり（ビルドとドロップ）", use: "追跡・乗り物", sections: "intro:8 build:8 drop:16 break:8 build:8 drop:16 outro:8", energy: [2, 5, 9, 3, 6, 10, 2], loop: false },
  crescendo: { no: 13, label: "クレッシェンド", use: "長い溜め・大技の前", sections: "intro:8 verse:8 verse:8 build:16 drop:16 tag:8", energy: [1, 2, 4, 6, 10, 2], loop: false },
  fakeEnd: { no: 14, label: "偽の終わり", use: "ボス撃破直前・どんでん返し", sections: "verse:8 pre:4 chorus:8 tag:4 build:4/riser drop:8 outro:4", energy: [3, 6, 9, 2, 6, 10, 3], loop: false },
  bossThree: { no: 15, label: "ボス3段", use: "ボス戦", sections: "intro:2 chorus:8 interlude:4 chorus:8 bridge:4 pre:4/stopBeat chorus:8 chorus:8", energy: [4, 9, 6, 9, 3, 6, 9, 10], loop: true },
  wander: { no: 16, label: "ゆるい波（探索）", use: "フィールド・旅", sections: "verse:8 interlude:8 chorus:8 interlude:8", energy: [4, 5, 6, 5], loop: true },
  chorusFirst: { no: 17, label: "サビ先出し", use: "主題曲・ポップ", sections: "chorus:4 verse:8 pre:4 chorus:8 interlude:4 verse:8 pre:4 chorus:8 chorus:8 outro:4", energy: [8, 3, 5, 9, 5, 4, 6, 9, 10, 3], loop: false },
  triumph: { no: 18, label: "凱旋", use: "勝利・取得", sections: "intro:1 chorus:4 outro:2", energy: [9, 10, 6], loop: false },
  suite: { no: 19, label: "組曲（長尺）", use: "裏ボス・最終章", sections: "intro:8 verse:16 interlude:8 bridge:16 solo:16 build:8 drop:16 tag:8", energy: [2, 4, 5, 3, 7, 8, 10, 2], loop: false },
  fadeAway: { no: 20, label: "引いていく", use: "別れ・夕暮れ・エンディング後半", sections: "chorus:8 chorus:8 interlude:8 verse:8 tag:8", energy: [8, 6, 4, 2, 1], loop: false },
} as const satisfies Record<string, CurveInfo>;

export type ExtraCurveName = keyof typeof CURVE_TABLE;
export const EXTRA_CURVES = Object.fromEntries(Object.entries(CURVE_TABLE).map(([k, v]) => [k, [...v.energy]])) as Record<ExtraCurveName, number[]>;
export const EXTRA_CURVE_NAMES = Object.keys(CURVE_TABLE) as ExtraCurveName[];

const KINDS: SectionKind[] = ["intro", "verse", "pre", "chorus", "interlude", "bridge", "outro", "build", "break", "drop", "solo", "tag"];
const FROMS: Transition[] = ["fill", "none", "stopBeat", "riser", "break1bar", "kime"];

/** 「intro:4 verse:8 pre:4/riser」の書き方を Section の並びにする（読めない所は捨てて warnings に書く）。 */
export function parseSectionText(text: string, warnings: string[] = []): Section[] {
  const out: Section[] = [];
  for (const tok of text.trim().split(/\s+/).filter(Boolean)) {
    const m = /^([a-z]+):(\d+)(?:\/([A-Za-z0-9]+))?$/.exec(tok);
    if (!m || !KINDS.includes(m[1] as SectionKind) || Number(m[2]) < 1) { warnings.push(`セクションの書き方が読めません「${tok}」（kind:小節 か kind:小節/from）`); continue; }
    const sec: Section = { kind: m[1] as SectionKind, bars: Number(m[2]) };
    if (m[3]) { if (FROMS.includes(m[3] as Transition)) sec.from = m[3] as Transition; else warnings.push(`from「${m[3]}」は使えません「${tok}」`); }
    out.push(sec);
  }
  return out;
}

/** 曲線の名前から、おすすめの sections を返す。 */
export function curveSections(name: ExtraCurveName): Section[] {
  return parseSectionText(CURVE_TABLE[name].sections);
}
