// タッピングに「緩急」をつける: 音の長さのゆらぎ(各小節の頭は少し前のめり、終わりはためる／出だしはゆっくり／終わりは大きく引く)と、強弱の山谷。
// 使い方: node tools/soundfont/tap-shape.mjs <元の音符.json> <出力.json>   (音符の6番目 = 音量の倍率)
import fs from "fs";
const ev = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const END = 30; // 最後のベンド音の頭（ここは動かさない）
// 進み方: 4拍ごとの区切りで「頭は押し、終わりはためる」。出だしと終わりは大きく引く
const mult = (b) => {
  const ph = (b % 4) / 4;
  let m = 0.94 + 0.16 * ph ** 3;
  if (b < 3) m *= 1.2 - 0.07 * b;          // 出だしはゆっくり
  if (b >= 14 && b < 16) m *= 1 + 0.35 * ((b - 14) / 2); // 前半の終わりで引く
  if (b >= 16 && b < 17) m *= 0.9;          // 後半はぱっと入る
  if (b >= 26) m *= 1 + 0.5 * ((b - 26) / 4) ** 2;       // 最後の駆け上がりのあと、大きくためる
  return m;
};
const N = 4000, cum = [0];
for (let i = 1; i <= N; i++) cum.push(cum[i - 1] + mult((i - 0.5) * 32 / N) * 32 / N);
const C = (b) => { const x = Math.min(32, Math.max(0, b)) * N / 32, k = Math.min(N - 1, Math.floor(x)); return cum[k] + (cum[k + 1] - cum[k]) * (x - k); };
const sc = END / C(END);
const W = (b) => b >= END ? b : C(b) * sc;
// 強弱の山谷（拍, 倍率）
const KEY = [[0, .38], [6, .75], [8, .9], [9, .5], [12, .7], [15, 1.0], [16, .5], [20, .85], [21, .55], [24, .75], [27, 1.1], [30, 1.0], [32, .9]];
const V = (b) => { for (let i = 1; i < KEY.length; i++) if (b <= KEY[i][0]) { const [a, x] = KEY[i - 1], [c, y] = KEY[i]; return x + (y - x) * (b - a) / (c - a); } return KEY.at(-1)[1]; };
const out = ev.map(([m, b, d, vib, bend]) => {
  const s = W(b), e = W(b + d);
  return [m, +s.toFixed(4), +(b >= END ? d : e - s).toFixed(4), vib, bend, +V(b).toFixed(3)];
});
fs.writeFileSync(process.argv[3], JSON.stringify(out));
console.log("ok", out.length, "音");
