import "./style.css";
import { GAME_TITLE } from "./core/status";
import { createGameLoop } from "./core/game-loop";
import { createGameCanvas, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./render/canvas";
import { createCamera, centerCameraOn } from "./render/camera";
import { renderTileMap } from "./render/tile-map-renderer";
import { renderPlayer } from "./render/player-renderer";
import { createTileMap } from "./game/map/tile-map";
import { createSampleMapData, SAMPLE_MAP_SPAWN } from "./game/map/sample-map";
import { createPlayer, updatePlayer } from "./game/player";
import { InputState } from "./input/input-state";
import { attachKeyboard } from "./input/keyboard";
import { createTouchControls } from "./input/touch-controls";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("#app が見つかりません");
}
app.innerHTML = "";

const { ctx, resize } = createGameCanvas(app);
resize();
window.addEventListener("resize", resize);

const map = createTileMap(createSampleMapData());
const camera = createCamera(LOGICAL_WIDTH, LOGICAL_HEIGHT);

let player = createPlayer(
  SAMPLE_MAP_SPAWN.tileX * map.data.tileWidth,
  SAMPLE_MAP_SPAWN.tileY * map.data.tileHeight,
);
let renderCamera = centerCameraOn(
  camera,
  player.x + player.width / 2,
  player.y + player.height / 2,
  map.widthPx,
  map.heightPx,
);

const input = new InputState();
attachKeyboard(input);
createTouchControls(app, input);

const loop = createGameLoop({
  update(dtMs) {
    player = updatePlayer(player, input.getDirection(), dtMs, map);
    renderCamera = centerCameraOn(
      camera,
      player.x + player.width / 2,
      player.y + player.height / 2,
      map.widthPx,
      map.heightPx,
    );
  },
  render() {
    ctx.fillStyle = "#101018";
    ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);

    renderTileMap(ctx, map, renderCamera);
    renderPlayer(ctx, player, renderCamera);

    ctx.fillStyle = "#f0f0f0";
    ctx.font = "10px monospace";
    ctx.textBaseline = "top";
    ctx.fillText(GAME_TITLE, 4, 2);

    if (import.meta.env.DEV) {
      ctx.fillStyle = "#88ff88";
      ctx.fillText(`FPS: ${loop.getFps()}`, 4, LOGICAL_HEIGHT - 12);
    }
  },
});

function frame(nowMs: number): void {
  loop.tick(nowMs);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
