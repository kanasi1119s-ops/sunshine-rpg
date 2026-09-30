import { describe, expect, it } from "vitest";
import { INITIAL_JOBS } from "./jobs";
import { cancelJobMenu, confirmJobMenu, createJobMenuState, moveJobMenu, openJobMenu } from "./job-menu";

describe("ジョブ画面の操作", () => {
  it("閉じているあいだは何も起きない", () => {
    const s = createJobMenuState();
    expect(moveJobMenu(s, 1, 3)).toBe(s);
    expect(confirmJobMenu(s).state).toBe(s);
    expect(cancelJobMenu(s)).toBe(s);
  });

  it("仲間を選ぶ→ジョブを選ぶ、で選ばれたジョブが返る", () => {
    let s = openJobMenu();
    s = moveJobMenu(s, 1, 3);
    expect(s.memberCursor).toBe(1);
    s = confirmJobMenu(s).state;
    expect(s.stage).toBe("job");
    s = moveJobMenu(s, 2, 3);
    const r = confirmJobMenu(s);
    expect(r.chosen).toBe(INITIAL_JOBS[2].id);
    expect(r.state.stage).toBe("member");
    expect(r.state.memberCursor).toBe(1);
  });

  it("カーソルは端で反対側に回る", () => {
    let s = openJobMenu();
    s = moveJobMenu(s, -1, 4);
    expect(s.memberCursor).toBe(3);
    s = confirmJobMenu(s).state;
    s = moveJobMenu(s, -1, 4);
    expect(s.jobCursor).toBe(INITIAL_JOBS.length - 1);
  });

  it("キャンセルは、ジョブ選択→仲間選択→閉じる の順に戻る", () => {
    let s = confirmJobMenu(openJobMenu()).state;
    s = cancelJobMenu(s);
    expect(s.open).toBe(true);
    expect(s.stage).toBe("member");
    expect(cancelJobMenu(s).open).toBe(false);
  });
});
