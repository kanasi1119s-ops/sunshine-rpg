/** マップの1つの層（地面、装飾など）。タイルIDを横一列に並べたものを、行の数だけ並べる。 */
export interface TileLayer {
  name: string;
  /** 長さ width*height。0 は「何も描かない」を表す。 */
  data: number[];
}

export interface TileMapData {
  width: number;
  height: number;
  tileWidth: number;
  tileHeight: number;
  layers: TileLayer[];
  /**
   * タイルIDごとの色。ドット絵ができるまでの仮の表示方法。
   * 将来、実際のドット絵タイルセットに差し替える。
   */
  tileColors: Record<number, string>;
  /**
   * タイルIDごとの地形カテゴリ（`tile-art.ts`の`TILE_ART`のキー。例: "grass"）。
   * 指定があれば、単色四角の代わりにそのカテゴリのドット絵模様で描く。
   * 省略時・未対応カテゴリは、これまで通り`tileColors`の色で描く。
   */
  tileArt?: Record<number, string>;
  /** ダンジョン・塔・洞窟などの床と壁の描き方（`dungeon-tiles.ts`）。省略時は従来どおり。 */
  theme?: string;
  /** 雪の地方か。木のタイルに雪をのせる（`ground-decor.ts`）。 */
  snowy?: boolean;
  /** 海岸のある地図（世界地図）。陸が水に接するところに砂浜を描く（`ground-decor.ts`）。 */
  coastal?: boolean;
  /** 町の建物（壁タイルのかたまり）を屋根と壁で描くときの指定（`building-tiles.ts`）。 */
  building?: { walls: number[]; roof: string; plaster: string; tent?: boolean };
  /**
   * 通行判定レイヤー（長さ width*height）。1=通れない、0=通れる。
   * 省略した場合はすべて通行可能とみなす。
   */
  collision?: number[];
  /** 飾り（木・家）。ドット絵を足元のマスにそろえて描き、足元のマスは通れなくする（`map-props.ts`）。 */
  props?: MapProp[];
  /** このタイルに乗ったら別マップへワープする出入り口。 */
  exits?: MapExit[];
}

export interface MapExit {
  tileX: number;
  tileY: number;
  targetMapId: string;
  targetTileX: number;
  targetTileY: number;
}

/** 地図の飾り。(tileX, tileY) は、絵の「足元・中央」のマス。 */
export interface MapProp {
  kind: MapPropKind;
  tileX: number;
  tileY: number;
}

/** 飾りの種類。`prop:<種類>` のドット絵がある。 */
export type MapPropKind = "tree" | "house" | "house-blue" | "house-green" | "manor" | "manor-blue" | "manor-green" | "rock" | "bush" | "tree-snow" | "tree-dead" | "rock-snow" | "bush-snow" | "palm" | "cactus" | "barrel" | "lamp" | "well" | "signpost" | "crates" | "flowerbed" | "icon-port" | "icon-village" | "icon-lake" | "icon-mine" | "icon-castle" | "icon-tents" | "icon-temple" | "icon-snowtown" | "icon-sky" | "icon-palace";
