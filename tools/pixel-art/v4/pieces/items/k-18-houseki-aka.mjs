import { kNew, kPoly, kPut, kOutline, kRows } from "../../lib4.mjs";
// 宝石（赤）: 上から見た八角のカット。面ごとに光の向きで明るさが変わる。
export const name = "宝石（赤）";
export const category = "item";
export const pal = { o: "#2a0818", W: "#fff0f4", h: "#ffb0c0", t: "#f0506c", r: "#d02048", R: "#a01038", d: "#700a2c", D: "#4c0620", w: "#ffffff", s: "#ffe8b0" };
const g = kNew();
const cx = 16, cy = 16;
const oc = (k, R) => [cx + R * Math.cos((Math.PI / 4) * k + Math.PI / 8), cy + R * Math.sin((Math.PI / 4) * k + Math.PI / 8)];
const ramp = ["d", "R", "r", "t", "h", "t", "r", "R"]; // 面の向き別（光は左上）
kPoly(g, Array.from({ length: 8 }, (_, k) => oc(k, 13.6)), "r");
for (let k = 0; k < 8; k++) {
  const a = oc(k, 13.6), b = oc(k + 1, 13.6), c = oc(k + 1, 7), d = oc(k, 7);
  // 面の向き: 中心から見た角度。左上(k=4,5付近)を明るく
  const ang = (k + 0.5) * 45 + 22.5; // 度、右=0 下=90
  const light = Math.cos(((ang - 225) * Math.PI) / 180); // 左上=225度
  const c1 = light > 0.8 ? "h" : light > 0.3 ? "t" : light > -0.3 ? "r" : light > -0.8 ? "R" : "d";
  kPoly(g, [a, b, c, d], c1);
  // 三角の面（ふちの角を割る）
}
kPoly(g, Array.from({ length: 8 }, (_, k) => oc(k, 7)), "t");
kPoly(g, Array.from({ length: 8 }, (_, k) => oc(k, 4)), "h");
// テーブル面のなかの明暗
kPoly(g, [[10, 12], [16, 9], [18, 10], [12, 14]], "W");
const r0 = kOutline(g, { h: "R", t: "d", r: "D", R: "D", d: "D", W: "R" }, "o");
for (const [x, y, c] of [[11, 11, "w"], [12, 10, "w"], [10, 12, "w"], [9, 8, "h"], [22, 21, "R"], [16, 17, "r"], [24, 12, "s"], [24, 11, "w"], [24, 13, "w"], [23, 12, "w"], [25, 12, "w"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
