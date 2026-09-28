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
import { CHAPTER0_OPENING_COMMANDS, CHAPTER0_START } from "./game/world/chapter0-world";
import { WORLD_MAPS, WORLD_NPCS } from "./game/world/world";
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
import { CHAPTER0_ITEM, CHAPTER0_SKILL, createChapter0Party, createYugamiBoss } from "./game/battle/chapter0-enemies";
import { TOURI_TOWN_SPAWN } from "./game/map/chapter0/touri-town";
import { TOURI_BRANCH_ENTRY } from "./game/map/chapter0/touri-branch";
import { TOURI_OUTSKIRTS_ENTRY } from "./game/map/chapter0/touri-outskirts";
import { MUGIKANO_VILLAGE_ENTRY } from "./game/map/chapter1/mugikano-village";
import { MUGIKANO_WATER_SOURCE_ENTRY } from "./game/map/chapter1/mugikano-water-source";
import { createRng } from "./game/random";
import { computeVictoryExp } from "./game/battle/battle-engine";
import { gainExp } from "./game/growth/level-up";
import { applyStatBonus, computeEquipmentBonus, type EquipmentSlots } from "./game/items/equipment";
import { createInventory, type Inventory } from "./game/items/inventory";
import { SAVE_VERSION, type SaveData } from "./game/save/types";
import { loadFromSlot, saveToSlot } from "./game/save/storage";
import { downloadSaveFile, readSaveFile } from "./io/save-file";
import { AudioEngine } from "./audio/audio-engine";
import { CHAPTER0_BATTLE_THEME, CHAPTER0_BOSS_THEME, CHAPTER0_OUTSKIRTS_THEME, CHAPTER0_TOWN_THEME } from "./audio/chapter0-tracks";
import {
  CHAPTER0_CONFIRM_SE,
  CHAPTER0_CURSOR_SE,
  CHAPTER0_DEFEAT_SE,
  CHAPTER0_DOOR_SE,
  CHAPTER0_VICTORY_SE,
} from "./audio/chapter0-se";
import type { Score } from "./audio/score";
import { createDebugMenuState, moveMenuCursor, toggleMenu } from "./game/debug/debug-menu";
import { renderDebugMenu, type DebugMenuRow } from "./render/debug-menu-renderer";
import { expRequiredForLevel } from "./game/growth/exp-curve";

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

let currentMapId = CHAPTER0_START.mapId;
let map = createTileMap(WORLD_MAPS[currentMapId]);
let npcs = WORLD_NPCS[currentMapId] ?? [];
let player = createPlayer(
  CHAPTER0_START.tileX * map.data.tileWidth,
  CHAPTER0_START.tileY * map.data.tileHeight,
);
let renderCamera = camera;

function switchMap(mapId: string, tileX: number, tileY: number): void {
  const data = WORLD_MAPS[mapId];
  if (!data) {
    return;
  }
  currentMapId = mapId;
  map = createTileMap(data);
  npcs = WORLD_NPCS[mapId] ?? [];
  player = { ...player, x: tileX * map.data.tileWidth, y: tileY * map.data.tileHeight };
  playMapBgm(mapId);
  if (audioStarted) {
    audio.playSe(CHAPTER0_DOOR_SE);
  }
}

/**
 * マップごとのBGM（`docs/sound/tracks.md`）。同じ曲がすでに鳴っていれば鳴らし直さない。
 * 第1章（麦香野）専用の曲はまだ無い（roadmap 4-4で作曲予定）ため、序章の曲を仮に流用する。
 */
function mapBgmFor(mapId: string): Score {
  if (mapId === "touri-outskirts" || mapId === "mugikano-water-source") {
    return CHAPTER0_OUTSKIRTS_THEME;
  }
  return CHAPTER0_TOWN_THEME;
}

let currentBgmTrack: Score | null = null;
function playMapBgm(mapId: string): void {
  if (!audioStarted) {
    return;
  }
  const track = mapBgmFor(mapId);
  if (track === currentBgmTrack) {
    return;
  }
  currentBgmTrack = track;
  audio.playBgm(track);
}

let pendingVictoryFlag: string | null = null;

const dialogue = new DialogueController(flags, {
  onWarp: (warp) => switchMap(warp.mapId, warp.tileX, warp.tileY),
  onStartBattle: (battleId) => startChapter0Battle(battleId),
});

function startChapter0Battle(battleId: string): void {
  if (battleId !== "chapter0-yugami" || battle) {
    return;
  }
  victoryExpApplied = false;
  victoryMessage = null;
  pendingVictoryFlag = "chapter0_yugami_defeated";
  const equipmentBonus = computeEquipmentBonus(heroEquipment, SAMPLE_ITEMS_BY_ID);
  const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
  if (debugInvincible) {
    effectiveStats.maxHp = 99999;
    effectiveStats.hp = 99999;
    effectiveStats.defense = 999;
  }
  battle = new BattleController(
    createChapter0Party(heroStats.level, effectiveStats),
    [createYugamiBoss()],
    createRng(Date.now()),
    { skill: CHAPTER0_SKILL, item: CHAPTER0_ITEM },
  );
  currentBgmTrack = CHAPTER0_BOSS_THEME;
  audio.playBgm(CHAPTER0_BOSS_THEME);
}

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
  playMapBgm(currentMapId);
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
    if (event.key === "b" && !battle && !dialogue.isActive() && !debugMenu.open && !debugNoEncounter) {
      victoryExpApplied = false;
      victoryMessage = null;
      const equipmentBonus = computeEquipmentBonus(heroEquipment, SAMPLE_ITEMS_BY_ID);
      const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
      if (debugInvincible) {
        effectiveStats.maxHp = 99999;
        effectiveStats.hp = 99999;
        effectiveStats.defense = 999;
      }
      battle = new BattleController(
        createSampleParty(heroStats.level, effectiveStats),
        createSampleEnemies(),
        createRng(Date.now()),
        { skill: SAMPLE_SKILL, item: SAMPLE_ITEM },
      );
      currentBgmTrack = CHAPTER0_BATTLE_THEME;
      audio.playBgm(CHAPTER0_BATTLE_THEME);
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

let debugMenu = createDebugMenuState();
let lastDebugDirection: Direction | null = null;
let debugInvincible = false;
let debugNoEncounter = false;

interface DebugMenuRowWithAction extends DebugMenuRow {
  action: () => void;
}

const DEBUG_MENU_ROWS: DebugMenuRowWithAction[] = [
  {
    label: () => "マップ: 灯里の町 へワープ",
    action: () => switchMap("touri-town", TOURI_TOWN_SPAWN.tileX, TOURI_TOWN_SPAWN.tileY),
  },
  {
    label: () => "マップ: 灯里支部（内部） へワープ",
    action: () => switchMap("touri-branch", TOURI_BRANCH_ENTRY.tileX, TOURI_BRANCH_ENTRY.tileY),
  },
  {
    label: () => "マップ: 町外れ・歪みの発生地点 へワープ",
    action: () => switchMap("touri-outskirts", TOURI_OUTSKIRTS_ENTRY.tileX, TOURI_OUTSKIRTS_ENTRY.tileY),
  },
  {
    label: () => "マップ: 麦香野の村 へワープ",
    action: () => switchMap("mugikano-village", MUGIKANO_VILLAGE_ENTRY.tileX, MUGIKANO_VILLAGE_ENTRY.tileY),
  },
  {
    label: () => "マップ: 麦香野・水源 へワープ",
    action: () =>
      switchMap("mugikano-water-source", MUGIKANO_WATER_SOURCE_ENTRY.tileX, MUGIKANO_WATER_SOURCE_ENTRY.tileY),
  },
  {
    label: () => `レベル +1（現在Lv${heroStats.level}）`,
    action: () => {
      heroStats = gainExp(createInitialHeroStats(), expRequiredForLevel(heroStats.level + 1), SAMPLE_GROWTH).stats;
    },
  },
  {
    label: () => `レベル -1（現在Lv${heroStats.level}）`,
    action: () => {
      const targetLevel = Math.max(1, heroStats.level - 1);
      heroStats = gainExp(createInitialHeroStats(), expRequiredForLevel(targetLevel), SAMPLE_GROWTH).stats;
    },
  },
  {
    label: () => `無敵: ${debugInvincible ? "ON" : "OFF"}`,
    action: () => {
      debugInvincible = !debugInvincible;
    },
  },
  {
    label: () => `エンカウントなし: ${debugNoEncounter ? "ON" : "OFF"}`,
    action: () => {
      debugNoEncounter = !debugNoEncounter;
    },
  },
  {
    label: () => "フラグを全部クリア",
    action: () => {
      for (const key of Object.keys(flags)) {
        delete flags[key];
      }
    },
  },
];

if (import.meta.env.DEV) {
  window.addEventListener("keydown", (event) => {
    if (event.key === "`") {
      debugMenu = toggleMenu(debugMenu, DEBUG_MENU_ROWS.length);
    }
  });
}

function applyVictoryExpIfNeeded(finishedBattle: BattleController): void {
  if (victoryExpApplied) {
    return;
  }
  victoryExpApplied = true;
  const outcome = finishedBattle.getUiState();
  if (outcome.kind !== "finished") {
    return;
  }
  if (outcome.outcome === "lost") {
    audio.playSe(CHAPTER0_DEFEAT_SE);
    return;
  }
  if (outcome.outcome !== "won") {
    return;
  }
  audio.playSe(CHAPTER0_VICTORY_SE);
  const expGained = computeVictoryExp(finishedBattle.getState());
  const result = gainExp(heroStats, expGained, SAMPLE_GROWTH);
  heroStats = result.stats;
  victoryMessage =
    result.levelsGained > 0
      ? `${expGained}の経験値を得た！ レベル${heroStats.level}に上がった！`
      : `${expGained}の経験値を得た！`;
  if (pendingVictoryFlag) {
    flags[pendingVictoryFlag] = true;
    pendingVictoryFlag = null;
  }
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
      audio.playSe(CHAPTER0_CONFIRM_SE);
    }

    if (debugMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastDebugDirection) {
        if (direction === "up") {
          debugMenu = moveMenuCursor(debugMenu, -1, DEBUG_MENU_ROWS.length);
          audio.playSe(CHAPTER0_CURSOR_SE);
        } else if (direction === "down") {
          debugMenu = moveMenuCursor(debugMenu, 1, DEBUG_MENU_ROWS.length);
          audio.playSe(CHAPTER0_CURSOR_SE);
        }
        lastDebugDirection = direction;
      }
      if (actionPressed) {
        DEBUG_MENU_ROWS[debugMenu.cursor]?.action();
      }
      return;
    }
    lastDebugDirection = null;

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
            audio.playSe(CHAPTER0_CURSOR_SE);
          } else if (direction === "down" || direction === "right") {
            battle.moveCursor(1);
            audio.playSe(CHAPTER0_CURSOR_SE);
          }
          lastBattleDirection = direction;
        }
      } else {
        lastBattleDirection = null;
      }
      if (actionPressed) {
        if (uiState.kind === "finished") {
          battle = null;
          playMapBgm(currentMapId);
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
            audio.playSe(CHAPTER0_CURSOR_SE);
          } else if (direction === "down") {
            dialogue.moveChoice(1);
            audio.playSe(CHAPTER0_CURSOR_SE);
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
        renderDebugMenu(ctx, debugMenu, DEBUG_MENU_ROWS, LOGICAL_WIDTH, LOGICAL_HEIGHT);
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
      renderDebugMenu(ctx, debugMenu, DEBUG_MENU_ROWS, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }
  },
});

if (!flags["chapter0_intro_seen"]) {
  dialogue.start(CHAPTER0_OPENING_COMMANDS);
}

function frame(nowMs: number): void {
  loop.tick(nowMs);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
