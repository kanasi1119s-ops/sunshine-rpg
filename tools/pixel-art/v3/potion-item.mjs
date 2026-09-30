import { mirror, overrides } from "./sprite.mjs";
// 回復薬（赤いびん）。左半分を描いて鏡写しにした、オリジナルの絵。
export const pal = { p: "#1a1030", G: "#7ac4e0", g: "#c0eefa", L: "#d02840", l: "#f0607a", D: "#801828", c: "#b07038", C: "#e0a868", w: "#ffffff", s: "#2a1a3a", y: "#ff9aa8" };
const half = [
"................", "................", "................", ".............ppp", ".............pcC", ".............pcC", ".............ppp", "..............pG",
"..............pG", "..............pG", "............pppG", "..........ppGGGG", ".........pGllLLL", "........pGllLLLL", ".......pGGlLLLLL", ".......pGlLLLLLL",
"......pGGlLLLLLL", "......pGlLLLLLLL", "......pGlLLLLLLL", "......pGlLLLLLLL", "......pGLLLLLLDD", "......pGLLLLLDDD", ".......pGLLLDDDD", ".......pGLLDDDDD",
"........pGLDDDDD", ".........pGGDDDD", "..........ppGGGG", "............pppp", "................", "................", "................", "................",
];
const L = [[10, 14, "w"], [10, 15, "w"], [11, 13, "w"], [10, 17, "g"], [12, 12, "y"], [13, 12, "y"], [19, 21, "l"], [21, 19, "l"], [17, 24, "y"]];
for (let x = 9; x <= 22; x++) L.push([x, 28, "s"]);
export const rows = overrides(mirror(half), L);
