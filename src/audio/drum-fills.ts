// ドラムのおかず（フィルイン）の型集。
// 1つの型は「小節の最後の2拍」を16分で8マスに分けて書く。マスの文字:
//   S（スネア）… x 普通 / X 強く / o ゴースト（弱く） ／ K（キック）… x / X ／ T（タム）… 1〜6 の数字 = 高い(C4) → 低いフロア(A2)
//   H（ハイハット）… 省略するとそのまま。書くと、おかずの間のハイハットをこの形に置き換える（"........" で止める）
//   "." は休み
// 大きさ: small＝フレーズの区切り（4・8小節ごと）/ medium＝次の場面への橋渡し / big＝サビ前・山場の前 / drop＝いったん止めて次の頭で一気に出す
import { REST, type NoteEvent, type Track } from "./score";

export type FillSize = "small" | "medium" | "big" | "drop";
export interface DrumFill {
  id: string;
  name: string;
  size: FillSize;
  /** どんなときに使うか */
  use: string;
  S: string;
  K: string;
  T: string;
  H?: string;
}

/** タムの高さ（数字 → 音名）。midi-export が、この音名でGMのタム(50/48/47/45/43/41)を選ぶ。 */
export const TOM_NOTE: Record<string, string> = { "1": "C4", "2": "A3", "3": "G3", "4": "E3", "5": "C3", "6": "A2" };

export const FILLS: DrumFill[] = [
  // small: 目立ちすぎない、フレーズの区切り
  { id: "one", name: "ひとつ", size: "small", use: "Aメロなど静かな場面の、4小節ごとの区切り。最後の裏にスネア1発", S: "......x.", K: "x.......", T: "........" },
  { id: "two", name: "ふたつ", size: "small", use: "4・8小節の終わり。最後の拍に「タンタン」", S: "......xx", K: "x.......", T: "........" },
  { id: "late", name: "うらから", size: "small", use: "次の頭を引き立てる。最初を休んで、最後の16分を3つ", S: ".....xxX", K: "x.......", T: "........" },
  { id: "ghost", name: "ゴースト加速", size: "small", use: "ノリを保ったまま、弱いスネアから強い1発へ。ゆるいバラード向き", S: "o.o.ooxX", K: "x.....x.", T: "........" },
  // medium: 次の場面へ橋渡し
  { id: "run", name: "かけあがり", size: "medium", use: "AメロからBメロへ。前半は8分、後半は16分に加速", S: "x.x.xxXX", K: "x.......", T: "........" },
  { id: "tom1", name: "タム回し（1拍）", size: "medium", use: "定番。最後の1拍で、高いタムから低いタムへ下りる", S: "x.x.....", K: "x.......", T: "....1234" },
  { id: "snaretom", name: "スネアからタム", size: "medium", use: "前半はスネア、後半はタムに移って立体感を出す", S: "xxx.....", K: "x.......", T: "....1244" },
  { id: "synco", name: "シンコペ", size: "medium", use: "拍の裏に引っかけて、グルーブを前に押す", S: "..x..xX.", K: "x.....x.", T: ".......3" },
  // big: サビ前・山場の前
  { id: "tom2", name: "タム回し（2拍）", size: "big", use: "サビ前の定番。2拍かけて高→低へ、16分でびっしり", S: "........", K: "x.......", T: "11223355", H: "x.x....." },
  { id: "snare2tom", name: "スネアのあとタム", size: "big", use: "前の2拍はスネアの16分、後ろはタムに下りて着地を重くする", S: "xxxx....", K: "x.....xx", T: "....1245", H: "x.x....." },
  { id: "wide", name: "広い音域", size: "big", use: "高いタムから低いフロアへ、最後はキックの2発。大きな転換点に", S: "........", K: "......xX", T: "1.2.3.54", H: "x......." },
  { id: "roll", name: "ロール", size: "big", use: "スネアを16分で連打して、だんだん強く。ビルドアップ", S: "ooxxxXXX", K: "x.......", T: "........", H: "x.x....." },
  // drop: いったん止める
  { id: "break", name: "ブレイク", size: "drop", use: "サビ直前に全部止めて、最後に低いタム1発。次の頭の全員の出がはっきりする", S: "........", K: "........", T: "......6.", H: "........" },
  { id: "stop", name: "ストップ", size: "drop", use: "最後の1拍だけ休んで、すぐ次の頭へ。バラードのサビ前・語りかける場面に", S: "........", K: "x.......", T: "........", H: "x.x....." },
];

/** 大きさごとの型。 */
export const fillsOf = (size: FillSize): DrumFill[] => FILLS.filter((f) => f.size === size);

/** n 番目に選ぶ型（同じ大きさの中でぐるぐる変える。続けて同じ型が出ないように）。 */
export function pickFill(size: FillSize, index: number): DrumFill {
  const list = fillsOf(size);
  return list[((index % list.length) + list.length) % list.length];
}

const SLOT = 0.25;

/** 型の1つの段（S・K・T・H）を、8マスぶんの音符にする。 */
function laneEvents(lane: "S" | "K" | "T" | "H", spec: string): NoteEvent[] {
  const out: NoteEvent[] = [];
  const add = (e: NoteEvent): void => {
    const last = out[out.length - 1];
    if (e.note === REST && last && last.note === REST) last.durationBeats += e.durationBeats;
    else out.push(e);
  };
  for (const ch of spec.padEnd(8, ".").slice(0, 8)) {
    if (ch === "." || ch === "-") add({ note: REST, durationBeats: SLOT });
    else if (lane === "T") add({ note: TOM_NOTE[ch] ?? "G3", durationBeats: SLOT, ...(ch === "1" || ch === "5" ? { velocity: 1.1 } : {}) });
    else add({ note: "C2", durationBeats: SLOT, ...(ch === "X" ? { velocity: 1.3 } : ch === "o" ? { velocity: 0.5 } : {}) });
  }
  return out;
}

/** 音符の列の [from, to) 拍を、置き換え用の音符で入れ替える（またがる音符は切る）。 */
export function overwriteRange(notes: NoteEvent[], from: number, to: number, repl: NoteEvent[]): NoteEvent[] {
  const out: NoteEvent[] = [];
  let pos = 0;
  let inserted = false;
  const insert = (): void => { if (!inserted) { out.push(...repl); inserted = true; } };
  const EPS = 1e-9;
  for (const n of notes) {
    const s = pos;
    const e = pos + n.durationBeats;
    pos = e;
    if (e <= from + EPS) { out.push(n); continue; }
    if (s >= to - EPS) { insert(); out.push(n); continue; }
    if (s < from - EPS) out.push({ ...n, durationBeats: from - s });
    insert();
    if (e > to + EPS) out.push({ note: REST, durationBeats: e - to });
  }
  if (pos < from + EPS) {
    if (from - pos > EPS) out.push({ note: REST, durationBeats: from - pos });
    insert();
  } else insert();
  return out;
}

/** 型を、トラック群に入れる。fromBeat から2拍ぶん。snare・kick・hihat・tom のトラックを書き換え、tom は無ければ作る。 */
export function placeFill(tracks: Track[], fill: DrumFill, fromBeat: number, totalBeats: number): Track[] {
  const to = fromBeat + 2;
  const out = tracks.map((t) => {
    const inst = t.instrument;
    if (inst === "snare") return { ...t, notes: overwriteRange(t.notes, fromBeat, to, laneEvents("S", fill.S)) };
    if (inst === "kick") return { ...t, notes: overwriteRange(t.notes, fromBeat, to, laneEvents("K", fill.K)) };
    if (inst === "hihat" && fill.H !== undefined) return { ...t, notes: overwriteRange(t.notes, fromBeat, to, laneEvents("H", fill.H)) };
    if (inst === "tom") return { ...t, notes: overwriteRange(t.notes, fromBeat, to, laneEvents("T", fill.T)) };
    return t;
  });
  if (fill.T.replace(/[.\-]/g, "") && !out.some((t) => t.instrument === "tom")) {
    const lead: NoteEvent[] = fromBeat > 0 ? [{ note: REST, durationBeats: fromBeat }] : [];
    const tail = totalBeats - to;
    out.push({ waveform: "square", instrument: "tom", volume: 0.11, pan: 0.15, notes: [...lead, ...laneEvents("T", fill.T), ...(tail > 0 ? [{ note: REST, durationBeats: tail }] : [])] });
  }
  return out;
}
