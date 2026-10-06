import type { SceneTime } from "../time-of-day";

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
  /** 宿屋: 「とまる／やめる」を選ばせ、とまると灯貨を払ってHP・MPが全快し、朝になる。home なら、自分の家のベッドで休む（宿屋の主人のセリフにしない。2026-10-06）。 */
  | { type: "inn"; price: number; home?: boolean }
  /** 映画のような演出（上下に黒い帯）を、入れる・はずす。会話がおわると、自動ではずれる。 */
  | { type: "cinematic"; on: boolean }
  /** 町にとめた飛空艇に乗って、飛び立つ（空の町・浮嶼。2026-10-06）。会話はここで終わる。 */
  | { type: "takeoff" }
  /** スタッフロール（エンディングの演出）を流す。 */
  | { type: "staffRoll" }
  /** 時計を、その時間帯まで進める（イベントの途中で「その夜」「翌朝」にする。2026-10-06）。 */
  | { type: "time"; time: SceneTime }
  /** 画面を暗くする・もどす（回想などを、暗い画面に文字だけで見せる。会話がおわると、自動でもどる。2026-10-06）。 */
  | { type: "screen"; dark: boolean };

/** イベント実行中、画面表示側に「今これを見せて」と伝える1コマ。 */
export type EventStep =
  | { kind: "message"; text: string; speaker?: string }
  | { kind: "choice"; text: string; labels: string[] };

/** 画面表示側からイベント実行側へ「プレイヤーがこう操作した」を伝える。 */
export type EventInput = { kind: "advance" } | { kind: "choose"; index: number };
