import "./style.css";
import { GAME_TITLE } from "./core/status";
import { backTitle, confirmTitle, createTitleState, moveTitleCursor } from "./game/title/title-menu";
import { renderTitle } from "./render/title-renderer";
import { battleSeFor } from "./game/battle/battle-se";
import { battleEffectFor, type BattleEffect } from "./game/battle/battle-effect";
import { createStaffRollState, skipStaffRoll, startStaffRoll, updateStaffRoll } from "./game/title/staff-roll";
import { renderStaffRoll } from "./render/staff-roll-renderer";
import { addGold, computeVictoryGold } from "./game/economy/gold";
import { ALL_ITEMS_BY_ID, buyItem } from "./game/economy/shop";
import { closeShopMenu, createShopMenuState, moveShopCursor, openShopMenu, withShopMessage } from "./game/economy/shop-menu";
import { renderShop } from "./render/shop-renderer";
import { backPauseMenu, confirmPauseMenu, createPauseMenuState, movePauseCursor, openPauseMenu } from "./game/menu/pause-menu";
import { renderPauseMenu, type StatusRow } from "./render/pause-menu-renderer";
import { expToNextLevel } from "./game/growth/exp-curve";
import { createGameLoop } from "./core/game-loop";
import { createGameCanvas, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./render/canvas";
import { createCamera, centerCameraOn } from "./render/camera";
import { renderTileMap } from "./render/tile-map-renderer";
import { renderPlayer } from "./render/player-renderer";
import { npcFeetY, renderNpcs } from "./render/npc-renderer";
import { faceNpc, opposite, updateWander } from "./game/npc-wander";
import { PartyTrail } from "./game/party-trail";
import { worldEntryProblems } from "./game/world/world-map-world";
import { buildVehicleCollision, canLandOn, groundIdAt, OCEAN, closeVortexChannel, openVortexChannel, VEHICLE_SPEED, type Vehicle } from "./game/vehicle";
import { WORLD_AIRSHIP_START, WORLD_SHIP_START } from "./game/map/world/world-map.generated";
import { drawAirship, drawShip } from "./render/vehicle-renderer";
import { renderStorm, renderVortex } from "./render/vortex-renderer";
import { setLitBeacons } from "./render/object-markers";
import { renderWorldOverview } from "./render/world-overview";
import { renderFollowers } from "./render/follower-renderer";
import { spriteSpecFromPortrait } from "./game/sprite/character-specs";
import { PORTRAITS } from "./game/portrait/portraits";
import { propFeetY, renderProps } from "./render/prop-renderer";
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
import { CHAPTER1_OPENING_COMMANDS } from "./game/world/chapter1-world";
import { CHAPTER2_OPENING_COMMANDS } from "./game/world/chapter2-world";
import { CHAPTER3_OPENING_COMMANDS } from "./game/world/chapter3-world";
import { CHAPTER4_OPENING_COMMANDS } from "./game/world/chapter4-world";
import { CHAPTER5_OPENING_COMMANDS } from "./game/world/chapter5-world";
import { WORLD_MAPS, WORLD_NPCS } from "./game/world/world";
import { BattleController } from "./game/battle/battle-controller";
import { awardVictoryMastery, changeJob, isJobSystemUnlocked, battleSkillsOf, withJobBonus } from "./game/job/party-job";
import { renderBattle, setBattleBiome } from "./render/battle-renderer";
import { biomeForMap, type Biome } from "./render/battle-backdrop";
import {
  createInitialEquipment,
  createInitialHeroStats,
  createSampleEnemies,
  SAMPLE_GROWTH,
  SAMPLE_ITEM,
  SAMPLE_SKILL,
} from "./game/battle/sample-battle";
import { CHAPTER0_ITEM, CHAPTER0_SKILL, createChapter0Party, createYugamiBoss } from "./game/battle/chapter0-enemies";
import { createMugikanoYugami } from "./game/battle/chapter1-enemies";
import { createGarasukoYugami } from "./game/battle/chapter2-enemies";
import { createTetsukusariYugami } from "./game/battle/chapter3-enemies";
import { createSanoneSunaarashiYugami } from "./game/battle/chapter4-enemies";
import { createKiriYogenYugami } from "./game/battle/chapter5-enemies";
import { createShimoharaShisakukiYugami } from "./game/battle/chapter6-enemies";
import { CHAPTER6_OPENING_COMMANDS } from "./game/world/chapter6-world";
import { createFushimaKanshitakuYugami } from "./game/battle/chapter7-enemies";
import { CHAPTER7_OPENING_COMMANDS } from "./game/world/chapter7-world";
import { createToushinBanninYugami } from "./game/battle/chapter8-enemies";
import { CHAPTER8_OPENING_COMMANDS } from "./game/world/chapter8-world";
import { createKyotoukyuEdreaYugami } from "./game/battle/chapter9-enemies";
import { CHAPTER9_OPENING_COMMANDS } from "./game/world/chapter9-world";
import { createDeepEchoYugami, createShogenYugami } from "./game/battle/chapter10-enemies";
import { DEEP_ENTRY } from "./game/map/chapter10/deep-maps";
import { createGodYugami, GODS } from "./game/battle/chapter11-enemies";
import { createDungeonEnemy, DUNGEON_ENEMIES } from "./game/battle/chapter12-enemies";
import { createEncounterEnemies, createEncounterState, ENCOUNTER_ZONES, stepEncounter, WORLD_ENCOUNTER_ZONES, worldZoneIdAt, type EncounterState } from "./game/encounter/encounter";
import { KYOTOUKYU_CORRIDOR_ENTRY, KYOTOUKYU_COURT_ENTRY, KYOTOUKYU_SANCTUM_ENTRY } from "./game/map/chapter9/kyotoukyu-maps";
import { AYAME, COMPANIONS, createCompanionCombatant, GUIDE, MINA, ORCA, RETO } from "./game/battle/companions";
import type { Combatant, Skill } from "./game/battle/types";
import type { LeveledStats } from "./game/growth/types";
import { TOURI_TOWN_SPAWN } from "./game/map/chapter0/touri-town";
import { TOURI_BRANCH_ENTRY } from "./game/map/chapter0/touri-branch";
import { TOURI_OUTSKIRTS_ENTRY } from "./game/map/chapter0/touri-outskirts";
import { MUGIKANO_VILLAGE_ENTRY } from "./game/map/chapter1/mugikano-village";
import { MUGIKANO_WATER_SOURCE_ENTRY } from "./game/map/chapter1/mugikano-water-source";
import { GARASUKO_TOWN_ENTRY } from "./game/map/chapter2/garasuko-town";
import { GARASUKO_WAREHOUSE_ENTRY } from "./game/map/chapter2/garasuko-warehouse";
import { TETSUKUSARI_TOWN_ENTRY } from "./game/map/chapter3/tetsukusari-town";
import { SANONE_TOWN_ENTRY } from "./game/map/chapter4/sanone-town";
import { SANONE_CAMP_ENTRY } from "./game/map/chapter4/sanone-camp";
import { KIRI_TOWN_ENTRY } from "./game/map/chapter5/kiri-town";
import { KIRI_ARCHIVE_ENTRY } from "./game/map/chapter5/kiri-archive";
import { SHIMOHARA_TOWN_ENTRY } from "./game/map/chapter6/shimohara-town";
import { SHIMOHARA_FACILITY_ENTRY } from "./game/map/chapter6/shimohara-facility";
import { FUSHIMA_TOWN_ENTRY } from "./game/map/chapter7/fushima-town";
import { FUSHIMA_BASE_ENTRY } from "./game/map/chapter7/fushima-base";
import { TOUSHIN_TOWN_ENTRY } from "./game/map/chapter8/toushin-town";
import { TOUSHIN_HALL_ENTRY } from "./game/map/chapter8/toushin-hall";
import { TETSUKUSARI_MINE_ENTRY } from "./game/map/chapter3/tetsukusari-mine";
import { createRng } from "./game/random";
import { computeVictoryExp } from "./game/battle/battle-engine";
import { gainExp, statsAtLevel } from "./game/growth/level-up";
import { applyStatBonus, computeEquipmentBonus, type EquipmentSlots } from "./game/items/equipment";
import { createInventory, type Inventory } from "./game/items/inventory";
import type { JobId, JobState } from "./game/job/types";
import { availableJobs } from "./game/job/jobs";
import { createJobState, starsOf } from "./game/job/mastery";
import { SAVE_VERSION, type SaveData } from "./game/save/types";
import { loadFromSlot, saveToSlot } from "./game/save/storage";
import { downloadSaveFile, readSaveFile } from "./io/save-file";
import { AudioEngine } from "./audio/audio-engine";
import { getTrackEdition, type Edition } from "./audio/catalog";
import "./audio/user-songs";
import { SE_LIBRARY } from "./audio/se-library";
import type { Score } from "./audio/score";
import { createDebugMenuState, moveMenuCursor, toggleMenu } from "./game/debug/debug-menu";
import { cancelJobMenu, confirmJobMenu, createJobMenuState, moveJobMenu, openJobMenu } from "./game/job/job-menu";
import { renderJobMenu } from "./render/job-menu-renderer";
import { renderDebugMenu, type DebugMenuRow } from "./render/debug-menu-renderer";
import { expRequiredForLevel } from "./game/growth/exp-curve";

/**
 * BGMの版。既定は現代的な音（modern）。`?edition=ps2`（PS2世代のサウンド版）や `?edition=real`（実際のバンド・オーケストラ・楽器の音色の版）をつけて開くと、その版で鳴る。
 */
const EDITION_PARAM = new URLSearchParams(window.location.search).get("edition");
const BGM_EDITION: Edition = EDITION_PARAM === "ps2" ? "ps2" : EDITION_PARAM === "real" ? "real" : "modern";
function getTrack(id: string): Score {
  return getTrackEdition(id, BGM_EDITION);
}

/** 効果音ライブラリ（`src/audio/se-library.ts`）から、IDで効果音を取り出す。 */
function seOf(id: string): Score {
  const entry = SE_LIBRARY.find((e) => e.id === id);
  if (!entry) {
    throw new Error(`効果音がありません: ${id}`);
  }
  return entry.score;
}

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

const partyTrail = new PartyTrail();

// ===== 乗り物（船・飛空艇）。世界地図だけ。 =====
let vehicle: Vehicle = "foot";
/** 停泊中の船（海のマス）・着陸中の飛空艇（陸のマス）の位置。 */
let shipPos = { x: WORLD_SHIP_START.x, y: WORLD_SHIP_START.y };
let airshipPos = { x: WORLD_AIRSHIP_START.x, y: WORLD_AIRSHIP_START.y };
let lastOceanTile = { x: WORLD_SHIP_START.x, y: WORLD_SHIP_START.y };
let prevWorldTile = { x: -1, y: -1 };
let vehicleMaps: { ship: ReturnType<typeof createTileMap>; air: ReturnType<typeof createTileMap> } | null = null;
let channelOpened = false;
let parkedShipIndex = -1;
let vehicleHint: { text: string; ms: number } | null = null;

function worldMapData() {
  return WORLD_MAPS["world-map"];
}

/** 乗り物の通行判定の地図（航路が開いたら作り直す）。 */
function getVehicleMaps() {
  const data = worldMapData();
  if (!vehicleMaps) {
    vehicleMaps = {
      ship: createTileMap({ ...data, collision: buildVehicleCollision(data, "ship") }),
      air: createTileMap({ ...data, collision: buildVehicleCollision(data, "air") }),
    };
  }
  return vehicleMaps;
}

/** 世界地図の状態をフラグにそろえる: 航路が開いたら渦の切れ目を海にし、停泊中の船のマスは、歩いて乗れるよう通れるようにする。 */
function syncWorldState(): void {
  const data = worldMapData();
  if (flags["vortex_route_open"] && !channelOpened) {
    channelOpened = true;
    if (openVortexChannel(data)) {
      vehicleMaps = null;
    }
  } else if (!flags["vortex_route_open"] && channelOpened) {
    // 「はじめから」やロードで、航路が開く前の状態に戻った
    channelOpened = false;
    if (closeVortexChannel(data)) {
      vehicleMaps = null;
    }
  }
  const want = flags["has_ship"] && vehicle !== "ship" ? shipPos.y * data.width + shipPos.x : -1;
  if (want !== parkedShipIndex) {
    if (parkedShipIndex >= 0 && data.collision) {
      data.collision[parkedShipIndex] = 1;
    }
    if (want >= 0 && data.collision) {
      data.collision[want] = 0;
    }
    parkedShipIndex = want;
  }
}

/** 歩いたあとの乗り降り。決定ボタンを使ったら true。 */
function updateVehicleAfterMove(tile: { x: number; y: number }, actionPressed: boolean): boolean {
  const data = worldMapData();
  const ground = groundIdAt(data, tile.x, tile.y);
  const entering = prevWorldTile.x !== tile.x || prevWorldTile.y !== tile.y;
  let usedAction = false;
  if (vehicle === "foot") {
    if (entering && flags["has_ship"] && tile.x === shipPos.x && tile.y === shipPos.y) {
      vehicle = "ship";
      lastOceanTile = { x: tile.x, y: tile.y };
      vehicleHint = { text: "船にのった。海を進める（海岸に近づくと、自動で降りる）。", ms: 3200 };
      if (audioStarted) audio.playSe(seOf("door"));
    } else if (entering && flags["has_airship"] && tile.x === airshipPos.x && tile.y === airshipPos.y) {
      vehicle = "air";
      vehicleHint = { text: "飛空艇にのった。決定ボタンで着陸できる。", ms: 3200 };
      if (audioStarted) audio.playSe(seOf("door"));
    }
  } else if (vehicle === "ship") {
    if (ground === OCEAN) {
      lastOceanTile = { x: tile.x, y: tile.y };
    } else {
      vehicle = "foot";
      shipPos = { ...lastOceanTile };
      vehicleHint = { text: "船を降りた。船は海岸にとめてある。", ms: 2800 };
    }
  } else if (vehicle === "air" && actionPressed) {
    usedAction = true;
    if (canLandOn(ground) && !findExitAt(map, tile.x, tile.y)) {
      vehicle = "foot";
      airshipPos = { x: tile.x, y: tile.y };
      vehicleHint = { text: "着陸した。", ms: 2000 };
    } else {
      vehicleHint = { text: "ここには着陸できない。", ms: 1800 };
    }
  }
  prevWorldTile = { x: tile.x, y: tile.y };
  return usedAction;
}

/** ついてくる仲間（加入済みの仲間）の、マップ用の絵の設計。加入した順。 */
function followerSpecs(): ReturnType<typeof spriteSpecFromPortrait>[] {
  const specs: ReturnType<typeof spriteSpecFromPortrait>[] = [];
  for (const id of Object.keys(companionStats)) {
    const name = COMPANIONS[id]?.name;
    const portrait = name ? PORTRAITS[name] : undefined;
    if (name && portrait) {
      specs.push(spriteSpecFromPortrait(portrait, name));
    }
  }
  return specs;
}

function switchMap(mapId: string, tileX: number, tileY: number): void {
  const data = WORLD_MAPS[mapId];
  if (!data) {
    return;
  }
  currentMapId = mapId;
  map = createTileMap(data);
  npcs = WORLD_NPCS[mapId] ?? [];
  player = { ...player, x: tileX * map.data.tileWidth, y: tileY * map.data.tileHeight };
  partyTrail.reset(player);
  vehicle = "foot";
  prevWorldTile = { x: -1, y: -1 };
  playMapBgm(mapId);
  if (audioStarted) {
    audio.playSe(seOf("door"));
  }
  if (mapId === "mugikano-village" && !flags["chapter1_intro_seen"]) {
    dialogue.start(CHAPTER1_OPENING_COMMANDS);
  }
  if (mapId === "garasuko-town" && !flags["chapter2_intro_seen"]) {
    dialogue.start(CHAPTER2_OPENING_COMMANDS);
  }
  if (mapId === "tetsukusari-town" && !flags["chapter3_intro_seen"]) {
    dialogue.start(CHAPTER3_OPENING_COMMANDS);
  }
  if (mapId === "sanone-town" && !flags["chapter4_intro_seen"]) {
    dialogue.start(CHAPTER4_OPENING_COMMANDS);
  }
  if (mapId === "kiri-town" && !flags["chapter5_intro_seen"]) {
    dialogue.start(CHAPTER5_OPENING_COMMANDS);
  }
  if (mapId === "shimohara-town" && !flags["chapter6_intro_seen"]) {
    dialogue.start(CHAPTER6_OPENING_COMMANDS);
  }
  if (mapId === "fushima-town" && !flags["chapter7_intro_seen"]) {
    dialogue.start(CHAPTER7_OPENING_COMMANDS);
  }
  if (mapId === "toushin-town" && !flags["chapter8_intro_seen"]) {
    dialogue.start(CHAPTER8_OPENING_COMMANDS);
  }
  if (mapId === "kyotoukyu-court" && !flags["chapter9_intro_seen"]) {
    dialogue.start(CHAPTER9_OPENING_COMMANDS);
  }
}

/**
 * マップごとのBGM（`docs/sound/tracks.md`）。同じ曲がすでに鳴っていれば鳴らし直さない。
 */
const MAP_BGM_ID: Record<string, string> = {
  "touri-town": "town-touri",
  "touri-branch": "town-touri",
  "touri-outskirts": "outskirts",
  "world-map": "field",
  "mugikano-village": "town-mugikano",
  "mugikano-water-source": "water-source",
  "garasuko-town": "town-garasuko",
  "garasuko-warehouse": "warehouse",
  "tetsukusari-town": "town-tetsu",
  "tetsukusari-mine": "mine",
  "sanone-town": "town-sanone",
  "sanone-camp": "camp",
  "kiri-town": "town-kiri",
  "kiri-archive": "archive",
  "shimohara-town": "town-shimo",
  "shimohara-facility": "facility",
  "fushima-town": "town-ukishima",
  "fushima-base": "ruins-ukishima",
  "toushin-town": "town-toushin",
  "toushin-hall": "hall-gikai",
  "kyotoukyu-court": "kyoto-road",
  "kyotoukyu-corridor": "kyoto-road",
  "kyotoukyu-sanctum": "unease",
  "deep-1": "kyoto-deep",
  "deep-2": "kyoto-deep",
  "deep-3": "kyoto-deep",
  "deep-4": "kyoto-deep",
  ...Object.fromEntries(GODS.map((god) => [`god-shrine-${god.no}`, "kyoto-deep"])),
  "tower-1": "ruins",
  "tower-2": "ruins",
  "tower-3": "ruins",
  "kanou-1": "unease",
  "kanou-2": "unease",
  "kanou-3": "unease",
  "kanou-4": "unease",
};
function mapBgmFor(mapId: string): Score {
  return getTrack(MAP_BGM_ID[mapId] ?? "town-touri");
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
  onStartBattle: (battleId) => startStoryBattle(battleId),
  onGiveGold: (amount) => {
    gold = addGold(gold, amount);
    if (audioStarted) {
      audio.playSe(seOf("item-get"));
    }
  },
  onOpenShop: (shopId) => {
    shopMenu = openShopMenu(shopId);
  },
  onStaffRoll: () => {
    staffRoll = startStaffRoll();
    currentBgmTrack = getTrack("staff-roll");
    audio.playBgm(currentBgmTrack);
  },
});
/** エンディングのスタッフロール。 */
let staffRoll = createStaffRollState();

/** イベントの`startBattle`コマンドが指すボス戦のデータ（章が増えるたびここに追加する）。 */
interface StoryBattleDef {
  createEnemy: () => Combatant;
  victoryFlag: string;
  bgmId: string;
}

const STORY_BATTLES: Record<string, StoryBattleDef> = {
  "chapter0-yugami": {
    createEnemy: createYugamiBoss,
    victoryFlag: "chapter0_yugami_defeated",
    bgmId: "boss-touri",
  },
  "mugikano-yugami": {
    createEnemy: createMugikanoYugami,
    victoryFlag: "chapter1_yugami_defeated",
    bgmId: "boss-mugikano",
  },
  "garasuko-yugami": {
    createEnemy: createGarasukoYugami,
    victoryFlag: "chapter2_yugami_defeated",
    bgmId: "boss-garasuko",
  },
  "tetsukusari-yugami": {
    createEnemy: createTetsukusariYugami,
    victoryFlag: "chapter3_yugami_defeated",
    bgmId: "boss-tetsu",
  },
  "sanone-yugami": {
    createEnemy: createSanoneSunaarashiYugami,
    victoryFlag: "chapter4_yugami_defeated",
    bgmId: "boss-sanone",
  },
  "kiri-yugami": {
    createEnemy: createKiriYogenYugami,
    victoryFlag: "chapter5_yugami_defeated",
    bgmId: "boss-kiri",
  },
  "shimohara-yugami": {
    createEnemy: createShimoharaShisakukiYugami,
    victoryFlag: "chapter6_yugami_defeated",
    bgmId: "boss-shimo",
  },
  "fushima-yugami": {
    createEnemy: createFushimaKanshitakuYugami,
    victoryFlag: "chapter7_yugami_defeated",
    bgmId: "boss-ukishima",
  },
  "toushin-yugami": {
    createEnemy: createToushinBanninYugami,
    victoryFlag: "chapter8_yugami_defeated",
    bgmId: "boss-toushin",
  },
  "kyotoukyu-yugami": {
    createEnemy: createKyotoukyuEdreaYugami,
    victoryFlag: "chapter9_yugami_defeated",
    bgmId: "boss-final",
  },
  "deep3-yugami": {
    createEnemy: createDeepEchoYugami,
    victoryFlag: "deep3_yugami_defeated",
    bgmId: "elite",
  },
  "deep-yugami": {
    createEnemy: createShogenYugami,
    victoryFlag: "deep_yugami_defeated",
    bgmId: "secret-boss",
  },
  // 芯環塔・環奥（roadmap 6-8〜6-11）。ラスト裏ボス「全環」は特別曲。
  ...Object.fromEntries(
    DUNGEON_ENEMIES.map((enemy) => [
      enemy.id,
      {
        createEnemy: () => createDungeonEnemy(enemy),
        victoryFlag: enemy.id === "zenkan" ? "zenkan_defeated" : `${enemy.id.replace("-guard", "")}_guard_defeated`,
        bgmId: enemy.id === "zenkan" ? "secret-boss-2" : "elite",
      },
    ]),
  ),
  // 8神（roadmap 6-4〜6-7）。
  ...Object.fromEntries(
    GODS.map((god) => [god.id, { createEnemy: () => createGodYugami(god), victoryFlag: `god${god.no}_defeated`, bgmId: "eight-gods" }]),
  ),
};

/** ランダムエンカウント（歩数のカウント）。地図を移ると数え直す。 */
let encounterState: EncounterState = createEncounterState(Math.random);
let lastStepTile: { x: number; y: number; mapId: string } | null = null;

/** 世界地図で、いま立っている地形の戦闘の背景。 */
let worldBattleBiome: Biome = "grass";

function startRandomBattle(enemies: Combatant[]): void {
  if (battle) {
    return;
  }
  setBattleBiome(currentMapId === "world-map" ? worldBattleBiome : biomeForMap(currentMapId));
  victoryExpApplied = false;
  victoryMessage = null;
  pendingVictoryFlag = null;
  const equipmentBonus = computeEquipmentBonus(heroEquipment, ALL_ITEMS_BY_ID);
  const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
  const party = buildActiveParty(effectiveStats);
  if (debugInvincible) {
    for (const member of party) {
      member.maxHp = 99999;
      member.hp = 99999;
      member.defense = 999;
    }
  }
  battle = new BattleController(
    party,
    enemies,
    createRng(Date.now()),
    { skills: buildSkillsMap(CHAPTER0_SKILL), item: CHAPTER0_ITEM, extraSkills: buildExtraSkillsMap() },
  );
  currentBgmTrack = getTrack("battle");
  if (audioStarted) {
    audio.playSe(seOf("encounter"));
  }
  audio.playBgm(currentBgmTrack);
}

function startStoryBattle(battleId: string): void {
  setBattleBiome(biomeForMap(currentMapId));
  const def = STORY_BATTLES[battleId];
  if (!def || battle) {
    return;
  }
  victoryExpApplied = false;
  victoryMessage = null;
  pendingVictoryFlag = def.victoryFlag;
  const equipmentBonus = computeEquipmentBonus(heroEquipment, ALL_ITEMS_BY_ID);
  const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
  const party = buildActiveParty(effectiveStats);
  if (debugInvincible) {
    for (const member of party) {
      member.maxHp = 99999;
      member.hp = 99999;
      member.defense = 999;
    }
  }
  battle = new BattleController(
    party,
    [def.createEnemy()],
    createRng(Date.now()),
    { skills: buildSkillsMap(CHAPTER0_SKILL), item: CHAPTER0_ITEM, extraSkills: buildExtraSkillsMap() },
  );
  currentBgmTrack = getTrack(def.bgmId);
  if (audioStarted) {
    audio.playSe(seOf("battle-start"));
  }
  audio.playBgm(currentBgmTrack);
}

if (import.meta.env.DEV) {
  // 開発用: ブラウザの自動確認（全地図の見た目・エラーの点検）から、地図を切り替えるための入口。
  (window as unknown as { __sunshine: unknown }).__sunshine = {
    mapIds: Object.keys(WORLD_MAPS),
    warp: (mapId: string, tileX: number, tileY: number) => switchMap(mapId, tileX, tileY),
    startNew: () => {
      title = { ...title, open: false };
    },
    startBattle: (battleId: string) => startStoryBattle(battleId),
    /** 開発用: いまの状態を保存データにして、すぐ読み込み直す（乗り物の保存の確認用）。保存した乗り物の情報を返す。 */
    saveLoadRoundtrip: () => {
      const saved = buildSaveData();
      applySaveData(JSON.parse(JSON.stringify(saved)) as SaveData);
      return { saved: saved.vehicles, mode: vehicle };
    },
    /** 開発用: 仲間の加入フラグを立てて、隊列（後ろをついてくる姿）を確かめる。 */
    /** 開発用: 船と飛空艇を手に入れた状態にする。 */
    giveVehicles: () => {
      flags["has_ship"] = true;
      flags["has_airship"] = true;
    },
    joinAll: () => {
      for (const { flag } of COMPANION_JOIN_FLAGS) {
        flags[flag] = true;
      }
      syncCompanionsFromFlags();
    },
    /** 開発用: 話者の顔グラフィックを会話欄で見る（絵の確認用）。 */
    startTestDialogue: (speaker: string) => dialogue.start([{ type: "message", speaker, text: "顔グラフィックの確認です。" }]),
    /** 開発用: 指定した地図のランダムエンカウントの敵と戦う（敵の絵の確認用）。 */
    startEncounter: (mapId: string) => {
      const zone = ENCOUNTER_ZONES[mapId] ?? WORLD_ENCOUNTER_ZONES[mapId];
      if (zone) {
        startRandomBattle(createEncounterEnemies(mapId, zone, Math.random));
      }
    },
  };
}

const input = new InputState();
const actionButton = new ActionButton();
attachKeyboard(input, actionButton);
createTouchControls(app, input, actionButton);
/** スマホ用: ジョブ画面を開く／閉じるボタン（キーボードの C／X と同じ動き）。 */
const jobButton = document.createElement("button");
jobButton.type = "button";
jobButton.className = "touch-job-button";
jobButton.textContent = "ジョブ";
jobButton.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  window.dispatchEvent(new KeyboardEvent("keydown", { key: jobMenu.open ? "x" : "c" }));
});
app.appendChild(jobButton);
/** スマホ用: ゲーム中のメニュー（つよさ・セーブ・タイトルへ）を開くボタン（キーボードの Tab と同じ動き）。 */
const menuButton = document.createElement("button");
menuButton.type = "button";
menuButton.className = "touch-menu-button";
menuButton.textContent = "メニュー";
menuButton.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  window.dispatchEvent(new KeyboardEvent("keydown", { key: pauseMenu.open ? "x" : "Tab" }));
});
app.appendChild(menuButton);

const audio = new AudioEngine();
let audioStarted = false;
function startAudioOnFirstInteraction(): void {
  if (audioStarted) {
    return;
  }
  audioStarted = true;
  if (title.open) {
    currentBgmTrack = getTrack("title");
    audio.playBgm(currentBgmTrack);
    return;
  }
  playMapBgm(currentMapId);
}

/** タイトル画面（起動時に開く）。自動セーブがあれば「つづきから」が選べる。 */
function hasAutosave(): boolean {
  try {
    return loadFromSlot(window.localStorage, "autosave") !== null;
  } catch {
    return false;
  }
}
let title = createTitleState(hasAutosave());

/** ゲーム中のメニュー（Tab／Escape、スマホは「メニュー」ボタン）。 */
let pauseMenu = createPauseMenuState();
let lastPauseDirection: Direction | null = null;
let pauseMessage: string | null = null;
let pauseMessageTimer = 0;
let jobMenuWasOpen = false;
window.addEventListener("keydown", () => { jobMenuWasOpen = jobMenu.open; }, true);
window.addEventListener("keydown", (event) => {
  if (pauseMenu.open) {
    if (event.key === "x" || event.key === "Escape") {
      pauseMenu = backPauseMenu(pauseMenu);
    }
    return;
  }
  if ((event.key === "Tab" || event.key === "Escape") && !jobMenuWasOpen) {
    event.preventDefault();
    if (!title.open && !battle && !dialogue.isActive() && !debugMenu.open && !jobMenu.open) {
      pauseMenu = openPauseMenu();
      pauseMessage = null;
      if (audioStarted) {
        audio.playSe(seOf("menu-open"));
      }
    }
  }
});

/** つよさ画面に出す、ユーリ＋仲間の現在の能力値（装備ボーナス込み）。 */
function statusRows(): StatusRow[] {
  const equipmentBonus = computeEquipmentBonus(heroEquipment, ALL_ITEMS_BY_ID);
  const rows: StatusRow[] = [];
  const add = (name: string, stats: LeveledStats): void => {
    rows.push({
      name, level: stats.level, hp: stats.hp, maxHp: stats.maxHp, mp: stats.mp, maxMp: stats.maxMp,
      attack: stats.attack, defense: stats.defense, speed: stats.speed, expToNext: expToNextLevel(stats.exp),
    });
  };
  add("ユーリ", applyStatBonus(heroStats, equipmentBonus));
  for (const [id, stats] of Object.entries(companionStats)) {
    add(COMPANIONS[id].name, stats);
  }
  return rows;
}
let lastTitleDirection: Direction | null = null;
window.addEventListener("keydown", (event) => {
  if ((event.key === "x" || event.key === "Escape") && title.open) {
    title = backTitle(title);
  }
});
window.addEventListener("keydown", startAudioOnFirstInteraction, { once: true });
window.addEventListener("pointerdown", startAudioOnFirstInteraction, { once: true });
window.addEventListener("keydown", (event) => {
  if (event.key === "m") {
    audio.setMuted(!audio.isMuted());
  }
});
/** 世界地図の全体図（Vキー）。世界地図にいて、会話・戦闘・メニューなどを開いていないときだけ。 */
let worldOverviewOpen = false;
window.addEventListener("keydown", (event) => {
  if (worldOverviewOpen && (event.key === "v" || event.key === "x" || event.key === "Escape" || event.key === "Enter" || event.key === " " || event.key === "z")) {
    worldOverviewOpen = false;
    event.preventDefault();
    return;
  }
  if (event.key === "v" && currentMapId === "world-map" && !title.open && !battle && !dialogue.isActive() && !pauseMenu.open && !jobMenu.open && !debugMenu.open) {
    worldOverviewOpen = true;
  }
}, true);

let lastDialogueDirection: Direction | null = null;
let lastBattleDirection: Direction | null = null;
/** 直前に効果音を鳴らした戦闘メッセージ（同じメッセージで2度鳴らさない）。 */
let battleEffect: { effect: BattleEffect; startedAt: number } | null = null;
let lastBattleMessage: string | null = null;
let battle: BattleController | null = null;
let heroStats = createInitialHeroStats();
let heroEquipment: EquipmentSlots = createInitialEquipment();
/** 仲間に加わったキャラクターのステータス（キャラクターIDをキーにする）。 */
let companionStats: Record<string, LeveledStats> = {};
let inventory: Inventory = createInventory();
/** 所持している灯貨（お金）。 */
let gold = 0;
/** お店の画面（町の武具屋で開く）。 */
let shopMenu = createShopMenuState();
let lastShopDirection: Direction | null = null;
window.addEventListener("keydown", (event) => {
  if ((event.key === "x" || event.key === "Escape") && shopMenu.open) {
    shopMenu = closeShopMenu(shopMenu);
  }
});

/** 加入フラグが立っているのに、まだパーティに反映していない仲間を反映する。 */
const COMPANION_JOIN_FLAGS: { flag: string; companionId: string }[] = [
  { flag: "chapter0_reto_joined", companionId: RETO.id },
  { flag: "chapter1_mina_joined", companionId: MINA.id },
  { flag: "chapter2_guide_joined", companionId: GUIDE.id },
  { flag: "chapter3_orca_joined", companionId: ORCA.id },
  { flag: "chapter6_ayame_joined", companionId: AYAME.id },
];

function syncCompanionsFromFlags(): void {
  for (const { flag, companionId } of COMPANION_JOIN_FLAGS) {
    if (flags[flag] && !(companionId in companionStats)) {
      // 途中加入の仲間は、ユーリのレベルより1つ下まで追いついた状態で加わる（Lv1のまま置いていかれないように）。
      companionStats[companionId] = statsAtLevel(
        COMPANIONS[companionId].createInitialStats(),
        COMPANIONS[companionId].growth,
        Math.max(1, heroStats.level - 1),
      );
    }
  }
}

/** 現在の実力（装備ボーナス込み）のユーリに、加入済みの仲間を加えた戦闘パーティ。 */
function buildActiveParty(effectiveHeroStats: LeveledStats): ReturnType<typeof createChapter0Party> {
  const unlocked = isJobSystemUnlocked(flags);
  const party = createChapter0Party(heroStats.level, withJobBonus(effectiveHeroStats, jobStates.hero, unlocked));
  for (const [id, stats] of Object.entries(companionStats)) {
    party.push(createCompanionCombatant(COMPANIONS[id], withJobBonus(stats, jobStates[id], unlocked)));
  }
  return party;
}

/** ヒーローのとくぎ＋加入済み仲間のとくぎをまとめた、戦闘用のとくぎ一覧。 */
function buildSkillsMap(heroSkill: Skill): Record<string, Skill> {
  const skills: Record<string, Skill> = { hero: heroSkill };
  for (const id of Object.keys(companionStats)) {
    skills[id] = COMPANIONS[id].skill;
  }
  return skills;
}
/** ジョブで覚えた戦闘用の特技（ユーリと加入済みの仲間）。機能が解禁前なら空。 */
function buildExtraSkillsMap(): Record<string, Skill[]> {
  const unlocked = isJobSystemUnlocked(flags);
  const result: Record<string, Skill[]> = {};
  for (const id of ["hero", ...Object.keys(companionStats)]) {
    result[id] = battleSkillsOf(jobStates[id], unlocked);
  }
  return result;
}
let victoryExpApplied = false;
let victoryMessage: string | null = null;
let saveMessage: string | null = null;
let saveMessageTimer = 0;

/** ジョブの状態（キャラクターIDごと。主人公は "hero"）。ジョブ画面・戦闘への接続は今後の作業。 */
let jobStates: Record<string, JobState> = {};

function buildSaveData(): SaveData {
  return {
    version: SAVE_VERSION,
    savedAt: new Date().toISOString(),
    player: { mapId: currentMapId, tileX: player.x / map.data.tileWidth, tileY: player.y / map.data.tileHeight, direction: player.direction },
    hero: { stats: heroStats, equipment: heroEquipment },
    companions: Object.fromEntries(
      Object.entries(companionStats).map(([id, stats]) => [id, { stats }]),
    ),
    jobs: jobStates,
    inventory,
    gold,
    flags,
    vehicles: {
      mode: vehicle,
      // 船に乗っている間は、船は自分のいる場所にある
      ship: vehicle === "ship" ? { x: Math.floor((player.x + player.width / 2) / map.data.tileWidth), y: Math.floor((player.y + player.height / 2) / map.data.tileHeight) } : { ...shipPos },
      airship: { ...airshipPos },
    },
  };
}

function applySaveData(data: SaveData): void {
  heroStats = data.hero.stats;
  heroEquipment = data.hero.equipment;
  companionStats = Object.fromEntries(
    Object.entries(data.companions).map(([id, entry]) => [id, entry.stats]),
  );
  jobStates = data.jobs;
  inventory = data.inventory;
  gold = data.gold ?? 0;
  for (const key of Object.keys(flags)) {
    delete flags[key];
  }
  Object.assign(flags, data.flags);
  resetVehicles(data.vehicles);
  switchMap(data.player.mapId, data.player.tileX, data.player.tileY);
  player = { ...player, direction: data.player.direction };
  // 船・飛空艇に乗ったまま保存したときは、乗ったまま再開する（海の上で動けなくならないように）
  if (data.vehicles && data.vehicles.mode !== "foot" && data.player.mapId === "world-map") {
    vehicle = data.vehicles.mode;
    lastOceanTile = { x: data.player.tileX, y: data.player.tileY };
    prevWorldTile = { x: data.player.tileX, y: data.player.tileY };
  }
}

/** 船・飛空艇の置き場所を、セーブの内容（無ければ初期位置）にそろえる。 */
function resetVehicles(saved?: SaveData["vehicles"]): void {
  shipPos = saved ? { ...saved.ship } : { x: WORLD_SHIP_START.x, y: WORLD_SHIP_START.y };
  airshipPos = saved ? { ...saved.airship } : { x: WORLD_AIRSHIP_START.x, y: WORLD_AIRSHIP_START.y };
  lastOceanTile = { ...shipPos };
  vehicle = "foot";
}

/** 「はじめから」: これまでの進み具合を初期状態に戻し、序章の開始地点に立つ。 */
function resetToNewGame(): void {
  heroStats = createInitialHeroStats();
  heroEquipment = createInitialEquipment();
  companionStats = {};
  jobStates = {};
  inventory = createInventory();
  gold = 0;
  for (const key of Object.keys(flags)) {
    delete flags[key];
  }
  encounterState = createEncounterState(Math.random);
  resetVehicles();
  switchMap(CHAPTER0_START.mapId, CHAPTER0_START.tileX, CHAPTER0_START.tileY);
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
      const equipmentBonus = computeEquipmentBonus(heroEquipment, ALL_ITEMS_BY_ID);
      const effectiveStats = applyStatBonus(heroStats, equipmentBonus);
      const party = buildActiveParty(effectiveStats);
      if (debugInvincible) {
        for (const member of party) {
          member.maxHp = 99999;
          member.hp = 99999;
          member.defense = 999;
        }
      }
      battle = new BattleController(
        party,
        createSampleEnemies(),
        createRng(Date.now()),
        { skills: buildSkillsMap(SAMPLE_SKILL), item: SAMPLE_ITEM, extraSkills: buildExtraSkillsMap() },
      );
      currentBgmTrack = getTrack("battle");
      audio.playSe(seOf("encounter"));
      audio.playBgm(currentBgmTrack);
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

/** ジョブ画面（Cキーで開く。アヤメが仲間に加わるまでは開けない）。 */
let jobMenu = createJobMenuState();
let lastJobDirection: Direction | null = null;
/** いま選ばれている仲間が、選べるジョブ（初期ジョブ8種＋育てて解放した上級ジョブ）。 */
function selectableJobIds(): JobId[] {
  const memberId = jobMenuMembers()[jobMenu.memberCursor]?.id;
  const state = (memberId && jobStates[memberId]) || createJobState();
  return availableJobs((id) => starsOf(state, id), flags, memberId).map((job) => job.id);
}
function jobMenuMembers(): { id: string; name: string }[] {
  return [
    { id: "hero", name: "ユーリ" },
    ...Object.keys(companionStats).map((id) => ({ id, name: COMPANIONS[id].name })),
  ];
}
window.addEventListener("keydown", (event) => {
  if (event.key === "c" && !battle && !dialogue.isActive() && !debugMenu.open && !jobMenu.open) {
    if (isJobSystemUnlocked(flags)) {
      jobMenu = openJobMenu();
    } else {
      saveMessage = "ジョブチェンジは、まだ使えない";
      saveMessageTimer = 2000;
    }
  } else if ((event.key === "x" || event.key === "Escape") && jobMenu.open) {
    jobMenu = cancelJobMenu(jobMenu);
  }
});
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
    label: () => "マップ: 硝子湖の町 へワープ",
    action: () => switchMap("garasuko-town", GARASUKO_TOWN_ENTRY.tileX, GARASUKO_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 硝子湖・密輸倉庫 へワープ",
    action: () => switchMap("garasuko-warehouse", GARASUKO_WAREHOUSE_ENTRY.tileX, GARASUKO_WAREHOUSE_ENTRY.tileY),
  },
  {
    label: () => "マップ: 鉄鏈鉱山の町 へワープ",
    action: () => switchMap("tetsukusari-town", TETSUKUSARI_TOWN_ENTRY.tileX, TETSUKUSARI_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 鉄鏈鉱山・坑内 へワープ",
    action: () => switchMap("tetsukusari-mine", TETSUKUSARI_MINE_ENTRY.tileX, TETSUKUSARI_MINE_ENTRY.tileY),
  },
  {
    label: () => "マップ: 砂音の町 へワープ",
    action: () => switchMap("sanone-town", SANONE_TOWN_ENTRY.tileX, SANONE_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 砂音・隊商の野営地 へワープ",
    action: () => switchMap("sanone-camp", SANONE_CAMP_ENTRY.tileX, SANONE_CAMP_ENTRY.tileY),
  },
  {
    label: () => "マップ: 霧断崖の町 へワープ",
    action: () => switchMap("kiri-town", KIRI_TOWN_ENTRY.tileX, KIRI_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 霧断崖・記録の間 へワープ",
    action: () => switchMap("kiri-archive", KIRI_ARCHIVE_ENTRY.tileX, KIRI_ARCHIVE_ENTRY.tileY),
  },
  {
    label: () => "マップ: 霜原の町 へワープ",
    action: () => switchMap("shimohara-town", SHIMOHARA_TOWN_ENTRY.tileX, SHIMOHARA_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 霜原・戦跡の施設 へワープ",
    action: () => switchMap("shimohara-facility", SHIMOHARA_FACILITY_ENTRY.tileX, SHIMOHARA_FACILITY_ENTRY.tileY),
  },
  {
    label: () => "マップ: 浮嶼の町 へワープ",
    action: () => switchMap("fushima-town", FUSHIMA_TOWN_ENTRY.tileX, FUSHIMA_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 浮嶼・隠れ拠点 へワープ",
    action: () => switchMap("fushima-base", FUSHIMA_BASE_ENTRY.tileX, FUSHIMA_BASE_ENTRY.tileY),
  },
  {
    label: () => "マップ: 灯芯都の町 へワープ",
    action: () => switchMap("toushin-town", TOUSHIN_TOWN_ENTRY.tileX, TOUSHIN_TOWN_ENTRY.tileY),
  },
  {
    label: () => "マップ: 灯芯都・合議会堂 へワープ",
    action: () => switchMap("toushin-hall", TOUSHIN_HALL_ENTRY.tileX, TOUSHIN_HALL_ENTRY.tileY),
  },
  {
    label: () => "マップ: 虚灯宮・外庭 へワープ",
    action: () => switchMap("kyotoukyu-court", KYOTOUKYU_COURT_ENTRY.tileX, KYOTOUKYU_COURT_ENTRY.tileY),
  },
  {
    label: () => "マップ: 虚灯宮・環の回廊 へワープ",
    action: () => switchMap("kyotoukyu-corridor", KYOTOUKYU_CORRIDOR_ENTRY.tileX, KYOTOUKYU_CORRIDOR_ENTRY.tileY),
  },
  {
    label: () => "マップ: 虚灯宮・奥の間 へワープ",
    action: () => switchMap("kyotoukyu-sanctum", KYOTOUKYU_SANCTUM_ENTRY.tileX, KYOTOUKYU_SANCTUM_ENTRY.tileY),
  },
  {
    label: () => "マップ: 虚灯宮・深部 第1階層 へワープ",
    action: () => switchMap("deep-1", DEEP_ENTRY.tileX, DEEP_ENTRY.tileY),
  },
  {
    label: () => "マップ: 8神の禁域（女神） へワープ",
    action: () => switchMap("god-shrine-1", 8, 9),
  },
  {
    label: () => "マップ: 芯環塔・根の階 へワープ",
    action: () => switchMap("tower-1", 10, 11),
  },
  {
    label: () => "マップ: 環奥・全環の間 へワープ",
    action: () => switchMap("kanou-4", 10, 11),
  },
  {
    label: () => `灯貨 +1000（現在${gold}）`,
    action: () => {
      gold = addGold(gold, 1000);
    },
  },
  {
    label: () => "お店を開く（3段目）",
    action: () => {
      shopMenu = openShopMenu("tier-3");
      debugMenu = { ...debugMenu, open: false };
    },
  },
  {
    label: () => "スタッフロールを流す",
    action: () => {
      debugMenu = { ...debugMenu, open: false };
      staffRoll = startStaffRoll();
    },
  },
  {
    label: () => "仲間5人を加える（ジョブ画面も使える）",
    action: () => {
      for (const { flag } of COMPANION_JOIN_FLAGS) {
        flags[flag] = true;
      }
      debugMenu = { ...debugMenu, open: false };
    },
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
    audio.playSe(seOf("defeat"));
    return;
  }
  if (outcome.outcome !== "won") {
    return;
  }
  audio.playSe(seOf("victory"));
  const expGained = computeVictoryExp(finishedBattle.getState());
  const result = gainExp(heroStats, expGained, SAMPLE_GROWTH);
  heroStats = result.stats;
  const levelUpNames: string[] = [];
  if (result.levelsGained > 0) {
    levelUpNames.push(`ユーリ（Lv${heroStats.level}）`);
  }
  for (const [id, stats] of Object.entries(companionStats)) {
    const companionResult = gainExp(stats, expGained, COMPANIONS[id].growth);
    companionStats[id] = companionResult.stats;
    if (companionResult.levelsGained > 0) {
      levelUpNames.push(`${COMPANIONS[id].name}（Lv${companionResult.stats.level}）`);
    }
  }
  if (isJobSystemUnlocked(flags)) {
    jobStates = awardVictoryMastery(jobStates, ["hero", ...Object.keys(companionStats)], expGained);
  }
  if (levelUpNames.length > 0) {
    window.setTimeout(() => audio.playSe(seOf("level-up")), 1800);
  }
  const goldGained = computeVictoryGold(finishedBattle.getState());
  gold = addGold(gold, goldGained);
  victoryMessage =
    levelUpNames.length > 0
      ? `${expGained}の経験値と${goldGained}灯貨を得た！ ${levelUpNames.join("、")}がレベルアップ！`
      : `${expGained}の経験値と${goldGained}灯貨を得た！`;
  if (pendingVictoryFlag) {
    flags[pendingVictoryFlag] = true;
    pendingVictoryFlag = null;
  }
  autosave();
}

const loop = createGameLoop({
  update(dtMs) {
    syncCompanionsFromFlags();

    if (saveMessageTimer > 0) {
      saveMessageTimer -= dtMs;
      if (saveMessageTimer <= 0) {
        saveMessageTimer = 0;
        saveMessage = null;
      }
    }

    const actionPressed = actionButton.consume();
    if (actionPressed) {
      audio.playSe(seOf("confirm"));
    }

    if (title.open) {
      const direction = input.getDirection();
      if (direction !== lastTitleDirection) {
        if (direction === "up") {
          title = moveTitleCursor(title, -1);
          audio.playSe(seOf("cursor"));
        } else if (direction === "down") {
          title = moveTitleCursor(title, 1);
          audio.playSe(seOf("cursor"));
        }
        lastTitleDirection = direction;
      }
      if (actionPressed) {
        const result = confirmTitle(title);
        title = result.state;
        if (result.action === "continue") {
          const data = loadFromSlot(window.localStorage, "autosave");
          if (data) {
            applySaveData(data);
          } else {
            dialogue.start(CHAPTER0_OPENING_COMMANDS);
          }
          playMapBgm(currentMapId);
        } else if (result.action === "new") {
          resetToNewGame();
          dialogue.start(CHAPTER0_OPENING_COMMANDS);
          playMapBgm(currentMapId);
        }
      }
      return;
    }
    lastTitleDirection = null;

    if (staffRoll.open) {
      staffRoll = actionPressed ? skipStaffRoll() : updateStaffRoll(staffRoll, dtMs, LOGICAL_HEIGHT);
      if (!staffRoll.open) {
        playMapBgm(currentMapId);
      }
      return;
    }

    if (pauseMessageTimer > 0) {
      pauseMessageTimer -= dtMs;
      if (pauseMessageTimer <= 0) {
        pauseMessage = null;
      }
    }
    if (pauseMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastPauseDirection) {
        if (direction === "up") {
          pauseMenu = movePauseCursor(pauseMenu, -1);
          audio.playSe(seOf("cursor"));
        } else if (direction === "down") {
          pauseMenu = movePauseCursor(pauseMenu, 1);
          audio.playSe(seOf("cursor"));
        }
        lastPauseDirection = direction;
      }
      if (actionPressed) {
        const result = confirmPauseMenu(pauseMenu);
        pauseMenu = result.state;
        if (result.action === "save") {
          autosave();
          audio.playSe(seOf("save"));
          pauseMessage = "セーブしました";
          pauseMessageTimer = 2000;
        } else if (result.action === "title") {
          autosave();
          title = createTitleState(hasAutosave());
          currentBgmTrack = getTrack("title");
          audio.playBgm(currentBgmTrack);
        }
      }
      return;
    }
    lastPauseDirection = null;

    if (shopMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastShopDirection) {
        if (direction === "up") {
          shopMenu = moveShopCursor(shopMenu, -1);
          audio.playSe(seOf("cursor"));
        } else if (direction === "down") {
          shopMenu = moveShopCursor(shopMenu, 1);
          audio.playSe(seOf("cursor"));
        }
        lastShopDirection = direction;
      }
      if (actionPressed) {
        const item = shopMenu.items[shopMenu.cursor];
        if (item) {
          const result = buyItem(item.id, gold, heroEquipment);
          if (result.ok) {
            gold = result.gold;
            heroEquipment = result.equipment;
            autosave();
            audio.playSe(seOf("buy"));
          } else {
            audio.playSe(seOf("error"));
          }
          shopMenu = withShopMessage(shopMenu, result.message);
        }
      }
      return;
    }
    lastShopDirection = null;

    if (debugMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastDebugDirection) {
        if (direction === "up") {
          debugMenu = moveMenuCursor(debugMenu, -1, DEBUG_MENU_ROWS.length);
          audio.playSe(seOf("cursor"));
        } else if (direction === "down") {
          debugMenu = moveMenuCursor(debugMenu, 1, DEBUG_MENU_ROWS.length);
          audio.playSe(seOf("cursor"));
        }
        lastDebugDirection = direction;
      }
      if (actionPressed) {
        DEBUG_MENU_ROWS[debugMenu.cursor]?.action();
      }
      return;
    }
    lastDebugDirection = null;

    if (jobMenu.open) {
      const members = jobMenuMembers();
      const direction = input.getDirection();
      if (direction !== lastJobDirection) {
        if (direction === "up") {
          jobMenu = moveJobMenu(jobMenu, -1, members.length, selectableJobIds().length);
          audio.playSe(seOf("cursor"));
        } else if (direction === "down") {
          jobMenu = moveJobMenu(jobMenu, 1, members.length, selectableJobIds().length);
          audio.playSe(seOf("cursor"));
        }
        lastJobDirection = direction;
      }
      if (actionPressed) {
        const memberId = members[jobMenu.memberCursor]?.id;
        const result = confirmJobMenu(jobMenu, selectableJobIds());
        jobMenu = result.state;
        if (result.chosen && memberId) {
          jobStates = changeJob(jobStates, memberId, result.chosen);
          autosave();
        }
      }
      return;
    }
    lastJobDirection = null;

    if (battle) {
      const uiState = battle.getUiState();
      // 戦闘のメッセージが出るたびに、その内容に合った効果音を1回鳴らす（斬撃・ダメージ・回復・倒したなど）。
      if (uiState.kind === "message") {
        if (uiState.text !== lastBattleMessage) {
          lastBattleMessage = uiState.text;
          const effect = battleEffectFor(uiState.text, battle.getState().party.map((c) => c.name));
          battleEffect = effect ? { effect, startedAt: performance.now() } : null;
          const se = battleSeFor(uiState.text, battle.getState().party.map((c) => c.name));
          if (se && audioStarted) {
            audio.playSe(seOf(se));
          }
        }
      } else {
        lastBattleMessage = null;
      }
      if (uiState.kind === "finished") {
        applyVictoryExpIfNeeded(battle);
      }
      if (uiState.kind === "command" || uiState.kind === "skillList" || uiState.kind === "target") {
        const direction = input.getDirection();
        if (direction !== lastBattleDirection) {
          if (direction === "up" || direction === "left") {
            battle.moveCursor(-1);
            audio.playSe(seOf("cursor"));
          } else if (direction === "down" || direction === "right") {
            battle.moveCursor(1);
            audio.playSe(seOf("cursor"));
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
          lastBattleMessage = null;
        }
      }
      return;
    }
    lastBattleDirection = null;

    if (dialogue.isActive()) {
      dialogue.update(dtMs);
      updateWander(npcs, map, { x: -1, y: -1 }, dtMs, true, Math.random);
      const state = dialogue.getRenderState();
      if (state?.kind === "choice") {
        const direction = input.getDirection();
        if (direction !== lastDialogueDirection) {
          if (direction === "up") {
            dialogue.moveChoice(-1);
            audio.playSe(seOf("cursor"));
          } else if (direction === "down") {
            dialogue.moveChoice(1);
            audio.playSe(seOf("cursor"));
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

    if (worldOverviewOpen) {
      return;
    }
    const onWorld = currentMapId === "world-map";
    if (onWorld) {
      syncWorldState();
    }
    const moveMap = onWorld && vehicle === "ship" ? getVehicleMaps().ship : onWorld && vehicle === "air" ? getVehicleMaps().air : map;
    player = updatePlayer(player, input.getDirection(), dtMs * (onWorld ? VEHICLE_SPEED[vehicle] : 1), moveMap);
    let actionUsed = false;
    if (onWorld) {
      actionUsed = updateVehicleAfterMove(
        { x: Math.floor((player.x + player.width / 2) / map.data.tileWidth), y: Math.floor((player.y + player.height / 2) / map.data.tileHeight) },
        actionPressed,
      );
      if (vehicleHint) {
        vehicleHint.ms -= dtMs;
        if (vehicleHint.ms <= 0) vehicleHint = null;
      }
    }
    partyTrail.update(player, dtMs, followerSpecs().length);
    updateWander(
      npcs,
      map,
      { x: Math.floor((player.x + player.width / 2) / map.data.tileWidth), y: Math.floor((player.y + player.height / 2) / map.data.tileHeight) },
      dtMs,
      false,
      Math.random,
    );
    renderCamera = centerCameraOn(
      camera,
      player.x + player.width / 2,
      player.y + player.height / 2,
      map.widthPx,
      map.heightPx,
    );

    const centerTileX = Math.floor((player.x + player.width / 2) / map.data.tileWidth);
    const centerTileY = Math.floor((player.y + player.height / 2) / map.data.tileHeight);
    const exit = vehicle === "foot" ? findExitAt(map, centerTileX, centerTileY) : undefined;
    if (exit) {
      // 世界地図から入る場所には、条件がある（章の順・乗り物・クリア後の航路など）。足りなければ、ヒントを出して押し戻す。
      const problems = currentMapId === "world-map" ? worldEntryProblems(exit.targetMapId, flags) : [];
      if (problems.length > 0) {
        player = { ...player, y: player.y + map.data.tileHeight, moving: false };
        dialogue.start(problems.map((text) => ({ type: "message" as const, text })));
        return;
      }
      if (exit.targetMapId === "tower-1") {
        flags["tower_gate_open"] = true;
      }
      switchMap(exit.targetMapId, exit.targetTileX, exit.targetTileY);
      autosave();
      return;
    }

    // 歩くたびに、ランダムエンカウントの歩数を進める（タイルが変わったときだけ数える）。
    if (!lastStepTile || lastStepTile.mapId !== currentMapId) {
      lastStepTile = { x: centerTileX, y: centerTileY, mapId: currentMapId };
    } else if (lastStepTile.x !== centerTileX || lastStepTile.y !== centerTileY) {
      lastStepTile = { x: centerTileX, y: centerTileY, mapId: currentMapId };
      if (!debugNoEncounter) {
        // 世界地図では、足もとの地形で出会う敵と戦闘の背景を決める（道の上では出会わない）。
        let encounterMapId: string | null = currentMapId;
        if (currentMapId === "world-map") {
          const tileId = map.data.layers[0].data[centerTileY * map.data.width + centerTileX];
          if (vehicle === "ship") {
            encounterMapId = "world-sea";
            worldBattleBiome = "coast";
          } else if (vehicle === "air") {
            encounterMapId = "world-air";
            worldBattleBiome = "sky";
          } else {
            encounterMapId = worldZoneIdAt(tileId, centerTileX, centerTileY);
            worldBattleBiome = tileId === 18 ? "lava" : tileId === 5 ? "desert" : tileId === 6 || tileId === 12 ? "snow" : "grass";
          }
        }
        const stepped = encounterMapId ? stepEncounter(encounterState, encounterMapId, Math.random) : { state: encounterState, enemies: null };
        encounterState = stepped.state;
        if (stepped.enemies) {
          startRandomBattle(stepped.enemies);
          return;
        }
      }
    }

    if (actionPressed && !actionUsed && vehicle === "foot") {
      const facing = getFacingTile(player, map.data.tileWidth, map.data.tileHeight);
      const npc = findNpcAt(npcs, facing.tileX, facing.tileY);
      if (npc) {
        faceNpc(npc, opposite(player.direction));
        dialogue.start(npc.commands);
      }
    }
  },
  render() {
    ctx.fillStyle = "#101018";
    ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);

    if (title.open) {
      renderTitle(ctx, title, GAME_TITLE, LOGICAL_WIDTH, LOGICAL_HEIGHT);
      return;
    }
    if (staffRoll.open) {
      renderStaffRoll(ctx, staffRoll, LOGICAL_WIDTH, LOGICAL_HEIGHT);
      return;
    }

    if (battle) {
      renderBattle(
        ctx,
        battle.getState(),
        battle.getUiState(),
        LOGICAL_WIDTH,
        LOGICAL_HEIGHT,
        battleEffect ? { effect: battleEffect.effect, elapsedMs: performance.now() - battleEffect.startedAt } : null,
      );
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

    setLitBeacons(new Set([1, 2, 3, 4, 5, 6, 7, 8].filter((n) => flags[`beacon${n}_lit`])));
    if (worldOverviewOpen) {
      renderWorldOverview(
        ctx,
        map,
        { x: Math.floor((player.x + player.width / 2) / map.data.tileWidth), y: Math.floor((player.y + player.height / 2) / map.data.tileHeight) },
        new Set([1, 2, 3, 4, 5, 6, 7, 8].filter((n) => flags[`beacon${n}_lit`])),
        LOGICAL_WIDTH,
        LOGICAL_HEIGHT,
        performance.now(),
      );
      return;
    }
    renderTileMap(ctx, map, renderCamera);
    // 奥にいる人を先に、手前にいる人をあとに描く（足元の位置の順）。
    const playerFeetY = player.y + player.height;
    renderProps(ctx, map.data, renderCamera, (prop) => propFeetY(prop, map.data.tileHeight) <= playerFeetY);
    renderNpcs(ctx, npcs, map, renderCamera, (npc) => npcFeetY(npc, map.data.tileHeight) <= playerFeetY);
    const followers = followerSpecs();
    const onWorldMap = currentMapId === "world-map";
    const riding = onWorldMap && vehicle !== "foot";
    const nowMs = performance.now();
    if (onWorldMap) {
      renderVortex(ctx, map, renderCamera, nowMs);
      // 停泊中の船・着陸中の飛空艇
      const ts = map.data.tileWidth;
      if (flags["has_ship"] && vehicle !== "ship") {
        drawShip(ctx, shipPos.x * ts + ts / 2 - renderCamera.x, shipPos.y * ts + ts - renderCamera.y, "right", true);
      }
      if (flags["has_airship"] && vehicle !== "air") {
        drawAirship(ctx, airshipPos.x * ts + ts / 2 - renderCamera.x, airshipPos.y * ts + ts - renderCamera.y, "down", nowMs, false);
      }
    }
    if (!riding) {
      renderFollowers(ctx, partyTrail, followers, renderCamera, (feetY) => feetY <= playerFeetY, onWorldMap ? 0.6 : 1);
      renderPlayer(ctx, player, renderCamera, onWorldMap ? 0.6 : 1);
      renderFollowers(ctx, partyTrail, followers, renderCamera, (feetY) => feetY > playerFeetY, onWorldMap ? 0.6 : 1);
    } else {
      const fx = player.x + player.width / 2 - renderCamera.x;
      const fy = player.y + player.height - renderCamera.y;
      if (vehicle === "ship") {
        drawShip(ctx, fx, fy, player.direction);
      } else {
        drawAirship(ctx, fx, fy, player.direction, nowMs, true);
      }
    }
    renderNpcs(ctx, npcs, map, renderCamera, (npc) => npcFeetY(npc, map.data.tileHeight) > playerFeetY);
    renderProps(ctx, map.data, renderCamera, (prop) => propFeetY(prop, map.data.tileHeight) > playerFeetY);
    if (onWorldMap) {
      if (!flags["vortex_route_open"]) {
        renderStorm(ctx, map, renderCamera, nowMs);
      }
      if (vehicleHint) {
        ctx.font = "9px monospace";
        ctx.textBaseline = "top";
        ctx.textAlign = "left";
        const w = Math.min(LOGICAL_WIDTH - 8, vehicleHint.text.length * 9 + 10);
        ctx.fillStyle = "rgba(10,14,34,0.8)";
        ctx.fillRect(4, LOGICAL_HEIGHT - 22, w, 14);
        ctx.fillStyle = "#f2c14e";
        ctx.fillText(vehicleHint.text, 8, LOGICAL_HEIGHT - 19);
      } else if (vehicle === "air") {
        ctx.font = "9px monospace";
        ctx.textBaseline = "top";
        ctx.textAlign = "left";
        ctx.fillStyle = "rgba(10,14,34,0.6)";
        ctx.fillRect(4, LOGICAL_HEIGHT - 20, 120, 12);
        ctx.fillStyle = "#dfe8f4";
        ctx.fillText("決定ボタンで着陸", 8, LOGICAL_HEIGHT - 18);
      }
    }

    const dialogueState = dialogue.getRenderState();
    if (dialogueState) {
      renderDialogue(ctx, dialogueState, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }

    ctx.fillStyle = "#f0f0f0";
    ctx.font = "10px monospace";
    ctx.textBaseline = "top";
    ctx.fillText(GAME_TITLE, 4, 2);
    ctx.textAlign = "right";
    ctx.fillText(`灯貨 ${gold}`, LOGICAL_WIDTH - 4, 2);
    ctx.textAlign = "left";

    if (saveMessage) {
      ctx.fillStyle = "#f2c14e";
      ctx.fillText(saveMessage, 4, 14);
    }
    renderJobMenu(ctx, jobMenu, jobMenuMembers(), jobStates, selectableJobIds(), LOGICAL_WIDTH, LOGICAL_HEIGHT);
    renderShop(ctx, shopMenu, gold, heroEquipment, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    renderPauseMenu(ctx, pauseMenu, pauseMenu.screen === "status" ? statusRows() : [], pauseMessage, gold, LOGICAL_WIDTH, LOGICAL_HEIGHT);

    if (import.meta.env.DEV) {
      ctx.fillStyle = "#88ff88";
      ctx.fillText(`FPS: ${loop.getFps()}`, 4, LOGICAL_HEIGHT - 12);
      renderDebugMenu(ctx, debugMenu, DEBUG_MENU_ROWS, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }
  },
});


function frame(nowMs: number): void {
  loop.tick(nowMs);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
