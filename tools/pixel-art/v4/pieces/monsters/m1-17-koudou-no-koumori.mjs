import { Cv, R } from "../../lib4.mjs";
// 坑道のコウモリ: 暗い坑道にひそむ大きなコウモリ。牙と赤い目が光る。
export const name = "坑道のコウモリ"; export const category = "monster";
export const pal = { ...R("abcde", "#0e1020", "#8a92b8", "#3a4068"), ...R("fgh", "#5a2a4a", "#d8809a"), z: "#0c0e1a", w: "#ffffff", e: "#080a14", r: "#ff3a4a" };
const c = new Cv();
c.shadow(16, 30, 7, "z");
for (const s of [0, 1]) { const X = (x) => (s ? 31 - x : x);
  c.poly([[X(12), 13], [X(5), 7], [X(0), 9], [X(3), 14], [X(1), 20], [X(6), 18], [X(6), 25], [X(11), 20], [X(13), 24]], "abcde", { lx: 0.5 });
  c.line(X(12), 14, X(1), 9, "a"); c.line(X(12), 15, X(2), 19, "a"); c.line(X(12), 17, X(6), 24, "a"); c.px(X(0), 8, "d"); }
c.ell(16, 19, 4, 6, "abcde");                                                            // 胴
c.ell(16, 21, 2, 3, "fgh", { outline: false });
c.poly([[12, 11], [11, 3], [15, 8]], "abcde"); c.poly([[20, 11], [21, 3], [17, 8]], "abcde"); c.px(12, 8, "g"); c.px(20, 8, "g");
c.ell(16, 11, 4, 4, "abcde");
c.eye(12, 10, "r"); c.eye(18, 10, "r"); c.px(15, 12, "e"); c.px(16, 12, "e");
c.px(14, 14, "w"); c.px(18, 14, "w"); c.px(15, 14, "e"); c.px(17, 14, "e"); c.px(16, 14, "e");
c.line(14, 26, 13, 28, "b"); c.line(18, 26, 19, 28, "b");
export const rows = c.rows();
