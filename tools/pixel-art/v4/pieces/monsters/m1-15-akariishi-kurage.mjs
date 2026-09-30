import { Cv, R } from "../../lib4.mjs";
// 灯り石のくらげ: かさの中に灯り石を抱いた、ふわふわ浮くクラゲ。
export const name = "灯り石のくらげ"; export const category = "monster";
export const pal = { ...R("abcde", "#1a2a5a", "#d8f0ff", "#5a9ad8"), ...R("fgh", "#3a5a9a", "#a8d0f0"), ...R("jklm", "#c06010", "#fff8b0"), z: "#101a34", w: "#ffffff", e: "#0a1230", r: "#ff6a8a" };
const c = new Cv();
c.shadow(16, 30, 6, "z");
const wave = (x0, ph, len) => { for (let y = 17; y < 17 + len; y++) c.px(x0 + Math.round(Math.sin(y * 0.8 + ph) * 1.4), y, y % 3 ? "h" : "c"); };
for (const [x, ph, len] of [[8, 0, 9], [12, 1.5, 12], [16, 3, 10], [20, 4.5, 12], [24, 6, 9]]) wave(x, ph, len);
c.shape((x, y) => ((x - 16) / 10.5) ** 2 + ((y - 17) / 10) ** 2 <= 1 && y <= 18, 6, 6, 26, 18, "abcde", { dither: true });
c.line(7, 18, 25, 18, "a");
for (const x of [9, 13, 19, 23]) c.px(x, 18, "f");
c.ell(16, 11, 3, 3, "jklm"); c.px(15, 10, "m"); c.px(14, 9, "w");
c.eye(9, 14, "e", "w"); c.eye(21, 14, "e", "w"); c.px(12, 16, "r"); c.px(19, 16, "r");
c.list([[10, 8, "d"], [11, 7, "e"], [12, 6, "e"], [9, 10, "e"], [22, 9, "c"], [26, 6, "h"], [4, 4, "w"], [27, 25, "h"], [5, 24, "h"]]);
export const rows = c.rows();
