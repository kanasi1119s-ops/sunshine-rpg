/**
 * 森のふちを四角にしないための小さな道具。四隅へ木のかたまりを食い込ませる。
 * 見本のマップ（森が不ぞろいに広がり、開けた場所とのさかいがぎざぎざ）から学んだ配置。
 * 出入口・道（`keep` が true を返すマス）には置かない。
 */
export function addCornerGroves(
  width: number,
  height: number,
  set: (x: number, y: number) => void,
  keep: (x: number, y: number) => boolean,
  big = false,
): void {
  const shape: Array<[number, number]> = [[1, 1], [2, 1], [1, 2], ...(big ? ([[3, 1], [2, 2], [1, 3]] as Array<[number, number]>) : [])];
  for (const [dx, dy] of shape) {
    for (const [x, y] of [[dx, dy], [width - 1 - dx, dy], [dx, height - 1 - dy], [width - 1 - dx, height - 1 - dy]]) {
      if (x > 0 && y > 0 && x < width - 1 && y < height - 1 && !keep(x, y)) {
        set(x, y);
      }
    }
  }
}
