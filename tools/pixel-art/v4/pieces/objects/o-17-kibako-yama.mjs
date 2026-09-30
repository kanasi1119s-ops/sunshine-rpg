import { painter } from "../../lib4.mjs";
export const name = "木箱の山";
export const category = "object";
export const pal = { o: "#2a1c12", h: "#f0d29a", T: "#d4a868", t: "#a87c48", d: "#7c5632", u: "#4c321e", r: "#c8b48c", R: "#e8dcbc", z: "#8a7654", S: "#2a2622", b: "#7a4a3a" };
const p = painter();
const crate = (x0, y0, x1, y1, th, brace) => { // 前面 (x0..x1, y0..y1) と上面(高さ th)
  p.poly([[x0 + 2, y0 - th], [x1 + 2, y0 - th], [x1 + 2, y0], [x0, y0]], "h"); p.poly([[x0 + 2, y0 - th], [x1 + 2, y0 - th], [x1 + 1, y0 - th + 1], [x0 + 1, y0 - th + 1]], "R");
  p.rect(x0, y0, x1, y1, "T"); p.rect(x0, y0, x1, y0, "h"); p.rect(x1 + 1, y0 - th + 1, x1 + 2, y1 - 1, "u"); p.rect(x1 - 1, y0 + 1, x1, y1, "d");
  p.rect(x0, y0, x0 + 1, y1, "d"); p.rect(x0, y1 - 1, x1, y1, "d"); p.rect(x0, y0, x1, y0 + 1, "d"); p.rect(x0, y0, x1, y0, "t");
  p.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "t"); p.rect(x0 + 2, y0 + 2, x1 - 2, y0 + 2, "T");
  if (brace) { p.line(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "d"); p.line(x1 - 2, y0 + 2, x0 + 2, y1 - 2, "d"); p.line(x0 + 3, y0 + 2, x1 - 2, y1 - 3, "T"); }
  else { for (let y = y0 + 4; y < y1 - 1; y += 3) p.rect(x0 + 2, y, x1 - 2, y, "d"); } };
crate(2, 19, 14, 27, 3, true);
crate(16, 21, 27, 27, 3, false);
crate(5, 11, 12, 18, 3, true);
// 荷ひもの袋
p.blob(22, 18, 4, 3, ["z", "r", "R"]); p.rect(20, 15, 23, 16, "r"); p.pts([[21, 15], [22, 15]], "z"); p.rect(21, 16, 22, 16, "b");
p.outline("o");
p.shadow(20, 29, 13, 1.6, "S");
export const rows = p.rows();
