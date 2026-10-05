import { WORLD_TOWNS } from "./game/map/world/world-map.generated";
import "./style.css";
import { GAME_TITLE } from "./core/status";
import { backTitle, confirmTitle, createTitleState, moveTitleCursor } from "./game/title/title-menu";
import { renderTitle } from "./render/title-renderer";
import { renderOpening } from "./render/opening-renderer";
import { drawWindow } from "./render/ui-frame";
import { renderItemsScreen, type ItemsView } from "./render/pause-menu-renderer";
import { objectKindOf, setOpenedChests } from "./render/object-markers";
import { npcLook } from "./game/sprite/character-specs";
import { advanceBootOpening, startBootOpening, updateBootOpening } from "./game/title/boot-opening";
import { renderBootOpening } from "./render/boot-opening-renderer";
import { getPixelLogo } from "./render/logo-pixel";
import { DUNGEON_PARENT } from "./game/world/dungeon-parent";
import { DUNGEON_PREP_FLAGS } from "./game/world/dungeon-extensions";
import { advanceBattleTransition, canSkipTransition, isCoverPhase, skipToReveal, startBattleTransition, type BattleTransition } from "./game/battle/battle-transition";
import { renderTransitionCover, renderTransitionReveal } from "./render/battle-transition-renderer";
import { advanceOpening, createOpeningState, skipOpening, startOpening, updateOpening } from "./game/title/opening";
import { battleSeFor, swingSeFor } from "./game/battle/battle-se";
import { battleEffectFor, type BattleEffect } from "./game/battle/battle-effect";
import { battleAnimFor, type BattleAnimSpec } from "./game/battle/battle-anim";
import { createStaffRollState, skipStaffRoll, startStaffRoll, updateStaffRoll } from "./game/title/staff-roll";
import { renderStaffRoll } from "./render/staff-roll-renderer";
import { addGold, computeVictoryGold, spendGold } from "./game/economy/gold";
import { ALL_ITEMS_BY_ID, describeBonus, purchaseConsumable, purchaseItem, receiveTreasure } from "./game/economy/shop";
import { closeShopMenu, createShopMenuState, moveShopCursor, openShopMenu, withShopMessage } from "./game/economy/shop-menu";
import { renderShop, renderShopWear, type ShopWearView } from "./render/shop-renderer";
import { backPauseMenu, confirmPauseMenu, createPauseMenuState, movePauseCursor, openPauseMenu } from "./game/menu/pause-menu";
import { renderPauseMenu, type StatusRow } from "./render/pause-menu-renderer";
import { backEquipMenu, confirmEquipMenu, createEquipMenuState, moveEquipCursor, openEquipMenu } from "./game/menu/equip-menu";
import { renderEquipMenu, type EquipMenuView, type EquipStatsView } from "./render/equip-menu-renderer";
import { candidatesFor, ensureOwned, equipTo, sanitizeParty, unequipFrom, type PartyEquipment } from "./game/items/party-equipment";
import type { EquipmentItemData, ItemData } from "./game/items/types";
import { canEquip, WEAPON_LABEL, WEAPON_TYPE_OF, weaponTypeOf, wielderOf } from "./game/items/weapon-types";
import { expToNextLevel } from "./game/growth/exp-curve";
import { createGameLoop } from "./core/game-loop";
import { createGameCanvas, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./render/canvas";
import { createCamera, centerCameraOn } from "./render/camera";
import { renderTileMap } from "./render/tile-map-renderer";
import { renderPlayer } from "./render/player-renderer";
import { renderNpcs, visibleNpcFeetY } from "./render/npc-renderer";
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
import { attachKeyRemap, loadBindings, rebind, resetBindings, saveBindings, describeBinding, CONTROL_ACTIONS, sendGameKey, type KeyBindings } from "./input/key-bindings";
import { createGamepadPoller } from "./input/gamepad";
import { cycleMoveSpeed, DEFAULT_MOVE_SPEED, loadMoveSpeed, MOVE_SPEEDS, saveMoveSpeed } from "./game/move-speed";
import { DIFFICULTY_ROW, SPEED_ROW, closeControlsMenu, confirmControlsMenu, createControlsMenuState, finishCapture, moveControlsCursor, openControlsMenu } from "./game/menu/controls-menu";
import { renderControlsMenu } from "./render/controls-menu-renderer";
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
import { dayFraction, isNight, isOutdoorMap, nextMorning, nightness, periodLabel, staysOutAtNight, warmGlow } from "./game/time-of-day";
import { backFieldUse, confirmFieldUse, createFieldUseState, moveFieldUse, openFieldUse, refreshFieldUse, type FieldUseApply, type FieldUseOption } from "./game/menu/field-use";
import { renderFieldUse } from "./render/field-use-renderer";
import { cycleDifficulty, loadDifficulty, saveDifficulty, type Difficulty } from "./game/difficulty";
import { applyVital, growVital, healVital, vitalsAfterBattle, type Vitals } from "./game/vitals";
import { awardVictoryMastery, changeJob, isJobSystemUnlocked, battleSkillsOf, withJobBonus } from "./game/job/party-job";
import { renderBattle, setBattleBiome, warmBattleBackdrops } from "./render/battle-renderer";
import { biomeForMap, ALL_BIOMES, type Biome } from "./render/battle-backdrop";
import {
  createInitialEquipment,
  createInitialHeroStats,
  createSampleEnemies,
  SAMPLE_GROWTH,
  SAMPLE_ITEM,
  SAMPLE_SKILL,
} from "./game/battle/sample-battle";
import { CHAPTER0_SKILL, createChapter0Party, createYugamiBoss } from "./game/battle/chapter0-enemies";
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
import { addItem, createInventory, getQuantity, removeItem, type Inventory } from "./game/items/inventory";
import { CONSUMABLES_BY_ID, CONSUMABLE_ITEMS, STARTER_CONSUMABLES } from "./game/items/consumables";
import { toBattleItem } from "./game/items/types";
import type { ItemStack } from "./game/battle/battle-controller";
import type { JobId, JobState } from "./game/job/types";
import { availableJobs } from "./game/job/jobs";
import { createJobState, starsOf } from "./game/job/mastery";
import { SAVE_VERSION, type SaveData } from "./game/save/types";
import { loadFromSlot, saveToSlot } from "./game/save/storage";
import { latestSaveSlot, summarizeSlots } from "./game/save/slots";
import { closeSlotMenu, confirmSlot, createSlotMenuState, moveSlotCursor, openSlotMenu, withSlotRows } from "./game/menu/slot-menu";
import { renderSlotMenu } from "./render/slot-menu-renderer";
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
// 戦闘の背景の絵を、遊びはじめて少したってから先に作っておく
setTimeout(() => warmBattleBackdrops(ALL_BIOMES, LOGICAL_WIDTH, LOGICAL_HEIGHT), 1500);

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

/** 場所を移った直後は、出口に触れても戻らない。キーをはなして、出口のマスからはずれるまで（下を押しっぱなしで、すぐ元の町に戻るのを防ぐ）。 */
let exitReleased = false;
let exitArmed = false;

function switchMap(mapId: string, tileX: number, tileY: number): void {
  exitReleased = false;
  exitArmed = false;
  const data = WORLD_MAPS[mapId];
  if (!data) {
    return;
  }
  currentMapId = mapId;
  map = createTileMap(data);
  npcs = withoutJoinedCompanions(WORLD_NPCS[mapId] ?? []);
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
  "touri-forest-1": "field",
  "touri-forest-2": "outskirts",
  "touri-outskirts": "outskirts",
  "world-map": "field",
  "mugikano-village": "town-mugikano",
  "mugikano-canal": "field",
  "mugikano-tunnel": "mine",
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
  return getTrack(MAP_BGM_ID[DUNGEON_PARENT[mapId] ?? mapId] ?? MAP_BGM_ID[mapId] ?? "town-touri");
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

/** 世界地図を歩く主人公たちの大きさ（1で町と同じ。以前は0.6で小さすぎた。2026-10-05、人間の指摘）。 */
const WORLD_MAP_CHARACTER_SCALE = 1;

/** 戦闘に入る演出（ふつうは短く、ボスは長い特別な登場）。演出の間は、戦闘の操作を受けつけない。 */
let battleTransition: BattleTransition | null = null;

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
  onGiveEquipment: (itemId) => {
    // 宝の装備は、まず持ち物に入る。ユーリがいまの装備より強ければ、その場でつける（そうでなくても、そうび画面で仲間に渡せる）
    inventory = ensureOwned(inventory, [itemId]);
    const result = receiveTreasure(itemId, heroEquipment);
    heroEquipment = result.equipment;
    // 専用武器は、持てる仲間（もう仲間になっていれば）の、いまの武器より強いときにつける
    const found = ALL_ITEMS_BY_ID[itemId];
    const type = found ? weaponTypeOf(found) : undefined;
    const owner = type && type !== "sword" ? wielderOf(type) : undefined;
    if (found && found.category === "weapon" && owner && owner !== "hero" && owner in companionStats) {
      const cur = companionEquipment[owner]?.weapon ? ALL_ITEMS_BY_ID[companionEquipment[owner].weapon!] : undefined;
      const sum = (it: ItemData | undefined): number => (it && it.category !== "consumable" ? Object.values(it.statBonus).reduce((a, v) => a + (v ?? 0), 0) : 0);
      if (sum(found) > sum(cur)) {
        setPartyEquipment(equipTo(partyEquipment(), owner, found, inventory));
      }
    }
    if (audioStarted) {
      audio.playSe(seOf("item-get"));
    }
  },
  onOpenShop: (shopId) => {
    shopMenu = openShopMenu(shopId);
  },
  onInnStay: (price) => {
    const paid = spendGold(gold, price);
    if (paid === null) return false;
    gold = paid;
    vitals = {};           // 宿屋では、HP・MPが全快する
    clockMs = nextMorning(clockMs);   // 朝になる
    if (audioStarted) audio.playSe(seOf("level-up"));
    autosave();
    return true;
  },
  onStaffRoll: () => {
    staffRoll = startStaffRoll();
    currentBgmTrack = getTrack("staff-roll");
    audio.playBgm(currentBgmTrack);
  },
});
/** エンディングのスタッフロール。 */
let staffRoll = createStaffRollState();
/** 「はじめから」のあとに流れるオープニング（あらすじのムービー）。終わると（飛ばすと）ゲームが始まる。 */
let opening = createOpeningState();

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

/**
 * 戦闘を始めるときに、いまいる場所の背景に切りかえる。人間の指摘「バトル画面の背景も一瞬違うやつが写る」（2026-10-05）:
 * 戦闘の決まり方によっては、前の戦闘の背景が残ったまま描かれることがあったので、戦闘を始める所すべてで、
 * 戦闘を作る直前にここを呼ぶ（もう戦闘中なら変えない）。前の戦闘の光や揺れの演出も消す。
 */
function prepareBattleScreen(): void {
  setBattleBiome(currentMapId === "world-map" ? worldBattleBiome : biomeForMap(currentMapId));
  battleEffect = null;
  battleAnim = null;
  lastBattleMessage = null;
}

function startRandomBattle(enemies: Combatant[]): void {
  if (battle) {
    return;
  }
  prepareBattleScreen();
  victoryExpApplied = false;
  victoryMessage = null;
  victoryLevelUps = [];
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
    { skills: buildSkillsMap(CHAPTER0_SKILL), items: battleItemStacks(), extraSkills: buildExtraSkillsMap() },
  );
  currentBgmTrack = getTrack("battle");
  battleTransition = startBattleTransition(false);
  if (audioStarted) {
    audio.playSe(seOf("encounter"));
  }
  audio.playBgm(currentBgmTrack);
}

function startStoryBattle(battleId: string): void {
  const def = STORY_BATTLES[battleId];
  if (!def || battle) {
    return;   // 戦闘中に呼ばれても、いまの戦闘の背景は変えない
  }
  prepareBattleScreen();
  victoryExpApplied = false;
  victoryMessage = null;
  victoryLevelUps = [];
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
    { skills: buildSkillsMap(CHAPTER0_SKILL), items: battleItemStacks(), extraSkills: buildExtraSkillsMap() },
  );
  currentBgmTrack = getTrack(def.bgmId);
  // ボス・強敵の戦闘は、特別な登場の演出（黒い帯・名前・白いひらめき）をはさむ
  battleTransition = startBattleTransition(true, battle.getState().enemies[0]?.name ?? "");
  if (audioStarted) {
    audio.playSe(seOf("battle-start"));
  }
  audio.playBgm(currentBgmTrack);
}

if (import.meta.env.DEV) {
  // 開発用: ブラウザの自動確認（全地図の見た目・エラーの点検）から、地図を切り替えるための入口。
  (window as unknown as { __sunshine: unknown }).__sunshine = {
    mapIds: Object.keys(WORLD_MAPS),
    setClock: (ms: number) => { clockMs = ms; },
    warp: (mapId: string, tileX: number, tileY: number) => switchMap(mapId, tileX, tileY),
    startNew: () => {
      bootOpening = { ...bootOpening, open: false };
      title = { ...title, open: false };
    },
    startBattle: (battleId: string) => startStoryBattle(battleId),
    /** 開発用: いまの状態を保存データにして、すぐ読み込み直す（乗り物の保存の確認用）。保存した乗り物の情報を返す。 */
    saveLoadRoundtrip: () => {
      const saved = buildSaveData();
      applySaveData(JSON.parse(JSON.stringify(saved)) as SaveData);
      return { saved: saved.vehicles, mode: vehicle };
    },
    /** 開発用: 世界地図の全体を、実際のタイルの絵・飾りで1枚に描いて、PNGのデータURLで返す（確認用）。 */
    renderWorldFull: () => {
      const full = createTileMap(WORLD_MAPS["world-map"]);
      const canvas = document.createElement("canvas");
      canvas.width = full.widthPx;
      canvas.height = full.heightPx;
      const c = canvas.getContext("2d")!;
      const cam = { x: 0, y: 0, viewportWidth: canvas.width, viewportHeight: canvas.height };
      renderTileMap(c, full, cam);
      renderProps(c, full.data, cam, () => true);
      return canvas.toDataURL("image/png");
    },
    /** 開発用: 地図ぜんたいを1枚に描く（形の確認用）。 */
    renderMapFull: (mapId: string) => {
      const full = createTileMap(WORLD_MAPS[mapId]);
      const canvas = document.createElement("canvas");
      canvas.width = full.widthPx;
      canvas.height = full.heightPx;
      const c = canvas.getContext("2d")!;
      const cam = { x: 0, y: 0, viewportWidth: canvas.width, viewportHeight: canvas.height };
      renderTileMap(c, full, cam);
      renderProps(c, full.data, cam, () => true);
      const list = WORLD_NPCS[mapId] ?? [];
      c.fillStyle = "#ff40ff";
      for (const n of list) c.fillRect(n.tileX * 16 + 4, n.tileY * 16 + 4, 8, 8);
      return canvas.toDataURL("image/png");
    },
    /** 開発用: タイトルロゴの絵（確認用）。 */
    logoDataUrl: () => getPixelLogo(GAME_TITLE)?.toDataURL() ?? "",
    /** 開発用: 灯貨をふやす・店を開く（買い物の確認用）。 */
    giveGold: (amount: number) => {
      gold += amount;
    },
    openShop: (shopId: string) => {
      shopMenu = openShopMenu(shopId);
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
/** 操作キーの設定（パソコン）。初期設定のときは、これまでのキーのまま。ほかのキー処理より先に動くよう、ここで最初に登録する。 */
let keyBindings: KeyBindings = loadBindings(typeof window !== "undefined" ? window.localStorage : undefined);
const keyRemap = attachKeyRemap(() => keyBindings);
attachKeyboard(input, actionButton);
/** 外部のコントローラー（ゲームパッド）。毎フレーム、状態を読む。 */
const gamepad = createGamepadPoller(input, (action, down) => {
  if (action === "confirm") {
    if (down) actionButton.press();
  } else {
    sendGameKey(down ? "keydown" : "keyup", action);
  }
});
createTouchControls(app, input, actionButton);
/** スマホ用: ジョブ画面を開く／閉じるボタン（キーボードの C／X と同じ動き）。 */
const jobButton = document.createElement("button");
jobButton.type = "button";
jobButton.className = "touch-job-button";
jobButton.textContent = "ジョブ";
jobButton.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  sendGameKey("keydown", jobMenu.open ? "back" : "job");
});
app.appendChild(jobButton);
/** スマホ用: ゲーム中のメニュー（つよさ・セーブ・タイトルへ）を開くボタン（キーボードの Tab と同じ動き）。 */
const menuButton = document.createElement("button");
menuButton.type = "button";
menuButton.className = "touch-menu-button";
menuButton.textContent = "メニュー";
menuButton.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  sendGameKey("keydown", pauseMenu.open ? "back" : "menu");
});
app.appendChild(menuButton);

/** スマホ用: もどるボタン（キーボードの x・Esc と同じ。十字キーとは別）。メニュー・ジョブ・買い物・戦闘の選び直しなどを、ひとつ戻る。 */
const backButton = document.createElement("button");
backButton.type = "button";
backButton.className = "touch-back-button";
backButton.textContent = "もどる";
backButton.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  sendGameKey("keydown", "back");
});
app.appendChild(backButton);

const audio = new AudioEngine();
let audioStarted = false;
function startAudioOnFirstInteraction(): void {
  if (audioStarted) {
    return;
  }
  audioStarted = true;
  if (bootOpening.open) {
    // 起動のオープニング: オーケストラの曲。最初の操作が遅れたときは、場面の進みにそろえて、途中から鳴らす
    currentBgmTrack = getTrack("boot-opening");
    const at = bootClockMs / 1000;
    audio.playBgm(currentBgmTrack, at < 34 ? at : 0);
    return;
  }
  if (title.open) {
    currentBgmTrack = getTrack("title");
    audio.playBgm(currentBgmTrack);
    return;
  }
  playMapBgm(currentMapId);
}

/** タイトル画面（起動時に開く）。自動セーブがあれば「つづきから」が選べる。 */
/** セーブ・ロードの場所えらび。 */
let slotMenu = createSlotMenuState();
let lastSlotDirection: Direction | null = null;

/** どこかにセーブがあるか（自動セーブも含む）。 */
function hasAnySave(): boolean {
  try {
    return latestSaveSlot(window.localStorage) !== null;
  } catch {
    return false;
  }
}

function hasAutosave(): boolean {
  return hasAnySave();
}
let title = createTitleState(hasAutosave());
/** ゲームを起動したときのオープニング（ロゴが上から落ちてきて、あらすじが流れる）。終わるとタイトル画面。 */
let bootOpening = startBootOpening();
/** 起動のオープニングが始まってからの時間（ms）。音が遅れて始まるとき、曲の位置をそろえるのに使う。 */
let bootClockMs = 0;

/** ゲーム中のメニュー（Tab／Escape、スマホは「メニュー」ボタン）。 */
let pauseMenu = createPauseMenuState();
/** 「もちもの」画面の、スクロール位置（行）。 */
let itemsScroll = 0;

/** 「もちもの」に出す、だいじなもの（フラグから決める）と、持っている装備。 */
function itemsView(): ItemsView {
  const KEY_ITEMS: { flag: string | null; name: string; note: string }[] = [
    { flag: null, name: "祖父の腕輪", note: "灯り石の腕輪。ほんのり温かい。" },
    { flag: "chapter0_got_lamp", name: "古いランタン", note: "暗い道を照らす灯り。" },
    { flag: "chapter0_kasen_farewell", name: "通行手形と通信石", note: "カセンから預かった。支部との連絡に使う。" },
    { flag: "chapter1_got_key", name: "水車小屋の鍵", note: "水源の扉をあける鍵。" },
    { flag: "chapter2_core_shard_taken", name: "環の文様のかけら", note: "倉庫で見つけた石のかけら。" },
    { flag: "chapter4_sailcar_obtained", name: "帆走車", note: "砂の海を走る乗り物。" },
    { flag: "has_ship", name: "船", note: "海を渡る乗り物。" },
    { flag: "has_airship", name: "空の乗り物", note: "空を飛ぶ乗り物。" },
  ];
  const party = partyEquipment();
  const nameOf = (id: string): string => (id === "hero" ? "ユーリ" : COMPANIONS[id]?.name ?? id);
  return {
    keyItems: KEY_ITEMS.filter((k) => !k.flag || flags[k.flag]).map((k) => ({ name: k.name, note: k.note })),
    equipment: inventory
      .filter((e) => e.quantity > 0 && ALL_ITEMS_BY_ID[e.itemId] && ALL_ITEMS_BY_ID[e.itemId].category !== "consumable")
      .map((e) => {
        const item = ALL_ITEMS_BY_ID[e.itemId] as EquipmentItemData;
        return {
          name: item.name,
          count: e.quantity,
          bonus: describeBonus(item),
          wearers: Object.entries(party).filter(([, slots]) => Object.values(slots).includes(item.id)).map(([id]) => nameOf(id)).join("、"),
        };
      }),
  };
}
let lastPauseDirection: Direction | null = null;
let pauseMessage: string | null = null;
let pauseMessageTimer = 0;
/** そうさ設定の画面。 */
let controlsMenu = createControlsMenuState();
let moveSpeed = loadMoveSpeed(window.localStorage);
/** モード（イージー＝戦闘後に全快、ノーマル＝ダメージ持ち越し）。ブラウザに保存し、セーブにも入れる。 */
let difficulty: Difficulty = loadDifficulty(window.localStorage);
/** ゲームの中の時間（ミリ秒）。外を歩いている間だけ進む。0＝朝。夜は町の人が減り、画面が暗くなる。 */
let clockMs = 0;
/** ノーマルで持ち越す、今のHP・MP（入っていない人は全快）。イージーでは使わない。 */
let vitals: Vitals = {};
function setDifficulty(next: Difficulty): void {
  difficulty = next;
  saveDifficulty(window.localStorage, difficulty);
  if (difficulty === "easy") vitals = {};
}
let lastControlsDirection: Direction | null = null;
window.addEventListener("keydown", (event) => {
  if ((event.key === "x" || event.key === "Escape") && controlsMenu.open) {
    if (controlsMenu.capturing) {
      // キー入力待ちの間にここへ届くのは、画面のボタン・コントローラーのもどる。待ちをやめる。
      keyRemap.cancelCapture();
      controlsMenu = finishCapture(controlsMenu, "かえなかった");
    } else {
      controlsMenu = closeControlsMenu(controlsMenu);
    }
    equipBackHandled = true;
    setTimeout(() => { equipBackHandled = false; }, 0);
  }
}, true);
let jobMenuWasOpen = false;
window.addEventListener("keydown", () => { jobMenuWasOpen = jobMenu.open; }, true);
window.addEventListener("keydown", (event) => {
  if (equipBackHandled || fieldUse.open || slotMenu.open) {
    return;
  }
  if (pauseMenu.open) {
    if (event.key === "x" || event.key === "Escape") {
      pauseMenu = backPauseMenu(pauseMenu);
    }
    return;
  }
  if ((event.key === "Tab" || event.key === "Escape") && !jobMenuWasOpen) {
    event.preventDefault();
    if (!title.open && !opening.open && !bootOpening.open && !battle && !dialogue.isActive() && !debugMenu.open && !jobMenu.open) {
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
  const add = (name: string, stats: LeveledStats, id: string): void => {
    const v = difficulty === "normal" ? vitals[id] : undefined;
    rows.push({
      name, level: stats.level, hp: v ? Math.min(stats.maxHp, v.hp) : stats.maxHp, maxHp: stats.maxHp, mp: v ? Math.min(stats.maxMp, v.mp) : stats.maxMp, maxMp: stats.maxMp,
      attack: stats.attack, defense: stats.defense, speed: stats.speed, expToNext: expToNextLevel(stats.exp),
    });
  };
  add("ユーリ", applyStatBonus(heroStats, equipmentBonus), "hero");
  for (const [id, stats] of Object.entries(companionStats)) {
    add(COMPANIONS[id].name, withEquipment(id, stats), id);
  }
  return rows;
}
let lastTitleDirection: Direction | null = null;
let openingSkipRequested = false;
/** 「もどる」（x・Esc・画面のもどるボタン）が押された。戦闘の選び直しに使う（毎フレーム、1回だけ読む）。 */
let backRequested = false;
window.addEventListener("keydown", (event) => {
  if (event.key === "x" || event.key === "Escape") {
    backRequested = true;
  }
  if ((event.key === "x" || event.key === "Escape") && title.open) {
    title = backTitle(title);
  }
  if ((event.key === "x" || event.key === "Escape") && opening.open) {
    openingSkipRequested = true;
  }
});
// 最初の画面（SUNSHINE SOFTWARE PRESENTS）は、画面のどこをタップしても決定になる（この操作が、音のはじまりにもなる）
window.addEventListener("pointerdown", () => {
  if (bootOpening.open && bootOpening.phase === "splash") actionButton.press();
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
/** 進行中の「動き」（武器をふる・魔法のエフェクト・のけぞり）。 */
let battleAnim: { spec: BattleAnimSpec; startedAt: number } | null = null;
/** 直前に唱えた魔法（全体魔法の2人目以降は、ためを省く）。コマンド選択にもどったら消す。 */
let lastCast: { fromId: string; fx: string } | null = null;
let lastBattleMessage: string | null = null;
let battle: BattleController | null = null;
let heroStats = createInitialHeroStats();
let heroEquipment: EquipmentSlots = createInitialEquipment();
/** 仲間に加わったキャラクターのステータス（キャラクターIDをキーにする）。 */
let companionStats: Record<string, LeveledStats> = {};
let inventory: Inventory = createInventory();
/** 仲間の装備（キャラクターIDごと。ユーリの装備は heroEquipment）。 */
let companionEquipment: Record<string, EquipmentSlots> = {};

/** ユーリと仲間みんなの装備。 */
function partyEquipment(): PartyEquipment {
  return { hero: heroEquipment, ...companionEquipment };
}

function setPartyEquipment(party: PartyEquipment): void {
  heroEquipment = party.hero ?? {};
  companionEquipment = Object.fromEntries(Object.entries(party).filter(([id]) => id !== "hero"));
}

/** 身につけている装備は、すべて持ち物に入っている（はずしたとき、ほかの人に渡せるように）。 */
function syncEquipmentToInventory(): void {
  inventory = ensureOwned(inventory, Object.values(partyEquipment()).flatMap((slots) => Object.values(slots)));
}

/** はじめの回復アイテムを持たせる（旅のはじめ・古いセーブを読んだときに1回だけ）。 */
function grantStarterItems(): void {
  if (flags["starter_items_granted"]) return;
  flags["starter_items_granted"] = true;
  for (const { itemId, quantity } of STARTER_CONSUMABLES) inventory = addItem(inventory, itemId, quantity);
}

syncEquipmentToInventory();
grantStarterItems();

/** そうび画面（メニューの「そうび」）。 */
let equipMenu = createEquipMenuState();
let lastEquipDirection: Direction | null = null;
let equipMessage: string | null = null;
/** そうび画面でもどるを押したとき、同じキーでメニューまで閉じないようにする目印。 */
let equipBackHandled = false;
window.addEventListener("keydown", (event) => {
  if ((event.key === "x" || event.key === "Escape") && equipMenu.open) {
    equipMenu = backEquipMenu(equipMenu);
    equipMessage = null;
    equipBackHandled = true;
    setTimeout(() => { equipBackHandled = false; }, 0);
  }
}, true);

/** そうび画面の仲間（ユーリと、加わった仲間）。 */
function equipMembers(): { id: string; name: string; stats: LeveledStats }[] {
  return [
    { id: "hero", name: "ユーリ", stats: heroStats },
    ...Object.entries(companionStats).map(([id, stats]) => ({ id, name: COMPANIONS[id].name, stats })),
  ];
}

const EQUIP_SLOT_LABELS = [
  { id: "weapon" as const, label: "ぶき" },
  { id: "armor" as const, label: "ぼうぐ" },
  { id: "accessory" as const, label: "かざり" },
];

function describeItemId(id: string | undefined): string {
  const item = id ? ALL_ITEMS_BY_ID[id] : undefined;
  return item && item.category !== "consumable" ? `${item.name}（${describeBonus(item)}）` : "なし";
}

function statsView(stats: LeveledStats): EquipStatsView {
  return { level: stats.level, maxHp: stats.maxHp, attack: stats.attack, defense: stats.defense, speed: stats.speed };
}

function equipCandidatesFor(): ReturnType<typeof candidatesFor> {
  const member = equipMembers()[equipMenu.member];
  return member ? candidatesFor(member.id, EQUIP_SLOT_LABELS[equipMenu.slot].id, partyEquipment(), inventory, ALL_ITEMS_BY_ID) : [];
}

function equipMenuView(): EquipMenuView {
  const members = equipMembers();
  const party = partyEquipment();
  const current = members[equipMenu.member];
  const baseOf = (id: string, p: PartyEquipment): LeveledStats => {
    const m = members.find((x) => x.id === id)!;
    return applyStatBonus(m.stats, computeEquipmentBonus(p[id] ?? {}, ALL_ITEMS_BY_ID));
  };
  const candidates: EquipMenuView["candidates"] = [];
  if (equipMenu.stage === "item" && current) {
    const category = EQUIP_SLOT_LABELS[equipMenu.slot].id;
    candidates.push({ label: "はずす", bonusText: "", after: statsView(baseOf(current.id, unequipFrom(party, current.id, category))) });
    for (const c of equipCandidatesFor()) {
      candidates.push({
        label: c.item.name,
        bonusText: describeBonus(c.item),
        note: c.takenBy ? `[${members.find((m) => m.id === c.takenBy)?.name ?? ""}]` : undefined,
        after: statsView(baseOf(current.id, equipTo(party, current.id, c.item, inventory))),
      });
    }
  }
  return {
    members: members.map((m) => ({
      id: m.id,
      name: m.name,
      stats: statsView(baseOf(m.id, party)),
      slots: EQUIP_SLOT_LABELS.map((slot) => ({ label: slot.label, itemText: describeItemId(party[m.id]?.[slot.id]) })),
    })),
    candidates,
    message: equipMessage,
  };
}

/** 買った品を、だれにつけるか選ぶ画面に出すもの。 */
function shopWearView(): ShopWearView {
  const item = shopWear ? ALL_ITEMS_BY_ID[shopWear.itemId] : undefined;
  const members = equipMembers();
  const party = partyEquipment();
  if (!item || item.category === "consumable") {
    return { itemName: "", bonusText: "", members: [] };
  }
  return {
    itemName: item.name,
    bonusText: describeBonus(item),
    members: members.map((m) => {
      const before = applyStatBonus(m.stats, computeEquipmentBonus(party[m.id] ?? {}, ALL_ITEMS_BY_ID));
      const after = applyStatBonus(m.stats, computeEquipmentBonus(equipTo(party, m.id, item, inventory)[m.id] ?? {}, ALL_ITEMS_BY_ID));
      return {
        name: m.name,
        currentText: canEquip(m.id, item) ? describeItemId(party[m.id]?.[item.category]) : `（${WEAPON_LABEL[WEAPON_TYPE_OF[m.id]]}しか もてない）`,
        before: statsView(before),
        after: statsView(after),
      };
    }),
  };
}

/** その人のその部位を、選んだ品にかえる（0番目は「はずす」）。 */
function applyEquipChoice(state: typeof equipMenu): void {
  const members = equipMembers();
  const member = members[state.member];
  if (!member) return;
  const category = EQUIP_SLOT_LABELS[state.slot].id;
  const choice = state.item;
  if (choice === 0) {
    setPartyEquipment(unequipFrom(partyEquipment(), member.id, category));
    equipMessage = `${member.name}は ${EQUIP_SLOT_LABELS[state.slot].label}を はずした`;
  } else {
    const candidate = candidatesFor(member.id, category, partyEquipment(), inventory, ALL_ITEMS_BY_ID)[choice - 1];
    if (!candidate) return;
    setPartyEquipment(equipTo(partyEquipment(), member.id, candidate.item, inventory));
    equipMessage = `${member.name}は ${candidate.item.name}を つけた`;
  }
  autosave();
  if (audioStarted) audio.playSe(seOf("confirm"));
}

/** その人の装備ボーナスを足した、今の実力。 */
function withEquipment(id: string, stats: LeveledStats): LeveledStats {
  const slots = id === "hero" ? heroEquipment : companionEquipment[id] ?? {};
  return applyStatBonus(stats, computeEquipmentBonus(slots, ALL_ITEMS_BY_ID));
}
/** 所持している灯貨（お金）。 */
let gold = 0;
/** お店の画面（町の武具屋で開く）。 */
let shopMenu = createShopMenuState();
let lastShopDirection: Direction | null = null;
/** 買った（持っている）装備を、その場でだれにつけるか選ぶ画面。itemId は品、cursor は仲間の何番目か（最後は「つけない」）。 */
let shopWear: { itemId: string; cursor: number } | null = null;
let lastShopWearDirection: Direction | null = null;
window.addEventListener("keydown", (event) => {
  if ((event.key === "x" || event.key === "Escape") && shopMenu.open) {
    if (shopWear) {
      shopWear = null; // つけない（品は持ち物に入っている。あとで「そうび」でつけられる）
    } else {
      shopMenu = closeShopMenu(shopMenu);
    }
  }
}, true);

/** 加入フラグが立っているのに、まだパーティに反映していない仲間を反映する。 */
const COMPANION_JOIN_FLAGS: { flag: string; companionId: string }[] = [
  { flag: "chapter0_reto_joined", companionId: RETO.id },
  { flag: "chapter1_mina_joined", companionId: MINA.id },
  { flag: "chapter2_guide_joined", companionId: GUIDE.id },
  { flag: "chapter3_orca_joined", companionId: ORCA.id },
  { flag: "chapter6_ayame_joined", companionId: AYAME.id },
];

/**
 * 先まで進んでいる人（ボスを倒した・調べ終えた）は、そこへ行くための準備（聞き込み・鍵・仕掛け）も済んでいるものとして扱う。
 * 道のりを長くする前のセーブや、デバッグで先へ進んだとき、通れなくならないように。
 */
const IMPLIED_FLAGS: { when: string[]; set: string[] }[] = [
  {
    when: ["chapter0_yugami_defeated", "chapter0_scorch_mark_found", "chapter0_clue_c001_found", "chapter0_reto_joined"],
    set: ["chapter0_quest_accepted", "chapter0_heard_rumor", "chapter0_got_lamp", "chapter0_lever_west", "chapter0_lever_east", "chapter0_shrine_open"],
  },
  {
    when: ["chapter1_yugami_defeated", "chapter1_excavation_found", "chapter1_clue_c002_found", "chapter1_reported_to_elder", "chapter1_mina_joined"],
    set: ["chapter1_quest_accepted", "chapter1_heard_miller", "chapter1_got_key", "chapter1_valve_west", "chapter1_valve_east", "chapter1_valves_open"],
  },
];

function applyImpliedFlags(): void {
  for (const rule of [...IMPLIED_FLAGS, ...DUNGEON_PREP_FLAGS.map((d) => ({ when: [d.boss], set: d.flags }))]) {
    if (rule.when.some((f) => flags[f])) {
      for (const f of rule.set) {
        if (!flags[f]) flags[f] = true;
      }
    }
  }
}

/** 仲間になった人は、もう町や家にはいない（いっしょに歩く）ので、その場所のNPCから外す。 */
const COMPANION_NPC_IDS: Record<string, string> = {
  "touri-reto": "chapter0_reto_joined",
  "mugikano-mina": "chapter1_mina_joined",
  "garasuko-guide": "chapter2_guide_joined",
  "tetsukusari-orca": "chapter3_orca_joined",
  "shimohara-ayame": "chapter6_ayame_joined",
};

function withoutJoinedCompanions(list: typeof npcs): typeof npcs {
  return list.filter(
    (npc) =>
      !(COMPANION_NPC_IDS[npc.id] && flags[COMPANION_NPC_IDS[npc.id]]) &&
      !(npc.hideWhenFlag && flags[npc.hideWhenFlag]) &&
      !(npc.showWhenFlag && !flags[npc.showWhenFlag]) &&
      // 夜は、ぶらぶら歩いている町の人が減る
      !(npc.wander && isOutdoorMap(currentMapId) && isNight(clockMs) && !staysOutAtNight(npc.id)),
  );
}

function syncCompanionsFromFlags(): void {
  applyImpliedFlags();
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
    party.push(createCompanionCombatant(COMPANIONS[id], withJobBonus(withEquipment(id, stats), jobStates[id], unlocked)));
  }
  // ノーマルでは、前の戦闘で受けたダメージ・使った魔力を持ち越す
  return difficulty === "normal" ? party.map((c) => applyVital(c, vitals[c.id])) : party;
}

/** いま持っている回復アイテムを、戦闘で使える形（種類と数）にしたもの。 */
function battleItemStacks(): ItemStack[] {
  return CONSUMABLE_ITEMS.map((item) => ({ item: toBattleItem(item), quantity: getQuantity(inventory, item.id) })).filter((s) => s.quantity > 0);
}

/** ヒーローのとくぎ＋加入済み仲間のとくぎをまとめた、戦闘用のとくぎ一覧。 */
function buildSkillsMap(heroSkill: Skill): Record<string, Skill> {
  const skills: Record<string, Skill> = { hero: heroSkill };
  for (const id of Object.keys(companionStats)) {
    skills[id] = COMPANIONS[id].skill;
  }
  return skills;
}
/** フィールドの「どうぐ」「まほう」の画面。 */
let fieldUse = createFieldUseState();
let lastFieldUseDirection: Direction | null = null;

/** 今のパーティ（装備・ジョブ・持ち越したHP/MP込み）。 */
function currentParty(): ReturnType<typeof createChapter0Party> {
  return buildActiveParty(applyStatBonus(heroStats, computeEquipmentBonus(heroEquipment, ALL_ITEMS_BY_ID)));
}

function fieldUseOptions(mode: "items" | "spells"): FieldUseOption[] {
  if (mode === "items") {
    return CONSUMABLE_ITEMS.filter((i) => getQuantity(inventory, i.id) > 0).map((i) => ({
      key: i.id, label: `${i.name} ×${getQuantity(inventory, i.id)}`, note: i.description ?? "", itemId: i.id,
    }));
  }
  const skills = buildSkillsMap(CHAPTER0_SKILL);
  const extras = buildExtraSkillsMap();
  const out: FieldUseOption[] = [];
  for (const id of ["hero", ...Object.keys(companionStats)]) {
    const name = id === "hero" ? "ユーリ" : COMPANIONS[id].name;
    for (const skill of [skills[id], ...(extras[id] ?? [])]) {
      if (skill && (skill.effect === "heal" || skill.effect === "healAll")) {
        out.push({ key: `${id}:${skill.id}`, label: `${name}：${skill.name}`, note: `MP${skill.mpCost}　${skill.effect === "healAll" ? "みんなのHPを回復" : "ひとりのHPを回復"}`, casterId: id, skill });
      }
    }
  }
  return out;
}

/** どうぐ・まほうを使う。メッセージを返す（使えなければ、何も減らさない）。 */
function applyFieldUse(apply: FieldUseApply): string {
  const party = currentParty().filter((c) => !c.isEnemy);
  const { option } = apply;
  if (option.itemId) {
    const item = CONSUMABLES_BY_ID[option.itemId];
    const target = apply.targetIndex === null ? undefined : party[apply.targetIndex];
    if (!item || !target) return "つかえない";
    const needHp = item.healAmount > 0 && target.hp < target.maxHp;
    const needMp = (item.mpAmount ?? 0) > 0 && target.mp < target.maxMp;
    if (!needHp && !needMp) return `${target.name.split(/[\s　]/)[0]}には、つかう必要がない`;
    vitals = healVital(vitals, target.id, target, item.healAmount, item.mpAmount ?? 0);
    inventory = removeItem(inventory, item.id, 1);
    if (audioStarted) audio.playSe(seOf("heal"));
    return `${item.name}を つかった！`;
  }
  const skill = option.skill;
  const caster = party.find((c) => c.id === option.casterId);
  if (!skill || !caster) return "つかえない";
  if (caster.mp < skill.mpCost) return "MPが たりない";
  const targets = skill.effect === "healAll" ? party : apply.targetIndex === null ? [] : [party[apply.targetIndex]];
  if (!targets.some((t) => t && t.hp < t.maxHp)) return "つかう必要がない";
  const amount = Math.max(1, Math.round(caster.attack * (skill.healRatio ?? 1)));
  for (const t of targets) vitals = healVital(vitals, t.id, t, amount, 0);
  vitals = healVital(vitals, caster.id, caster, 0, -skill.mpCost);
  if (audioStarted) audio.playSe(seOf("heal"));
  return `${skill.name}！ HPが かいふくした`;
}

function fieldUseMembers(): { name: string; hp: number; maxHp: number; mp: number; maxMp: number }[] {
  return currentParty().map((c) => ({ name: c.name.split(/[\s　]/)[0], hp: c.hp, maxHp: c.maxHp, mp: c.mp, maxMp: c.maxMp }));
}

/** ジョブで覚えた戦闘用の特技（ユーリと加入済みの仲間）。機能が解禁前なら空。 */
function buildExtraSkillsMap(): Record<string, Skill[]> {
  const unlocked = isJobSystemUnlocked(flags);
  const result: Record<string, Skill[]> = {};
  for (const id of ["hero", ...Object.keys(companionStats)]) {
    const level = id === "hero" ? heroStats.level : companionStats[id]?.level ?? 1;
    const innate = (COMPANIONS[id]?.extraSkills ?? []).filter((e) => level >= e.minLevel).map((e) => e.skill);
    result[id] = [...innate, ...battleSkillsOf(jobStates[id], unlocked)];
  }
  return result;
}
let victoryExpApplied = false;
let victoryMessage: string | null = null;
/** 勝ったあとにレベルアップした人と、上がった能力値（戦闘画面に表で出す）。 */
let victoryLevelUps: { name: string; from: number; to: number; gains: [string, number][] }[] = [];
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
      Object.entries(companionStats).map(([id, stats]) => [id, { stats, equipment: companionEquipment[id] }]),
    ),
    jobs: jobStates,
    inventory,
    gold,
    flags,
    difficulty,
    vitals,
    clockMs,
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
  companionEquipment = Object.fromEntries(Object.entries(data.companions).map(([id, entry]) => [id, entry.equipment ?? {}]));
  jobStates = data.jobs;
  inventory = data.inventory;
  // 持てない武器（杖のミナが剣、など）をつけていたら、はずす（専用武器の導入前のセーブ）
  setPartyEquipment(sanitizeParty(partyEquipment(), ALL_ITEMS_BY_ID));
  syncEquipmentToInventory();
  gold = data.gold ?? 0;
  vitals = difficulty === "normal" ? { ...(data.vitals ?? {}) } : {};
  clockMs = data.clockMs ?? 0;
  for (const key of Object.keys(flags)) {
    delete flags[key];
  }
  Object.assign(flags, data.flags);
  grantStarterItems();
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
  companionEquipment = {};
  jobStates = {};
  inventory = createInventory();
  syncEquipmentToInventory();
  vitals = {};
  clockMs = 0;
  gold = 0;
  for (const key of Object.keys(flags)) {
    delete flags[key];
  }
  grantStarterItems();
  encounterState = createEncounterState(Math.random);
  resetVehicles();
  switchMap(CHAPTER0_START.mapId, CHAPTER0_START.tileX, CHAPTER0_START.tileY);
}

/** 全滅したとき: いちばん新しいセーブ（自動セーブも含む）の場所からやりなおす。HP・MPは全快。セーブが無ければタイトルへ。 */
function restartFromLastSave(): void {
  const slot = latestSaveSlot(window.localStorage);
  const data = slot ? loadFromSlot(window.localStorage, slot) : null;
  if (!data) {
    title = createTitleState(hasAutosave());
    currentBgmTrack = getTrack("title");
    audio.playBgm(currentBgmTrack);
    return;
  }
  applySaveData(data);
  vitals = {};
  playMapBgm(currentMapId);
  saveMessage = "全滅してしまった…。セーブした場所から やりなおす";
  saveMessageTimer = 4000;
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
      prepareBattleScreen();
      victoryExpApplied = false;
      victoryMessage = null;
  victoryLevelUps = [];
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
    label: () => "マップ: 全体フィールド（灯里の近く） へワープ",
    action: () => switchMap("world-map", WORLD_TOWNS["touri-town"].x, WORLD_TOWNS["touri-town"].y + 1),
  },
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
  // 戦闘で使った回復アイテムを、持ち物から引く
  for (const [itemId, count] of Object.entries(finishedBattle.getItemUsage())) {
    inventory = removeItem(inventory, itemId, Math.min(count, getQuantity(inventory, itemId)));
  }
  // ノーマル: 戦闘が終わったときのHP・MPを持ち越す（全滅のときは全員HP1で立ち上がる）
  if (difficulty === "normal") {
    vitals = vitalsAfterBattle(finishedBattle.getState().party, outcome.outcome === "lost");
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
  const heroBefore = heroStats;
  const result = gainExp(heroStats, expGained, SAMPLE_GROWTH);
  heroStats = result.stats;
  const levelUpNames: string[] = [];
  victoryLevelUps = [];
  const record = (name: string, before: LeveledStats, after: LeveledStats, id: string): void => {
    vitals = growVital(vitals, id, after.maxHp - before.maxHp, after.maxMp - before.maxMp);
    victoryLevelUps.push({
      name,
      from: before.level,
      to: after.level,
      gains: [
        ["HP", after.maxHp - before.maxHp],
        ["MP", after.maxMp - before.maxMp],
        ["こうげき", after.attack - before.attack],
        ["ぼうぎょ", after.defense - before.defense],
        ["すばやさ", after.speed - before.speed],
      ],
    });
  };
  if (result.levelsGained > 0) {
    levelUpNames.push(`ユーリ（Lv${heroStats.level}）`);
    record("ユーリ", heroBefore, heroStats, "hero");
  }
  for (const [id, stats] of Object.entries(companionStats)) {
    const companionResult = gainExp(stats, expGained, COMPANIONS[id].growth);
    companionStats[id] = companionResult.stats;
    if (companionResult.levelsGained > 0) {
      levelUpNames.push(`${COMPANIONS[id].name}（Lv${companionResult.stats.level}）`);
      record(COMPANIONS[id].name, stats, companionResult.stats, id);
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

/** 1コマぶんの画面をすべて描く（戦闘に入る演出の前後でも、これを使う）。 */
function renderGameSceneBase(): void {
  ctx.fillStyle = "#101018";
  ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);

  if (bootOpening.open) {
    renderBootOpening(ctx, bootOpening, LOGICAL_WIDTH, LOGICAL_HEIGHT, GAME_TITLE);
    return;
  }
  if (title.open) {
    renderTitle(ctx, title, GAME_TITLE, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    renderSlotMenu(ctx, slotMenu, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    return;
  }
  if (staffRoll.open) {
    renderStaffRoll(ctx, staffRoll, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    return;
  }
  if (opening.open) {
    renderOpening(ctx, opening, LOGICAL_WIDTH, LOGICAL_HEIGHT, GAME_TITLE);
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
      battle.hasUsableItems(),
      battleAnim ? { spec: battleAnim.spec, elapsedMs: performance.now() - battleAnim.startedAt } : null,
    );
    if (victoryMessage && battle.getUiState().kind === "finished") {
      ctx.fillStyle = "#f2c14e";
      ctx.font = "10px monospace";
      ctx.textBaseline = "top";
      ctx.fillText(victoryMessage, 8, LOGICAL_HEIGHT - 56 + 18);
      if (victoryLevelUps.length > 0) {
        // レベルアップした人の、上がった能力値（HP・MP・こうげき・ぼうぎょ・すばやさ）
        const rowH = 22;
        const winH = 16 + victoryLevelUps.length * rowH;
        const winW = 330;
        const wx = Math.round((LOGICAL_WIDTH - winW) / 2);
        const wy = 14;
        drawWindow(ctx, wx, wy, winW, winH);
        ctx.textAlign = "left";
        victoryLevelUps.forEach((u, i) => {
          const y = wy + 8 + i * rowH;
          ctx.fillStyle = "#f2c14e";
          ctx.fillText(`${u.name}  Lv${u.from} → Lv${u.to}`, wx + 10, y);
          ctx.fillStyle = "#c8f0c8";
          ctx.fillText(u.gains.map(([k, v]) => `${k}+${v}`).join("  "), wx + 10, y + 10);
        });
      }
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
  // 家・木・NPCは、プレイヤーとの前後だけでなく、お互いの前後も足元の位置の順に並べて描く（家の裏を歩く人が家より手前に出ないように）。
  const depthItems: { feetY: number; draw: () => void }[] = [];
  for (const prop of map.data.props ?? []) {
    depthItems.push({ feetY: propFeetY(prop, map.data.tileHeight), draw: () => renderProps(ctx, map.data, renderCamera, () => true, [prop]) });
  }
  for (const npc of npcs) {
    depthItems.push({ feetY: visibleNpcFeetY(npc, map.data.tileHeight), draw: () => renderNpcs(ctx, [npc], map, renderCamera) });
  }
  depthItems.sort((a, b) => a.feetY - b.feetY);
  for (const item of depthItems) {
    if (item.feetY <= playerFeetY) item.draw();
  }
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
    renderFollowers(ctx, partyTrail, followers, renderCamera, (feetY) => feetY <= playerFeetY, onWorldMap ? WORLD_MAP_CHARACTER_SCALE : 1);
    renderPlayer(ctx, player, renderCamera, onWorldMap ? WORLD_MAP_CHARACTER_SCALE : 1);
    renderFollowers(ctx, partyTrail, followers, renderCamera, (feetY) => feetY > playerFeetY, onWorldMap ? WORLD_MAP_CHARACTER_SCALE : 1);
  } else {
    const fx = player.x + player.width / 2 - renderCamera.x;
    const fy = player.y + player.height - renderCamera.y;
    if (vehicle === "ship") {
      drawShip(ctx, fx, fy, player.direction);
    } else {
      drawAirship(ctx, fx, fy, player.direction, nowMs, true);
    }
  }
  for (const item of depthItems) {
    if (item.feetY > playerFeetY) item.draw();
  }
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

  // 夜の色（外の地図だけ）。夕方はあかね色、夜は青く暗く
  if (isOutdoorMap(currentMapId)) {
    const f = dayFraction(clockMs);
    const n = nightness(f);
    const glow = warmGlow(f);
    if (glow > 0.02) {
      ctx.fillStyle = `rgba(255, 140, 60, ${0.2 * glow})`;
      ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }
    if (n > 0.01) {
      ctx.save();
      ctx.globalCompositeOperation = "multiply";
      const lerp = (a: number, b: number): number => Math.round(a + (b - a) * n);
      ctx.fillStyle = `rgb(${lerp(255, 78)}, ${lerp(255, 92)}, ${lerp(255, 158)})`;
      ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);
      ctx.restore();
      ctx.fillStyle = `rgba(16, 24, 80, ${0.14 * n})`;
      ctx.fillRect(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT);
    }
    // 時間の表示（小さく、右上）
    ctx.font = "9px monospace";
    ctx.textBaseline = "top";
    ctx.textAlign = "right";
    ctx.fillStyle = "rgba(10,14,34,0.55)";
    ctx.fillRect(LOGICAL_WIDTH - 40, 17, 37, 12);
    ctx.fillStyle = n >= 0.7 ? "#a8b8ff" : "#f2c14e";
    ctx.fillText(`${n >= 0.7 ? "☾" : "☀"} ${periodLabel(clockMs)}`, LOGICAL_WIDTH - 6, 19);
    ctx.textAlign = "left";
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
  renderShop(ctx, shopMenu, gold, heroEquipment, inventory, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  if (shopWear && shopMenu.open) {
    renderShopWear(ctx, shopWearView(), shopWear.cursor, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  }
  if (!fieldUse.open) renderPauseMenu(ctx, pauseMenu, pauseMenu.screen === "status" ? statusRows() : [], pauseMessage, gold, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  renderSlotMenu(ctx, slotMenu, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  if (fieldUse.open) renderFieldUse(ctx, fieldUse, fieldUseMembers(), LOGICAL_WIDTH, LOGICAL_HEIGHT);
  if (pauseMenu.open && pauseMenu.screen === "items") {
    renderItemsScreen(ctx, itemsView(), itemsScroll, gold, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  }
  if (equipMenu.open) {
    renderEquipMenu(ctx, equipMenu, equipMenuView(), LOGICAL_WIDTH, LOGICAL_HEIGHT);
  }

  if (import.meta.env.DEV) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(`FPS: ${loop.getFps()}`, 4, LOGICAL_HEIGHT - 12);
    renderDebugMenu(ctx, debugMenu, DEBUG_MENU_ROWS, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  }
}

function renderGameScene(): void {
  renderGameSceneBase();
  if (controlsMenu.open) {
    renderControlsMenu(ctx, controlsMenu, keyBindings, moveSpeed, difficulty, LOGICAL_WIDTH, LOGICAL_HEIGHT);
  }
}

const loop = createGameLoop({
  update(dtMs) {
    syncCompanionsFromFlags();
    // 外を歩いている間だけ、時間が進む（メニュー・会話・戦闘・タイトルのあいだは止まる）
    if (!title.open && !battle && !bootOpening.open && !opening.open && !staffRoll.open && !pauseMenu.open && !shopMenu.open && !jobMenu.open && !fieldUse.open && !slotMenu.open && !dialogue.isActive() && isOutdoorMap(currentMapId)) {
      clockMs += dtMs;
    }
    // 開けた宝箱は、ふたが開いた絵にする
    setOpenedChests(new Set(npcs.filter((n) => n.openedFlag && flags[n.openedFlag]).map((n) => n.id)));
    // 会話が終わったあと（仲間になった直後）に、その人を場所から外す
    if (!dialogue.isActive()) {
      // 仲間になった人・倒されて去った人は場所から外し、あとから現れるもの（跡）は出す
      const wanted = withoutJoinedCompanions(WORLD_NPCS[currentMapId] ?? []);
      if (wanted.length !== npcs.length || wanted.some((n, i) => n.id !== npcs[i]?.id)) {
        npcs = wanted;
      }
    }

    if (saveMessageTimer > 0) {
      saveMessageTimer -= dtMs;
      if (saveMessageTimer <= 0) {
        saveMessageTimer = 0;
        saveMessage = null;
      }
    }

    const actionPressed = actionButton.consume();
    const backPressed = backRequested;
    backRequested = false;
    if (battleTransition) {
      battleTransition = actionPressed && canSkipTransition(battleTransition) ? skipToReveal(battleTransition) : advanceBattleTransition(battleTransition, dtMs);
      return;
    }
    // 決定の音は、メニューを選ぶとき（タイトル・つよさ・買い物・ジョブ・戦闘）だけ。会話を送るたび・歩いて調べるたびに鳴ると、うるさいので鳴らさない
    if (actionPressed && !bootOpening.open && (title.open || pauseMenu.open || shopMenu.open || jobMenu.open || battle)) {
      audio.playSe(seOf("confirm"));
    }

    if (bootOpening.open) {
      if (bootOpening.phase !== "splash") bootClockMs += dtMs;
      const before = bootOpening;
      bootOpening = actionPressed ? advanceBootOpening(bootOpening) : updateBootOpening(bootOpening, dtMs, LOGICAL_HEIGHT);
      if (!bootOpening.open && before.open) {
        // タイトル画面へ。曲をタイトルの曲にかえる
        currentBgmTrack = getTrack("title");
        if (audioStarted) {
          audio.playBgm(currentBgmTrack);
        }
      }
      return;
    }

    if (controlsMenu.open) {
      const direction = input.getDirection();
      if (!controlsMenu.capturing && direction !== lastControlsDirection) {
        if (direction === "up" || direction === "down") {
          controlsMenu = moveControlsCursor(controlsMenu, direction === "up" ? -1 : 1);
          audio.playSe(seOf("cursor"));
        } else if ((direction === "left" || direction === "right") && controlsMenu.cursor === SPEED_ROW) {
          moveSpeed = cycleMoveSpeed(moveSpeed, direction === "left" ? -1 : 1);
          saveMoveSpeed(window.localStorage, moveSpeed);
          audio.playSe(seOf("cursor"));
        } else if ((direction === "left" || direction === "right") && controlsMenu.cursor === DIFFICULTY_ROW) {
          setDifficulty(cycleDifficulty(difficulty, direction === "left" ? -1 : 1));
          audio.playSe(seOf("cursor"));
        }
        lastControlsDirection = direction;
      }
      if (actionPressed && !controlsMenu.capturing) {
        const result = confirmControlsMenu(controlsMenu);
        controlsMenu = result.state;
        const choice = result.choice;
        if (choice?.kind === "capture") {
          keyRemap.captureNextKey((key) => {
            if (key === "Escape") {
              controlsMenu = finishCapture(controlsMenu, "かえなかった");
              return;
            }
            keyBindings = rebind(keyBindings, choice.action, key);
            saveBindings(window.localStorage, keyBindings);
            const label = CONTROL_ACTIONS.find((a) => a.id === choice.action)?.label ?? "";
            controlsMenu = finishCapture(controlsMenu, `${label}を ${describeBinding(keyBindings, choice.action)} に した`);
          });
        } else if (choice?.kind === "speed") {
          moveSpeed = cycleMoveSpeed(moveSpeed, 1);
          saveMoveSpeed(window.localStorage, moveSpeed);
        } else if (choice?.kind === "difficulty") {
          setDifficulty(cycleDifficulty(difficulty, 1));
        } else if (choice?.kind === "reset") {
          keyBindings = resetBindings();
          moveSpeed = DEFAULT_MOVE_SPEED;
          saveMoveSpeed(window.localStorage, moveSpeed);
          saveBindings(window.localStorage, keyBindings);
        }
      }
      return;
    }
    lastControlsDirection = null;

    if (slotMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastSlotDirection) {
        if (direction === "up" || direction === "down") {
          slotMenu = moveSlotCursor(slotMenu, direction === "up" ? -1 : 1);
          audio.playSe(seOf("cursor"));
        }
        lastSlotDirection = direction;
      }
      if (backPressed) slotMenu = closeSlotMenu(slotMenu);
      if (actionPressed) {
        const slot = confirmSlot(slotMenu);
        if (slot) {
          if (slotMenu.mode === "save") {
            saveToSlot(window.localStorage, slot, buildSaveData());
            audio.playSe(seOf("save"));
            slotMenu = withSlotRows(slotMenu, summarizeSlots(window.localStorage, false), "セーブしました");
          } else {
            const data = loadFromSlot(window.localStorage, slot);
            if (data) {
              slotMenu = closeSlotMenu(slotMenu);
              title = { ...title, open: false };
              applySaveData(data);
              playMapBgm(currentMapId);
            }
          }
        } else {
          audio.playSe(seOf("error"));
        }
      }
      return;
    }
    lastSlotDirection = null;

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
        if (result.action === "keys") {
          controlsMenu = openControlsMenu();
        } else if (result.action === "continue") {
          // 「つづきから」: どのセーブから始めるか選ぶ（自動セーブも入る）。選ぶまでタイトルは開いたまま
          title = { ...title, open: true };
          slotMenu = openSlotMenu("load", summarizeSlots(window.localStorage, true));
        } else if (result.action === "new") {
          // まずオープニング（あらすじ）を流す。曲は壮大な `fate`。終わったらゲームを始める。
          opening = startOpening();
          if (audioStarted) {
            currentBgmTrack = getTrack("fate");
            audio.playBgm(currentBgmTrack);
          }
        }
      }
      return;
    }
    lastTitleDirection = null;

    if (opening.open) {
      opening = actionPressed ? advanceOpening(opening) : updateOpening(opening, dtMs);
      if (openingSkipRequested) {
        opening = skipOpening(opening);
      }
      openingSkipRequested = false;
      if (!opening.open) {
        resetToNewGame();
        dialogue.start(CHAPTER0_OPENING_COMMANDS);
        playMapBgm(currentMapId);
      }
      return;
    }

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
    if (equipMenu.open) {
      const direction = input.getDirection();
      const counts = { members: equipMembers().length, slots: EQUIP_SLOT_LABELS.length, items: equipMenu.stage === "item" ? equipCandidatesFor().length + 1 : 1 };
      if (direction !== lastEquipDirection) {
        if (direction === "up" || direction === "down") {
          equipMenu = moveEquipCursor(equipMenu, direction === "up" ? -1 : 1, counts);
          audio.playSe(seOf("cursor"));
        }
        lastEquipDirection = direction;
      }
      if (actionPressed) {
        const before = equipMenu;
        const result = confirmEquipMenu(before);
        equipMenu = result.state;
        if (result.apply) {
          applyEquipChoice(before);
        } else {
          equipMessage = null;
        }
      }
      return;
    }
    lastEquipDirection = null;
    if (fieldUse.open) {
      const direction = input.getDirection();
      if (direction !== lastFieldUseDirection) {
        if (direction === "up" || direction === "down" || direction === "left" || direction === "right") {
          const members = fieldUseMembers().length;
          fieldUse = moveFieldUse(fieldUse, direction === "up" || direction === "left" ? -1 : 1, fieldUse.stage === "target" ? members : fieldUse.options.length);
          audio.playSe(seOf("cursor"));
        }
        lastFieldUseDirection = direction;
      }
      if (backPressed) fieldUse = backFieldUse(fieldUse);
      if (actionPressed) {
        const result = confirmFieldUse(fieldUse);
        fieldUse = result.state;
        if (result.apply) {
          const message = applyFieldUse(result.apply);
          fieldUse = refreshFieldUse(fieldUse, fieldUseOptions(fieldUse.mode), message);
          if (fieldUse.stage === "target" && fieldUse.options.length === 0) fieldUse = { ...fieldUse, stage: "pick" };
        }
      }
      return;
    }
    lastFieldUseDirection = null;

    if (pauseMenu.open) {
      const direction = input.getDirection();
      if (direction !== lastPauseDirection && pauseMenu.screen === "items") {
        if (direction === "up") itemsScroll = Math.max(0, itemsScroll - 3);
        if (direction === "down") itemsScroll += 3;
        lastPauseDirection = direction;
      } else if (direction !== lastPauseDirection) {
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
        if (result.state.screen === "items" && pauseMenu.screen !== "items") itemsScroll = 0;
        pauseMenu = result.state;
        if (result.action === "save") {
          slotMenu = openSlotMenu("save", summarizeSlots(window.localStorage, false));
        } else if (result.action === "keys") {
          controlsMenu = openControlsMenu();
        } else if (result.action === "use" || result.action === "magic") {
          const mode = result.action === "use" ? "items" : "spells";
          fieldUse = openFieldUse(mode, fieldUseOptions(mode));
        } else if (result.action === "equip") {
          equipMenu = openEquipMenu();
          equipMessage = null;
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
      if (shopWear) {
        // 買った品を、だれにつけるか選ぶ（ユーリも仲間も。最後は「つけない」）
        const members = equipMembers();
        if (direction !== lastShopWearDirection) {
          if (direction === "up" || direction === "down") {
            shopWear = { ...shopWear, cursor: (shopWear.cursor + (direction === "up" ? -1 : 1) + members.length + 1) % (members.length + 1) };
            audio.playSe(seOf("cursor"));
          }
          lastShopWearDirection = direction;
        }
        if (actionPressed) {
          const member = members[shopWear.cursor];
          const item = ALL_ITEMS_BY_ID[shopWear.itemId];
          if (member && item && item.category !== "consumable" && !canEquip(member.id, item)) {
            audio.playSe(seOf("error"));
            shopMenu = withShopMessage(shopMenu, `${member.name}は ${WEAPON_LABEL[WEAPON_TYPE_OF[member.id]]}しか もてない`);
            return;
          }
          if (member && item && item.category !== "consumable") {
            setPartyEquipment(equipTo(partyEquipment(), member.id, item, inventory));
            shopMenu = withShopMessage(shopMenu, `${member.name}は ${item.name}を つけた！`);
            autosave();
          } else {
            shopMenu = withShopMessage(shopMenu, "つけなかった（「そうび」であとからつけられる）");
          }
          shopWear = null;
        }
        return;
      }
      lastShopWearDirection = null;
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
        if (item && item.category === "consumable") {
          const result = purchaseConsumable(item.id, gold, getQuantity(inventory, item.id));
          if (result.ok) {
            gold = result.gold;
            inventory = addItem(inventory, item.id, 1);
            audio.playSe(seOf("buy"));
            autosave();
          } else {
            audio.playSe(seOf("error"));
          }
          shopMenu = withShopMessage(shopMenu, result.message);
        } else if (item) {
          // 同じ品を何個でも買える（仲間みんなに同じ武器・防具をつけられる）
          const result = purchaseItem(item.id, gold);
          if (result.ok) {
            gold = result.gold;
            inventory = addItem(inventory, item.id, 1);
            audio.playSe(seOf("buy"));
            autosave();
            // 買ったら、その場でだれにつけるか選ぶ
            shopWear = { itemId: item.id, cursor: 0 };
            shopMenu = withShopMessage(shopMenu, `${result.item.name}を買った！ だれにつける？`);
          } else {
            audio.playSe(seOf("error"));
            shopMenu = withShopMessage(shopMenu, result.message);
          }
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
          const anim = battleAnimFor(uiState.text, battle.getState(), (id) => WEAPON_TYPE_OF[id]);
          // 全体魔法の2人目からは、ためを省いて、すぐ当てる（柱・いなずまが続けて立つ）
          let animSpec = anim;
          if (anim?.fx && anim.fromId && (anim.casterId || anim.motion === "cast")) {
            if (lastCast && lastCast.fromId === anim.fromId && lastCast.fx === anim.fx && anim.area) {
              animSpec = { ...anim, fxStart: 0, durationMs: 760, motion: null, casterId: undefined };
            }
            lastCast = { fromId: anim.fromId, fx: anim.fx };
          }
          battleAnim = animSpec ? { spec: animSpec, startedAt: performance.now() } : null;
          const se = battleSeFor(uiState.text, battle.getState().party.map((c) => c.name));
          if (audioStarted) {
            if (anim?.motion) audio.playSe(seOf(swingSeFor(anim.motion)));
            else if (anim?.casterId) audio.playSe(seOf("magic-charge"));
            // 当たる音・魔法の音は、武器がとどく／魔法が出るときに合わせる
            if (se) {
              const delay = anim ? Math.round(anim.durationMs * anim.fxStart) : 0;
              if (delay > 0) window.setTimeout(() => audio.playSe(seOf(se)), delay);
              else audio.playSe(seOf(se));
            }
          }
        }
      } else {
        lastBattleMessage = null;
        lastCast = null;
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
      if (backPressed) {
        battle.cancel();
      }
      if (actionPressed) {
        if (uiState.kind === "finished") {
          const lost = uiState.outcome === "lost";
          battle = null;
          if (lost) {
            restartFromLastSave();
          } else {
            playMapBgm(currentMapId);
          }
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
    player = updatePlayer(player, input.getDirection(), dtMs * (onWorld ? VEHICLE_SPEED[vehicle] : 1) * MOVE_SPEEDS[moveSpeed].factor, moveMap, onWorld ? [] : npcs.filter((n) => !(npcLook(n) === "object" && objectKindOf(n.id) === "generic")));
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
    partyTrail.update(player, dtMs, followerSpecs().length, Math.max(1, (onWorld ? VEHICLE_SPEED[vehicle] : 1) * MOVE_SPEEDS[moveSpeed].factor));
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
    const exitHere = findExitAt(map, centerTileX, centerTileY);
    if (input.getDirection() === null) exitReleased = true;
    if (exitReleased && !exitHere) exitArmed = true;
    // 家の玄関は、家のほう（上）へ押しているときだけ入る。前を通るだけでは入らない
    const exit = vehicle === "foot" && exitArmed && (!exitHere?.enter || input.getDirection() === exitHere.enter) ? exitHere : undefined;
    if (exit && exit.requireFlag && !flags[exit.requireFlag]) {
      // 条件（仕掛け・道具など）が足りない出口は、ヒントを出して1マス押し戻す
      const back = { up: { x: 0, y: 1 }, down: { x: 0, y: -1 }, left: { x: 1, y: 0 }, right: { x: -1, y: 0 } }[player.direction];
      player = { ...player, x: player.x + back.x * map.data.tileWidth, y: player.y + back.y * map.data.tileHeight, moving: false };
      dialogue.start([{ type: "message", text: exit.blockedMessage ?? "まだ先へは進めない。" }]);
      return;
    }
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
            worldBattleBiome = "ship";
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
    if (battleTransition && battle) {
      if (isCoverPhase(battleTransition)) {
        // 前半: 戦闘はまだ見せず、フィールドの上に演出を重ねる
        const hiddenBattle = battle;
        battle = null;
        try {
          renderGameScene();
        } finally {
          battle = hiddenBattle;
        }
        renderTransitionCover(ctx, battleTransition, LOGICAL_WIDTH, LOGICAL_HEIGHT);
      } else {
        // 後半: 戦闘画面が、暗いところからひらく
        renderGameScene();
        renderTransitionReveal(ctx, battleTransition, LOGICAL_WIDTH, LOGICAL_HEIGHT);
      }
      return;
    }
    renderGameScene();
  },
});


function frame(nowMs: number): void {
  gamepad.poll();
  loop.tick(nowMs);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
