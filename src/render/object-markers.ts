import { shadeColor } from "../game/color-utils";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";

/**
 * マップ上の「物」（宝箱・木箱・階段・石碑・機械・祭壇・焦げ跡・荷馬車）の絵。1マス（16×16）に、
 * 縁取り・地の色・影の2〜3段で描く（ハイライトなし、光は左上）。種類は、物のIDに含まれる言葉で決める（`character-specs.ts`の OBJECT_WORDS）。
 */
export type ObjectKind = "beacon" | "boat" | "chest" | "crate" | "stairs" | "tablet" | "machine" | "altar" | "scorch" | "wagon" | "generic";

export function objectKindOf(id: string): ObjectKind {
  const words = id.split("-");
  const has = (...ws: string[]): boolean => words.some((w) => ws.includes(w));
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
      const art = getSpriteCanvas(opened ? "prop:chest-open" : "prop:chest-closed", SPRITE_DATA);
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
    case "tablet": {
      r(ctx, INK, x + 3, top, w - 6, 14);
      r(ctx, "#8a8f9c", x + 4, top + 1, w - 8, 12);
      r(ctx, "#686d7a", x + 9, top + 1, w - 13, 12);
      const glow = shadeColor(color, 0.3);
      for (let i = 0; i < 4; i++) {
        r(ctx, glow, x + 5 + (i % 2), top + 3 + i * 2, 4 - (i % 2), 1);
      }
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
