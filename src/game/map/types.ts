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
  /** 地図の下に敷く1枚絵（`sprite-data` の名前。例 "prop:church-interior"）。あればタイルの代わりにこの絵を描く（通れるかは collision のまま）。 */
  backdropSprite?: string;
  /** 1枚絵の中の、ろうそくの炎の位置（絵の左上からのドット）。ゲームで揺らめかせる。 */
  backdropFlames?: readonly { x: number; y: number; big: boolean }[];
  /** 上下左右がつながる地図（世界地図）。端から出ると、反対の端から入る。 */
  wrap?: boolean;
  /**
   * タイルIDごとの地形カテゴリ（`tile-art.ts`の`TILE_ART`のキー。例: "grass"）。
   * 指定があれば、単色四角の代わりにそのカテゴリのドット絵模様で描く。
   * 省略時・未対応カテゴリは、これまで通り`tileColors`の色で描く。
   */
  tileArt?: Record<number, string>;
  /** タイルid → 128×128の地形テクスチャのキー（`sprite-data.generated.ts` の `terrain:*`）。あれば `tileArt` より先に使う（全体フィールド用、2026-10-04）。 */
  tileTexture?: Record<number, string>;
  /** ダンジョン・塔・洞窟などの床と壁の描き方（`dungeon-tiles.ts`）。省略時は従来どおり。 */
  theme?: string;
  /** 町を囲む石の塀を、地図のいちばん外の1マスに描く（出入り口は門としてあける。`render/town-wall.ts`）。 */
  townWall?: boolean;
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
  /** このフラグが立っていないと通れない（仕掛けの扉・灯りがないと進めない道など）。 */
  requireFlag?: string;
  /** 家の玄関など: この向きに押しているときだけ入る（前を通るだけでは入らない）。 */
  enter?: "up" | "down" | "left" | "right";
  /** 通れないときに出す言葉（ヒント）。 */
  blockedMessage?: string;
}

/** 地図の飾り。(tileX, tileY) は、絵の「足元・中央」のマス。 */
export interface MapProp {
  kind: MapPropKind;
  tileX: number;
  tileY: number;
}

/** 飾りの種類。`prop:<種類>` のドット絵がある。 */
export type MapPropKind = "tree" | "church" | "church-interior" | "house" | "house-blue" | "house-green" | "house-white" | "manor" | "manor-blue" | "manor-green" | "rock" | "bush" | "tree-snow" | "tree-pine" | "tree-dead" | "rock-snow" | "bush-snow" | "palm" | "cactus" | "barrel" | "lamp" | "well" | "signpost" | "crates" | "flowerbed" | "icon-port" | "icon-village" | "icon-lake" | "icon-mine" | "icon-castle" | "icon-tents" | "icon-temple" | "icon-snowtown" | "icon-sky" | "icon-palace" | "icon-ruin" | "icon-shrine" | "icon-cave" | "icon-stones" | "icon-bigtree" | "icon-vortex" | "icon-volcano" | "icon-dive" | "icon-spire" | "icon-islet-ruin" | "icon-islet-cave" | "icon-islet-shrine" | "icon-islet-fort" | "icon-hut" | "icon-core-spire" | "icon-village-mist" | "icon-tents-grass" | "icon-mineshaft"
  | "fountain" | "stall" | "haystack" | "cart" | "laundry" | "fence" | "fence-end" | "bench" | "statue-traveler" | "grave-cross" | "grave-round" | "noticeboard" | "brazier" | "shrine" | "pillar" | "pillar-broken" | "statue-soldier" | "statue-winged" | "banner-purple" | "banner-red" | "bones" | "cobweb" | "candelabra" | "coffin" | "barrel-broken" | "box-broken" | "crystal-blue" | "crystal-red" | "mushrooms" | "chest-closed" | "chest-open" | "chains" | "jail-bars" | "tent";
