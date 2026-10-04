import { shadeColor } from "../game/color-utils";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";

/**
 * マップ上の「物」（宝箱・木箱・階段・石碑・機械・祭壇・焦げ跡・荷馬車）の絵。1マス（16×16）に、
 * 縁取り・地の色・影の2〜3段で描く（ハイライトなし、光は左上）。種類は、物のIDに含まれる言葉で決める（`character-specs.ts`の OBJECT_WORDS）。
 */
export type ObjectKind = "table" | "tansu" | "bed" | "shelf" | "beacon" | "boat" | "chest" | "crate" | "stairs" | "tablet" | "machine" | "altar" | "scorch" | "wagon" | "sign" | "oldsign" | "generic";

export function objectKindOf(id: string): ObjectKind {
  const words = id.split("-");
  const has = (...ws: string[]): boolean => words.some((w) => ws.includes(w));
  if (has("signpost", "oldsign")) return "oldsign";
  if (has("sign", "signboard")) return "sign";
  if (has("table")) return "table";
  if (has("tansu")) return "tansu";
  if (has("bed")) return "bed";
  if (has("shelf")) return "shelf";
  if (has("beacon")) return "beacon";
  if (has("ferry")) return "boat";
  if (has("chest")) return "chest";
  if (has("crate")) return "crate";
  if (has("stairs", "entrance")) return "stairs";
  if (has("tablet", "mural", "lore", "record", "ledger", "log", "echo", "truth")) return "tablet";
  if (has("machine", "panel", "console")) return "machine";
  if (has("altar", "pedestal", "circle", "fork", "gate")) return "altar";
  if (has("scorch", "excavation")) return "scorch";
  if (has("wagon")) return "wagon";
  return "generic";
}

const INK = "#1c1410";

/** 開けたあとの宝箱の絵: 作りこんだ「開いた箱」から、金貨の山を消して、中の暗がりにしたもの（中身は取ったあと）。 */
let emptyChestArt: HTMLCanvasElement | null = null;
function getEmptyChestArt(): HTMLCanvasElement | null {
  if (emptyChestArt) return emptyChestArt;
  const src = getSpriteCanvas("prop:chest-open", SPRITE_DATA);
  if (!src || typeof document === "undefined") return null;
  const c = document.createElement("canvas");
  c.width = src.width;
  c.height = src.height;
  const g = c.getContext("2d", { willReadFrequently: true });
  if (!g) return null;
  g.drawImage(src, 0, 0);
  const img = g.getImageData(0, 0, c.width, c.height);
  const d = img.data;
  const hex = (r: number, gg: number, b: number): string => ((r << 16) | (gg << 8) | b).toString(16).padStart(6, "0");
  for (let y = 0; y < c.height; y++) {
    for (let x = 0; x < c.width; x++) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] === 0) continue;
      const col = hex(d[i], d[i + 1], d[i + 2]);
      // 金貨の色（明るい金・金）は全部。濃い金（a8761c）は、箱の中（左右の金具の帯のあいだ。絵は48×48の中で、左に11・上に17ずれている）だけ。
      const coin = col === "ffe070" || col === "e0a830" || ((col === "a8761c" || col === "7a5210") && x >= 18 && x <= 29 && y >= 24 && y <= 34);
      if (coin) {
        d[i] = 0x1a;
        d[i + 1] = 0x10;
        d[i + 2] = 0x14;
      }
    }
  }
  g.putImageData(img, 0, 0);
  emptyChestArt = c;
  return c;
}

/** 開けた宝箱のID（`main.ts` が、毎フレーム、フラグから入れる）。 */
let openedChests = new Set<string>();
export function setOpenedChests(ids: Set<string>): void {
  openedChests = ids;
}

/** 光がともっている環灯台の番号（`main.ts` が、毎フレーム、フラグから入れる）。 */
let litBeacons = new Set<number>();
export function setLitBeacons(lit: Set<number>): void {
  litBeacons = lit;
}

function r(ctx: CanvasRenderingContext2D, c: string, x: number, y: number, w: number, h: number): void {
  ctx.fillStyle = c;
  ctx.fillRect(x, y, w, h);
}

function ground(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number): void {
  r(ctx, "rgba(0,0,0,0.28)", x + 2, y + h - 3, w - 4, 2);
}

export function drawObjectMarker(ctx: CanvasRenderingContext2D, kind: ObjectKind, color: string, x: number, y: number, w: number, h: number, id = ""): boolean {
  if (kind === "generic") {
    return false;
  }
  ground(ctx, x, y, w, h);
  const top = y + h - 14;
  switch (kind) {
    case "beacon": {
      // 環灯台: 石の塔（左が地・右が影）と、てっぺんの火皿。ともると、神の色の炎と光が灯る。
      const no = Number(id.split("-").pop());
      const lit = litBeacons.has(no);
      const tx = x + 4;
      const ty = y - 10;
      r(ctx, INK, tx - 1, ty + 8, 10, 18);
      r(ctx, "#a8a8b4", tx, ty + 9, 4, 16);
      r(ctx, "#7a7a88", tx + 4, ty + 9, 4, 16);
      for (let k = 0; k < 4; k++) r(ctx, "#5a5a68", tx, ty + 12 + k * 4, 8, 1);
      r(ctx, INK, tx - 2, ty + 4, 12, 5);
      r(ctx, "#6a6a78", tx - 1, ty + 5, 10, 3);
      r(ctx, lit ? shadeColor(color, -0.2) : "#3a3a44", tx + 1, ty + 2, 6, 3);
      if (lit) {
        const t = typeof performance !== "undefined" ? performance.now() : 0;
        const flick = Math.sin(t / 110 + no) > 0 ? 1 : 0;
        r(ctx, color, tx + 2, ty - 2 - flick, 4, 5 + flick);
        r(ctx, "#fff8d0", tx + 3, ty - 0, 2, 3);
        const g = ctx.createRadialGradient(tx + 4, ty, 2, tx + 4, ty, 26);
        g.addColorStop(0, `${color}88`);
        g.addColorStop(1, `${color}00`);
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.fillStyle = g;
        ctx.fillRect(tx - 24, ty - 26, 56, 56);
        ctx.restore();
      }
      return true;
    }
    case "boat": {
      // 渡し場の小舟と桟橋
      r(ctx, "#6a4a2a", x, y + h - 5, w, 2);
      r(ctx, INK, x + 1, y + h - 9, 14, 6);
      r(ctx, "#a0723c", x + 2, y + h - 8, 12, 4);
      r(ctx, "#74502a", x + 8, y + h - 8, 6, 4);
      r(ctx, "#e8dcc0", x + 7, y + h - 15, 1, 6);
      r(ctx, "#f4f0e0", x + 8, y + h - 15, 4, 4);
      return true;
    }
    case "chest": {
      // 宝箱（16×16）: 丸みのあるふた・鉄の帯・金のかざり・錠。開けたあとは、ふたが開いて空っぽ。光は左上。
      const opened = openedChests.has(id);
      // 作りこんだ宝箱のドット絵（`prop:chest-closed` / `prop:chest-open`）があれば、それを足元にそろえて描く
      const art = opened ? getEmptyChestArt() : getSpriteCanvas("prop:chest-closed", SPRITE_DATA);
      if (art) {
        const prev = ctx.imageSmoothingEnabled;
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(art, Math.round(x + w / 2 - art.width / 2), Math.round(y + h - art.height));
        ctx.imageSmoothingEnabled = prev;
        if (!opened) {
          const t = (performance.now() / 900) % 1;
          if (t < 0.25) r(ctx, "#ffffff", x + w - 5, y + h - art.height + 2, 1, 1);
        }
        return true;
      }
      const IRON = "#46465a";
      const IRON_HI = "#8a8aa0";
      if (opened) {
        r(ctx, INK, x + 1, top + 1, w - 2, 13);
        // 開いたふた（奥に立っている）
        r(ctx, "#8a5a2c", x + 2, top + 2, w - 4, 3);
        r(ctx, "#6a4220", x + 9, top + 2, w - 11, 3);
        r(ctx, IRON, x + 3, top + 2, 2, 3);
        r(ctx, IRON, x + 11, top + 2, 2, 3);
        // 空っぽの中
        r(ctx, "#2a1a10", x + 2, top + 5, w - 4, 3);
        r(ctx, "#4a2e18", x + 2, top + 5, w - 4, 1);
        // 胴
        r(ctx, "#a8742e", x + 2, top + 8, w - 4, 5);
        r(ctx, "#7a5020", x + 9, top + 8, w - 11, 5);
        r(ctx, IRON, x + 3, top + 8, 2, 5);
        r(ctx, IRON, x + 11, top + 8, 2, 5);
        r(ctx, "#e0b038", x + 2, top + 8, w - 4, 1);
        return true;
      }
      r(ctx, INK, x + 1, top + 2, w - 2, 12);
      r(ctx, INK, x + 2, top + 1, w - 4, 1); // ふたの丸み
      // ふた
      r(ctx, "#c8903e", x + 2, top + 2, w - 4, 5);
      r(ctx, "#e0aa58", x + 3, top + 2, w - 8, 1); // 上の照り
      r(ctx, "#8a5a24", x + 10, top + 3, w - 12, 4); // 影の側
      // 胴
      r(ctx, "#a8742e", x + 2, top + 8, w - 4, 5);
      r(ctx, "#6a4220", x + 10, top + 8, w - 12, 5);
      r(ctx, "#8a5a2c", x + 6, top + 8, 1, 5); // 板の継ぎ目
      // 金の帯（ふたと胴のさかい）
      r(ctx, "#f2c14e", x + 2, top + 7, w - 4, 1);
      r(ctx, "#b88418", x + 2, top + 8, w - 4, 1);
      // 鉄の帯（縦）とびょう
      r(ctx, IRON, x + 3, top + 2, 2, 11);
      r(ctx, IRON, x + 11, top + 2, 2, 11);
      r(ctx, IRON_HI, x + 3, top + 3, 1, 1);
      r(ctx, IRON_HI, x + 11, top + 3, 1, 1);
      r(ctx, IRON_HI, x + 3, top + 11, 1, 1);
      r(ctx, IRON_HI, x + 11, top + 11, 1, 1);
      // 錠
      r(ctx, "#f2c14e", x + 6, top + 6, 4, 4);
      r(ctx, "#fff0a0", x + 6, top + 6, 4, 1);
      r(ctx, "#8a6010", x + 7, top + 8, 2, 1);
      r(ctx, "#2a1a08", x + 7, top + 7, 2, 1);
      // ときどききらりと光る（まだ開けていない宝箱の目印）
      const phase = (typeof performance !== "undefined" ? performance.now() : 0) / 900 + (id.length % 5) * 0.37;
      const blink = phase % 1;
      if (blink < 0.18) {
        r(ctx, "#ffffff", x + 2, top, 1, 1);
        r(ctx, "#ffffff", x + 1, top + 1, 3, 1);
        r(ctx, "#ffffff", x + 2, top + 2, 1, 1);
      }
      return true;
    }
    case "table":
    case "tansu":
    case "bed":
    case "shelf": {
      // 作りこんだ家具のドット絵（`prop:*`）があれば、足もとにそろえて描く
      const art = getSpriteCanvas(`prop:${kind === "shelf" ? "bookshelf" : kind}`, SPRITE_DATA);
      if (art) {
        const prev = ctx.imageSmoothingEnabled;
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(art, Math.round(x + w / 2 - art.width / 2), Math.round(y + h - art.height));
        ctx.imageSmoothingEnabled = prev;
        return true;
      }
      return false; // 絵が読めないときは、ふつうの物のしるしで描く
    }
    case "crate": {
      r(ctx, INK, x + 1, top + 2, w - 2, 12);
      r(ctx, "#a0723c", x + 2, top + 3, w - 4, 10);
      r(ctx, "#7a5228", x + 9, top + 3, w - 11, 10);
      r(ctx, "#5a3a1c", x + 2, top + 3, w - 4, 1);
      for (let i = 0; i < 9; i++) {
        r(ctx, "#5a3a1c", x + 3 + i, top + 4 + i, 1, 1);
        r(ctx, "#5a3a1c", x + 11 - i, top + 4 + i, 1, 1);
      }
      return true;
    }
    case "stairs": {
      r(ctx, INK, x + 1, top + 2, w - 2, 12);
      for (let i = 0; i < 4; i++) {
        r(ctx, i % 2 ? "#6a6a78" : "#8a8a98", x + 2, top + 3 + i * 3, w - 4, 2);
        r(ctx, "#3a3a46", x + 2, top + 5 + i * 3, w - 4, 1);
      }
      return true;
    }
    case "sign":
    case "oldsign": {
      // 木の看板（16×16）: 2本の杭に板を打ちつけたもの。光は左上。古い看板は、色あせて、割れ・欠け・コケがあり、少し傾く。
      const old = kind === "oldsign";
      const wood = old ? "#a08a66" : "#c08e50";
      const woodLight = old ? "#b8a47e" : "#dcae6c";
      const woodDark = old ? "#6e5a40" : "#8e6232";
      const grain = old ? "#86714f" : "#a67a40";
      const post = old ? "#6a5238" : "#8a5a2c";
      const postLight = old ? "#82684a" : "#aa7638";
      const postDark = old ? "#4a3826" : "#664020";
      const bx = x + 1;
      const by = y + 1;
      const bw = 14;
      const bh = 7;
      // 杭（板のうしろ。足もとは地面に刺さる）
      for (const px of [x + 4, x + 10]) {
        r(ctx, INK, px - 1, by + bh, 4, h - (by + bh - y) - 1);
        r(ctx, post, px, by + bh, 2, h - (by + bh - y) - 2);
        r(ctx, postLight, px, by + bh, 1, h - (by + bh - y) - 2);
        r(ctx, postDark, px + 1, by + bh, 1, h - (by + bh - y) - 2);
      }
      // 板（ふち取り→地→上の明るい縁→下の影→木目）
      r(ctx, INK, bx, by, bw, bh);
      r(ctx, wood, bx + 1, by + 1, bw - 2, bh - 2);
      r(ctx, woodLight, bx + 1, by + 1, bw - 2, 1);
      r(ctx, woodDark, bx + 1, by + bh - 2, bw - 2, 1);
      r(ctx, grain, bx + 8, by + 4, 4, 1);
      // 釘
      r(ctx, "#3a3a44", bx + 1, by + 1, 1, 1);
      r(ctx, "#3a3a44", bx + bw - 2, by + 1, 1, 1);
      // 彫った文字（横の短い線）
      const ink = old ? "#7a6644" : "#6a4420";
      r(ctx, ink, bx + 3, by + 2, 8, 1);
      r(ctx, ink, bx + 3, by + 4, 6, 1);
      if (old) {
        // 割れ・欠け・コケ
        r(ctx, INK, bx + 9, by + 1, 1, 2);
        r(ctx, INK, bx + 10, by + 3, 1, 2);
        r(ctx, INK, bx + bw - 2, by, 2, 2);
        const moss = "#5f8a3c";
        const mossDark = "#3f6428";
        r(ctx, moss, bx + 2, by + 1, 4, 1);
        r(ctx, mossDark, bx + 1, by + 2, 2, 1);
        r(ctx, moss, bx + 6, by + 1, 2, 1);
        r(ctx, moss, x + 4, y + h - 3, 2, 1);
        r(ctx, mossDark, x + 10, y + h - 3, 2, 1);
      }
      return true;
    }
    case "tablet": {
      // 石板（16×16）: 上が丸い立て石に、台座。左が明るく右が暗い。刻まれた文字がうっすら光り、ひび・欠け・コケがある。
      const stone = "#9ba0ae";
      const light = "#c2c6d2";
      const dark = "#6c7180";
      const deep = "#50556a";
      const glow = shadeColor(color, 0.3);
      const sx = x + 3;
      const sw = 10;
      const st = y + 1;
      // 立て石: 丸い肩を作るため、上の段ほど幅をせまく
      r(ctx, INK, sx + 2, st, sw - 4, 1);
      r(ctx, INK, sx + 1, st + 1, sw - 2, 1);
      r(ctx, INK, sx, st + 2, sw, 11);
      r(ctx, light, sx + 2, st + 1, 3, 1);
      r(ctx, stone, sx + 1, st + 2, sw - 2, 10);
      r(ctx, light, sx + 1, st + 2, 2, 10);
      r(ctx, dark, sx + sw - 3, st + 2, 2, 10);
      r(ctx, deep, sx + sw - 2, st + 3, 1, 9);
      // 台座
      r(ctx, INK, x + 2, y + h - 5, 12, 4);
      r(ctx, "#8a8f9c", x + 3, y + h - 4, 10, 2);
      r(ctx, light, x + 3, y + h - 4, 4, 1);
      r(ctx, dark, x + 3, y + h - 3, 10, 1);
      // 刻まれた文字（輪の印と、短い刻み。光る線と、ほりの影）
      const glyph: Array<[number, string]> = [[3, ".XX."], [4, "X..X"], [5, ".XX."], [7, "X.XX"], [9, "XX.X"]];
      for (const [gy, row] of glyph) {
        for (let k = 0; k < row.length; k++) {
          if (row[k] !== "X") continue;
          if (gy < 9) r(ctx, deep, sx + 3 + k, st + gy + 1, 1, 1);
          r(ctx, glow, sx + 3 + k, st + gy, 1, 1);
        }
      }
      // ひびと欠け・コケ
      r(ctx, dark, sx + 6, st + 2, 1, 2);
      r(ctx, dark, sx + 5, st + 4, 1, 1);
      r(ctx, "#5f8a3c", x + 3, y + h - 5, 3, 1);
      r(ctx, "#3f6428", x + 3, y + h - 6, 1, 1);
      return true;
    }
    case "machine": {
      r(ctx, INK, x + 1, top + 3, w - 2, 11);
      r(ctx, "#6a7684", x + 2, top + 4, w - 4, 9);
      r(ctx, "#4a5462", x + 9, top + 4, w - 11, 9);
      r(ctx, "#2a323c", x + 3, top + 5, 6, 4);
      r(ctx, "#58d878", x + 4, top + 6, 1, 1);
      r(ctx, "#e85858", x + 6, top + 6, 1, 1);
      r(ctx, "#e8c858", x + 11, top + 6, 2, 2);
      r(ctx, "#8a96a4", x + 3, top + 11, 10, 1);
      return true;
    }
    case "altar": {
      r(ctx, INK, x + 2, top + 5, w - 4, 9);
      r(ctx, "#8a8a98", x + 3, top + 6, w - 6, 7);
      r(ctx, "#686876", x + 9, top + 6, w - 12, 7);
      r(ctx, "#a0a0ae", x + 3, top + 6, w - 6, 1);
      // 上に浮かぶ光の結晶（色は物の色）
      const c = shadeColor(color, 0.2);
      r(ctx, INK, x + 6, top, 4, 5);
      r(ctx, c, x + 7, top + 1, 2, 3);
      r(ctx, shadeColor(color, -0.3), x + 8, top + 2, 1, 2);
      return true;
    }
    case "scorch": {
      r(ctx, "rgba(20,12,8,0.55)", x + 2, top + 6, w - 4, 7);
      r(ctx, "rgba(20,12,8,0.7)", x + 4, top + 7, w - 8, 5);
      r(ctx, "#e8681c", x + 5, top + 9, 1, 1);
      r(ctx, "#f0a030", x + 9, top + 8, 1, 1);
      r(ctx, "#3a2a22", x + 3, top + 5, 2, 1);
      r(ctx, "#3a2a22", x + 11, top + 11, 2, 1);
      return true;
    }
    case "wagon": {
      r(ctx, INK, x, top + 3, w, 9);
      r(ctx, "#9a6a38", x + 1, top + 4, w - 2, 6);
      r(ctx, "#74502a", x + 9, top + 4, w - 11, 6);
      r(ctx, "#c8b078", x + 2, top + 2, w - 4, 2);   // 幌
      r(ctx, INK, x + 2, top + 10, 5, 5);
      r(ctx, "#5a4630", x + 3, top + 11, 3, 3);
      r(ctx, INK, x + 10, top + 10, 5, 5);
      r(ctx, "#5a4630", x + 11, top + 11, 3, 3);
      return true;
    }
  }
  return false;
}
