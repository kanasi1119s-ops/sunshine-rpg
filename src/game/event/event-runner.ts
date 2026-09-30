import type { EventCommand, EventInput, EventStep, Flags } from "./types";

export interface WarpRequest {
  mapId: string;
  tileX: number;
  tileY: number;
}

interface RunnerOptions {
  onWarp?: (warp: WarpRequest) => void;
  onStartBattle?: (battleId: string) => void;
  onGiveGold?: (amount: number) => void;
  onOpenShop?: (shopId: string) => void;
  onStaffRoll?: () => void;
}

/**
 * イベントコマンドの列を順番に実行するジェネレーター。
 * message・choice ではポーズして呼び出し側に EventStep を渡し、
 * 呼び出し側が .next(input) を呼ぶまで先に進まない。
 * これにより、DOM・Canvasに触れずにイベントの進行をテストできる。
 */
function* runCommands(
  commands: EventCommand[],
  flags: Flags,
  options: RunnerOptions,
): Generator<EventStep, void, EventInput | undefined> {
  for (const command of commands) {
    switch (command.type) {
      case "message":
        yield { kind: "message", text: command.text, speaker: command.speaker };
        break;

      case "choice": {
        const input = yield {
          kind: "choice",
          text: command.text,
          labels: command.options.map((option) => option.label),
        };
        const index = input?.kind === "choose" ? input.index : 0;
        const chosen = command.options[index];
        if (chosen) {
          yield* runCommands(chosen.commands, flags, options);
        }
        break;
      }

      case "setFlag":
        flags[command.flag] = command.value;
        break;

      case "if": {
        const matches = Boolean(flags[command.flag]) === command.equals;
        yield* runCommands(matches ? command.then : (command.else ?? []), flags, options);
        break;
      }

      case "warp":
        options.onWarp?.({
          mapId: command.mapId,
          tileX: command.tileX,
          tileY: command.tileY,
        });
        break;

      case "startBattle":
        options.onStartBattle?.(command.battleId);
        break;

      case "giveGold":
        options.onGiveGold?.(command.amount);
        break;

      case "shop":
        options.onOpenShop?.(command.shopId);
        break;

      case "staffRoll":
        options.onStaffRoll?.();
        break;
    }
  }
}

export interface EventRunner {
  /** 次のステップまで進める。入力が要らない最初の呼び出しは input を省略してよい。 */
  next: (input?: EventInput) => { done: boolean; step?: EventStep };
}

export function createEventRunner(
  commands: EventCommand[],
  flags: Flags,
  options: RunnerOptions = {},
): EventRunner {
  const generator = runCommands(commands, flags, options);
  return {
    next(input) {
      const result = generator.next(input);
      if (result.done) {
        return { done: true };
      }
      return { done: false, step: result.value };
    },
  };
}
