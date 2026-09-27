import "./style.css";
import { GAME_TITLE } from "./core/status";
import { createGameLoop } from "./core/game-loop";
import { createGameCanvas, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./render/canvas";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("#app が見つかりません");
}
app.innerHTML = "";

const { ctx, resize } = createGameCanvas(app);
resize();
window.addEventListener("resize", resize);

const loop = createGameLoop({
  update() {
    // ここに歩行・戦闘などのゲームの中身を今後追加していく。
  },
  render() {
    ctx.fillStyle = "#182038";
    ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);

    ctx.fillStyle = "#f0f0f0";
    ctx.font = "12px monospace";
    ctx.textBaseline = "top";
    ctx.fillText(GAME_TITLE, 8, 8);
    ctx.fillText("準備中…", 8, 24);

    if (import.meta.env.DEV) {
      ctx.fillStyle = "#88ff88";
      ctx.fillText(`FPS: ${loop.getFps()}`, 8, LOGICAL_HEIGHT - 16);
    }
  },
});

function frame(nowMs: number): void {
  loop.tick(nowMs);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
