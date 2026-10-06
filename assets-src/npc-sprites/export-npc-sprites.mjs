import { chromium } from "/opt/node-tools/node_modules/playwright/index.mjs";
import fs from "fs";
const OUT = "/home/user/sunshine-rpg/assets-src/npc-sprites";
fs.mkdirSync(OUT + "/each", { recursive: true });
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await (await b.newContext({ viewport: { width: 1200, height: 900 } })).newPage();
p.on("pageerror", (e) => console.log("PAGEERR", e.message));
await p.goto("http://localhost:5199/"); await p.waitForTimeout(3000);
const res = await p.evaluate(async () => {
  const W = await import("/src/game/world/world.ts");
  const CS = await import("/src/game/sprite/character-specs.ts");
  const SR = await import("/src/render/sprite-renderer.ts");
  const seen = new Map();
  for (const [map, list] of Object.entries(W.WORLD_NPCS)) {
    for (const n of list ?? []) {
      if (CS.npcLook(n) !== "person") continue;
      const spec = CS.spriteSpecForNpc(n);
      const key = JSON.stringify(spec);
      if (seen.has(key)) { seen.get(key).maps.add(map); continue; }
      const sp = CS.firstSpeaker(n.commands ?? []);
      seen.set(key, { spec, id: n.id, name: sp.speaker || n.spriteName || "町の人", maps: new Set([map]) });
    }
  }
  const dirs = ["down", "left", "right", "up"];
  const each = [];
  const all = [...seen.values()];
  for (const e of all) {
    // 1枚: 4方向 × 3コマ（16×32）を横に並べた 192×32
    const c = document.createElement("canvas"); c.width = 16 * 12; c.height = 32;
    const g = c.getContext("2d");
    dirs.forEach((d, di) => [0, 1, 2].forEach((f) => SR.drawSprite(g, e.spec, d, f, (di * 3 + f) * 16, 0)));
    each.push({ id: e.id, name: e.name, maps: [...e.maps], png: c.toDataURL("image/png") });
  }
  // 一覧（正面、4倍、名前つき）
  const cols = 10, cw = 112, ch = 180, S = 4;
  const c = document.createElement("canvas"); c.width = cols * cw; c.height = Math.ceil(all.length / cols) * ch;
  const g = c.getContext("2d"); g.imageSmoothingEnabled = false; g.fillStyle = "#2a2f3a"; g.fillRect(0, 0, c.width, c.height);
  const tmp = document.createElement("canvas"); tmp.width = 16; tmp.height = 32; const tg = tmp.getContext("2d");
  all.forEach((e, i) => {
    tg.clearRect(0, 0, 16, 32); SR.drawSprite(tg, e.spec, "down", 0, 0, 0);
    const x = (i % cols) * cw, y = Math.floor(i / cols) * ch;
    g.fillStyle = "#3a4150"; g.fillRect(x + 3, y + 3, cw - 6, ch - 6);
    g.drawImage(tmp, x + (cw - 64) / 2, y + 8, 64, 128);
    g.fillStyle = "#fff"; g.font = "12px sans-serif"; g.textAlign = "center";
    g.fillText(e.name.slice(0, 9), x + cw / 2, y + 152);
    g.fillStyle = "#9cc"; g.font = "10px sans-serif"; g.fillText([...e.maps][0].slice(0, 18), x + cw / 2, y + 168);
  });
  return { each, sheet: c.toDataURL("image/png") };
});
const save = (f, u) => fs.writeFileSync(f, Buffer.from(u.split(",")[1], "base64"));
const index = [];
res.each.forEach((e, i) => {
  const f = `${String(i + 1).padStart(3, "0")}-${e.id.replace(/[^A-Za-z0-9_-]/g, "_")}.png`;
  save(`${OUT}/each/${f}`, e.png); index.push({ file: `each/${f}`, id: e.id, name: e.name, maps: e.maps });
});
save(`${OUT}/all-npcs.png`, res.sheet);
fs.writeFileSync(`${OUT}/index.json`, JSON.stringify(index, null, 1));
console.log(index.length);
await b.close();
