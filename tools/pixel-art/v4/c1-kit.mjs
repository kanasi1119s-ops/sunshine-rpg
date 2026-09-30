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
    if (brow) for (let k = 0; k < 3; k++) p.push([x0 + k, 6, brow]);
  }
  if (mouth === "small") p.push([15, 11, "n"], [16, 11, "n"]);
  if (mouth === "smile") p.push([14, 11, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"], [13, 10, "n"], [18, 10, "n"]);
  if (mouth === "flat") p.push([14, 11, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"]);
  if (mouth === "open") p.push([15, 10, "n"], [16, 10, "n"], [15, 11, "e"], [16, 11, "e"]);
  if (mouth === "frown") p.push([14, 12 - 1, "n"], [15, 11, "n"], [16, 11, "n"], [17, 11, "n"]);
  if (blush) p.push([10, 10, "B"], [21, 10, "B"]);
  return p;
}
/** 光が左上から当たる「塊」を、輪郭つきで塗る。y0: 最初の行, sp: 行ごとの [x0,x1] の配列（null で空行）, ramp: 明→暗の文字列（例 "4321"）。
 * o.out: 左と上の輪郭の色  o.outD: 右と下の輪郭の色（既定は out）  o.strand: [a,b] で (x*a+y)%b==0 の点を1段暗く（髪の房・服のしわ）  o.bias: 暗くなる速さ(既定1)  o.noTop: true で最上段を輪郭にしない */
export function mass(y0, sp, ramp, o = {}) {
  const { out = ramp[ramp.length - 1], strand = null, bias = 1 } = o; const outD = o.outD ?? out; const pts = [];
  const xs0 = Math.min(...sp.filter(Boolean).map((s) => s[0])), xs1 = Math.max(...sp.filter(Boolean).map((s) => s[1])); const n = ramp.length;
  const has = (i, x) => sp[i] && x >= sp[i][0] && x <= sp[i][1];
  sp.forEach((s, i) => { if (!s) return; const y = y0 + i;
    for (let x = s[0]; x <= s[1]; x++) {
      const up = !has(i - 1, x), dn = !has(i + 1, x), lf = x === s[0], rt = x === s[1];
      if (up && !o.noTop) { pts.push([x, y, lf ? out : out]); continue; }
      if (lf) { pts.push([x, y, out]); continue; }
      if (dn && !rt) { pts.push([x, y, o.outB ?? outD]); continue; }
      if (rt || dn) { pts.push([x, y, outD]); continue; }
      const u = (x - xs0) / Math.max(1, xs1 - xs0), v = i / Math.max(1, sp.length - 1);
      const sv = Math.min(1, (u * 0.65 + v * 0.35) * bias); let t = sv < 0.12 ? 0 : 1 + Math.min(n - 2, Math.floor(((sv - 0.12) / 0.88) * (n - 1)));
      if (strand && (x * strand[0] + y) % strand[1] === 0 && t > 0) t = Math.min(n - 1, t + 1);
      if (o.folds && o.folds.some(([fx, fy0, fy1]) => x === fx && y >= fy0 && y <= fy1) && t > 0) t = Math.min(n - 1, t + 1);
      t = Math.max(0, Math.min(n - 1, t));
      pts.push([x, y, ramp[t]]);
    } });
  return pts;
}
/** 行ごとの範囲を、[中心, 半幅…] ではなく手で書くための短縮: rs("8-23", "7-24") → [[8,23],[7,24]] */
export const rs = (...a) => a.map((s) => (s ? s.split("-").map(Number) : null));
