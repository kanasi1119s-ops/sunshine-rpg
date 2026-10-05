/**
 * ろうそくの炎の揺らめき（2026-10-05、人間の指示「ろうそくには揺らめきを」）。
 * 1枚絵の地図（聖堂の中など）は動かないので、炎の位置に、小さな炎のコマを時間で切りかえて上から描き、まわりの明かりもふくらませたり縮めたりする。
 * 炎のコマはドットで1つずつ決めてある（下の行が炎の根もと。左右にゆれる・のびる・ちぢむ）。炎ごとに始まりをずらして、そろって動かないようにする。
 */
const COLORS: Record<string, string> = { a: "#ff9a3c", A: "#ffe060", Y: "#fff6c8", r: "#ffc070" };

/** 大きい炎（祭壇・燭台）。上→下の5行、横3ドット。まん中の列が芯。 */
const BIG: readonly string[][] = [
  [".a.", ".A.", "aYa", "AYA", ".A."],
  ["a..", ".a.", "aA.", "AYa", ".A."],
  [".a.", ".A.", ".Y.", "aYa", ".A."],
  ["..a", ".a.", ".Aa", "aYA", ".A."],
  ["...", ".a.", "aAa", "AYA", ".A."],
  [".r.", ".a.", ".Aa", "aYA", ".A."],
];
/** 小さい炎（壁のろうそく受け・くぼみ）。上→下の3行。 */
const SMALL: readonly string[][] = [
  [".a.", ".A.", ".A."],
  ["a..", ".A.", ".A."],
  [".a.", ".Y.", ".A."],
  ["..a", ".A.", ".A."],
  ["...", ".a.", ".A."],
];
/** コマの順（同じコマが続かないよう、ゆらぎらしく並べた）。 */
const ORDER = [0, 1, 0, 2, 3, 0, 4, 1, 5, 0, 3, 2];

export interface CandleFlame {
  x: number;
  y: number;
  big: boolean;
}

/** 炎ごとのコマの番号（時刻 ms と、炎の位置から決まるずれ）。テストでも使う。 */
export function flameFrame(flame: CandleFlame, ms: number): number {
  const phase = (flame.x * 7 + flame.y * 13) % ORDER.length;
  const step = Math.floor(ms / (flame.big ? 110 : 130)) + phase;
  const k = ORDER[step % ORDER.length];
  return flame.big ? k : k % SMALL.length;
}

/** ox, oy は絵の左上の画面の位置。 */
export function drawCandleFlames(ctx: CanvasRenderingContext2D, flames: readonly CandleFlame[], ox: number, oy: number, ms: number): void {
  ctx.save();
  for (const f of flames) {
    const sx = Math.round(ox + f.x);
    const sy = Math.round(oy + f.y);
    // まわりの明かり（ふくらんだり縮んだり）
    const pulse = 0.5 + 0.5 * Math.sin(ms / 170 + f.x * 0.9 + f.y * 0.4);
    const r = (f.big ? 7 : 5) + pulse * 1.5;
    ctx.globalAlpha = (f.big ? 0.13 : 0.1) + pulse * 0.05;
    ctx.fillStyle = "#ffcf6a";
    ctx.beginPath();
    ctx.arc(sx + 0.5, sy - 1, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 0.18 + pulse * 0.08;
    ctx.beginPath();
    ctx.arc(sx + 0.5, sy - 1, r * 0.45, 0, Math.PI * 2);
    ctx.fill();
    // 炎のコマ
    ctx.globalAlpha = 1;
    const rows = (f.big ? BIG : SMALL)[flameFrame(f, ms)];
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      for (let j = 0; j < 3; j++) {
        const ch = row[j];
        if (ch === ".") continue;
        ctx.fillStyle = COLORS[ch];
        ctx.fillRect(sx - 1 + j, sy - (rows.length - 1) + i, 1, 1);
      }
    }
  }
  ctx.restore();
}
