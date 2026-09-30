import { charBase, overrides } from "../../lib4.mjs";
import { hs, st, face, mass, rs } from "../../c1-kit.mjs";
// 麦香野の村長。大きな麦わら帽子・真っ白なまゆ毛と長いひげ・麦の穂を挿した若草色のうわっぱり・縄の帯・木のつえ。少し小柄でまるい老人。
export const name = "麦香野の村長"; export const category = "character";
export const pal = {
  p: "#7a5a20", "1": "#a8802c", "2": "#d0a848", "3": "#ecc860", "4": "#fff0a0",
  r: "#3e4a1c", J: "#5e7028", j: "#88983c", k: "#b0c060", K: "#dce890", C: "#fbf8ee", y: "#c8b890", Q: "#8a5a34", P: "#5a3a22",
  A: "#e8b838", X: "#fff0a8", i: "#4a6a48", s: "#3a2a1e", W: "#e8e4dc", m: "#b8b0a0",
};
export const rows = overrides(charBase({ hair: 0 }), [
  // つえ（右手＝画面右）
  ...mass(12, rs(...Array(18).fill("27-28")), "yQQP", { out: "P", noTop: true }), ...st(10, ["26|QQQ", "26|yQQ"]),
  // 腕
  ...mass(14, rs("8-9", "7-9", "7-9", "7-9", "7-9", "7-9"), "KkjJ", { out: "r", folds: [[8, 17, 19]] }), ...mass(14, rs("22-23", "22-24", "22-24", "22-24", "22-24", "22-24"), "kjJJ", { out: "r" }),
  ...st(20, ["25|qcc", "25|qbb"]),
  // うわっぱり（膝上まで）
  ...mass(13, rs("10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "9-22", "9-22", "9-22", "8-23"), "KkjJ", { out: "r", strand: [1, 6], folds: [[13, 16, 24], [18, 17, 23]] }),
  ...st(13, ["14|Cc", "14|CCCC", "15|CC"]),
  // 縄の帯
  ...st(20, ["10|yyPyyPyyPyyP"]), ...st(21, ["9|yPyPyPyPyPyPyP"]),
  // 麦の穂（左胸）
  ...st(14, ["11|A", "10|A", "11|AA", "11|A"]), ...st(18, ["12|J"]),
  // ズボン（すそをまくった）
  ...st(25, ["11|yyyP", "11|yyyP"]), ...st(25, ["17|yPPP", "17|yPPP"]),
  // 顔: まゆ毛・目・長いひげ
  ...face({ eye: "narrow", brow: "W", mouth: "none", ic: "i", blush: false }),
  ...mass(10, rs("9-22", "9-22", "10-21", "11-20", "12-19", "13-18", "14-17", "15-16"), "CWWm", { out: "m", strand: [1, 4] }),
  [15, 10, "C"], [16, 10, "C"], [10, 10, "B"], [21, 10, "B"], [15, 9, "b"], [16, 9, "b"],
  // 麦わら帽子
  ...mass(1, rs("11-20", "9-22", "8-23"), "4321", { out: "p", strand: [1, 5] }),
  ...mass(4, rs("3-28", "2-29", "3-28"), "3221", { out: "p", strand: [1, 4], folds: [[7, 4, 6], [15, 4, 6], [24, 4, 6]] }),
  ...st(3, ["8|PPPPPPPPPPPPPPPP"]),
  ...st(7, ["8|p", "8|p"]), ...st(7, ["23|p", "23|p"]),
  ...face({ eye: "narrow", brow: "W", mouth: "none", ic: "i", blush: false }).filter(([x, y]) => y >= 6 && y <= 9),
]);
