import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * サブストーリーの実装フォーマット（roadmap 5-1、`docs/design/side-stories.md`）。
 * 1本のサブストーリーは「依頼人（giver）」と、調べる場所（steps）と、報告で終わる。
 * 依頼人の会話は、状態（未解放→受注前→受注中→報告できる→完了）でフラグを見て切り替わる。
 * フラグの名前は `side_<key>_accepted` / `side_<key>_step<番号>` / `side_<key>_done`。
 * 報酬は、灯貨・所持品の仕組みができるまで「ごほうび（仮）」の会話として見せ、`side_<key>_done` で記録する。
 */
export interface SideStoryStep {
  mapId: string;
  tileX: number;
  tileY: number;
  color: string;
  /** 調べたときの会話。 */
  commands: EventCommand[];
  /** すでに調べたあとの会話（省略時は決まった一言）。 */
  afterCommands?: EventCommand[];
}

export interface SideStory {
  /** "S-001" のような番号（`docs/story/side-stories.md`）。 */
  id: string;
  /** フラグ名に使う小文字の識別子（例: "s001"）。 */
  key: string;
  title: string;
  /** すべて立っているとき、依頼を受けられる。 */
  unlockFlags: string[];
  giver: { mapId: string; tileX: number; tileY: number; color: string; spriteName?: string };
  /** 解放前に話しかけたときの会話。 */
  locked: EventCommand[];
  /** 依頼の説明（受注の選択肢の前）。 */
  offer: EventCommand[];
  offerPrompt: string;
  acceptLabel: string;
  declineLabel?: string;
  /** 受注後・まだ調べ終わっていないときの会話。 */
  hint: EventCommand[];
  steps: SideStoryStep[];
  /** すべて調べ終わって報告したときの会話。 */
  complete: EventCommand[];
  /** 「ごほうび」の一文（仮）。 */
  reward: string;
  /** 完了後の会話。 */
  after: EventCommand[];
}

export function say(speaker: string | undefined, text: string): EventCommand {
  return speaker ? { type: "message", text, speaker } : { type: "message", text };
}

const flag = (key: string, name: string): string => `side_${key}_${name}`;

/** すべてのフラグが立っているときだけ then を実行し、そうでなければ otherwise を実行する。 */
function whenAll(flags: string[], then: EventCommand[], otherwise: EventCommand[]): EventCommand[] {
  if (flags.length === 0) {
    return then;
  }
  const [first, ...rest] = flags;
  return [{ type: "if", flag: first, equals: true, then: whenAll(rest, then, otherwise), else: otherwise }];
}

function giverCommands(story: SideStory): EventCommand[] {
  const { key } = story;
  const stepFlags = story.steps.map((_, i) => flag(key, `step${i + 1}`));
  const accept: EventCommand[] = [
    ...story.offer,
    {
      type: "choice",
      text: story.offerPrompt,
      options: [
        {
          label: story.acceptLabel,
          commands: [{ type: "setFlag", flag: flag(key, "accepted"), value: true }, ...(stepFlags.length === 0 ? story.complete : [])],
        },
        { label: story.declineLabel ?? "あとにする", commands: [] },
      ],
    },
  ];
  // 調べる場所がない話は、受注した場で完結する。
  if (stepFlags.length === 0) {
    accept[accept.length - 1] = {
      type: "choice",
      text: story.offerPrompt,
      options: [
        {
          label: story.acceptLabel,
          commands: [
            ...story.complete,
            say(undefined, `【ごほうび（仮）】${story.reward}`),
            { type: "setFlag", flag: flag(key, "accepted"), value: true },
            { type: "setFlag", flag: flag(key, "done"), value: true },
          ],
        },
        { label: story.declineLabel ?? "あとにする", commands: [] },
      ],
    };
  }
  const report: EventCommand[] = [
    ...story.complete,
    say(undefined, `【ごほうび（仮）】${story.reward}`),
    { type: "setFlag", flag: flag(key, "done"), value: true },
  ];
  return [
    {
      type: "if",
      flag: flag(key, "done"),
      equals: true,
      then: story.after,
      else: [
        {
          type: "if",
          flag: flag(key, "accepted"),
          equals: true,
          then: whenAll(stepFlags, report, story.hint),
          else: whenAll(story.unlockFlags, accept, story.locked),
        },
      ],
    },
  ];
}

function stepCommands(story: SideStory, index: number): EventCommand[] {
  const step = story.steps[index];
  const own = flag(story.key, `step${index + 1}`);
  return [
    {
      type: "if",
      flag: flag(story.key, "accepted"),
      equals: true,
      then: [
        {
          type: "if",
          flag: own,
          equals: true,
          then: step.afterCommands ?? [say(undefined, "ここでは、もう気になるものは見つからなかった。")],
          else: [...step.commands, { type: "setFlag", flag: own, value: true }],
        },
      ],
      else: [say(undefined, "ふつうの景色が広がっている。今は、気になるものは見当たらない。")],
    },
  ];
}

/** サブストーリーの一覧から、地図ごとのNPC（依頼人と調べる場所）を作る。 */
export function buildSideStoryNpcs(stories: SideStory[]): Record<string, Npc[]> {
  const result: Record<string, Npc[]> = {};
  const add = (mapId: string, npc: Npc): void => {
    (result[mapId] ??= []).push(npc);
  };
  for (const story of stories) {
    add(story.giver.mapId, {
      id: `side-${story.key}-giver`,
      tileX: story.giver.tileX,
      tileY: story.giver.tileY,
      color: story.giver.color,
      ...(story.giver.spriteName ? { spriteName: story.giver.spriteName } : {}),
      commands: giverCommands(story),
    });
    story.steps.forEach((step, i) => {
      add(step.mapId, {
        id: `side-${story.key}-step${i + 1}`,
        tileX: step.tileX,
        tileY: step.tileY,
        color: step.color,
        commands: stepCommands(story, i),
      });
    });
  }
  return result;
}
