/**
 * AIソング形式のリズム・グルーヴ関連の項目を、Score に直す（docs/sound/rhythm-groove-guide.md §10）。
 * ai-song.ts から呼ぶ。新しい項目はすべて省略可能で、省略すれば今までと同じ曲になる。
 *
 * 曲の項目: tempo（テンポの変化）・rit・rubato・bossTempo・grouping・swing16・humanProfile・humanDist・lockToKick・grooveFeel・hihatBySection・trapRolls
 * パートの項目: pushMs・human・humanTiming・humanVelocity・swing・swing16・lockToKick
 */
import type { Section } from "./arrangement";
import { bossPhasePlan, type BossPlanOptions } from "./drum-extras";
import { GROOVE_FEELS, grooveFeelMs, grooveRoleOf, humanTableFor, ROLE_HUMAN_DEFAULT } from "./groove-feel";
import type { Score, Track } from "./score";
import { loopTempoWarning, makeTempoClock, ritPoints, rubatoPoints, type TempoPoint } from "./tempo-map";

export interface AiTempoPoint { bar: number; bpm: number; ramp?: number }
export interface AiRit { bar: number; bars: number; to: number; q?: number; aTempo?: boolean }
export interface AiRubato { amount?: number }

/** 曲全体のリズム関連の項目（AiSong に足す）。 */
export interface RhythmSongFields {
  /** テンポの変化。bar（1始まり）からのテンポ。ramp（小節）があれば、その長さで直線的に変わる。 */
  tempo?: AiTempoPoint[];
  /** 終わりの減速（rit.）: bar（1始まり）から bars 小節かけて、最後の速さが最初の to 倍（0.7＝30%遅く）に。aTempo: true なら終わったところで元のテンポに戻る。 */
  rit?: AiRit;
  /** ルバート 0〜1（バラード・フィールド曲向け。±3% ほどのゆるやかなテンポのゆれと、フレーズ終わりの小さな伸び）。ループで元に戻る。 */
  rubato?: number;
  /** ボス曲のフェーズ表。true で標準（第1形態→第2形態 +5%→最終形態 +10%、最後の2小節で元のテンポへ）。 */
  bossTempo?: boolean | { phases?: BossPlanOptions["phases"]; loopBack?: boolean };
  /** 8分の裏と別に、16分の裏の swing（0〜1）。 */
  swing16?: number;
  /** パート別の human 倍率の表。"role"＝役割ごとの標準（キック0.5・ベース0.8・スネア0.8・ハット1.2・リード1.2…）、"genre"＝drumGenre の表。 */
  humanProfile?: "role" | "genre";
  /** "triangle" で human のずれを三角分布（極端なずれが少ない）に。 */
  humanDist?: "triangle";
  /** true でベースを、キックと同じ拍に重なる音ではキックと同じだけずらす。 */
  lockToKick?: boolean;
  /** ノリ。tight（きっちり）・laidback（あと乗り）・pushed（前のめり）・genre（drumGenre の表）。push／pushMs を書いたパートはそちらが優先。 */
  grooveFeel?: "tight" | "laidback" | "pushed" | "genre";
  /** true で、自動伴奏のハイハットを drumGenre の型でセクションごとに変える（verse＝4分、chorus＝16分、4小節ごとにオープン）。sections と drumGenre が要る。 */
  hihatBySection?: boolean;
  /** true（または { every, kind }）で、ハイハットの小節末にトラップのロールを自動で入れる。 */
  trapRolls?: boolean | { every?: number; kind?: "triplet" | "thirtysecond" | "auto" };
}

/** パートのリズム関連の項目（AiPart に足す）。 */
export interface RhythmPartFields {
  pushMs?: number;
  human?: number;
  humanTiming?: number;
  humanVelocity?: number;
  humanPitch?: number;
  swing?: number;
  swing16?: number;
  lockToKick?: boolean;
}

const finite = (x: unknown): x is number => x !== undefined && x !== null && x !== "" && Number.isFinite(Number(x));
const clamp = (x: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, x));

/** tempo・rit・bossTempo・rubato から、テンポマップを作る。無ければ undefined。 */
export function resolveTempoMap(
  song: RhythmSongFields & { bpm: number },
  ctx: { beatsPerBar: number; totalBars: number; sections?: Section[]; warnings: string[] },
): TempoPoint[] | undefined {
  const { beatsPerBar, totalBars, warnings } = ctx;
  const totalBeats = totalBars * beatsPerBar;
  const bpm = Number(song.bpm);
  let explicit: TempoPoint[] = [];
  if (song.tempo !== undefined) {
    if (!Array.isArray(song.tempo)) warnings.push("tempo は { bar, bpm, ramp? } の並びで書いてください。無視しました");
    else {
      song.tempo.forEach((t, i) => {
        if (!t || !finite(t.bar) || !finite(t.bpm) || Number(t.bar) < 1 || Number(t.bar) > totalBars + 1) { warnings.push(`tempo[${i}]: bar は 1〜${totalBars}、bpm は数字で書いてください。無視しました`); return; }
        const b = Number(t.bpm);
        if (b < 20 || b > 300) warnings.push(`tempo[${i}]: bpm ${b} は 20〜300 にしてください`);
        const ramp = finite(t.ramp) && Number(t.ramp) > 0 ? Number(t.ramp) * beatsPerBar : undefined;
        explicit.push({ beat: (Math.round(Number(t.bar)) - 1) * beatsPerBar, bpm: clamp(b, 20, 300), ...(ramp ? { ramp } : {}) });
      });
    }
  }
  if (song.bossTempo) {
    const opt = typeof song.bossTempo === "object" ? song.bossTempo : {};
    explicit.push(...bossPhasePlan(bpm, totalBars, beatsPerBar, ctx.sections, { phases: opt.phases, loopBack: opt.loopBack }).tempo);
  }
  if (song.rit !== undefined) {
    const r = song.rit;
    if (!r || !finite(r.bar) || !finite(r.bars) || !finite(r.to) || Number(r.bar) < 1 || Number(r.bars) <= 0) warnings.push("rit は { bar, bars, to } で書いてください（例 { bar: 31, bars: 2, to: 0.7 }）。無視しました");
    else {
      const beat = (Number(r.bar) - 1) * beatsPerBar;
      const before = makeTempoClock(bpm, explicit).bpmAt(beat);
      explicit.push(...ritPoints({ beat, beats: Number(r.bars) * beatsPerBar, to: Number(r.to), ...(finite(r.q) ? { q: Number(r.q) } : {}), ...(r.aTempo ? { aTempo: true } : {}) }, before));
    }
  }
  explicit = explicit.sort((a, b) => a.beat - b.beat);
  const warn = loopTempoWarning(bpm, explicit, totalBeats);
  if (warn) warnings.push(warn);
  const amount = finite(song.rubato) ? clamp(Number(song.rubato), 0, 1) : 0;
  if (amount > 0) return rubatoPoints(bpm, explicit, { amount, totalBeats, beatsPerBar });
  return explicit.length ? explicit : undefined;
}

/** 曲のうち、Score のそのままのフィールドになる項目。 */
export function scoreRhythmFields(song: RhythmSongFields & { drumGenre?: string }, warnings: string[]): Partial<Score> {
  const out: Partial<Score> = {};
  if (finite(song.swing16)) out.swing16 = clamp(Number(song.swing16), 0, 1);
  if (song.humanProfile === "role") out.humanRoles = { ...ROLE_HUMAN_DEFAULT };
  else if (song.humanProfile === "genre") out.humanRoles = humanTableFor(song.drumGenre);
  else if (song.humanProfile !== undefined) warnings.push(`humanProfile「${String(song.humanProfile)}」は使えません（role・genre）。無視しました`);
  if (song.humanDist === "triangle") out.humanDist = "triangle";
  if (song.lockToKick === true) out.lockToKick = true;
  return out;
}

/** パートのリズム関連の項目を Track の項目にする。 */
export function trackRhythmFields(p: RhythmPartFields): Partial<Track> {
  const out: Partial<Track> = {};
  if (finite(p.pushMs) && Number(p.pushMs) !== 0) out.pushMs = clamp(Number(p.pushMs), -50, 50);
  if (finite(p.human)) out.human = clamp(Number(p.human), 0, 2);
  if (finite(p.humanTiming)) out.humanTiming = clamp(Number(p.humanTiming), 0, 2);
  if (finite(p.humanVelocity)) out.humanVelocity = clamp(Number(p.humanVelocity), 0, 2);
  if (finite(p.humanPitch)) out.humanPitch = clamp(Number(p.humanPitch), 0, 2);
  if (finite(p.swing)) out.swing = clamp(Number(p.swing), 0, 1);
  if (finite(p.swing16)) out.swing16 = clamp(Number(p.swing16), 0, 1);
  if (p.lockToKick === true) out.lockToKick = true;
  return out;
}

/** grooveFeel を、push も pushMs も書いていないパート（自動伴奏を含む）に当てる。 */
export function applyGrooveFeel(tracks: Track[], song: RhythmSongFields & { drumGenre?: string }, explicitPush: ReadonlySet<Track>, warnings: string[]): Track[] {
  const feel = song.grooveFeel;
  if (feel === undefined) return tracks;
  if (feel !== "genre" && !GROOVE_FEELS.includes(feel)) {
    warnings.push(`grooveFeel「${String(feel)}」は使えません（tight・laidback・pushed・genre）。無視しました`);
    return tracks;
  }
  if (feel === "genre" && !song.drumGenre) {
    warnings.push("grooveFeel: \"genre\" には drumGenre が要ります。無視しました");
    return tracks;
  }
  return tracks.map((t) => {
    if (explicitPush.has(t) || t.push !== undefined || t.pushMs !== undefined) return t;
    const ms = grooveFeelMs(feel, song.drumGenre, grooveRoleOf(t.instrument));
    return ms ? { ...t, pushMs: ms } : t;
  });
}


/** AI_SONG_GUIDE の末尾に足す、リズム・グルーヴの新しい項目の説明（詳しくは docs/sound/rhythm-groove-guide.md）。 */
export const RHYTHM_GUIDE_ADDENDUM = `

- リズム・グルーヴの追加項目（すべて省略できる。詳しくは docs/sound/rhythm-groove-guide.md §10・§12）:
  - パートごとの human: parts[].human（0〜2の倍率。0＝そのパートは機械的に正確、1.2＝ハットなど）、humanTiming／humanVelocity（ずれと強さを別々に）。曲の humanProfile: "role"（キック0.5・ベース0.8・スネア0.8・ハット1.2・リード1.2）か "genre"（drumGenre の表）で一括。humanDist: "triangle" で極端なずれを減らす。lockToKick: true（または parts[].lockToKick）でベースがキックと同じだけずれてそろったまま。
  - ミリ秒の push: parts[].pushMs（-50〜50。スネア +5〜+12、ハット -3〜0、キック 0）。曲の grooveFeel: "tight"・"laidback"・"pushed"・"genre"（drumGenre の表）で一括。push／pushMs を書いたパートはそちらが優先。
  - swing の分離: parts[].swing（そのパートだけ。0 でまっすぐ。キックをまっすぐにしてハットだけ揺らす）、swing16・曲の swing16（16分の裏だけ別の量）。
  - 三連グリッド: ドラムの音に t:x.xx.xx.xx.x と書くと、1文字が三連の1つ（1拍＝3文字、4/4の1小節＝12文字）。x X o O . -。シャッフル・12/8・トラップの三連ロール・3対2に。
  - 拍子: beats は 2〜12 の整数（5・9・11拍子など）。grouping: [2,2,3]（合計が beats）か "auto" で、自動伴奏のドラムがまとまりの頭にキック・スネア・強いハットを置く。
  - テンポの変化: tempo: [{ bar: 17, bpm: 96, ramp: 2 }]（bar から。ramp 小節かけて直線的に）、rit: { bar: 31, bars: 2, to: 0.7, aTempo: false }（終わりの減速。aTempo: true なら終わったところで元のテンポに戻る）、rubato: 0〜1（ゆるやかなゆれ。バラード向け。ループで元に戻る）、bossTempo: true（第2形態 +5%・最終形態 +10%、最後の2小節で元に戻す。sections を併用）。ループ曲は、最後のテンポが最初と違うと警告が出る。
  - ドラムの自動化: hihatBySection: true（drumGenre と sections が要る。verse＝4分、chorus＝16分に細かく）、trapRolls: true（ハイハットの小節末に三連と32分のロール。{ every: 4, kind: "auto" }）。
  - 点検: node tools/audio-check/check-groove.mjs 曲.json（push・human・volume・swing・格子の長さ・ベタ打ち・シンコペ率など）。`;
