import { Cv, R } from "../../lib4.mjs";
// 実験の失敗作: 鉱山の秘密の実験でできそこなった、つぎはぎの生き物。目が大小ばらばら。
export const name = "実験の失敗作"; export const category = "monster";
export const pal = { ...R("abcde", "#3a1428", "#ffc0b8", "#c0687a"), ...R("fgh", "#1a4a3a", "#9af0b0"), ...R("ij", "#4a4a5a", "#c8c8d8"), z: "#1c1020", w: "#ffffff", e: "#100810", y: "#ffe040", r: "#e03a4a" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
c.poly([[24, 20], [30, 14], [31, 21], [28, 24]], "fgh"); c.line(30, 14, 31, 10, "f"); c.line(31, 21, 31, 26, "f");            // 余分な腕
c.ell(22, 19, 6, 6, "fgh"); 
c.ell(16, 22, 9, 7, "abcde", { dither: true });                                        // 体
c.ell(9, 27, 3, 2, "abcd"); c.ell(21, 28, 4, 1, "abcd"); c.ell(15, 28, 2, 1, "fgh");
c.line(8, 20, 24, 24, "a"); for (let x = 9; x <= 23; x += 2) { c.px(x, 19 + Math.round((x - 8) / 4) - 0, "j"); c.px(x, 21 + Math.round((x - 8) / 4), "j"); }   // 縫い目
c.ell(11, 15, 4, 4, "abcde"); c.ell(11, 15, 3, 3, "hhhhh", { outline: false }); c.ell(11, 15, 3, 3, "yyyyy", { outline: false }); c.box(10, 15, 12, 17, "eeee", { outline: false }); c.px(9, 13, "w"); c.px(10, 13, "w");   // 大きな目
c.eye(20, 14, "y"); c.px(24, 17, "y"); c.px(24, 18, "e"); c.px(17, 17, "w"); c.px(17, 18, "e");
c.box(16, 4, 17, 9, "ij"); c.px(16, 3, "j"); c.box(14, 9, 19, 10, "ij", { outline: false }); c.line(16, 4, 20, 2, "i");       // ボルトとパイプ
c.ell(24, 23, 1, 1, "rrr");
c.line(13, 24, 20, 25, "e"); for (const x of [14, 16, 18]) c.px(x, 25, "w");
c.list([[13, 12, "d"], [8, 19, "d"], [26, 17, "h"], [27, 16, "h"]]);
export const rows = c.rows();
