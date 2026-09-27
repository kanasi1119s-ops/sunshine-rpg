import "./style.css";
import { GAME_TITLE } from "./core/status";
import { createGameLoop } from "./core/game-loop";
import { createGameCanvas, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./render/canvas";
import { createCamera, centerCameraOn } from "./render/camera";
import { renderTileMap } from "./render/tile-map-renderer";
import { renderPlayer } from "./render/player-renderer";
import { renderNpcs } from "./render/npc-renderer";
import { renderDialogue } from "./render/dialogue-renderer";
import { createTileMap, findExitAt } from "./game/map/tile-map";
import { createPlayer, updatePlayer } from "./game/player";
import { findNpcAt, getFacingTile } from "./game/npc";
import { DialogueController } from "./game/dialogue/dialogue-controller";
import type { Flags } from "./game/event/types";
import { InputState } from "./input/input-state";
import { ActionButton } from "./input/action-button";
import { attachKeyboard } from "./input/keyboard";
import { createTouchControls } from "./input/touch-controls";
import type { Direction } from "./input/direction";
import { SAMPLE_MAPS, SAMPLE_NPCS, SAMPLE_START } from "./game/world/sample-world";
import { BattleController } from "./game/battle/battle-controller";
import { renderBattle } from "./render/battle-renderer";
import {
  createInitialHeroStats,
  createSampleEnemies,
  createSampleParty,
  SAMPLE_GROWTH,
  SAMPLE_ITEM,
  SAMPLE_SKILL,
} from "./game/battle/sample-battle";
import { createRng } from "./game/random";
import { computeVictoryExp } from "./game/battle/battle-engine";
import { gainExp } from "./game/growth/level-up";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("#app が見つかりません");
}
app.innerHTML = "";

const { ctx, resize } = createGameCanvas(app);
resize();
window.addEventListener("resize", resize);

const flags: Flags = {};
const camera = createCamera(LOGICAL_WIDTH, LOGICAL_HEIGHT);

let currentMapId = SAMPLE_START.mapId;
let map = createTileMap(SAMPLE_MAPS[currentMapId]);
let npcs = SAMPLE_NPCS[currentMapId] ?? [];
let player = createPlayer(
  SAMPLE_START.tileX * map.data.tileWidth,
  SAMPLE_START.tileY * map.data.tileHeight,
);
let renderCamera = camera;

function switchMap(mapId: string, tileX: number, tileY: number): void {
  const data = SAMPLE_MAPS[mapId];
  if (!data) {
    return;
  }
  currentMapId = mapId;
  map = createTileMap(data);
  npcs = SAMPLE_NPCS[mapId] ?? [];
  player = { ...player, x: tileX * map.data.tileWidth, y: tileY * map.data.tileHeight };
}

const dialogue = new DialogueController(flags, {
  onWarp: (warp) => switchMap(warp.mapId, warp.tileX, warp.tileY),
});

const input = new InputState();
const actionButton = new ActionButton();
attachKeyboard(input, actionButton);
createTouchControls(app, input, actionButton);

let lastDialogueDirection: Direction | null = null;
let lastBattleDirection: Direction | null = null;
let battle: BattleController | null = null;
let heroStats = createInitialHeroStats();
let victoryExpApplied = false;
let victoryMessage: string | null = null;

if (import.meta.env.DEV) {
  window.addEventListener("keydown", (event) => {
    if (event.key === "b" && !battle && !dialogue.isActive()) {
      victoryExpApplied = false;
      victoryMessage = null;
      battle = new BattleController(
        createSampleParty(heroStats),
        createSampleEnemies(),
        createRng(Date.now()),
        { skill: SAMPLE_SKILL, item: SAMPLE_ITEM },
      );
    }
  });
}

function applyVictoryExpIfNeeded(finishedBattle: BattleController): void {
  if (victoryExpApplied) {
    return;
  }
  victoryExpApplied = true;
  const outcome = finishedBattle.getUiState();
  if (outcome.kind !== "finished" || outcome.outcome !== "won") {
    return;
  }
  const expGained = computeVictoryExp(finishedBattle.getState());
  const result = gainExp(heroStats, expGained, SAMPLE_GROWTH);
  heroStats = result.stats;
  victoryMessage =
    result.levelsGained > 0
      ? `${expGained}の経験値を得た！ レベル${heroStats.level}に上がった！`
      : `${expGained}の経験値を得た！`;
}

const loop = createGameLoop({
  update(dtMs) {
    const actionPressed = actionButton.consume();

    if (battle) {
      const uiState = battle.getUiState();
      if (uiState.kind === "finished") {
        applyVictoryExpIfNeeded(battle);
      }
      if (uiState.kind === "command" || uiState.kind === "target") {
        const direction = input.getDirection();
        if (direction !== lastBattleDirection) {
          if (direction === "up" || direction === "left") {
            battle.moveCursor(-1);
          } else if (direction === "down" || direction === "right") {
            battle.moveCursor(1);
          }
          lastBattleDirection = direction;
        }
      } else {
        lastBattleDirection = null;
      }
      if (actionPressed) {
        if (uiState.kind === "finished") {
          battle = null;
        } else {
          battle.confirm();
        }
      }
      return;
    }
    lastBattleDirection = null;

    if (dialogue.isActive()) {
      dialogue.update(dtMs);
      const state = dialogue.getRenderState();
      if (state?.kind === "choice") {
        const direction = input.getDirection();
        if (direction !== lastDialogueDirection) {
          if (direction === "up") {
            dialogue.moveChoice(-1);
          } else if (direction === "down") {
            dialogue.moveChoice(1);
          }
          lastDialogueDirection = direction;
        }
      } else {
        lastDialogueDirection = null;
      }
      if (actionPressed) {
        dialogue.confirm();
      }
      return;
    }
    lastDialogueDirection = null;

    player = updatePlayer(player, input.getDirection(), dtMs, map);
    renderCamera = centerCameraOn(
      camera,
      player.x + player.width / 2,
      player.y + player.height / 2,
      map.widthPx,
      map.heightPx,
    );

    const centerTileX = Math.floor((player.x + player.width / 2) / map.data.tileWidth);
    const centerTileY = Math.floor((player.y + player.height / 2) / map.data.tileHeight);
    const exit = findExitAt(map, centerTileX, centerTileY);
    if (exit) {
      switchMap(exit.targetMapId, exit.targetTileX, exit.targetTileY);
      return;
    }

    if (actionPressed) {
      const facing = getFacingTile(player, map.data.tileWidth, map.data.tileHeight);
      const npc = findNpcAt(npcs, facing.tileX, facing.tileY);
      if (npc) {
        dialogue.start(npc.commands);
      }
    }
  },
  render() {
    ctx.fillStyle = "#101018";
    ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);

    if (battle) {
      renderBattle(ctx, battle.getState(), battle.getUiState(), LOGICAL_WIDTH, LOGICAL_HEIGHT);
      if (victoryMessage && battle.getUiState().kind === "finished") {
        ctx.fillStyle = "#f2c14e";
        ctx.font = "10px monospace";
        ctx.textBaseline = "top";
        ctx.fillText(victoryMessage, 8, LOGICAL_HEIGHT - 56 + 18);
      }
      if (import.meta.env.DEV) {
        ctx.fillStyle = "#88ff88";
        ctx.font = "10px monospace";
        ctx.textBaseline = "top";
        ctx.fillText(`FPS: ${loop.getFps()}`, 4, LOGICAL_HEIGHT - 12);
      }
      return;
    }

    renderTileMap(ctx, map, renderCamera);
    renderNpcs(ctx, npcs, map, renderCamera);
    renderPlayer(ctx, player, renderCamera);

    const dialogueState = dialogue.getRenderState();
    if (dialogueState) {
      renderDialogue(ctx, dialogueState, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }

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
