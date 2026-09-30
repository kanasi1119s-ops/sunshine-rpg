import { createEventRunner, type WarpRequest } from "../event/event-runner";
import type { EventCommand, EventInput, EventStep, Flags } from "../event/types";
import { computeVisibleChars } from "./typewriter";

export type DialogueRenderState =
  | { kind: "message"; speaker?: string; visibleText: string; fullyShown: boolean }
  | { kind: "choice"; text: string; labels: string[]; selectedIndex: number };

export interface DialogueControllerOptions {
  onWarp?: (warp: WarpRequest) => void;
  onStartBattle?: (battleId: string) => void;
  onGiveGold?: (amount: number) => void;
  onOpenShop?: (shopId: string) => void;
  charsPerSecond?: number;
}

/**
 * イベント実行（event-runner）と、文字送り・選択カーソルなどの
 * 画面表示用の状態をまとめて扱う。DOM・Canvasには一切触れない。
 */
export class DialogueController {
  private runner: ReturnType<typeof createEventRunner> | null = null;
  private currentStep: EventStep | null = null;
  private elapsedMs = 0;
  private choiceIndex = 0;
  private readonly charsPerSecond: number;

  constructor(
    private readonly flags: Flags,
    private readonly options: DialogueControllerOptions = {},
  ) {
    this.charsPerSecond = options.charsPerSecond ?? 30;
  }

  isActive(): boolean {
    return this.currentStep !== null;
  }

  start(commands: EventCommand[]): void {
    this.runner = createEventRunner(commands, this.flags, {
      onWarp: this.options.onWarp,
      onStartBattle: this.options.onStartBattle,
      onGiveGold: this.options.onGiveGold,
      onOpenShop: this.options.onOpenShop,
    });
    this.advance(undefined);
  }

  update(dtMs: number): void {
    if (this.currentStep?.kind === "message") {
      this.elapsedMs += dtMs;
    }
  }

  moveChoice(delta: number): void {
    if (this.currentStep?.kind !== "choice") {
      return;
    }
    const count = this.currentStep.labels.length;
    this.choiceIndex = (this.choiceIndex + delta + count) % count;
  }

  /** 決定操作。文字送り中なら全部表示、表示済みなら次へ進む／選択肢を確定する。 */
  confirm(): void {
    if (!this.currentStep) {
      return;
    }
    if (this.currentStep.kind === "message") {
      const visible = computeVisibleChars(this.currentStep.text, this.elapsedMs, this.charsPerSecond);
      if (visible < this.currentStep.text.length) {
        this.elapsedMs = Number.MAX_SAFE_INTEGER;
        return;
      }
      this.advance({ kind: "advance" });
      return;
    }
    this.advance({ kind: "choose", index: this.choiceIndex });
  }

  getRenderState(): DialogueRenderState | null {
    if (!this.currentStep) {
      return null;
    }
    if (this.currentStep.kind === "message") {
      const visible = computeVisibleChars(this.currentStep.text, this.elapsedMs, this.charsPerSecond);
      return {
        kind: "message",
        speaker: this.currentStep.speaker,
        visibleText: this.currentStep.text.slice(0, visible),
        fullyShown: visible >= this.currentStep.text.length,
      };
    }
    return {
      kind: "choice",
      text: this.currentStep.text,
      labels: this.currentStep.labels,
      selectedIndex: this.choiceIndex,
    };
  }

  private advance(input: EventInput | undefined): void {
    if (!this.runner) {
      return;
    }
    const result = this.runner.next(input);
    if (result.done || !result.step) {
      this.runner = null;
      this.currentStep = null;
      return;
    }
    this.currentStep = result.step;
    this.elapsedMs = 0;
    this.choiceIndex = 0;
  }
}
