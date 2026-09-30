import { Cv, ramp } from "../lib5.mjs";
// 沼うお（中型 96×96）: 沼に住む魚人。前かがみで、片手に光る釣り針つきの釣りざおを持つ。
export const name = "沼うお"; export const category = "monster"; export const size = 96;
export const pal = {
  ...ramp("abcde", "#12142e", "#a8b0e8", "#4a4e98"),   // 肌（青緑）
  ...ramp("fgh", "#8a7a68", "#f0e4c8"),                 // おなか
  ...ramp("ijkl", "#0a3040", "#8af0e0", "#2a9a9a"),     // ひれ
  o: "#08161c", w: "#ffffff", y: "#dfe9fa", E: "#10141c",
  m: "#5a0f24", p: "#d8506a",                           // 口の中・舌
  q: "#3a2414", r: "#8a5c32",                           // 竿
  G: "#9aaab8", H: "#f4fbff",                           // 釣り針
  Y: "#c8fff0", s: "#0a1a20",
};
const c = new Cv(96);
const skin = "abcde", belly = "fgh", fin = "ijkl";
c.shadow(46, 90, 33, 4.5, "s");
const ROD = [[66,78],[91,8]];
// ---- 釣りざお ----
const rod = c.limb(ROD[0][0], ROD[0][1], ROD[1][0], ROD[1][1], 1.7, 0.7);
c.paint(rod, "qr", { round: 2, dither: false });
// ---- 背びれ（背中のカーブにそって） ----
const dorsal = c.poly([[36,26],[20,14],[24,27],[8,26],[18,38],[4,46],[18,50],[10,62],[26,62],[34,56]]);
c.paint(dorsal, fin, { round: 4 });
c.line(36,27,20,15,"k"); c.line(28,36,9,27,"k"); c.line(26,46,5,46,"k"); c.line(28,54,11,62,"k");
// ---- 奥の腕（左手） ----
const armL = c.union(c.limb(28,48,17,62,5.5,4), c.limb(17,62,19,76,4,3.4));
c.paint(armL, skin, { round: 3 }); c.edge(armL, "a", "all");
const elbowFinL = c.poly([[13,58],[6,62],[12,64],[15,66]]); c.paint(elbowFinL, fin, { round: 2 });
const handL = c.poly([[14,74],[9,83],[14,82],[16,88],[21,83],[26,86],[25,75]]);
c.paint(handL, skin, { round: 3, bias: -0.1 });
for (const [x0,y0,x1,y1] of [[16,78,11,83],[19,79,17,87],[22,79,25,85]]) c.strokeIn(handL, x0,y0,x1,y1,"a");
// ---- 脚（ひざを曲げる） ----
const legL = c.union(c.ell(35,70,9,8), c.limb(33,74,28,83,6,4.5));
const footL = c.poly([[17,89],[22,83],[28,82],[34,79],[39,84],[34,90],[26,91]]);
c.paint(legL, skin, { round: 4 }); c.paint(footL, skin, { round: 3, bias: -0.1 });
for (const [x0,y0,x1,y1] of [[24,84,20,89],[29,83,28,90],[34,82,36,88]]) c.strokeIn(footL,x0,y0,x1,y1,"a");
const legR = c.union(c.ell(56,70,9,9), c.limb(57,75,62,83,7,5));
const footR = c.poly([[52,90],[57,82],[63,82],[69,79],[76,84],[71,90],[61,92]]);
c.paint(legR, skin, { round: 4 }); c.paint(footR, skin, { round: 3, bias: -0.1 });
for (const [x0,y0,x1,y1] of [[59,84,55,90],[64,83,64,91],[69,82,73,89]]) c.strokeIn(footR,x0,y0,x1,y1,"a");
c.edge(c.sub(legL, footL), "a", "lower"); c.edge(c.sub(legR, footR), "a", "lower");
// ---- 胴（前かがみ：背中がまるく盛り上がる） ----
const torso = c.union(c.ell(42,58,17,18), c.ell(31,46,13,13), c.ell(47,67,14,10));
c.paint(torso, skin, { round: 10 });
const bel = c.inter(c.union(c.ell(50,60,9,14), c.ell(49,71,8,6)), torso);
c.paint(bel, belly, { round: 5 });
c.edge(bel, "c", "all");
for (let y = 52; y < 76; y += 4) c.line(46,y,56,y+1,"f");
const back = c.inter(torso, c.union(c.ell(28,50,9,15), c.ell(36,42,10,6)));
c.speckle(back, "b", 0.22, 5); c.speckle(back, "d", 0.07, 9);
// ---- 手前の腕（右手・竿を持つ） ----
const armR = c.union(c.limb(56,50,70,58,5.5,4.5), c.limb(70,58,74,56,4.5,4));
c.paint(armR, skin, { round: 3 });
c.edge(armR, "a", "lower");
const elbowFinR = c.poly([[66,62],[62,69],[68,66],[71,63]]); c.paint(elbowFinR, fin, { round: 2 });
const handR = c.union(c.ell(75,55,5,5), c.poly([[72,51],[70,59],[75,60],[80,59],[81,53],[78,50]]));
c.paint(handR, skin, { round: 3 });
for (const [x,y] of [[72,59],[76,60],[80,58]]) { c.fill(c.ell(x,y,2.2,2.6), "c"); c.edge(c.ell(x,y,2.2,2.6), "a", "lower"); }
// ---- 頭（体の前にせり出す・別の紙に描いてずらして重ねる） ----
const h = new Cv(96);
const head = h.union(h.ell(46,32,17,12), h.ell(57,37,13,8));
const crest = h.poly([[34,26],[30,10],[39,20],[42,5],[48,18],[55,7],[56,23],[46,28]]);
h.paint(crest, fin, { round: 3 });
h.line(35,25,31,12,"k"); h.line(41,19,42,7,"k"); h.line(49,17,55,9,"k");
h.paint(head, skin, { round: 9 });
h.speckle(h.inter(head, h.ell(46,22,9,3)), "d", 0.25, 11);

const jaw = h.union(h.ell(54,46,11,4.5), h.poly([[43,42],[64,43],[62,50],[49,50]]));
h.paint(jaw, skin, { round: 3, bias: -0.1 });
const mouth = h.union(h.ell(54,41,11,5), h.poly([[43,39],[65,38],[68,42],[59,46],[47,45]]));
h.fill(mouth, "m"); h.fill(h.ell(56,44,5.5,2), "p");
for (const x of [45,48,51,54,57,60,63,66]) { h.put(x,38,"w"); h.put(x,39,"w"); h.put(x+0.5,40,"Y"); }
for (const x of [47,50,53,56,59,62,65]) { h.put(x,46,"w"); h.put(x,45,"w"); }
h.edge(mouth, "o", "all");
// 目（大きな魚の目）
h.fill(h.ell(37,27,7.3,7.3), "o"); h.fill(h.ell(55,28,5.8,6.2), "o");
h.fill(h.ell(37,27,6,6), "y"); h.fill(h.ell(55,28,4.6,5), "y");
h.fill(h.ell(37,28,1.7,4.6), "E"); h.fill(h.ell(55,29,1.4,4), "E");
h.put(34,23,"w"); h.put(35,23,"w"); h.put(35,24,"w"); h.put(53,24,"w"); h.put(54,24,"w"); h.put(39,31,"H");
// えら
h.line(34,36,37,41,"b"); h.line(31,37,34,43,"b"); h.line(29,38,31,44,"a");

for (let y = 0; y < 96; y++) for (let x = 0; x < 96; x++) { const k = h.g[y][x]; if (k !== ".") c.put(x - 3, y + 5, k); }
// ぬれた光
for (const [x,y,rx,ry] of [[36,20,4,1.4],[26,50,3,1.5],[52,58,2.4,4],[58,68,2,3],[75,50,2,1.4],[44,36,2,1]]) c.fill(c.ell(x,y,rx,ry), "Y");
c.put(22,58,"Y"); c.put(18,70,"Y"); c.put(33,68,"Y");
// ---- 輪郭 ----
c.outline("o", { a:"o", b:"a", c:"a", d:"b", e:"c", i:"o", j:"i", k:"j", l:"k", f:"a", g:"c", h:"c", q:"o", r:"q", m:"o", p:"m", y:"m" });
c.despeckle("wYHEyG");
// ---- つり糸・つり針（輪郭のあとに描く） ----
c.line(91,8,90,44,"H");
c.line(90,45,90,52,"G"); c.line(90,52,87,55,"G"); c.line(87,55,85,52,"G"); c.line(90,49,92,51,"G");
c.put(85,52,"H"); c.put(90,46,"H"); c.put(87,55,"H");
c.put(90,58,"Y"); c.put(93,50,"Y"); c.put(84,58,"Y"); c.put(88,60,"j");
export const rows = c.rows();
