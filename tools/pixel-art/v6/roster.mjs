// マップ用人物の一覧（v4 の60人と同じ人物）。髪型・服・小物の組み合わせと、色（v4の絵の色）から、v6の絵のファイルを書き出す。
// 使い方: node roster.mjs  → pieces/w-<番号>-<名前>.mjs を作る（すでにあるものは上書き）
import fs from "fs"; import path from "path"; import { pathToFileURL } from "url";
const SPEC = {
  "c1-01-yuri": ["spiky", "tunic", ["bag"]], "c1-02-reto": ["short", "coat", ["scarf"]], "c1-03-mina": ["twin", "dress", []], "c1-04-guide": ["short", "tunic", ["band", "bag"]], "c1-05-orca": ["short", "tunic", ["band"]],
  "c1-06-ayame": ["long", "coat", []], "c1-07-kasen": ["bob", "coat", []], "c1-08-edrea": ["long", "robe", []], "c1-09-dorn": ["short", "coat", ["hat"]], "c1-10-sonchou": ["short", "tunic", ["beard"]],
  "c1-11-watashimori": ["short", "tunic", ["hat"]], "c1-12-kumiaichou": ["short", "tunic", ["beard"]], "c1-13-taishou": ["short", "coat", ["scarf"]], "c1-14-shisai": ["short", "robe", []], "c1-15-shijikan": ["short", "tunic", ["glasses"]],
  "c1-16-bansho": ["short", "armor", ["cap"]], "c1-17-osananajimi": ["short", "tunic", []], "c1-18-shisha": ["short", "robe", []], "c1-19-motojime": ["short", "coat", ["beard"]], "c1-20-shinja": ["short", "robe", ["hood"]],
  "c2-01-yadonushi": ["bald", "apron", ["beard"]], "c2-02-okami": ["bun", "apron", []], "c2-03-dogu-shonin": ["short", "apron", ["bag"]], "c2-04-buki-ya": ["short", "apron", ["beard"]], "c2-05-kajiya": ["bald", "apron", ["band"]],
  "c2-06-shinkan": ["short", "robe", []], "c2-07-shudojo": ["bun", "robe", ["hood"]], "c2-08-nofu": ["short", "tunic", ["hat"]], "c2-09-nofu-fujin": ["bun", "dress", ["band"]], "c2-10-ryoshi": ["short", "tunic", ["cap"]],
  "c2-11-sendo": ["short", "coat", ["cap"]], "c2-12-koufu": ["short", "tunic", ["band"]], "c2-13-heishi": ["short", "armor", ["cap"]], "c2-14-eihei-cho": ["short", "armor", ["beard"]], "c2-15-gakusha": ["short", "robe", ["glasses"]],
  "c2-16-ginyu-shijin": ["pony", "coat", ["hat"]], "c2-17-odoriko": ["pony", "dress", ["band"]], "c2-18-tabi-shonen": ["spiky", "tunic", ["bag"]], "c2-19-tabi-shojo": ["twin", "tunic", ["bag"]], "c2-20-neko-ko": ["short", "tunic", []],
  "c3-01-ojiisan": ["bald", "tunic", ["beard"]], "c3-02-obaasan": ["bun", "dress", []], "c3-03-otokonoko": ["spiky", "tunic", []], "c3-04-onnanoko": ["twin", "dress", []], "c3-05-haha": ["bun", "dress", []],
  "c3-06-panya": ["short", "apron", ["cap"]], "c3-07-ryourinin": ["bald", "apron", ["cap"]], "c3-08-kusuriya": ["bob", "apron", ["bag"]], "c3-09-uranaishi": ["long", "robe", ["hood"]], "c3-10-gaka": ["short", "coat", ["cap"]],
  "c3-11-tabinokenshi": ["short", "armor", ["scarf"]], "c3-12-kyoumei-hoteri": ["spiky", "tunic", ["scarf"]], "c3-13-kyoumei-suimon": ["long", "dress", []], "c3-14-yumitsukai": ["pony", "tunic", ["band"]], "c3-15-touzoku": ["short", "coat", ["hood"]],
  "c3-16-reijou": ["long", "dress", []], "c3-17-shinshi": ["short", "coat", ["hat"]], "c3-18-toshokanin": ["bob", "coat", ["glasses"]], "c3-19-yuubin": ["short", "tunic", ["cap", "bag"]], "c3-20-yopparai": ["short", "tunic", []],
};
const v4 = new URL("../v4/", import.meta.url); const { DEFAULT_PAL } = await import(new URL("lib4.mjs", v4).href);
const dark = (h, k = 0.55) => "#" + [1, 3, 5].map((i) => Math.round(parseInt(h.slice(i, i + 2), 16) * k).toString(16).padStart(2, "0")).join("");
let n = 0;
for (const [id, [hair, outfit, acc]] of Object.entries(SPEC)) {
  const m = await import(new URL(`pieces/characters/${id}.mjs`, v4).href); const P = { ...DEFAULT_PAL, ...m.pal };
  const pal = { skin: [P.a, P.b, P.B], hair: [P["1"], P["2"], P["3"]], cloth: [P.J, P.j, P.k], trim: P.C, accent: P.A, accent2: dark(P.j, 0.8), pants: [P.P, P.Q], boots: [P.s, P.P] };
  const src = `import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ${m.name}（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = ${JSON.stringify(m.name)}; export const category = "map-character";
export const pal = palFrom(${JSON.stringify(pal)});
export const frames = makeSheet(${JSON.stringify({ hair, outfit, acc })});
export const rows = sheetRows(frames);
`;
  fs.writeFileSync(new URL(`pieces/w-${id}.mjs`, import.meta.url), src, "utf8"); n++;
}
console.log(n, "人ぶんのファイルを書き出した");
