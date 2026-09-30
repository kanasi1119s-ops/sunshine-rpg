import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 金髪のお姫様（マップ用 16×24・4方向×3コマ）。長い金髪・小さな金の冠（赤い宝石）・ピンクのドレス（ひろがるすそ・金のふち）。目は青。
export const name = "金髪のお姫様（マップ用・4方向）"; export const category = "map-character";
export const pal = palFrom({ skin: ["#d99a88", "#f9d0b6", "#f4a0a4"], hair: ["#b07e1c", "#f0c23c", "#fff08a"], cloth: ["#b04a7c", "#ec8cb8", "#ffc8e2"], trim: "#ffd84a", accent: "#f2b428", accent2: "#c0508a", pants: ["#8a4a6a", "#c07a9a"], boots: ["#6a3a50", "#a8607e"], eye: "#26389a", jewel: "#e0405c", gold2: "#fff0a0", outline: "#2a1a30" });
export const frames = makeSheet({ hair: "long", outfit: "gown", acc: ["crown"] });
export const rows = sheetRows(frames);
