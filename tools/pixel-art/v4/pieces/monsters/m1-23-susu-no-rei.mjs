import { Cv, R, rng } from "../../lib4.mjs";
// 煤の霊: 鉱山の煤がまとまって生まれた、ふわふわの黒い霊。大きな目と小さな火の粉。
export const name = "煤の霊"; export const category = "monster";
export const pal = { ...R("abcde", "#0a080e", "#5a5468", "#2a2634"), ...R("fgh", "#c04010", "#ffe070"), z: "#0e0a14", w: "#ffffff", e: "#08060c", y: "#e8e0d0" };
const c = new Cv(); const r = rng(11);
c.shadow(16, 30, 9, "z");
c.ell(16, 19, 9, 8, "bcdde", { outline: false, dither: true });
// 毛羽立ち: 縁の外側にとげ状の煤を出す
for (let a = 0; a < 40; a++) { const t = (a / 40) * Math.PI * 2; const len = 2 + Math.floor(r() * 3); for (let k = 0; k < len; k++) { const x = 16 + Math.cos(t) * (9.5 + k), y = 19 + Math.sin(t) * (8.5 + k); if (y < 29) c.px(x, y, k < len - 1 ? "c" : "b"); } }
c.ell(16, 19, 8, 7, "bcdde", { outline: false, dither: true }); c.line(9, 26, 23, 26, "b");
c.ell(11, 18, 3, 3, "yyyy", { outline: false }); c.ell(21, 18, 3, 3, "yyyy", { outline: false });
c.box(11, 18, 12, 20, "eeee", { outline: false }); c.box(21, 18, 22, 20, "eeee", { outline: false }); c.px(10, 16, "w"); c.px(20, 16, "w"); c.px(11, 17, "w"); c.px(21, 17, "w");
c.line(14, 24, 18, 24, "e"); c.px(13, 23, "e"); c.px(19, 23, "e");
c.list([[14, 12, "h"], [26, 10, "g"], [5, 12, "g"], [24, 6, "f"], [8, 7, "h"], [28, 17, "f"]]);
c.list([[12, 14, "d"], [13, 13, "d"], [15, 14, "d"], [8, 20, "d"]]);
export const rows = c.rows();
