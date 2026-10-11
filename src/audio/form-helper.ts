import { SECTION_KINDS, type Section, type SectionKind } from "./arrangement";
import { CURVE_TABLE, curveSections, type ExtraCurveName } from "./energy-curves";
import { expandBars, transposeChord } from "./song-plan";

/**
 * 形式の略記（docs/sound/form-structure-guide.md §12 の提案1）。
 * 曲のJSONに "form": "AABA" と書くと、sections と、必要なら sectionChords・chords・repeats の土台を作る。
 *   "form": "AABA"                                   … 名前つきの型（FORM_PRESETS）か、"AABBA" のような文字の並び
 *   "form": "sawtooth"                               … energy-curves.ts の曲線の名前（sections と energy が入る）
 *   "form": { "pattern": "ABAC", "unit": 8, "kinds": { "B": "chorus" }, "bars": { "C": 4 }, "chords": { "A": "C Am F G", "B": "F G Em Am" } }
 *   "form": "blues12" / { "pattern": "blues12", "key": "C", "quickChange": true, "minor": false, "laps": 4 }
 * 同じ文字は同じ kind（同じ種類）になる。書いたことがないとき（form なし）は何も変えない。
 * sections を自分で書いた曲では form の sections は使わない（注意を出す）。
 */
export interface FormObject {
  pattern: string;
  /** 1つの塊の小節数（既定は型ごと。多くは8）。 */
  unit?: number;
  /** 文字ごとの小節数の上書き。 */
  bars?: Record<string, number>;
  /** 文字ごとの kind の上書き。 */
  kinds?: Record<string, SectionKind>;
  /** 文字ごとのコード進行（sectionChords になる）。 */
  chords?: Record<string, string>;
  /** blues12 の主音（既定 C）。 */
  key?: string;
  /** blues12 を短調（Cm7 Fm7 G7）にする。 */
  minor?: boolean;
  /** blues12 で2小節目に IV7 を入れる（クイックチェンジ）。 */
  quickChange?: boolean;
  /** blues12 の周回数（省略は repeats が2以上ならそれ、なければ3）。 */
  laps?: number;
}

export interface FormFields {
  form?: unknown;
  chords: string;
  barsPerChord: number;
  repeats: number;
  sections?: unknown;
  sectionChords?: Record<string, string>;
  energy?: unknown;
  occurrence?: boolean;
}

interface Preset { letters: string; kinds: Record<string, SectionKind>; unit: number; label: string; energy?: number[]; occurrence?: boolean }
/** 文字の既定の kind と、既定の小節数（unit と違うものだけ）。 */
const LETTER_KIND: Record<string, SectionKind> = { A: "verse", B: "chorus", C: "bridge", D: "interlude", E: "pre", I: "intro", O: "outro", S: "solo" };
const LETTER_BARS: Record<string, number> = { I: 4, E: 4, D: 4, O: 4 };

export const FORM_PRESETS: Record<string, Preset> = {
  strophic: { letters: "AAA", kinds: { A: "verse" }, unit: 8, label: "AAA（ストロフィック）", occurrence: true },
  AAA: { letters: "AAA", kinds: { A: "verse" }, unit: 8, label: "AAA（ストロフィック）", occurrence: true },
  AABA: { letters: "AABA", kinds: { A: "verse", B: "bridge" }, unit: 8, label: "AABA（32小節形式）", occurrence: true },
  ABAC: { letters: "ABAC", kinds: { A: "verse", B: "interlude", C: "bridge" }, unit: 8, label: "ABAC（町型）", occurrence: true },
  ABAB: { letters: "ABAB", kinds: { A: "verse", B: "chorus" }, unit: 8, label: "ABAB", occurrence: true },
  AB: { letters: "AB", kinds: { A: "verse", B: "chorus" }, unit: 8, label: "短い2部ループ" },
  ABA: { letters: "ABA", kinds: { A: "verse", B: "bridge" }, unit: 8, label: "三部形式（ABA′）", occurrence: true },
  rondo: { letters: "ABACA", kinds: { A: "verse", B: "interlude", C: "bridge" }, unit: 8, label: "ロンド（ABACA）", occurrence: true },
  ABACA: { letters: "ABACA", kinds: { A: "verse", B: "interlude", C: "bridge" }, unit: 8, label: "ロンド（ABACA）", occurrence: true },
  verseChorus: { letters: "IAEBDAEBCBO", kinds: { I: "intro", A: "verse", E: "pre", B: "chorus", D: "interlude", C: "bridge", O: "outro" }, unit: 8, label: "ヴァース／コーラス", occurrence: true },
  ground: { letters: "AAAAAAAA", kinds: { A: "verse" }, unit: 4, label: "周回型（パッサカリア）", energy: [2, 3, 4, 5, 6, 7, 8, 9], occurrence: true },
  variations: { letters: "AAAAA", kinds: { A: "verse" }, unit: 8, label: "主題と変奏", energy: [3, 4, 5, 7, 9], occurrence: true },
};

export const FORM_NAMES: string[] = [...Object.keys(FORM_PRESETS), "blues12", ...(Object.keys(CURVE_TABLE))];

/** 12小節ブルースの進行（1小節ごと）。 */
export function bluesChords(key = "C", opts: { quickChange?: boolean; minor?: boolean } = {}): string[] {
  const root = /^[A-G][#b]?$/.test(key) ? key : "C";
  const I = root, IV = transposeChord(root, 5), V = transposeChord(root, 7);
  const q = opts.minor ? "m7" : "7";
  const one = (r: string, minor = true): string => `${r}${minor ? q : "7"}`;
  const tonic = one(I), sub = one(IV), dom = `${V}7`;
  return [tonic, opts.quickChange ? sub : tonic, tonic, tonic, sub, sub, tonic, tonic, dom, sub, tonic, dom];
}

function asObject(form: unknown, warnings: string[]): FormObject | null {
  if (typeof form === "string") return form.trim() ? { pattern: form.trim() } : null;
  if (form && typeof form === "object" && !Array.isArray(form) && typeof (form as FormObject).pattern === "string") return form as FormObject;
  warnings.push("form は \"AABA\" のような文字列か、{ \"pattern\": \"AABA\", ... } の形で書いてください。無視しました");
  return null;
}

const toKind = (k: unknown): SectionKind | undefined => (SECTION_KINDS.includes(k as SectionKind) ? (k as SectionKind) : undefined);

/** form を展開する。何も書かれていなければ同じものをそのまま返す。 */
export function expandForm<T extends FormFields>(song: T, warnings: string[] = []): T {
  if (!song || typeof song !== "object" || song.form === undefined || song.form === null) return song;
  const f = asObject(song.form, warnings);
  if (!f) return song;
  const pattern = f.pattern;
  const out: T = { ...song };

  // 12小節ブルース: chords と repeats（周回数）を作る
  if (pattern === "blues12") {
    const laps = Math.max(1, Math.min(16, Math.round(Number(f.laps ?? (Number(song.repeats) > 1 ? song.repeats : 3)))));
    const bars = bluesChords(f.key, { quickChange: f.quickChange === true, minor: f.minor === true });
    out.chords = bars.join(" ");
    out.barsPerChord = 1;
    out.repeats = laps;
    if (song.sections === undefined) {
      out.sections = Array.from({ length: laps }, (_, i) => ({ kind: laps >= 3 && i === laps - 1 ? "chorus" : "verse", bars: 12 }));
      if (out.occurrence === undefined) out.occurrence = true;
    } else warnings.push("form: blues12 の chords と周回数は入れましたが、sections は曲に書かれたものを使います");
    return out;
  }

  // 曲線の名前: sections と energy
  if (pattern in CURVE_TABLE) {
    if (song.sections !== undefined) { warnings.push(`form「${pattern}」: sections が曲に書かれているので、form の sections は使いません`); return out; }
    const sections = curveSections(pattern as ExtraCurveName);
    out.sections = sections;
    if (out.energy === undefined) out.energy = pattern;
    return reconcileLength(out, sections, f, warnings);
  }

  const preset = FORM_PRESETS[pattern];
  const letters = preset ? preset.letters : pattern;
  if (!/^[A-Z]+$/.test(letters) || letters.length > 32) {
    warnings.push(`form「${pattern}」は使えません（${FORM_NAMES.join("・")}、または AABA のような大文字の並び）。無視しました`);
    return song;
  }
  if (song.sections !== undefined) { warnings.push(`form「${pattern}」: sections が曲に書かれているので、form の sections は使いません`); return song; }
  const unit = Math.round(Number(f.unit ?? preset?.unit ?? 8));
  if (!(unit >= 1 && unit <= 64)) { warnings.push(`form.unit は 1〜64 の整数にしてください（${String(f.unit)}）。無視しました`); return song; }
  const kindOf: Record<string, SectionKind> = {};
  const sections: Section[] = [];
  for (const ch of letters) {
    const kind = toKind(f.kinds?.[ch]) ?? preset?.kinds[ch] ?? LETTER_KIND[ch];
    if (!kind) { warnings.push(`form: 文字「${ch}」の kind が決まりません。kinds で指定してください（例 "kinds": {"${ch}": "verse"}）。この文字は飛ばしました`); continue; }
    kindOf[ch] = kind;
    const own = Math.round(Number(f.bars?.[ch]));
    // unit を指定していなければ、導入・Bメロ・間奏・終わりの文字（I・E・D・O）は4小節
    const defaultBars = f.unit !== undefined ? unit : (LETTER_BARS[ch] ?? unit);
    sections.push({ kind, bars: own >= 1 ? own : defaultBars });
  }
  if (!sections.length) return song;
  out.sections = sections;
  if (preset?.energy && out.energy === undefined) out.energy = preset.energy;
  if (preset?.occurrence && out.occurrence === undefined) out.occurrence = true;

  // 文字ごとのコード進行 → sectionChords（kind をキーにする。同じ kind に別の文字が当たると片方しか使えない）
  if (f.chords && typeof f.chords === "object") {
    const sc: Record<string, string> = { ...(out.sectionChords ?? {}) };
    const byKind: Record<string, string> = {};
    for (const [ch, prog] of Object.entries(f.chords)) {
      const kind = kindOf[ch];
      if (!kind) { warnings.push(`form.chords: 文字「${ch}」は pattern にありません`); continue; }
      if (byKind[kind] && byKind[kind] !== ch) { warnings.push(`form.chords: 「${byKind[kind]}」と「${ch}」が同じ kind（${kind}）なので、進行を分けられません。kinds で kind を分けてください`); continue; }
      byKind[kind] = ch;
      sc[kind] = String(prog);
    }
    out.sectionChords = sc;
    if (!out.chords) out.chords = Object.values(f.chords)[0] ?? "C";
    return out;
  }
  return reconcileLength(out, sections, f, warnings);
}

/** chords の小節数と form の合計小節数をそろえる（repeats を直す）。割り切れなければ注意を出す。 */
function reconcileLength<T extends FormFields>(out: T, sections: Section[], f: FormObject, warnings: string[]): T {
  const total = sections.reduce((a, s) => a + s.bars, 0);
  let n = 0;
  try { n = expandBars(out.chords, out.barsPerChord === 2 ? 2 : 1).length; } catch { return out; }
  if (!n) return out;
  if (total % n === 0) out.repeats = total / n;
  else {
    out.repeats = Math.ceil(total / n);
    warnings.push(`form「${f.pattern}」の合計 ${total} 小節が、chords の ${n} 小節の整数倍ではありません。repeats を ${out.repeats} にして、sections を曲の長さに合わせて切り詰めます。chords を ${total} 小節ぶん（または ${total} の約数）で書くか、form.chords で塊ごとの進行を書いてください`);
  }
  return out;
}

/** form の合計小節数（sections を展開した値）。表示・検査用。 */
export function formTotalBars(sections: Section[]): number {
  return sections.reduce((a, s) => a + s.bars, 0);
}
