import { mirror, overrides } from "./sprite.mjs";
// 薬草（葉を束ねた回復のアイテム）。左半分を描いて鏡写しにした、オリジナルの絵。
export const pal = { p: "#0e2416", G: "#2a6a30", g: "#4a9a44", h: "#88d060", H: "#c8f890", b: "#7a5a30", B: "#a88048", r: "#d8404a", s: "#1a2a1a", w: "#ffffff" };
const half = [
"................", "................", "................", "...........pp...", "..........pgHp..", ".........pghhHp.", "........pgghhhp.", "........pgghhgp.", ".....pp.pggghgp.", "....pgHppgggggp.", "...pghhHpgGggGp.", "..pgghhhppGGGpp.", "..pgghhgphpppGp.", "...pgggpphGpppp.", "...pGGGpppGGp.p.", "....pGGpp.pGGpp.",
".....ppp.ppGGp..", ".........pGGGp..", "..........pGGp..", "..........pbBp..", "..........pbBp..", "..........pbBp..", ".........pbBBbp.", "..........pppp..", "................", "................", "................", "................", "................", "................", "................", "................",
];
const L = [];
for (let y = 5; y <= 17; y++) L.push([15, y, y % 3 ? "g" : "h"], [16, y, y % 3 ? "g" : "G"]);
L.push([15, 4, "H"], [16, 4, "H"], [11, 9, "H"], [12, 10, "H"], [13, 6, "H"]);
for (const [x, y] of [[15, 18], [16, 18], [15, 19], [16, 19]]) L.push([x, y, "r"]);   // 束ねる赤いひも
for (let x = 9; x <= 22; x++) L.push([x, 24, "s"]);
export const rows = overrides(mirror(half), L);
