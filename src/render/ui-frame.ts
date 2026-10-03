/** 会話・戦闘・メニューの窓の枠。紺のグラデーション、金の縁（左上が明るく右下が暗い）、内側の線、四隅の飾り。 */
export function drawWindow(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number): void {
  const grad = ctx.createLinearGradient(0, y, 0, y + h);
  grad.addColorStop(0, "rgba(34, 30, 76, 0.95)");
  grad.addColorStop(1, "rgba(12, 10, 34, 0.96)");
  ctx.fillStyle = grad;
  ctx.fillRect(x, y, w, h);
  // 外側の暗い線
  ctx.strokeStyle = "#0a0818";
  ctx.strokeRect(x - 0.5, y - 0.5, w + 1, h + 1);
  // 金の縁（上と左が明るく、下と右が暗い）
  ctx.fillStyle = "#f0d070";
  ctx.fillRect(x, y, w, 1);
  ctx.fillRect(x, y, 1, h);
  ctx.fillStyle = "#9a6a28";
  ctx.fillRect(x, y + h - 1, w, 1);
  ctx.fillRect(x + w - 1, y, 1, h);
  // 内側の線
  ctx.fillStyle = "#4a4896";
  ctx.fillRect(x + 2, y + 2, w - 4, 1);
  ctx.fillRect(x + 2, y + 2, 1, h - 4);
  ctx.fillStyle = "#1a1844";
  ctx.fillRect(x + 2, y + h - 3, w - 4, 1);
  ctx.fillRect(x + w - 3, y + 2, 1, h - 4);
  // 四隅の飾り（小さな金の点）
  ctx.fillStyle = "#ffe89a";
  for (const [cx, cy] of [[x + 1, y + 1], [x + w - 3, y + 1], [x + 1, y + h - 3], [x + w - 3, y + h - 3]]) {
    ctx.fillRect(cx, cy, 2, 2);
  }
}
