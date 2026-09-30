import { Cv, R } from "../../lib4.mjs";
// 鉄鎖の亡霊: 鎖に縛られたまま死んだ坑夫の霊。ぼろぼろのフードと、青白い光る目。
export const name = "鉄鎖の亡霊"; export const category = "monster";
export const pal = { ...R("abcde", "#1a2440", "#c8e0f8", "#5a7ab0"), ...R("fgh", "#6a6a80", "#f0f0ff"), z: "#101830", w: "#ffffff", e: "#06081a", y: "#a8f0ff" };
const c = new Cv();
c.shadow(16, 30, 7, "z");
c.poly([[16, 3], [9, 8], [7, 18], [4, 28], [8, 26], [11, 29], [14, 26], [17, 29], [20, 26], [23, 29], [26, 27], [25, 18], [23, 8]], "abcde", { lx: 0.35, dither: true });
c.ell(16, 11, 5, 6, "eeee", { outline: false });                                          // フードの奥
c.eye(12, 10, "y"); c.eye(18, 10, "y"); c.px(14, 15, "a"); c.px(15, 15, "a"); c.px(16, 15, "a"); c.px(17, 15, "a");
c.ell(16, 11, 5, 6, "aaaa", { outline: false }); c.ell(16, 11, 4, 5, "eeee", { outline: false }); c.eye(12, 10, "y"); c.eye(18, 10, "y"); c.line(14, 15, 17, 15, "a");
c.ell(6, 18, 2, 2, "abcde"); c.ell(26, 18, 2, 2, "abcde");                                // 手
const link = (x, y, v) => { if (v) c.box(x, y, x + 1, y + 2, "fghh"); else c.box(x, y, x + 2, y + 1, "fghh"); };
let k = 0; for (let t = 0; t <= 8; t++) { const x = 6 + t * 2.5, y = 19 + Math.sin(t * 0.8) * 3 + t * 0.6; link(Math.round(x), Math.round(y), k++ % 2); }   // 胸の鎖
for (const y of [9, 12, 15]) { c.line(9 + (y - 9) / 2, y, 12, y - 1, "b"); }
for (let y = 3; y < 8; y += 2) link(22 + (y - 3), y, y % 4 === 1);
c.list([[8, 22, "c"], [9, 24, "c"], [24, 22, "c"], [12, 26, "d"], [19, 27, "d"]]);
export const rows = c.rows();
