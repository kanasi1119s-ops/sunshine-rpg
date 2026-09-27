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
   * 通行判定レイヤー（長さ width*height）。1=通れない、0=通れる。
   * 省略した場合はすべて通行可能とみなす。
   */
  collision?: number[];
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
