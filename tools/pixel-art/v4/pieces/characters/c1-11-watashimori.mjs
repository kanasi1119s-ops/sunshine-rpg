import { charBase, overrides } from "../../lib4.mjs";
import { hs, st, face, mass, rs, finish } from "../../c1-kit.mjs";
// 硝子湖の渡し守。水色の頭巾（結び目が右うしろに出る）・海の青灰のうわっぱり・縄の帯・ズボンをまくって素足にわらじ・右にたてた長いかい（オール）・腰の小さなガラスの灯り。
export const name = "硝子湖の渡し守"; export const category = "character";
export const pal = {
  p: "#3a3436", "1": "#5c5456", "2": "#847a7a", "3": "#aca4a0", "4": "#d0c8c0",
  r: "#1a3440", J: "#2c5462", j: "#4a8090", k: "#78b0b8", K: "#b8e0dc", C: "#f0eee0", y: "#c8b48c", Q: "#9a7248", P: "#6a4a30",
  W: "#8cc8f0", S: "#3a8ac8", u: "#1e4a82", X: "#fff0a8", A: "#e8b030", s: "#3a2a24", i: "#3a5a70", M: "#c8dcf0",
};
const raw = overrides(charBase({ hair: 0 }), [
  // かい（オール）: 水かきの部分は上、柄は長く
  ...mass(9, rs(...Array(21).fill("27-28")), "yQQP", { out: "P", noTop: true }),
  ...mass(1, rs("28-29", "26-30", "26-30", "26-30", "26-30", "26-30", "27-29", "27-29"), "yyQP", { out: "P", strand: [1, 5] }),
  // 腕
  ...mass(14, rs("8-9", "7-9", "7-9", "7-9", "7-9", "7-9"), "KkjJ", { out: "r", folds: [[8, 17, 19]] }), ...mass(14, rs("22-23", "22-24", "22-24", "22-24", "22-24", "22-24"), "kjJJ", { out: "r" }),
  ...st(20, ["25|qc", "25|qb"]), ...st(20, ["24|cc"]), ...st(19, ["25|qcc"]),
  // うわっぱり
  ...mass(13, rs("10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "9-22", "9-22", "9-22"), "KkjJ", { out: "r", strand: [1, 6], folds: [[13, 16, 24], [19, 17, 24]] }),
  ...st(13, ["14|Cc", "14|CCCC", "15|CC"]),
  // 波もよう
  ...st(23, ["10|kJkJkJkJkJkJ"]),
  // 縄の帯
  ...st(19, ["10|yyQyyQyyQyyQ"]),
  // 腰の灯り
  ...st(19, ["21|Q", "21|Q", "21|rMMr", "21|rMXr", "21|rMMr", "21|rrrr"]),
  // まくったズボンと素足・わらじ
  ...st(24, ["11|yyyP", "11|yyyP", "11|bbba", "11|bbba"]), ...st(24, ["17|yPPP", "17|yPPP", "17|bbaa", "17|bbaa"]),
  ...st(28, ["10|QQQQQ", "10|PPPPP"]), ...st(28, ["17|QQQQQ", "17|PPPPP"]),
  // 頭巾
  ...mass(1, rs("12-19", "9-22", "8-23", "8-23", "8-23", "8-23"), "WSSu", { out: "u", outB: "u", strand: [1, 4] }),
  ...st(3, ["23|SS", "24|SuS", "24|Suu", "25|uu"]),
  ...hs(6, ["9|c c u u c"]),
  ...hs(7, ["8|q1", "8|q1"]),
  ...face({ eye: "narrow", brow: "1", mouth: "flat", ic: "i" }),
  // ひげのそりあと
  [12, 11, "a"], [14, 12, "a"], [17, 12, "a"], [19, 11, "a"],
]);
export const rows = finish(raw, pal);
