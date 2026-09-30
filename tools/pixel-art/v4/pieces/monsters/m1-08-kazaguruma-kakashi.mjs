import { Cv, R } from "../../lib4.mjs";
// 風車のかかし: 腕の先に風車の羽をつけたかかし。ぼろ布とワラでできている。
export const name = "風車のかかし"; export const category = "monster";
export const pal = { ...R("abcde", "#2a1c10", "#c8a060", "#7a5a30"), ...R("fghi", "#5a1018", "#f08070"), ...R("jkl", "#a89060", "#fff0b0"), ...R("mno", "#1a1a30", "#6a6a98"), z: "#1c140c", w: "#ffffff", e: "#160a06", y: "#ffb020" };
const c = new Cv();
c.shadow(16, 30, 8, "z");
c.box(15, 20, 17, 29, "abcd");                                                       // 支柱
c.box(3, 12, 28, 14, "abcde");                                                       // 横木
for (const x of [6, 25]) { c.poly([[x, 13], [x - 4, 5], [x + 1, 4]], "fghi"); c.poly([[x, 13], [x + 5, 21], [x, 22]], "fghi"); c.poly([[x, 13], [x - 5, 21], [x - 1, 22]], "mno"); c.poly([[x, 13], [x + 5, 6], [x + 4, 11]], "mno"); c.ell(x, 13, 1, 1, "kkkk"); }
c.poly([[10, 14], [22, 14], [23, 24], [9, 24]], "fghi", { dither: true });          // ぼろ布の胴
for (const x of [10, 13, 16, 19, 22]) { c.px(x, 25, "h"); c.px(x, 26, "g"); }
c.list([[9, 22, "k"], [8, 23, "j"], [23, 22, "k"], [24, 23, "j"], [12, 25, "l"], [20, 25, "k"]]);
c.ell(16, 7, 4, 4, "jklll");                                                        // 頭のずだ袋
c.poly([[9, 5], [23, 5], [20, 0], [12, 0]], "mno", { dither: false }); c.line(8, 5, 24, 5, "n");   // 帽子
c.eye(12, 7, "y"); c.eye(18, 7, "y"); c.line(13, 10, 19, 10, "e"); for (const x of [14, 16, 18]) c.px(x, 10, "l");
c.list([[10, 12, "l"], [22, 12, "l"], [12, 10, "k"], [21, 10, "k"]]);
export const rows = c.rows();
