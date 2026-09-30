import { Cv, R } from "../../lib4.mjs";
// 岩喰い: 岩を丸のみにする、口ばかりの大きな岩の獣。岩のような牙が並ぶ。
export const name = "岩喰い"; export const category = "monster";
export const pal = { ...R("abcde", "#1e1a20", "#b0a498", "#6a5e5a"), ...R("fgh", "#3a0e18", "#d84a4a"), ...R("ij", "#e8e0d0", "#ffffff"), z: "#14101a", w: "#ffffff", e: "#0a0608", y: "#ffd040" };
const c = new Cv();
c.shadow(16, 30, 13, "z");
c.ell(16, 20, 13, 9, "abcde", { dither: true });
c.poly([[5, 12], [8, 6], [12, 11]], "abcde"); c.poly([[20, 11], [24, 5], [27, 12]], "abcde"); c.poly([[13, 11], [16, 8], [19, 11]], "abcde");
c.ell(16, 22, 8, 5, "ffgh", { outline: true }); c.box(9, 17, 23, 20, "eeee", { outline: false });
c.ell(16, 22, 8, 5, "fgh", { outline: false }); c.line(10, 20, 22, 20, "e");
for (const x of [10, 13, 16, 19, 22]) c.poly([[x - 1, 19], [x + 1, 19], [x, 23]], "ij", { outline: false });
for (const x of [11, 14, 18, 21]) c.poly([[x - 1, 27], [x + 1, 27], [x, 24]], "ij", { outline: false });
c.line(13, 25, 19, 25, "g");
c.eye(9, 14, "y"); c.eye(21, 14, "y"); c.line(8, 13, 11, 13, "e"); c.line(20, 13, 23, 13, "e");
c.list([[6, 20, "b"], [5, 21, "a"], [26, 19, "a"], [25, 18, "b"], [8, 26, "a"], [24, 26, "a"], [12, 15, "d"], [15, 13, "d"]]);
export const rows = c.rows();
