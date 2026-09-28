import type { EventCommand } from "./types";

/**
 * イベントスクリプトの中身を検査するための補助関数。
 * QA（roles.md 3-10）の「データの整合性チェック」を自動テストにするために使う。
 */

function walk(commands: EventCommand[], visit: (command: EventCommand) => void): void {
  for (const command of commands) {
    visit(command);
    switch (command.type) {
      case "choice":
        for (const option of command.options) {
          walk(option.commands, visit);
        }
        break;
      case "if":
        walk(command.then, visit);
        if (command.else) {
          walk(command.else, visit);
        }
        break;
      default:
        break;
    }
  }
}

/** setFlag で立てられる可能性があるフラグ名の一覧（重複なし）。 */
export function collectSetFlags(commands: EventCommand[]): Set<string> {
  const flags = new Set<string>();
  walk(commands, (command) => {
    if (command.type === "setFlag") {
      flags.add(command.flag);
    }
  });
  return flags;
}

/** if で参照されるフラグ名の一覧（重複なし）。 */
export function collectReferencedFlags(commands: EventCommand[]): Set<string> {
  const flags = new Set<string>();
  walk(commands, (command) => {
    if (command.type === "if") {
      flags.add(command.flag);
    }
  });
  return flags;
}

/** warp コマンドが指す移動先マップIDの一覧（重複なし）。 */
export function collectWarpTargets(commands: EventCommand[]): Set<string> {
  const mapIds = new Set<string>();
  walk(commands, (command) => {
    if (command.type === "warp") {
      mapIds.add(command.mapId);
    }
  });
  return mapIds;
}

/** startBattle コマンドが指す戦闘IDの一覧（重複なし）。 */
export function collectBattleIds(commands: EventCommand[]): Set<string> {
  const battleIds = new Set<string>();
  walk(commands, (command) => {
    if (command.type === "startBattle") {
      battleIds.add(command.battleId);
    }
  });
  return battleIds;
}
