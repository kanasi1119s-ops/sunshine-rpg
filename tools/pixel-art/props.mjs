// マップの飾り（木・家）。練習（docs/design/pixel-practice-log.md 第7・8回）で一から描いた絵（assets-src/pixel-practice/）を、
// 48×48の枠の下そろえで置いて書き出す。参考素材の絵は写していない（自作）。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/", import.meta.url);
function piece(name, dir, grid, palFile, recolor = {}, frame = 48) {
  const rows = fs.readFileSync(new URL(`${dir}/${grid}`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = { ...JSON.parse(fs.readFileSync(new URL(`${dir}/${palFile}`, ROOT), "utf8")), ...recolor };
  const keys = Object.keys(pal);
  const h = rows.length, w = Math.max(...rows.map((r) => r.length));
  return {
    name,
    pal: keys.map((k) => [k, pal[k]]),
    build() {
      const g = Array.from({ length: frame }, () => Array(frame).fill(-1));
      const ox = Math.floor((frame - w) / 2), oy = frame - h;   // 横は中央、縦は下そろえ
      rows.forEach((r, y) => [...r].forEach((ch, x) => { const k = keys.indexOf(ch); if (k >= 0) g[oy + y][ox + x] = k; }));
      return g;
    },
  };
}
export const PIECES = [
  // 磨き直した版（assets-src/pixel-practice/r17-polish/。生成の元は tree.py・house_brick.py（2026-10-06 からレンガの家。前は house3d.py）・smallprops.py）
  piece("P1-木", "r17-polish", "tree4.txt", "pal-tree.json", {}, 80),   // 2026-10-06 大きなリアルな木（64×80）
  piece("P2-家", "r17-polish", "house-r.txt", "pal-house-r.json", {}, 64),   // 2026-10-06 木の技法（restyle.py --houses）
  piece("P3-家青", "r17-polish", "house-blue-r.txt", "pal-house-blue-r.json", {}, 64),
  piece("P4-家緑", "r17-polish", "house-green-r.txt", "pal-house-green-r.json", {}, 64),
  piece("P5-岩", "r17-polish", "rock2.txt", "pal-rock2.json"),
  piece("P6-茂み", "r17-polish", "bush2.txt", "pal-bush2.json"),
  piece("P7-屋敷", "r17-polish", "manor-r.txt", "pal-manor-r.json", {}, 80),
  piece("P8-屋敷青", "r17-polish", "manor-blue-r.txt", "pal-manor-blue-r.json", {}, 80),
  piece("P9-屋敷緑", "r17-polish", "manor-green-r.txt", "pal-manor-green-r.json", {}, 80),
  // 霧断崖の民家: 平屋の白い石の壁の版（house_brick.py の WHITE。2026-10-06）
  piece("P50-白い家", "r17-polish", "house-white-r.txt", "pal-house-white-r.json", {}, 64),
  // 雪の地方の飾り（r17-polish/snow.py で、既存の木・岩・茂みを雪化／枯れ木は一から）
  piece("P10-雪の木", "r17-polish", "tree-snow.txt", "pal-tree-snow.json"),
  piece("P51-針葉樹", "r17-polish", "tree-pine.txt", "pal-tree-pine.json"),
  piece("P11-枯れ木", "r17-polish", "tree-dead.txt", "pal-tree-dead.json"),
  piece("P12-雪の岩", "r17-polish", "rock-snow.txt", "pal-rock-snow.json"),
  piece("P13-雪の茂み", "r17-polish", "bush-snow.txt", "pal-bush-snow.json"),
  // 砂漠の飾り（r17-polish/desert.py で一から）
  piece("P14-ヤシ", "r17-polish", "palm.txt", "pal-palm.json"),
  piece("P15-サボテン", "r17-polish", "cactus.txt", "pal-cactus.json"),
  // 町の小さな飾り（r17-polish/townprops.py で一から）
  piece("P16-樽", "r17-polish", "barrel.txt", "pal-barrel.json"),
  piece("P17-街灯", "r17-polish", "lamp.txt", "pal-lamp.json"),
  piece("P18-井戸", "r17-polish", "well.txt", "pal-well.json"),
  piece("P19-道しるべ", "r17-polish", "signpost.txt", "pal-signpost.json"),
  piece("P20-木箱の山", "r17-polish", "crates.txt", "pal-crates.json"),
  piece("P21-花壇", "r17-polish", "flowerbed.txt", "pal-flowerbed.json"),
  // 世界地図の町のアイコン（r17-polish/worldicons.py で一から）
  piece("P22-アイコンport", "r28-game-icons", "icon-port.txt", "pal-icon-port.json", {}, 64),
  piece("P23-アイコンvillage", "r28-game-icons", "icon-village.txt", "pal-icon-village.json", {}, 64),
  piece("P24-アイコンlake", "r28-game-icons", "icon-lake.txt", "pal-icon-lake.json", {}, 64),
  piece("P25-アイコンmine", "r28-game-icons", "icon-mine.txt", "pal-icon-mine.json", {}, 64),
  piece("P26-アイコンcastle", "r28-game-icons", "icon-castle.txt", "pal-icon-castle.json", {}, 64),
  piece("P27-アイコンtents", "r28-game-icons", "icon-tents.txt", "pal-icon-tents.json", {}, 64),
  piece("P28-アイコンtemple", "r28-game-icons", "icon-temple.txt", "pal-icon-temple.json", {}, 64),
  piece("P29-アイコンsnowtown", "r28-game-icons", "icon-snowtown.txt", "pal-icon-snowtown.json", {}, 64),
  piece("P30-アイコンsky", "r28-game-icons", "icon-sky.txt", "pal-icon-sky.json", {}, 64),
  piece("P31-アイコンpalace", "r28-game-icons", "icon-palace.txt", "pal-icon-palace.json", {}, 64),
];

PIECES.push(
  piece("P40-アイコンruin", "r17-polish", "icon-ruin.txt", "pal-icon-ruin.json"),
  piece("P41-アイコンshrine", "r17-polish", "icon-shrine.txt", "pal-icon-shrine.json"),
  piece("P42-アイコンcave", "r17-polish", "icon-cave.txt", "pal-icon-cave.json"),
  piece("P43-アイコンstones", "r17-polish", "icon-stones.txt", "pal-icon-stones.json"),
  piece("P44-アイコンbigtree", "r17-polish", "icon-bigtree.txt", "pal-icon-bigtree.json"),
  piece("P45-アイコンvortex", "r17-polish", "icon-vortex.txt", "pal-icon-vortex.json"),
  piece("P46-アイコンvolcano", "r17-polish", "icon-volcano.txt", "pal-icon-volcano.json"),
  piece("P47-アイコンdive", "r17-polish", "icon-dive.txt", "pal-icon-dive.json"),
  // 霧断崖の環の聖堂（r17-polish/church.py で一から。2026-10-05）。外観と、中の1枚絵
  piece("P48-教会", "r17-polish", "cathedral-r.txt", "pal-cathedral-r.json", {}, 176),   // 2026-10-06 大聖堂版を採用（cathedral3d.py）
  piece("P49-教会の中", "r17-polish", "church-interior.txt", "pal-church-interior.json", {}, 224),
  piece("P50-船大工の小屋", "r25-hut", "icon-hut.txt", "pal-icon-hut.json"),
  // 芯環塔（世界地図のまんなか。2026-10-05、自然にできた岩の柱。上は嵐の雲。assets-src/pixel-practice/r27-spire/spire.py）。章の塔のダンジョンの印は、これまでどおり r22 の spire
  // 町・村・お城の印（2026-10-05、6回目: 64×64で細かく。r28-game-icons/icons6.py。5回目の勉強から。町は地形になじむ作り方、お城は3回目の作り方で影なし。assets-src/pixel-practice/r26-game-icons/icons.py）
  // 鉄鏈鉱山のダンジョン（坑道）の入口は、これまでの鉱山の印のまま（町の印 icon-mine は町の絵に替えたため、別の名前にする）
  piece("P54-アイコンmineshaft", "r17-polish", "icon-mine.txt", "pal-icon-mine.json"),
  piece("P52-アイコンvillage-mist", "r28-game-icons", "icon-village-mist.txt", "pal-icon-village-mist.json", {}, 64),
  piece("P53-アイコンtents-grass", "r28-game-icons", "icon-tents-grass.txt", "pal-icon-tents-grass.json", {}, 64),
  piece("P51-芯環塔", "r27-spire", "spire-natural.txt", "pal-spire-natural.json", {}, 256)
);

// 町・遺跡の飾り33点（assets-src/pixel-practice/r20-props/、エージェントが一から作成）。大きさが48を超えるものは64の枠。
export const R20_NAMES = fs.readdirSync(new URL("r20-props/", ROOT)).filter((f) => f.endsWith(".txt")).map((f) => f.replace(".txt", "")).sort();
for (const n of R20_NAMES) {
  const rows = fs.readFileSync(new URL(`r20-props/${n}.txt`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const big = Math.max(rows.length, ...rows.map((r) => r.length)) > 48;
  PIECES.push(piece(`R20-${n}`, "r20-props", `${n}.txt`, `pal-${n}.json`, {}, big ? 64 : 48));
}

// 船・飛空艇・芯環塔・隠しダンジョンの小島（assets-src/pixel-practice/r22-vehicles/、エージェントが一から作成）。絵は枠の下そろえ（足元の位置を保つ）。
// 飛空艇は r24-airship の「風待ち」（2026-10-05）に替えたので、r22 の古い飛空艇（airship-*）は使わない。
export const R22_NAMES = fs.readdirSync(new URL("r22-vehicles/", ROOT)).filter((f) => f.endsWith(".txt") && !f.startsWith("whirlpool") && !f.startsWith("airship")).map((f) => f.replace(".txt", "")).sort();
for (const n of R22_NAMES) {
  const rows = fs.readFileSync(new URL(`r22-vehicles/${n}.txt`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const big = Math.max(rows.length, ...rows.map((r) => r.length));
  PIECES.push(piece(`R22-${n}`, "r22-vehicles", `${n}.txt`, `pal-${n}.json`, {}, big > 48 ? 112 : 48));
}
// 飛空艇「風待ち」（assets-src/pixel-practice/r24-airship/airship.py。第7章の場面の姿: 細長い木の船・帆布の二枚の羽根・灯り石の丸い機関・空鳥の彫刻）
export const R24_NAMES = fs.readdirSync(new URL("r24-airship/", ROOT)).filter((f) => f.startsWith("airship-") && f.endsWith(".txt") && !f.includes("showcase")).map((f) => f.replace(".txt", "")).sort();
for (const n of R24_NAMES) PIECES.push(piece(`R24-${n}`, "r24-airship", `${n}.txt`, `pal-${n}.json`, {}, 48));
