import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// ねむり のアイコン。三日月とZの文字。完全オリジナル。
export const name = "ねむり";
export const category = "icon";
export const pal = { p: "#141040", "1": "#3a2a90", "2": "#6a5ad8", "3": "#a49af8", "4": "#e0dcff", y: "#ffe070", Y: "#fff8b8", o: "#b08828", D: "#20102a" };
const c = cv();
fillEll(c, 14, 29, 8, 1, "D");
// 三日月
ell(c, 13, 17, 9, 9, "poyyY");
fillEll(c, 17, 14, 8, 8, ".");
// 月の縁をなじませ
for (let y = 6; y <= 27; y++) for (let x = 3; x <= 26; x++) { if (c.get(x, y) !== ".") { const rt = c.get(x + 1, y) === "." && x > 14; if (rt && c.get(x, y) !== "o") c.put(x, y, "o"); } }
// Z（2ドット幅。光は左上）
const Z = (x, y, s, ch, hi, lo) => { for (let i = 0; i < s; i++) { c.put(x + i, y, hi); c.put(x + i, y + 1, ch); c.put(x + i, y + s - 2, ch); c.put(x + i, y + s - 1, lo); } for (let i = 1; i < s - 1; i++) { const px = x + s - 1 - i - 1; c.put(px, y + i, hi); c.put(px + 1, y + i, ch); c.put(px + 2, y + i, lo); } };
Z(17, 15, 9, "2", "3", "1"); Z(22, 8, 7, "3", "4", "2"); Z(26, 2, 5, "3", "4", "2");
export const rows = c.rows();
