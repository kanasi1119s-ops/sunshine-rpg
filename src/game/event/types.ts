export type Flags = Record<string, boolean>;

export interface ChoiceOption {
  label: string;
  commands: EventCommand[];
}

export type EventCommand =
  | { type: "message"; text: string; speaker?: string }
  | { type: "choice"; text: string; options: ChoiceOption[] }
  | { type: "setFlag"; flag: string; value: boolean }
  | { type: "if"; flag: string; equals: boolean; then: EventCommand[]; else?: EventCommand[] }
  | { type: "warp"; mapId: string; tileX: number; tileY: number }
  | { type: "startBattle"; battleId: string }
  /** 灯貨（お金）を手に入れる。 */
  | { type: "giveGold"; amount: number }
  /** 宝箱などで装備を手に入れる（`src/game/economy/treasure.ts` の品ID。同じ部位の今の装備より強ければ、その場で装備する）。 */
  | { type: "giveEquipment"; itemId: string }
  /** お店の画面を開く（`src/game/economy/shop.ts` の店ID）。 */
  | { type: "shop"; shopId: string }
  /** 宿屋: 「とまる／やめる」を選ばせ、とまると灯貨を払ってHP・MPが全快し、朝になる。 */
  | { type: "inn"; price: number }
  /** スタッフロール（エンディングの演出）を流す。 */
  | { type: "staffRoll" };

/** イベント実行中、画面表示側に「今これを見せて」と伝える1コマ。 */
export type EventStep =
  | { kind: "message"; text: string; speaker?: string }
  | { kind: "choice"; text: string; labels: string[] };

/** 画面表示側からイベント実行側へ「プレイヤーがこう操作した」を伝える。 */
export type EventInput = { kind: "advance" } | { kind: "choose"; index: number };
