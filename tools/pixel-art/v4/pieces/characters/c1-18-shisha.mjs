import { charBase, overrides } from "../../lib4.mjs";
import { hs, st, face, mass, rs, finish } from "../../c1-kit.mjs";
// 合議会の使者。金のバッジつきの平たい制帽・きちんとなでつけた黒髪・金のふちの紫の短いマント・肩から斜めにかけた書類かばん・白い手ぶくろで封蝋つきの手紙をかかげる。背すじの伸びた細身の姿。
export const name = "合議会の使者"; export const category = "character";
export const pal = {
  p: "#1c1a2c", "1": "#2c2a44", "2": "#44405e", "3": "#5e5a80", "4": "#8480aa",
  r: "#241848", J: "#38286e", j: "#54409a", k: "#7862c4", K: "#a898ec", C: "#f4f0fa", y: "#c8c0d8",
  A: "#e0b048", X: "#fff0b0", o: "#a8741c", Q: "#a8a4bc", P: "#6e6a88", s: "#2a2030", t: "#b02c30", W: "#fbf8f0", m: "#8a8098", i: "#3a4a78",
};
const raw = overrides(charBase({ hair: 0 }), [
  // 手紙をかかげる右手（画面右）
  ...mass(11, rs("25-27", "24-26", "23-25", "22-24"), "KkjJ", { out: "r" }), ...st(9, ["25|qcc", "25|qcc"]),
  ...st(3, ["25|rrrrrr", "25|rWWWWr", "25|rWttWr", "25|rWWWWr", "25|rrrrrr"]),
  // 左腕
  ...mass(14, rs("8-9", "7-9", "7-9", "7-9", "7-9", "7-9"), "KkjJ", { out: "r", folds: [[8, 17, 19]] }),
  ...st(20, ["7|Cy", "7|yC", "7|qc"]),
  // 制服
  ...mass(13, rs("10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21"), "KkjJ", { out: "r", strand: [1, 6], folds: [[12, 16, 22], [19, 17, 22]] }),
  ...st(13, ["14|Cc", "14|CCCC", "15|CC"]), ...st(14, ["15|tt", "15|tt"]),
  ...st(16, ["14|A", "14|A", "14|A"]), ...st(16, ["17|A", "17|A", "17|A"]),
  // 金のふちの短いマント（肩）
  ...mass(13, rs("8-13", "7-12", "7-11", "7-10"), "jJJr", { out: "A", outB: "o", strand: [1, 4] }), ...mass(13, rs("18-23", "19-24", "20-24", "21-24"), "JJrr", { out: "A", outB: "o" }),
  // かばん（肩から斜めに）
  ...st(14, ["20|P"]), ...st(15, ["19|P"]), ...st(16, ["18|P"]), ...mass(19, rs("18-23", "18-23", "18-23", "18-23"), "QPmm", { out: "m" }), ...st(20, ["20|AA"]),
  // 腰と脚
  ...st(22, ["10|CCCCCCCCCCCC"]), ...st(22, ["10|yyyyyyyyyyyy"]).slice(0, 0),
  ...st(23, ["11|QQQP", "11|QQQP", "11|QQQP"]), ...st(23, ["17|QPPP", "17|QPPP", "17|QPPP"]),
  ...st(26, ["10|ssssss", "10|ssssss", "10|ssssss"]), ...st(26, ["17|ssssss", "17|ssssss", "17|ssssss"]),
  // 髪と制帽
  ...mass(3, rs("10-21", "9-22", "8-23", "8-23", "8-23"), "3221", { out: "p", outB: "1", strand: [1, 4] }),
  ...hs(7, ["8|p2", "8|p1"]),
  ...mass(0, rs("10-21", "9-22", "9-22", "9-22"), "jjJr", { out: "r" }), ...st(0, ["10|kk"]),
  ...mass(4, rs("8-23", "8-23"), "PPmm", { out: "m" }),
  ...st(2, ["14|AA", "14|AX", "15|A"]),
  ...face({ eye: "std", brow: "p", mouth: "flat", ic: "i" }),
]);
export const rows = finish(raw, pal);
