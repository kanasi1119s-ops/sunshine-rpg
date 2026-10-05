import { chromium } from "/opt/node-tools/node_modules/playwright/index.mjs";
import fs from "node:fs";
const out = process.argv[2];
const dir = out + "/cm-frames";
fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
const FPS = 24, DUR = 34;
const only = process.argv[3] ? process.argv[3].split(",").map(Number) : null; // 確認用: 秒を指定
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
const errs = []; p.on("pageerror", (e) => errs.push(String(e)));
await p.goto("http://localhost:5199/"); await p.waitForTimeout(2500);
await p.evaluate(() => { window.__sunshine.startNew(); window.__sunshine.joinSome(["reto", "mina"]); });
await p.waitForTimeout(500);
for (let i = 0; i < 8; i++) { await p.keyboard.press("Enter"); await p.waitForTimeout(80); }
// 実際のゲーム画面の静止画
const stills = [["town", "touri-town", 18, 12, 0], ["inn", "inn-touri-town-1f", 14, 10, 0], ["night", "touri-town", 18, 12, 0.75 * 480000], ["village", "mugikano-village", 22, 10, 0]];
for (const [name, map, x, y, clock] of stills) {
  await p.evaluate(([m, x, y, c]) => { window.__sunshine.setClock(c); window.__sunshine.warp(m, x, y); }, [map, x, y, clock]);
  await p.waitForTimeout(900);
  for (let i = 0; i < 6; i++) { await p.keyboard.press("Enter"); await p.waitForTimeout(80); }
  await p.waitForTimeout(300);
  await p.evaluate((n) => {
    const src = document.querySelector("canvas");
    const c = document.createElement("canvas"); c.width = src.width; c.height = src.height;
    c.getContext("2d").drawImage(src, 0, 0);
    (window.__stills ??= {})[n] = c;
  }, name);
}
await p.evaluate(() => window.__sunshine.setClock(0));
await p.evaluate(async () => {
  const R = await import("/src/render/battle-renderer.ts");
  const O = await import("/src/render/boot-opening-renderer.ts");
  const FW = 1080, FH = 1920;
  const TITLE = "Ringlight Chronicle";
  const chars = [["ユーリ", "hero"], ["レト", "reto"], ["ミナ", "mina"]];
  const mk = ([n, id], over = {}) => ({ id, name: `${n} Lv12`, maxHp: 90, hp: 90, maxMp: 20, mp: 20, attack: 10, defense: 5, speed: 5, isEnemy: false, guarding: false, ...over });
  const en = (id, name, over = {}) => ({ id, name, maxHp: 200, hp: 200, maxMp: 0, mp: 0, attack: 5, defense: 1, speed: 3, isEnemy: true, guarding: false, ...over });
  const spec = (o) => ({ actorId: undefined, casterId: undefined, fromId: undefined, motion: null, targetIds: ["hero"], fx: null, hurt: false, durationMs: 2000, fxStart: 0.45, area: false, ...o });
  const party = chars.map((c) => mk(c));
  const E1 = "enc-garasuko-warehouse-2#0", E2 = "enc-tetsukusari-mine-1#0", E3 = "enc-sanone-camp-1#0";
  const foes = [en(E1, "倉庫の影"), en(E2, "坑道の影"), en(E3, "風の影")];
  const bossE = [en("god-1", "恵みの残照", { maxHp: 6000, hp: 6000 })];
  const bctx = (state, ui, anim) => {
    const c = document.createElement("canvas"); c.width = 400; c.height = 225;
    R.renderBattle(c.getContext("2d"), state, ui, 400, 225, null, true, anim);
    return c;
  };
  const msg = (t) => ({ kind: "message", text: t });
  // ---- 画面の下ごしらえ ----
  const sky = document.createElement("canvas"); sky.width = 225; sky.height = 400;
  O.drawBandedSky(sky.getContext("2d"), 0, 0, 225, 400);
  const big = document.createElement("canvas"); big.width = FW; big.height = FH;
  const g = big.getContext("2d");
  const ease = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
  const FONT = "'IPAGothic','Noto Sans JP','Hiragino Sans',sans-serif";
  function caption(lines, y, t, size = 78, color = "#ffffff", fade = 1) {
    g.save(); g.globalAlpha = Math.max(0, Math.min(1, fade)); g.textAlign = "center"; g.textBaseline = "middle"; g.lineJoin = "round";
    g.font = `bold ${size}px ${FONT}`;
    lines.forEach((ln, i) => {
      const yy = y + i * (size * 1.25) + (1 - ease(t * 3)) * 24;
      g.lineWidth = 16; g.strokeStyle = "rgba(10,6,24,0.92)"; g.strokeText(ln, FW / 2, yy);
      g.fillStyle = color; g.fillText(ln, FW / 2, yy);
    });
    g.restore();
  }
  function portraitBg() { g.imageSmoothingEnabled = false; g.drawImage(sky, 0, 0, FW, FH); for (let i = 0; i < 70; i++) { const h = (i * 2654435761) >>> 0; const x = (h % 225), y = ((h >> 8) % 400); g.globalAlpha = 0.35 + 0.65 * Math.abs(Math.sin(performance.now() / 700 + i)); g.fillStyle = "#dfe8ff"; g.fillRect(x * 4.8, y * 4.8, 5, 5); } g.globalAlpha = 1; }
  function band(src, u, zoom = 0.1, pan = 0) {
    // 横長の画面を、縦動画の中ほどに、ゆっくり拡大しながら置く
    portraitBg();
    // 画面の上の端（ゲーム名）と下の端（開発用の表示）は切りとる
    const top = src.height * (12 / 225), usable = src.height * (201 / 225);
    const bw = FW, bh = Math.round(FW * 201 / 400), by = Math.round((FH - bh) / 2) - 40;
    const z = 1 + zoom * u;
    const sw = src.width / z, sh = usable / z;
    const sx = (src.width - sw) * (0.5 + pan * (u - 0.5)), sy = top + (usable - sh) * 0.5;
    g.imageSmoothingEnabled = false;
    g.drawImage(src, sx, sy, sw, sh, 0, by, bw, bh);
    g.strokeStyle = "#f2c14e"; g.lineWidth = 6; g.strokeRect(3, by - 3, bw - 6, bh + 6);
  }
  function opening(phase, ms, hideHint = true) {
    const c = document.createElement("canvas"); c.width = 225; c.height = 400;
    const cx = c.getContext("2d");
    O.renderBootOpening(cx, { open: true, phase, ms }, 225, 400, TITLE, 1, phase === "story" ? 2 : 1);
    if (hideHint) { cx.fillStyle = "#03030c"; cx.fillRect(120, 0, 105, 18); }
    g.imageSmoothingEnabled = false; g.drawImage(c, 0, 0, FW, FH);
  }
  // 戦闘の場面（時間の流れ: 各 [長さ秒, 場面の関数(u)]）
  const mina = (u) => bctx({ party, enemies: foes, log: [], fled: false }, msg("ミナは 炎の術を となえた！"), { spec: spec({ actorId: "mina", fromId: "mina", motion: "cast", fx: "fire", targetIds: [E1], durationMs: 2000, fxStart: 0.45 }), elapsedMs: u * 2000 });
  const enemyBolt = (u) => bctx({ party, enemies: foes, log: [], fled: false }, msg("風の影は 雷の術を となえた！"), { spec: spec({ casterId: E3, fromId: E3, fx: "bolt", hurt: true, targetIds: ["hero"], durationMs: 2000 }), elapsedMs: u * 2000 });
  const multi = (u) => {
    // 3回こうげき: 1回ごとに剣をふる
    const k = Math.min(2, Math.floor(u * 3)); const uu = (u * 3) - k;
    return bctx({ party, enemies: foes, log: [], fled: false }, msg(`ユーリは すばやい動きで 3回 こうげき！（${k + 1}）`), { spec: spec({ actorId: "hero", motion: "slash", targetIds: [E2], durationMs: 520, fxStart: 0.5 }), elapsedMs: uu * 520 });
  };
  const boss = (u) => bctx({ party, enemies: bossE, log: [], fled: false }, msg("ミナの 水紋ノ波！"), { spec: spec({ actorId: "mina", fromId: "mina", motion: "cast", fx: "water", targetIds: ["god-1"], durationMs: 2000 }), elapsedMs: u * 2000 });
  const lineup = (u) => bctx({ party, enemies: foes, log: [], fled: false }, msg("ユーリ・レト・ミナの 3人で たびに 出る！"), null);
  const T = [
    [0, 3.6, "open"],
    [3.6, 5.8, "still", "town", ["灯りの町で、", "調査がはじまる。"]],
    [5.8, 8.0, "still", "inn", ["宿屋で ひと休み。"]],
    [8.0, 10.2, "still", "night", ["昼も夜も、", "世界は動いている。"]],
    [10.2, 12.4, "still", "village", ["仲間と、", "ひなたの道を行く。"]],
    [12.4, 14.6, "fn", mina, ["魔法がひらく、", "火・水・雷。"]],
    [14.6, 16.8, "fn", enemyBolt, ["敵も、", "魔法を使ってくる。"]],
    [16.8, 19.0, "fn", multi, ["素早ければ", "2回・3回・4回攻撃！"]],
    [19.0, 21.2, "fn", boss, ["強敵を倒せば、", "特別な装備が手に入る。"]],
    [21.2, 23.6, "fn", lineup, ["仲間と、", "長い旅へ。"]],
    [23.6, 25.7, "flash"],
    [25.7, 40, "reveal"],
  ];
  const flashStills = ["town", "inn", "night", "village", "town", "village"];
  window.__frame = (t) => {
    const seg = T.find((s) => t >= s[0] && t < s[1]) ?? T[T.length - 1];
    g.clearRect(0, 0, FW, FH);
    const u = (t - seg[0]) / (seg[1] - seg[0]);
    if (seg[2] === "open") {
      opening("story", t * 1000);
      if (t > 1.5) caption(["砕けた光が、", "世界をつくった。"], 1380, t - 1.5, 84, "#ffe9a0", Math.min(1, (3.5 - t) * 2));
    } else if (seg[2] === "still") {
      band(window.__stills[seg[3]], u, 0.12, 0.6);
      caption(seg[4], 330, t - seg[0], 84, "#ffffff", Math.min(1, (seg[1] - t) * 4 + 0.2));
      caption(["Ringlight Chronicle"], 1640, 1, 48, "#f2c14e", 0.85);
    } else if (seg[2] === "fn") {
      band(seg[3](u), 0, 0, 0);
      caption(seg[4], 330, t - seg[0], 84, "#ffffff", Math.min(1, (seg[1] - t) * 4 + 0.2));
      caption(["Ringlight Chronicle"], 1640, 1, 48, "#f2c14e", 0.85);
    } else if (seg[2] === "flash") {
      const i = Math.floor(((t - 23.6) / 2.1) * flashStills.length);
      band(window.__stills[flashStills[Math.min(flashStills.length - 1, i)]], ((t - 23.6) * 6) % 1, 0.1, 0);
      caption(["謎を追え。", "真実に近づけ。"], 330, 1, 92, "#ffe9a0");
      g.fillStyle = `rgba(255,244,200,${Math.max(0, 0.7 - ((t - 23.6) * 6 % 1) * 1.6)})`; g.fillRect(0, 0, FW, FH);
    } else {
      opening("reveal", (t - 25.7) * 1000);
      const a = t - 29.4;
      if (a > 0) caption(["ブラウザで遊べる長編RPG", "（制作中）"], 1450, a, 62, "#ffe9a0", Math.min(1, a * 2));
      if (t > 31) caption(["SUNSHINE SOFTWARE"], 1700, t - 31, 44, "#c8c8e0", Math.min(1, (t - 31) * 2));
    }
    // 制作中のバッジ（完成前であることを、全場面で見せる）
    g.save(); g.fillStyle = "rgba(10,6,24,0.8)"; g.fillRect(FW - 250, 36, 214, 74); g.strokeStyle = "#f2c14e"; g.lineWidth = 5; g.strokeRect(FW - 250, 36, 214, 74);
    g.fillStyle = "#f2c14e"; g.font = `bold 44px ${FONT}`; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("制作中", FW - 143, 74); g.restore();
    return big.toDataURL("image/jpeg", 0.9);
  };
});
const times = only ?? Array.from({ length: FPS * DUR }, (_, i) => i / FPS);
let n = 0;
for (const t of times) {
  const url = await p.evaluate((tt) => window.__frame(tt), t);
  fs.writeFileSync(`${dir}/f${String(only ? Math.round(t * 100) : n).padStart(5, "0")}.jpg`, Buffer.from(url.split(",")[1], "base64"));
  n++;
  if (n % 100 === 0) console.log("frames", n);
}
console.log("done", n, errs.slice(0, 3));
await b.close();
