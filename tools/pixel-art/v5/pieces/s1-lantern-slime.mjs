import { Cv, ramp } from "../lib5.mjs";
// 灯苔スライム（小型 64×64）: 苔むした半透明のスライム。頭の上に小さな灯りキノコが生えている。
export const name = "灯苔スライム"; export const category = "monster"; export const size = 64;
export const pal = { ...ramp("abcde", "#173a2c", "#a8e08a", "#3f9a5a"), ...ramp("fgh", "#20402a", "#7ac860"), o: "#0b1a16", w: "#ffffff", E: "#10141c", ...ramp("ijk", "#a06a20", "#fff0a0"), y: "#fff8c8", z: "#0b1a16", ...ramp("lm", "#5a3a2a", "#a87a52"), s: "#0d2a2a", q: "#b8c890" };
const c = new Cv(64);
const body = c.union(c.ell(32, 42, 24, 15), c.ell(32, 34, 19, 15), c.rect(10, 44, 54, 53));
const bodyM = c.sub(body, c.rect(0, 54, 63, 63));
c.paint(bodyM, "abcde", { round: 14 });
// 底のふくらみ（地面に接する側は暗く）
c.speckle(c.inter(bodyM, c.rect(0, 46, 63, 54)), "a", 0.18, 3);
// つや（ぬれた光）
c.fill(c.ell(21, 30, 4, 2.4), "d"); c.fill(c.ell(20, 29, 2.4, 1.2), "y"); c.put(28, 27, "y"); c.put(29, 27, "y");
// 苔のかたまり（背中と横）
const moss = c.union(c.ell(42, 24, 8, 4.5), c.ell(50, 33, 5, 3.5), c.ell(16, 40, 4, 3));
c.paint(c.inter(moss, bodyM), "fgh", { round: 3 });
c.speckle(c.inter(moss, bodyM), "h", 0.15, 7);
// 目と口
c.fill(c.ell(25, 38, 4.5, 5.5), "z"); c.fill(c.ell(39, 38, 4.5, 5.5), "z");
c.fill(c.ell(25, 38, 3.4, 4.4), "E"); c.fill(c.ell(39, 38, 3.4, 4.4), "E");
c.fill(c.ell(24, 36, 1.5, 1.6), "w"); c.fill(c.ell(38, 36, 1.5, 1.6), "w"); c.put(26, 40, "y"); c.put(40, 40, "y");
c.line(28, 46, 31, 48, "o"); c.line(31, 48, 34, 48, "o"); c.line(34, 48, 37, 46, "o");
// 灯りキノコ（頭の上）
c.fill(c.rect(31, 12, 33, 19), "l"); c.fill(c.rect(31, 12, 31, 19), "m"); c.put(33, 18, "m");
const cap = c.ell(32, 11, 7, 5); c.paint(c.sub(cap, c.rect(0, 13, 63, 63)), "ijk", { round: 4, dither: false });
c.put(29, 9, "y"); c.put(30, 9, "y"); c.put(36, 11, "j"); c.put(34, 8, "y");
// 灯りのにじみ
c.outline("o", { a: "o", b: "a", i: "o", j: "l", k: "j", l: "o", m: "l" });
c.despeckle("wyEq");
c.shadow(32, 55, 25, 3.5, "s", false);
for (const [x, y] of [[24, 7], [40, 8], [26, 4], [38, 4], [32, 2]]) c.put(x, y, "q");
export const rows = c.rows();
