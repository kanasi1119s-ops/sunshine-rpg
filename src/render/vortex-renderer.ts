import type { TileMap } from "../game/map/tile-map";
import { WORLD_TOWER } from "../game/map/world/world-map.generated";

/** 大滝のドット絵（assets-src/pixel-practice/r29-falls/falls.py で描き、エディタで確かめたもの。横に4コマ）。 */
const FALLS_URLS = import.meta.glob("../assets/falls/*.png", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
const fallsImages = new Map<string, HTMLImageElement>();
function fallsImage(name: string): HTMLImageElement | null {
  if (typeof Image === "undefined") return null;
  let img = fallsImages.get(name);
  if (!img) {
    const url = FALLS_URLS[`../assets/falls/${name}.png`];
    if (!url) return null;
    img = new Image();
    img.src = url;
    fallsImages.set(name, img);
  }
  return img.complete && img.naturalWidth > 0 ? img : null;
}
if (typeof window !== "undefined") {
  fallsImage("scene");
  fallsImage("whirl");
  fallsImage("bolt");
  fallsImage("cloud");
  fallsImage("spire-top");
}
import type { Camera } from "./camera";

function hash2(x: number, y: number, k: number): number {
  let h = (x * 374761393 + y * 668265263 + k * 2147483647) >>> 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

/**
 * 芯環塔と大滝（2026-10-05、人間の指示「滝と塔をくっつけて、ドットで滝が流れていて、周りが大雨・嵐になって、雷まであるドットの動きを」）。
 * 穴と大滝・塔・塔の足もとを包む霧・嵐の雲・大雨を、ひとつの絵（320×360・16コマ、assets-src/pixel-practice/r29-falls/scene.py）にして重ねる。
 * 絵（320×440）の (160, 280) が塔のマスのまん中。塔は雲を突き抜けて、雲の上に頂が出る。
 * 雲は、写真をトレースした積乱雲（cloud.png、352×256・4コマ、assets-src/pixel-practice/r30-cumulonimbus）を上に重ね、
 * 雲の中の黄色く光る所に、ときどき雷が走る（cloudFlashFrame）。塔の上のほう（spire-top.png）は雲のさらに上に重ね、雲を突き抜けて見せる。
 * まわりの海の渦潮は、その下に描く。地形のすぐあと（建物・人より前）に描く。
 */
export function renderBasin(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  if (map.data.width < WORLD_TOWER.x + 12) return;
  const s = map.data.tileWidth;
  const cx = (WORLD_TOWER.x + 0.5) * s - camera.x;
  const cy = (WORLD_TOWER.y + 0.5) * s - camera.y;
  if (cx < -260 || cx > camera.viewportWidth + 260 || cy < -260 || cy > camera.viewportHeight + 300) return;
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  // まわりの海の渦潮（大滝のふちと渦の輪のあいだに6つ。少しずつ速さがちがう）
  const whirl = fallsImage("whirl");
  if (whirl) {
    for (let i = 0; i < 6; i++) {
      const a = i * (Math.PI / 3) + 0.4;
      const rr = (11 + (i % 2) * 0.8) * s;
      const wf = Math.floor(nowMs / (95 + i * 9) + i * 3) % 8;
      ctx.drawImage(whirl, wf * 48, 0, 48, 48, Math.round(cx + Math.cos(a) * rr - 24), Math.round(cy + Math.sin(a) * rr - 24), 48, 48);
    }
  }
  const scene = fallsImage("scene");
  if (scene) {
    const fr = Math.floor(nowMs / 65) % 16;   // 16コマ。水も雨も、本当に流れて・降って見える
    ctx.drawImage(scene, fr * 320, 0, 320, 440, Math.round(cx - 160), Math.round(cy - 280), 320, 440);
  }
  ctx.restore();
}

/**
 * 芯環塔の上の積乱雲と、雲を突き抜ける塔の上のほう。船や人より上に描く（船は雲のうしろを進む。2026-10-05、
 * 人間の指示「船は雲の後ろ側を動けるようにしてほしい」）。飛空艇に乗っているときは、雲より上を飛ぶので、先に描く（main.ts）。
 */
export function renderTowerCloud(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  if (map.data.width < WORLD_TOWER.x + 12) return;
  const s = map.data.tileWidth;
  const cx = (WORLD_TOWER.x + 0.5) * s - camera.x;
  const cy = (WORLD_TOWER.y + 0.5) * s - camera.y;
  if (cx < -260 || cx > camera.viewportWidth + 260 || cy < -260 || cy > camera.viewportHeight + 360) return;
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  const cloud = fallsImage("cloud");
  if (cloud) {
    const cf = cloudFlashFrame(nowMs);
    ctx.drawImage(cloud, cf * 352, 0, 352, 256, Math.round(cx - 176), Math.round(cy - 351), 352, 256);
  }
  const spireTop = fallsImage("spire-top");
  if (spireTop) ctx.drawImage(spireTop, Math.round(cx - 160), Math.round(cy - 280));
  ctx.restore();
}

/**
 * 雲の中の雷（約3.3秒ごと）。雲の絵のコマ: 0=ふだん 1=光る 2=稲妻A 3=稲妻B。
 * 光る→稲妻→光る→（少し暗く）→もう一度稲妻→光る、の順。回ごとに A と B を入れかえる。
 */
const CLOUD_FLASH_PERIOD = 3300;
const CLOUD_FLASH: [number, number][] = [[0, 1], [60, 2], [130, 1], [190, 0], [270, 3], [330, 1], [400, 0]];
export function cloudFlashFrame(nowMs: number): number {
  const ph = nowMs % CLOUD_FLASH_PERIOD;
  const odd = Math.floor(nowMs / CLOUD_FLASH_PERIOD) % 2 === 1;
  let f = 0;
  for (const [t, fr] of CLOUD_FLASH) if (ph >= t) f = fr;
  if (odd && f >= 2) f = f === 2 ? 3 : 2;
  return f;
}

/** 稲妻の時間（約5.2秒ごと）。いまのコマ（0〜5）と、何回目の稲妻か。光っていなければ null。 */
const BOLT_PERIOD = 5200;
const BOLT_TIMES = [0, 60, 110, 220, 260, 330, 450];   // コマ 0〜5 の始まり（ミリ秒）と終わり
export function boltFrame(nowMs: number): { frame: number; strike: number } | null {
  const ph = nowMs % BOLT_PERIOD;
  for (let k = 0; k < 6; k++) if (ph >= BOLT_TIMES[k] && ph < BOLT_TIMES[k + 1]) return { frame: k, strike: Math.floor(nowMs / BOLT_PERIOD) };
  return null;
}

/** 嵐: 塔のまわりを、暗い雲が覆い、雨が降り、ときどき稲光が走る（2026-10-05から、航路が開いたあとも、いつも嵐）。 */
export function renderStorm(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera, nowMs: number): void {
  const s = map.data.tileWidth;
  const cx = (WORLD_TOWER.x + 0.5) * s - camera.x;
  const cy = (WORLD_TOWER.y + 0.5) * s - camera.y;
  if (cx < -260 || cx > camera.viewportWidth + 260 || cy < -260 || cy > camera.viewportHeight + 260) {
    return;
  }
  const g = ctx.createRadialGradient(cx, cy, 20, cx, cy, 230);
  g.addColorStop(0, "rgba(30,34,52,0.12)");
  g.addColorStop(0.55, "rgba(24,28,44,0.38)");
  g.addColorStop(1, "rgba(24,28,44,0)");
  ctx.fillStyle = g;
  ctx.fillRect(cx - 240, cy - 240, 480, 480);
  // （コードで描いていた、ぼんやりした雲のかたまりは、2026-10-05 にやめた。雲はドット絵の雲だけにする）
  // 雨: ななめに降る細い線（嵐のまんなかほど多い）。雲の底（塔のマスから約6マス上）より下にだけ降る
  ctx.save();
  ctx.strokeStyle = "rgba(200,215,240,0.45)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = 0; i < 90; i++) {
    const seedX = hash2(i, 3, 1), seedY = hash2(i, 5, 2);
    const fall = ((nowMs / 420 + seedY) % 1);
    const x = cx - 230 + seedX * 460 + fall * 18;
    const y = cy - 230 + ((seedY * 460 + fall * 460) % 460);
    if (Math.hypot(x - cx, y - cy) > 225 || y < cy - 104) continue;
    ctx.moveTo(Math.round(x), Math.round(y));
    ctx.lineTo(Math.round(x - 3), Math.round(y + 7));
  }
  ctx.stroke();
  ctx.restore();
  // 稲妻（ドット絵）: 約5.2秒ごとに、雲の底から穴のふちへ落ちる。いちばん明るいコマで、あたりが白く光る
  const bf = boltFrame(nowMs);
  if (bf) {
    if (bf.frame === 1 || bf.frame === 4) {
      ctx.fillStyle = bf.frame === 1 ? "rgba(230,240,255,0.28)" : "rgba(230,240,255,0.18)";
      ctx.fillRect(cx - 230, cy - 230, 460, 460);
    }
    const bolt = fallsImage("bolt");
    if (bolt) {
      const variant = bf.strike % 2;
      const xs = [-96, -44, 52, 104];
      const bx = Math.round(cx + xs[bf.strike % 4] - 48);
      ctx.save();
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(bolt, (variant * 6 + bf.frame) * 96, 0, 96, 220, bx, Math.round(cy - 104), 96, 220);
      ctx.restore();
    }
  }
}
