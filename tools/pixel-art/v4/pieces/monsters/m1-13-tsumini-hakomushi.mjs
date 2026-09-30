import { Cv, R } from "../../lib4.mjs";
// 積荷の箱虫: 港の積荷の木箱に虫がもぐりこんで動かしているもの。すき間から目が光る。
export const name = "積荷の箱虫"; export const category = "monster";
export const pal = { ...R("abcde", "#2a1808", "#d8a468", "#8a5a2a"), ...R("fgh", "#2a2a3a", "#a8a8c0"), ...R("ijk", "#3a2a10", "#e8c880"), z: "#1c1408", w: "#ffffff", e: "#100804", y: "#ffd020", r: "#e04a30" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
for (const s of [0, 1]) { const X = (x) => (s ? 31 - x : x);
  c.line(X(9), 23, X(4), 25, "f"); c.line(X(4), 25, X(3), 29, "f"); c.line(X(10), 25, X(8), 29, "f"); c.line(X(12), 26, X(12), 29, "f");
  c.line(X(12), 9, X(8), 4, "f"); c.line(X(8), 4, X(4), 3, "f"); c.px(X(4), 3, "y"); }
c.box(6, 9, 25, 25, "abcde");                                                        // 箱
for (const y of [13, 17, 21]) c.line(7, y, 24, y, "a");                              // 板の合わせめ
c.box(6, 9, 8, 25, "fgh"); c.box(23, 9, 25, 25, "fgh"); c.box(6, 9, 25, 10, "fgh");   // 金具
c.list([[7, 12, "h"], [7, 18, "h"], [7, 23, "h"], [24, 12, "g"], [24, 18, "g"], [24, 23, "g"]]);
c.box(10, 14, 21, 17, "eeee", { outline: false });                                    // すき間
c.eye(11, 14, "y"); c.eye(18, 14, "y");
c.list([[10, 12, "d"], [12, 11, "e"], [15, 21, "d"], [18, 23, "a"], [20, 12, "d"]]);
c.line(12, 18, 19, 18, "e"); for (const x of [13, 15, 17]) { c.px(x, 19, "w"); }
c.px(16, 24, "r"); c.px(9, 21, "r");
export const rows = c.rows();
