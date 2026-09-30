import { mirror, overrides } from "./sprite.mjs";
// 灯り蛾（小さな敵。灯りに集まる、羽が光る蛾）。左半分を描いて鏡写しにした、オリジナルの絵。
export const pal = { p: "#1c1230", "1": "#4a3a78", "2": "#7a68b8", "3": "#b0a0e8", "4": "#e8e0ff", A: "#ffd870", X: "#fff4b8", e: "#2a1a40", w: "#ffffff", b: "#6a4a3a", B: "#a08060", s: "#22183a", i: "#ff7a9a" };
const half = [
"................", "................", "....p...........", "....pp..........", ".....pp.......pp", "......pp....pppb", ".......pp..pbBBb", "...pppp.ppppbBBb", "..p3333pp44pbBBb", ".p333444p4444ebB", ".p33444ppp444eeB", ".p3344ppXXpp44Bb", ".p344ppXXXXpp4bb",
".pp44ppXXAApp444", "..p444pXAAAAp444", "..p444pXAAAAp44b", "..pp44pXAAAAp44b", "...p44ppXAAppp4b", "...pp44pppXppp4b", "....pp444pppp444", "....p44444pppp44", ".....pp4444pppp4", "......ppp444pbBb", "........pp44ppbB", "..........pppp.b", "................", "................", "................", "................", "................", "................", "................",
];
const L = [];
for (const x0 of [12, 17]) { L.push([x0, 9, "e"], [x0 + 1, 9, "e"], [x0, 10, "w"], [x0 + 1, 10, "e"]); }   // 目
L.push([13, 4, "b"], [12, 3, "b"], [11, 2, "b"], [18, 4, "b"], [19, 3, "b"], [20, 2, "b"]);   // 触角
for (const [x, y] of [[4, 6], [27, 6], [3, 18], [28, 18], [8, 3], [23, 3]]) L.push([x, y, "X"]);
for (let x = 9; x <= 22; x++) L.push([x, 27, "s"]);
export const rows = overrides(mirror(half), L);
