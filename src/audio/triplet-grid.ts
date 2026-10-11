/**
 * 三連グリッド `t:`（docs/sound/rhythm-groove-guide.md §10 提案4）。
 * 1文字＝三連の1つ（1拍＝3文字、4/4 の1小節＝12文字）。x＝打つ、X＝強く、o＝弱く（ゴースト）、O＝オープンハイハット、. か - ＝休み。
 * 3つで1拍になるよう 0.3333・0.3333・0.3334 の長さにする。シャッフル、12/8、トラップの三連ロール、3対2のポリリズムに。
 * `swing` は 0.5・0.25・0.75 拍目だけを動かすので、三連には影響しない。
 */
import { REST, type NoteEvent } from "./score";

/** 三連1拍の3つ分の長さ（合計がちょうど1拍）。 */
export const TRIPLET_STEPS = [0.3333, 0.3333, 0.3334] as const;

export const TRIPLET_CELLS = /^[xXoO.\-]+$/;

/** `t:` の中身（"x.xx.xx.xx.x" のような文字）を、ドラムの音の列にする。文字数が3の倍数でなければ null（errors に理由を足す）。 */
export function parseTripletGrid(cells: string, errors: string[], where: string, token = `t:${cells}`): NoteEvent[] | null {
  if (!TRIPLET_CELLS.test(cells)) {
    errors.push(`${where}: 三連グリッドは x X o O . - だけで書きます「${token}」`);
    return null;
  }
  if (cells.length % 3 !== 0) {
    errors.push(`${where}: 三連グリッドは3文字で1拍です（${cells.length} 文字。3の倍数に。4/4の1小節は12文字）「${token}」`);
    return null;
  }
  const out: NoteEvent[] = [];
  [...cells].forEach((c, i) => {
    const durationBeats = TRIPLET_STEPS[i % 3];
    if (c === "." || c === "-") out.push({ note: REST, durationBeats });
    else out.push({ note: "C2", durationBeats, ...(c === "X" ? { velocity: 1.3 } : c === "O" ? { velocity: 1.25, open: true } : c === "o" ? { velocity: 0.5 } : {}) });
  });
  return out;
}

/** 三連の格子を、拍の数（beats）ぶんくり返した文字にする。例: tripletBar("x.xx.xx.xx.x") */
export const tripletBeats = (cells: string): number => cells.length / 3;
