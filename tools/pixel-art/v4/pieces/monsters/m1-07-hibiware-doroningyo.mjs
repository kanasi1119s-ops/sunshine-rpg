import { Cv, R } from "../../lib4.mjs";
// ひび割れ泥人形: 乾いた泥をこねた人形。ひびの奥に熱い光がもれる。
export const name = "ひび割れ泥人形"; export const category = "monster";
export const pal = { ...R("abcde", "#2a1610", "#c89060", "#7a4a30"), ...R("fgh", "#c04010", "#ffd060"), z: "#1c100c", w: "#ffffff", e: "#1a0c08" };
const c = new Cv();
c.shadow(16, 30, 11, "z");
c.box(11, 24, 14, 29, "abcde"); c.box(17, 24, 20, 29, "abcde");                      // 足
c.box(4, 13, 8, 23, "abcde"); c.box(23, 13, 27, 23, "abcde");                        // 腕
c.ell(5, 24, 3, 3, "abcde"); c.ell(26, 24, 3, 3, "abcde");                           // 手
c.box(9, 12, 22, 25, "abcde", { dither: true });                                     // 胴
c.ell(16, 8, 5, 5, "abcde");                                                         // 頭
c.ell(6, 12, 3, 2, "abcde"); c.ell(25, 12, 3, 2, "abcde");                           // 肩
c.list([[14, 13, "f"], [15, 14, "g"], [15, 15, "g"], [16, 16, "f"], [17, 17, "g"], [17, 18, "h"], [16, 19, "g"], [16, 20, "f"], [15, 21, "f"]]);
c.list([[11, 20, "f"], [12, 21, "g"], [13, 22, "f"], [20, 15, "f"], [20, 16, "g"], [21, 17, "f"], [6, 16, "f"], [6, 17, "g"], [7, 18, "f"], [25, 18, "f"], [24, 19, "g"]]);
c.list([[12, 26, "e"], [13, 27, "e"], [18, 27, "e"], [19, 28, "e"]]);
c.box(12, 7, 14, 9, "eeee", { outline: false }); c.box(18, 7, 20, 9, "eeee", { outline: false }); c.px(12, 7, "w"); c.px(18, 7, "w"); c.px(13, 8, "h"); c.px(19, 8, "h"); c.px(14, 9, "g"); c.px(20, 9, "g");
c.line(14, 12, 18, 12, "e"); c.line(15, 5, 16, 6, "f");
export const rows = c.rows();
