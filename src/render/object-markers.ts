import { shadeColor } from "../game/color-utils";

/**
 * マップ上の「物」（宝箱・木箱・階段・石碑・機械・祭壇・焦げ跡・荷馬車）の絵。1マス（16×16）に、
 * 縁取り・地の色・影の2〜3段で描く（ハイライトなし、光は左上）。種類は、物のIDに含まれる言葉で決める（`character-specs.ts`の OBJECT_WORDS）。
 */
export type ObjectKind = "chest" | "crate" | "stairs" | "tablet" | "machine" | "altar" | "scorch" | "wagon" | "generic";

export function objectKindOf(id: string): ObjectKind {
  const words = id.split("-");
  const has = (...ws: string[]): boolean => words.some((w) => ws.includes(w));
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

function r(ctx: CanvasRenderingContext2D, c: string, x: number, y: number, w: number, h: number): void {
  ctx.fillStyle = c;
  ctx.fillRect(x, y, w, h);
}

function ground(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number): void {
  r(ctx, "rgba(0,0,0,0.28)", x + 2, y + h - 3, w - 4, 2);
}

export function drawObjectMarker(ctx: CanvasRenderingContext2D, kind: ObjectKind, color: string, x: number, y: number, w: number, h: number): boolean {
  if (kind === "generic") {
    return false;
  }
  ground(ctx, x, y, w, h);
  const top = y + h - 14;
  switch (kind) {
    case "chest": {
      r(ctx, INK, x + 1, top + 3, w - 2, 11);
      r(ctx, "#8a5a2c", x + 2, top + 8, w - 4, 5);   // 胴
      r(ctx, "#6a4220", x + 9, top + 8, w - 11, 5);  // 胴（影の側）
      r(ctx, "#a8742e", x + 2, top + 4, w - 4, 4);   // ふた
      r(ctx, "#7a5020", x + 9, top + 4, w - 11, 4);
      r(ctx, "#e0b038", x + 2, top + 8, w - 4, 1);   // 金の帯
      r(ctx, "#e0b038", x + 7, top + 6, 2, 4);       // 錠
      r(ctx, "#6a4a10", x + 7, top + 8, 2, 1);
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
