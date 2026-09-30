// 担当C1（主要・物語の人物）用の小さな道具。lib4.mjs は変えず、その外に置く。
// hs(): 左半分（x0〜15）の絵を書くと、右半分は鏡写し＋ひと段暗い色（光は左上）で自動で置く。
// st(): 左右非対称の絵を、x座標つきで置く。行の形式は "x|文字列"（文字列の各文字が x, x+1, … の点。空白は「触らない」、'.' は透明）。
export const DK = {
  "4": "3", "3": "2", "2": "1", d: "c", c: "b", b: "a", K: "k", k: "j", j: "J", Q: "P", X: "A", M: "m", O: "o", T: "t", U: "u", G: "g", W: "S", y: "y",
};
const parse = (line) => { const i = line.indexOf("|"); return [Number(line.slice(0, i)), line.slice(i + 1)]; };
/** 左半分の絵。lines は "x|文字列"。右半分は 31-x に鏡写しで、色を1段暗くする（dk で追加・上書き）。 */
export function hs(y0, lines, dk = {}) {
  const D = { ...DK, ...dk }; const pts = [];
  lines.forEach((ln, i) => { if (ln == null) return; const [x0, s] = parse(ln); [...s].forEach((ch, k) => { if (ch === " ") return; const x = x0 + k; pts.push([x, y0 + i, ch]); pts.push([31 - x, y0 + i, D[ch] ?? ch]); }); });
  return pts;
}
/** 非対称の絵。 */
export function st(y0, lines) {
  const pts = []; lines.forEach((ln, i) => { if (ln == null) return; const [x0, s] = parse(ln); [...s].forEach((ch, k) => { if (ch !== " ") pts.push([x0 + k, y0 + i, ch]); }); });
  return pts;
}
/** 目・まゆ・口。どの目にも白いハイライト w を入れる。
 * eye: std | narrow | sleepy | sharp | big   brow: 色の文字（既定 なし）  mouth: small | smile | flat | open | frown | none   ec: まぶたの色(既定 e)  ic: 瞳の色(既定 i)  blush: true/false */
export function face(o = {}) {
  const { eye = "std", brow = null, mouth = "small", ec = "e", ic = "i", blush = true, browTilt = 0 } = o; const p = [];
  for (const [x0, right] of [[11, false], [18, true]]) {
    const E = ec, I = ic;
    if (eye === "std") p.push([x0, 7, E], [x0 + 1, 7, E], [x0 + 2, 7, E], [x0, 8, "w"], [x0 + 1, 8, I], [x0 + 2, 8, E], [x0, 9, I], [x0 + 1, 9, I], [x0 + 2, 9, E]);
    if (eye === "big") p.push([x0, 6, E], [x0 + 1, 6, E], [x0 + 2, 6, E], [x0, 7, "w"], [x0 + 1, 7, I], [x0 + 2, 7, E], [x0, 8, I], [x0 + 1, 8, I], [x0 + 2, 8, E], [x0, 9, I], [x0 + 1, 9, I], [x0 + 2, 9, E]);
    if (eye === "narrow") p.push([x0, 7, E], [x0 + 1, 7, E], [x0 + 2, 7, E], [x0, 8, "w"], [x0 + 1, 8, I], [x0 + 2, 8, E], [x0, 9, "c"], [x0 + 1, 9, "c"], [x0 + 2, 9, "c"]);
    if (eye === "sleepy") p.push([x0, 7, "c"], [x0 + 1, 7, "c"], [x0 + 2, 7, "c"], [x0, 8, E], [x0 + 1, 8, E], [x0 + 2, 8, E], [x0, 9, "w"], [x0 + 1, 9, I], [x0 + 2, 9, I]);
    if (eye === "sharp") { p.push([x0, 8, E], [x0 + 1, 8, E], [x0 + 2, 8, E], [x0, 9, "w"], [x0 + 1, 9, I], [x0 + 2, 9, E]); p.push(right ? [x0 + 3, 7, E] : [x0 - 1, 7, E]); p.push([x0 + 1, 7, "c"], right ? [x0, 7, "c"] : [x0 + 2, 7, "c"]); p.push(right ? [x0 + 2, 7, E] : [x0, 7, E]); }
    if (brow) { for (let k = 0; k < 4; k++) { const bx = right ? x0 - 1 + k : x0 - 1 + k; p.push([bx, 6 - (browTilt > 0 ? (right ? (3 - k >= 2 ? 0 : 1) * 0 : 0) : 0), brow]); } }
  }
  if (mouth === "small") p.push([15, 11, "n"], [16, 11, "n"]);
  if (mouth === "smile") p.push([14, 11, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"], [13, 10, "n"], [18, 10, "n"]);
  if (mouth === "flat") p.push([14, 11, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"]);
  if (mouth === "open") p.push([15, 10, "n"], [16, 10, "n"], [15, 11, "e"], [16, 11, "e"]);
  if (mouth === "frown") p.push([14, 12 - 1, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"]);
  if (blush) p.push([10, 10, "B"], [21, 10, "B"]);
  return p;
}
