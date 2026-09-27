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
  createInitialEquipment,
  createInitialHeroStats,
  createSampleEnemies,
  createSampleParty,
  SAMPLE_GROWTH,
  SAMPLE_ITEM,
  SAMPLE_ITEMS_BY_ID,
  SAMPLE_SKILL,
} from "./game/battle/sample-battle";
import { createRng } from "./game/random";
import { computeVictoryExp } from "./game/battle/battle-engine";
import { gainExp } from "./game/growth/level-up";
import { applyStatBonus, computeEquipmentBonus, type EquipmentSlots } from "./game/items/equipment";
import { createInventory, type Inventory } from "./game/items/inventory";
import { SAVE_VERSION, type SaveData } from "./game/save/types";
import { loadFromSlot, saveToSlot } from "./game/save/storage";
import { downloadSaveFile, readSaveFile } from "./io/save-file";
import { AudioEngine } from "./audio/audio-engine";
import { SAMPLE_BGM_LOOP, SAMPLE_CONFIRM_SE } from "./audio/sample-tracks";

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

const audio = new AudioEngine();
let audioStarted = false;
function startAudioOnFirstInteraction(): void {
  if (audioStarted) {
    return;
  }
  audioStarted = true;
  audio.playBgm(SAMPLE_BGM_LOOP);
}
window.addEventListener("keydown", startAudioOnFirstInteraction, { once: true });
window.addEventListener("pointerdown", startAudioOnFirstInteraction, { once: true });
window.addEventListener("keydown", (event) => {
  if (event.key === "m") {
    audio.setMuted(!audio.isMuted());
  }
});

let lastDialogueDirection: Direction | null = null;
let lastBattleDirection: Direction | null = null;
let battle: BattleController | null = null;
let heroStats = createInitialHeroStats();
let heroEquipment: EquipmentSlots = createInitialEquipment();
let inventory: Inventory = createInventory();
let victoryExpApplied = false;
let victoryMessage: string | null = null;
let saveMessage: string | null = null;
let saveMessageTimer = 0;

function buildSaveData(): SaveData {
  return {
    version: SAVE_VERSION,
    savedAt: new Date().toISOString(),
    player: { mapId: currentMapId, tileX: player.x / map.data.tileWidth, tileY: player.y / map.data.tileHeight, direction: player.direction },
    hero: { stats: heroStats, equipment: heroEquipment },
    inventory,
    flags,
  };
}

function applySaveData(data: SaveData): void {
  heroStats = data.hero.stats;
  heroEquipment = data.hero.equipment;
  inventory = data.inventory;
  for (const key of Object.keys(flags)) {
    delete flags[key];
  }
  Object.assign(flags, data.flags);
  switchMap(data.player.mapId, data.player.tileX, data.player.tileY);
  player = { ...player, direction: data.player.direction };
}

function autosave(): void {
  saveToSlot(window.localStorage, "autosave", buildSaveData());
}

const fileInput = document.createElement("input");
fileInput.type = "file";
fileInput.accept = "application/json";
fileInput.style.display = "none";
fileInput.addEventListener("change", () => {
  const file = fileInput.files?.[0];
  if (!file) {
    return;
  }
  readSaveFile(file)
    .then((data) => {
      applySaveData(data);
      saveMessage = "セーブデータを読み込みました";
      saveMessageTimer = 2000;
    })
    .catch(() => {
      saveMessage = "セーブデータを読み込めませんでした";
      saveMessageTimer = 2000;
    })
    .finally(() => {
      fileInput.value = "";
    });
});
document.body.appendChild(fileInput);

if (import.meta.env.DEV) {
  window.addEventListener("keydown", (event) => {
    if (event.key === "b" && !battle && !dialogue.isActive()) {
      victoryExpApplied = false;
      victoryMessage = null;
      const equipmentBonus = computeEquipmentBonus(heroEquipment, SAMPLE_ITEMS_BY_ID);
      const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
      battle = new BattleController(
        createSampleParty(heroStats.level, effectiveStats),
        createSampleEnemies(),
        createRng(Date.now()),
        { skill: SAMPLE_SKILL, item: SAMPLE_ITEM },
      );
    } else if (event.key === "k" && !battle) {
      saveToSlot(window.localStorage, "slot1", buildSaveData());
      saveMessage = "スロット1にセーブしました";
      saveMessageTimer = 2000;
    } else if (event.key === "l" && !battle) {
      const data = loadFromSlot(window.localStorage, "slot1");
      if (data) {
        applySaveData(data);
        saveMessage = "スロット1から読み込みました";
      } else {
        saveMessage = "スロット1にセーブデータがありません";
      }
      saveMessageTimer = 2000;
    } else if (event.key === "j" && !battle) {
      downloadSaveFile(buildSaveData());
    } else if (event.key === "u" && !battle) {
      fileInput.click();
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
  autosave();
}

const loop = createGameLoop({
  update(dtMs) {
    if (saveMessageTimer > 0) {
      saveMessageTimer -= dtMs;
      if (saveMessageTimer <= 0) {
        saveMessageTimer = 0;
        saveMessage = null;
      }
    }

    const actionPressed = actionButton.consume();
    if (actionPressed) {
      audio.playSe(SAMPLE_CONFIRM_SE);
    }

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
      autosave();
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

    if (saveMessage) {
      ctx.fillStyle = "#f2c14e";
      ctx.fillText(saveMessage, 4, 14);
    }

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
