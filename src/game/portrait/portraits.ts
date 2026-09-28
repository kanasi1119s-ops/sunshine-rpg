/**
 * キャラクターの顔グラフィック（ドット絵）。`docs/decisions.md`（2026-09-28、
 * HD-2Dの代わりにドット絵のクオリティを高める方針）に基づき、単色四角の
 * 代わりに使う。既存作品のデザインを参照せず、色番号を並べたデータ
 * （`.claude/skills/rpg-cycle/roles.md` 3-8）として管理し、プログラムで
 * 画像にする。1文字＝1ドット。'.'=何も描かない、'H'=髪、'S'=肌、'E'=目、
 * 'A'=アクセント（服・小物の色）。
 */

import { shadeColor } from "../color-utils";

export type HairStyle = "short" | "long" | "twin" | "slick";
export type PortraitAccessory = "none" | "headband" | "circlet" | "glasses";

export interface PortraitSpec {
  skin: string;
  hair: string;
  eyes: string;
  accent: string;
  hairStyle: HairStyle;
  accessory: PortraitAccessory;
}

export const PORTRAIT_GRID_WIDTH = 12;
export const PORTRAIT_GRID_HEIGHT = 14;

/** 髪型「short」を基準にした、顔・首まわりの共通の土台（左右対称）。 */
const BASE_ROWS: string[] = [
  "....HHHH....",
  "..HHHHHHHH..",
  ".HHHHHHHHHH.",
  "HSSSSSSSSSSH",
  ".SSSSSSSSSS.",
  ".SSESSSSESS.",
  ".SSSSSSSSSS.",
  ".SSSSSSSSSS.",
  "..SSSSSSSS..",
  "...SSSSSS...",
  "....SSSS....",
  "...AAAAAA...",
  "..AAAAAAAA..",
  ".AAAAAAAAAA.",
];

function toGrid(rows: string[]): string[][] {
  return rows.map((row) => row.split(""));
}

function fromGrid(grid: string[][]): string[] {
  return grid.map((row) => row.join(""));
}

function applyHairStyle(style: HairStyle): string[][] {
  const grid = toGrid(BASE_ROWS);
  const set = (row: number, col: number, ch: string): void => {
    grid[row][col] = ch;
  };

  if (style === "slick") {
    // もみあげを消し、撫でつけたような生え際にする。
    grid[3] = ".SSSSSSSSSS.".split("");
  } else if (style === "twin") {
    // 顎から下、左右に細い毛束（ツインテール）を垂らす。
    set(8, 0, "H");
    set(8, 11, "H");
    set(9, 1, "H");
    set(9, 10, "H");
    set(10, 2, "H");
    set(10, 9, "H");
    set(11, 1, "H");
    set(11, 10, "H");
    set(12, 0, "H");
    set(12, 11, "H");
  } else if (style === "long") {
    // 頬から肩まで、髪が顔の両脇を覆うようにする。
    for (const row of [5, 6, 7, 8, 9, 10]) {
      set(row, 0, "H");
      set(row, 11, "H");
    }
    set(11, 0, "H");
    set(11, 1, "H");
    set(11, 10, "H");
    set(11, 11, "H");
    set(12, 0, "H");
    set(12, 1, "H");
    set(12, 10, "H");
    set(12, 11, "H");
    set(13, 0, "H");
    set(13, 11, "H");
  }
  // "short" は土台のまま（追加なし）。

  return grid;
}

function applyAccessory(grid: string[][], accessory: PortraitAccessory): string[][] {
  if (accessory === "headband") {
    for (let col = 1; col <= 10; col++) {
      grid[3][col] = "A";
    }
  } else if (accessory === "circlet") {
    for (let col = 4; col <= 7; col++) {
      grid[2][col] = "A";
    }
  } else if (accessory === "glasses") {
    grid[5][2] = "A";
    grid[5][9] = "A";
  }
  return grid;
}

/** 指定したキャラクターの見た目に応じた、14行×12列のドットの並びを作る。 */
export function buildPortraitRows(spec: PortraitSpec): string[] {
  const withHair = applyHairStyle(spec.hairStyle);
  const withAccessory = applyAccessory(withHair, spec.accessory);
  return fromGrid(withAccessory);
}

/** ドットの記号を、そのキャラクターの色に変換する。'.'は何も描かない。 */
export function colorForCell(spec: PortraitSpec, cell: string): string | null {
  switch (cell) {
    case "H":
      return spec.hair;
    case "S":
      return spec.skin;
    case "E":
      return spec.eyes;
    case "A":
      return spec.accent;
    default:
      return null;
  }
}

export interface ShadedCell {
  row: number;
  col: number;
  color: string;
}

function clampShadeAmount(amount: number): number {
  return Math.max(-0.4, Math.min(0.15, amount));
}

/** そのマスが、何も描かないマスや枠の外に接していれば true（輪郭線を付ける対象）。 */
function isSilhouetteEdge(rows: string[], row: number, col: number): boolean {
  const height = rows.length;
  const width = rows[0].length;
  const neighbors: [number, number][] = [
    [row - 1, col],
    [row + 1, col],
    [row, col - 1],
    [row, col + 1],
  ];
  return neighbors.some(([r, c]) => {
    if (r < 0 || r >= height || c < 0 || c >= width) {
      return true;
    }
    return rows[r][c] === ".";
  });
}

/**
 * 実際に描く色の一覧を作る。単なる単色塗りにせず、(1)左上から光が当たって
 * いるような上→下の明暗、(2)シルエットの輪郭を1段暗くする縁取りを加えて、
 * 単色四角より立体感・視認性のあるドット絵にする（`docs/decisions.md`
 * 「ドット絵のクオリティを高める」方針）。
 */
export function buildShadedCells(spec: PortraitSpec): ShadedCell[] {
  const rows = buildPortraitRows(spec);
  const width = rows[0].length;
  const cells: ShadedCell[] = [];
  for (let row = 0; row < rows.length; row++) {
    for (let col = 0; col < width; col++) {
      const symbol = rows[row][col];
      const baseColor = colorForCell(spec, symbol);
      if (!baseColor) {
        continue;
      }
      const lightFromLeft = col < width / 2 ? 0.05 : -0.02;
      const gradient = clampShadeAmount(-0.018 * row + lightFromLeft);
      const amount = isSilhouetteEdge(rows, row, col) ? Math.min(gradient, -0.3) : gradient;
      cells.push({ row, col, color: shadeColor(baseColor, amount) });
    }
  }
  return cells;
}

/**
 * 会話の話者名（`speaker`）をキーにした、顔グラフィックの登録一覧。
 * `docs/story/characters.md` の主要キャラクターに対応する（CLAUDE.md 1-1、
 * 既存作品のデザインとの酷似なし。配色は各キャラクターの設定・既存の
 * プレースホルダー色を踏まえてオリジナルに決めた）。
 */
export const PORTRAITS: Record<string, PortraitSpec> = {
  ユーリ: {
    skin: "#f0c8a0",
    hair: "#8a4a3a",
    eyes: "#c98a3a",
    accent: "#f2c14e",
    hairStyle: "twin",
    accessory: "none",
  },
  レト: {
    skin: "#e0b48a",
    hair: "#7a2f2f",
    eyes: "#6a6a5a",
    accent: "#a65a5a",
    hairStyle: "short",
    accessory: "none",
  },
  ミナ: {
    skin: "#f2d6bd",
    hair: "#4f8fae",
    eyes: "#3a6ea5",
    accent: "#5a9ac9",
    hairStyle: "long",
    accessory: "none",
  },
  ガイド: {
    skin: "#e6bd8f",
    hair: "#c9a35a",
    eyes: "#4f8f5a",
    accent: "#d68a3a",
    hairStyle: "slick",
    accessory: "headband",
  },
  オルカ: {
    skin: "#b98860",
    hair: "#3a2f28",
    eyes: "#3a2f20",
    accent: "#7a5a3a",
    hairStyle: "short",
    accessory: "none",
  },
  アヤメ: {
    skin: "#eddce8",
    hair: "#b9aee0",
    eyes: "#7a5aa5",
    accent: "#9a8fd0",
    hairStyle: "long",
    accessory: "circlet",
  },
  ドルン: {
    skin: "#d8c0a8",
    hair: "#20201f",
    eyes: "#c9a03a",
    accent: "#5a3a5a",
    hairStyle: "slick",
    accessory: "none",
  },
  カセン: {
    skin: "#d9a878",
    hair: "#7a746a",
    eyes: "#6a4a2f",
    accent: "#7a8fa6",
    hairStyle: "short",
    accessory: "glasses",
  },
  エドレア: {
    skin: "#e5d6c6",
    hair: "#2a2a3a",
    eyes: "#8a8a99",
    accent: "#3f3f6a",
    hairStyle: "long",
    accessory: "circlet",
  },
};
