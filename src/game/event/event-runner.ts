import type { EventCommand, EventInput, EventStep, Flags } from "./types";

export interface WarpRequest {
  mapId: string;
  tileX: number;
  tileY: number;
}

interface RunnerOptions {
  onWarp?: (warp: WarpRequest) => void;
  /** 町にとめた飛空艇に乗って、飛び立つ。 */
  onTakeoff?: () => void;
  onStartBattle?: (battleId: string) => void;
  onGiveGold?: (amount: number) => void;
  onGiveEquipment?: (itemId: string) => void;
  onOpenShop?: (shopId: string) => void;
  /** 宿屋にとまる。灯貨が足りて、とまれたら true（灯貨を払う・全快・朝にする、は呼び出し側）。 */
  onInnStay?: (price: number) => boolean;
  onStaffRoll?: () => void;
  onCinematic?: (on: boolean) => void;
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

      case "takeoff":
        options.onTakeoff?.();
        break;

      case "startBattle":
        options.onStartBattle?.(command.battleId);
        break;

      case "giveGold":
        options.onGiveGold?.(command.amount);
        break;

      case "giveEquipment":
        options.onGiveEquipment?.(command.itemId);
        break;

      case "shop":
        options.onOpenShop?.(command.shopId);
        break;

      case "inn": {
        if (command.home) {
          const input = yield { kind: "choice", text: "少し休んでいこうか？", labels: ["休む", "やめる"] };
          if (input?.kind === "choose" && input.index === 0) {
            options.onInnStay?.(0);
            yield { kind: "message", text: "自分のベッドで、ぐっすり眠った。体も心も、すっかり元気になった！（HP・MPが全回復）" };
          }
          break;
        }
        const input = yield { kind: "choice", text: `一晩 ${command.price}灯貨 です。とまっていきますか？`, labels: ["とまる", "やめる"] };
        if (input?.kind === "choose" && input.index === 0) {
          const ok = options.onInnStay?.(command.price) ?? false;
          yield {
            kind: "message",
            text: ok ? "ぐっすり眠って、朝になった。体も心も、すっかり元気になった！（HP・MPが全回復）" : "おっと、灯貨が足りないようだね。",
            speaker: "宿屋の主人",
          };
        } else {
          yield { kind: "message", text: "また、いつでもどうぞ。", speaker: "宿屋の主人" };
        }
        break;
      }

      case "cinematic":
        options.onCinematic?.(command.on);
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
