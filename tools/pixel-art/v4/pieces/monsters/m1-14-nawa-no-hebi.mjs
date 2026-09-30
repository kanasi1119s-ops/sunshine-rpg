import { Cv, R } from "../../lib4.mjs";
// 縄の蛇: 太い船の縄が蛇のようにとぐろを巻いた敵。縄のよりもようが体のしま。
export const name = "縄の蛇"; export const category = "monster";
export const pal = { ...R("abcde", "#2a1c0c", "#e8cc90", "#a88450"), ...R("fghi", "#3a2410", "#c8a468"), z: "#1c140a", w: "#ffffff", e: "#100a04", r: "#e83a3a", y: "#ffd040" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
const path = []; for (let i = 0; i <= 40; i++) { const t = i / 40; const a = Math.PI * 2 * 1.7 * t + 0.4; const rad = 11 - t * 4; path.push([16 + Math.cos(a) * rad * 1.05, 25 - t * 4 + Math.sin(a) * rad * 0.34 - t * 9]); }
path.forEach(([x, y], i) => c.ell(x, y, 2, 2, i % 2 ? "acdee" : "afghh", { outline: false }));
c.outlineAround("a"); c.ell(8, 7, 5, 4, "abcde");                                                           // 頭
c.poly([[4, 8], [0, 10], [4, 11]], "abcde");
c.line(3, 11, 1, 13, "r"); c.line(1, 13, 0, 13, "r"); c.line(1, 13, 1, 15, "r");     // 舌
c.eye(7, 5, "y"); c.px(9, 5, "e"); c.px(9, 6, "e"); c.line(4, 10, 8, 10, "e");
c.list([[7, 3, "d"], [8, 3, "d"], [12, 8, "b"], [13, 9, "a"]]);
export const rows = c.rows();
