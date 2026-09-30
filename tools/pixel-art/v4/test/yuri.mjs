import { charBase, overrides, sym, rect } from "../lib4.mjs";
export const name = "ユーリ（2.5頭身）"; export const category = "character";
export const pal = {};
export const rows = overrides(charBase({ hair: 5, fringe: "spiky" }), [
  ...sym([[9, 1, "p"], [10, 1, "p"], [8, 2, "p"]]),        // 髪のはね
  [23, 19, "A"], [24, 19, "A"],
]);
