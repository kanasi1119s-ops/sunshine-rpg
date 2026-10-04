// 戦闘画面の「文字と窓」だけ（背景・敵・味方の絵なし）を、ゲームの描画（battle-renderer.ts）で、
// ゲームと同じ細かさ（論理の3倍、1200×675）の透明なPNGに書き出す（エフェクトの見本の動画に重ねる。2026-10-04）。
// 使い方: (開発用サーバーを http://localhost:5174 で動かして) node battle-ui-layer.mjs 出力.png "下の窓の文"
// 黒と白の背景で2回描き、その差から透明さを求める（文字のふちのなめらかさも残る）。
import { chromium } from "playwright-core";
import fs from "fs";
const [out, text] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const p = await b.newPage({ viewport: { width: 800, height: 600 } });
await p.goto("http://localhost:5174/");
await p.waitForTimeout(1500);
const png = await p.evaluate(async (msg) => {
  const R = await import("/src/render/battle-renderer.ts");
  const mk = (id, name, enemy, hp) => ({ id, name, maxHp: hp, hp, maxMp: 20, mp: 20, attack: 10, defense: 5, speed: 5, isEnemy: enemy, guarding: false });
  const Z = "​";   // 名前に見えない文字を足して、味方の絵を出さない
  const st = { party: [mk("p1", "ユーリ" + Z, false, 120), mk("p2", "レト" + Z, false, 140), mk("p3", "ミナ" + Z, false, 100), mk("p4", "ガイド" + Z, false, 95)],
    enemies: [mk("kiri-yugami", "予言の歪み", true, 900)], log: [], fled: false };
  R.setBattleBiome("none-for-ui");
  const draw = (bg) => {
    const c = document.createElement("canvas"); c.width = 1200; c.height = 675;
    const ctx = c.getContext("2d");
    ctx.setTransform(3, 0, 0, 3, 0, 0);
    ctx.drawImage = () => {};                       // 背景・ボスの絵は描かない
    const fr = ctx.fillRect.bind(ctx);
    ctx.fillRect = (x, y, w, h) => { if (x === 0 && y === 0 && w === 400 && h === 225) { const s = ctx.fillStyle; ctx.fillStyle = bg; fr(x, y, w, h); ctx.fillStyle = s; } else fr(x, y, w, h); };
    R.renderBattle(ctx, st, { kind: "message", text: msg }, 400, 225, null);
    return ctx.getImageData(0, 0, 1200, 675).data;
  };
  const k = draw("#000000"), w = draw("#ffffff");
  const out = document.createElement("canvas"); out.width = 1200; out.height = 675;
  const oc = out.getContext("2d"); const img = oc.createImageData(1200, 675);
  for (let i = 0; i < k.length; i += 4) {
    const a = 1 - (w[i] - k[i] + w[i + 1] - k[i + 1] + w[i + 2] - k[i + 2]) / 765;
    img.data[i + 3] = Math.round(Math.max(0, Math.min(1, a)) * 255);
    for (let c = 0; c < 3; c++) img.data[i + c] = a > 0.004 ? Math.min(255, Math.round(k[i + c] / a)) : 0;
  }
  oc.putImageData(img, 0, 0);
  return out.toDataURL();
}, text);
fs.writeFileSync(out, Buffer.from(png.split(",")[1], "base64"));
await b.close();
