import type { EventCommand } from "../event/types";
import { placeName } from "../save/slots";
import type { SideStory } from "./side-story";

/**
 * 「依頼の記録」（2026-10-06、人間の指示「サブストーリーわかりにくいんだよな・・・サブストーリーを受注した一覧つけようかな…」）。
 * サブストーリーのフラグ（`side_<key>_accepted` / `_step<n>` / `_done`）から、メニューに出す一覧を作る。
 *  - 受けている依頼: 依頼人・場所・すすみ具合（調べた所の数）・手がかり（依頼人の言葉）・次に行く場所。調べ終わったら「報告できる」
 *  - 受けられる依頼（まだ受けていないもの）: 依頼人と場所だけ
 *  - 終わった依頼: 題名だけ
 */
export type QuestStatus = "progress" | "report" | "available" | "done";

export interface QuestEntry {
  id: string;
  title: string;
  status: QuestStatus;
  giver: string;
  /** 依頼人のいる場所。 */
  place: string;
  stepsDone: number;
  stepsTotal: number;
  /** 依頼人の言葉（手がかり）。受けている依頼だけ。 */
  hint?: string;
  /** 次に調べに行く場所。受けている依頼だけ。 */
  next?: string;
}

function firstSpeaker(commands: EventCommand[]): string | undefined {
  for (const c of commands) if (c.type === "message" && c.speaker) return c.speaker;
  return undefined;
}

function firstText(commands: EventCommand[]): string | undefined {
  for (const c of commands) if (c.type === "message") return c.text;
  return undefined;
}

const ORDER: Record<QuestStatus, number> = { report: 0, progress: 1, available: 2, done: 3 };

export function sideQuestLog(stories: SideStory[], flags: Record<string, boolean | undefined>): QuestEntry[] {
  const out: QuestEntry[] = [];
  for (const story of stories) {
    const f = (name: string): boolean => flags[`side_${story.key}_${name}`] === true;
    const unlocked = story.unlockFlags.every((u) => flags[u] === true);
    const doneSteps = story.steps.filter((_, i) => f(`step${i + 1}`)).length;
    const status: QuestStatus | null = f("done") ? "done" : f("accepted") ? (doneSteps >= story.steps.length ? "report" : "progress") : unlocked ? "available" : null;
    if (!status) continue;
    const nextStep = story.steps.find((_, i) => !f(`step${i + 1}`));
    out.push({
      id: story.id,
      title: story.title,
      status,
      giver: firstSpeaker(story.offer) ?? firstSpeaker(story.locked) ?? "依頼人",
      place: placeName(story.giver.mapId),
      stepsDone: doneSteps,
      stepsTotal: story.steps.length,
      ...(status === "progress" ? { hint: firstText(story.hint), next: nextStep ? placeName(nextStep.mapId) : undefined } : {}),
    });
  }
  return out.sort((a, b) => ORDER[a.status] - ORDER[b.status] || a.id.localeCompare(b.id));
}
