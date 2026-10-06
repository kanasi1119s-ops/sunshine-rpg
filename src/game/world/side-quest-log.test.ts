import { describe, expect, it } from "vitest";
import { SIDE_STORIES } from "./side-stories";
import { sideQuestLog } from "./side-quest-log";

describe("依頼の記録", () => {
  const s001 = SIDE_STORIES.find((s) => s.id === "S-001")!;
  it("受けていない・解放前の依頼は出ない。解放されると「受けられる」", () => {
    expect(sideQuestLog([s001], {})).toEqual([]);
    const log = sideQuestLog([s001], Object.fromEntries(s001.unlockFlags.map((f) => [f, true])));
    expect(log[0].status).toBe("available");
    expect(log[0].giver).toBe("タケ");
    expect(log[0].place).toBe("灯里");
  });
  it("受けると、すすみ具合・手がかり・次の場所が出る。調べ終わると「報告できる」、報告すると「終わった」", () => {
    const base = { ...Object.fromEntries(s001.unlockFlags.map((f) => [f, true])), side_s001_accepted: true };
    let e = sideQuestLog([s001], base)[0];
    expect(e.status).toBe("progress");
    expect(e.stepsDone).toBe(0);
    expect(e.stepsTotal).toBe(s001.steps.length);
    expect(e.hint).toContain("ルル");
    expect(e.next).toBe("灯里");
    const all = { ...base, ...Object.fromEntries(s001.steps.map((_, i) => [`side_s001_step${i + 1}`, true])) };
    expect(sideQuestLog([s001], all)[0].status).toBe("report");
    e = sideQuestLog([s001], { ...all, side_s001_done: true })[0];
    expect(e.status).toBe("done");
  });
  it("報告できる→受けている→受けられる→終わった、の順に並ぶ", () => {
    const flags: Record<string, boolean> = {};
    // ほかの依頼が終わっていることを条件にする依頼もあるので、依頼の終わりのフラグは立てない
    for (const s of SIDE_STORIES) for (const u of s.unlockFlags) if (!u.startsWith("side_")) flags[u] = true;
    const [a, b, c] = SIDE_STORIES.filter((s) => s.steps.length > 0 && s.unlockFlags.every((u) => !u.startsWith("side_")));
    Object.assign(flags, { [`side_${a.key}_accepted`]: true, [`side_${b.key}_accepted`]: true, [`side_${c.key}_done`]: true });
    b.steps.forEach((_, i) => { flags[`side_${b.key}_step${i + 1}`] = true; });
    const order = { report: 0, progress: 1, available: 2, done: 3 } as const;
    const log = sideQuestLog(SIDE_STORIES, flags);
    expect(log.map((e) => order[e.status])).toEqual([...log.map((e) => order[e.status])].sort((x, y) => x - y));
    expect(log.find((e) => e.id === b.id)?.status).toBe("report");
    expect(log.find((e) => e.id === a.id)?.status).toBe("progress");
  });
});
