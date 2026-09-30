import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 八神の一柱・無神「在らざる歌」（裏ボス）。何も語らない白い仮面と、欠けた円環。完全オリジナル。
export const name = "八神の一柱";
export const category = "boss";
export const pal = { p: "#141a24", "1": "#3a4658", "2": "#6a7a92", "3": "#a4b4c8", "4": "#e0e8f4", c: "#30c0c8", C: "#b8fcff", e: "#0a1018", w: "#ffffff", r: "#405068", R: "#8ea0b8", s: "#dcd0a8", S: "#8a7c58", D: "#1a2030", v: "#7a6cd0" };
const c = cv(); const MK = "p1234", RB = "pSsss".slice(0, 5), RG = "1r2R3";
ground(c, 16, 30, 8, 1.2, "D");
// 円環（大きな輪。数か所が欠け、目盛りが刻まれる）
for (let t = 0; t < 720; t++) { const a = (t / 720) * Math.PI * 2; const k = Math.floor((t / 720) * 12); if (k === 4 || k === 10) continue; for (const r of [14.6, 13.6, 12.6]) { const x = 15.5 + r * Math.cos(a), y = 14.5 + r * Math.sin(a); const lit = -Math.cos(a) * 0.6 - Math.sin(a) * 0.75 > 0.25; c.put(x, y, r > 14 ? (lit ? "R" : "r") : r > 13 ? (lit ? "3" : "2") : (lit ? "2" : "1")); } }
for (let t = 0; t < 12; t++) { const a = (t / 12) * Math.PI * 2 + 0.26; if (t === 4 || t === 10) continue; const x = 15.5 + 13.6 * Math.cos(a), y = 14.5 + 13.6 * Math.sin(a); c.put(x, y, "C"); }
// 衣（下へ行くほどほどけて消える）
poly(c, [[9, 19], [23, 19], [26, 27], [6, 27]], MK);
for (const [x, y] of [[8, 29], [12, 30], [17, 29], [21, 30], [24, 29], [5, 28], [27, 28]]) { c.put(x, y, "2"); c.put(x + 1, y, "1"); }
for (const x of [11, 16, 21]) bline(c, x, 21, x - (x - 16) / 3, 27, "1");
// 手（合わせた白い指）
box(c, 14, 22, 17, 25, "p1234"); c.put(15, 23, "w");
// 仮面（顔は白い円。口がない）
ell(c, 16, 11, 7, 8, MK);
// 目（細い切れ込みに青緑の光）
for (const x of [12, 18]) { for (let dx = 0; dx < 3; dx++) c.put(x + dx, 11 + (dx === 1 ? 0 : 0), "e"); c.put(x + 1, 11, "c"); c.put(x + 1, 12, "c"); c.put(x, 10, "e"); c.put(x + 2, 10, "e"); }
c.put(12, 10, "w"); c.put(18, 10, "w");
// 額の印と涙のすじ
fillEll(c, 16, 6, 1, 1, "c"); c.put(16, 6, "C"); for (let y = 13; y <= 16; y++) { c.put(11, y, "v"); c.put(21, y, "v"); }
// 仮面のひび
bline(c, 16, 15, 15, 18, "1");
export const rows = c.rows();
