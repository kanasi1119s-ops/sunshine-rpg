import { describe, expect, it } from "vitest";
import { attachAudioLifecycle, unlockAudio, waitUntilReady, type CtxLike, type DocLike } from "./audio-lifecycle";

class FakeCtx implements CtxLike {
  state = "suspended";
  calls: string[] = [];
  private listeners: (() => void)[] = [];
  resumeFails = false;
  async resume(): Promise<void> { this.calls.push("resume"); if (this.resumeFails) throw new Error("no gesture"); this.set("running"); }
  async suspend(): Promise<void> { this.calls.push("suspend"); this.set("suspended"); }
  addEventListener(_t: "statechange", fn: () => void): void { this.listeners.push(fn); }
  removeEventListener(_t: "statechange", fn: () => void): void { this.listeners = this.listeners.filter((f) => f !== fn); }
  set(s: string): void { this.state = s; this.listeners.forEach((f) => f()); }
  get listenerCount(): number { return this.listeners.length; }
}
class FakeDoc implements DocLike {
  hidden = false;
  private map = new Map<string, (() => void)[]>();
  addEventListener(t: string, fn: () => void): void { this.map.set(t, [...(this.map.get(t) ?? []), fn]); }
  removeEventListener(t: string, fn: () => void): void { this.map.set(t, (this.map.get(t) ?? []).filter((f) => f !== fn)); }
  emit(t: string): void { (this.map.get(t) ?? []).forEach((f) => f()); }
  count(): number { return [...this.map.values()].reduce((a, l) => a + l.length, 0); }
}
const tick = (): Promise<void> => new Promise((r) => setTimeout(r, 0));

describe("unlockAudio", () => {
  it("止まっていれば resume して true", async () => {
    const c = new FakeCtx();
    expect(await unlockAudio(c)).toBe(true);
    expect(c.calls).toEqual(["resume"]);
  });
  it("すでに鳴っていれば何もしない／resume が失敗したら false", async () => {
    const c = new FakeCtx(); c.state = "running";
    expect(await unlockAudio(c)).toBe(true);
    expect(c.calls).toEqual([]);
    const d = new FakeCtx(); d.resumeFails = true;
    expect(await unlockAudio(d)).toBe(false);
  });
});

describe("attachAudioLifecycle", () => {
  it("隠れたら suspend、戻ったら resume", async () => {
    const doc = new FakeDoc(), ctx = new FakeCtx(); ctx.state = "running";
    attachAudioLifecycle(doc, ctx);
    doc.hidden = true; doc.emit("visibilitychange"); await tick();
    expect(ctx.calls).toEqual(["suspend"]);
    doc.hidden = false; doc.emit("visibilitychange"); await tick();
    expect(ctx.calls).toEqual(["suspend", "resume"]);
    expect(ctx.state).toBe("running");
  });

  it("最初から鳴っていないときは、隠れても suspend しない", async () => {
    const doc = new FakeDoc(), ctx = new FakeCtx();
    attachAudioLifecycle(doc, ctx);
    doc.hidden = true; doc.emit("visibilitychange"); await tick();
    expect(ctx.calls).toEqual([]);
  });

  it("keepPlayingInBackground なら suspend しない", async () => {
    const doc = new FakeDoc(), ctx = new FakeCtx(); ctx.state = "running";
    attachAudioLifecycle(doc, ctx, { keepPlayingInBackground: true });
    doc.hidden = true; doc.emit("visibilitychange"); await tick();
    expect(ctx.calls).toEqual([]);
  });

  it("電話などで止められたあと、次の操作で再開する", async () => {
    const doc = new FakeDoc(), ctx = new FakeCtx(); ctx.state = "running";
    const states: string[] = [];
    attachAudioLifecycle(doc, ctx, { onState: (s) => states.push(s) });
    ctx.set("interrupted");
    expect(states).toEqual(["interrupted"]);
    doc.emit("touchend"); await tick();
    expect(ctx.calls).toEqual(["resume"]);
    expect(ctx.state).toBe("running");
    doc.emit("keydown"); await tick();
    expect(ctx.calls).toEqual(["resume"]); // 鳴っているので何もしない
  });

  it("戻ったとき resume が拒否されたら、次の操作でもう一度", async () => {
    const doc = new FakeDoc(), ctx = new FakeCtx(); ctx.state = "running";
    attachAudioLifecycle(doc, ctx);
    doc.hidden = true; doc.emit("visibilitychange"); await tick();
    ctx.resumeFails = true;
    doc.hidden = false; doc.emit("visibilitychange"); await tick();
    expect(ctx.state).toBe("suspended");
    ctx.resumeFails = false;
    doc.emit("pointerdown"); await tick();
    expect(ctx.state).toBe("running");
  });

  it("外すと、すべてのつなぎがなくなる", () => {
    const doc = new FakeDoc(), ctx = new FakeCtx();
    const detach = attachAudioLifecycle(doc, ctx);
    expect(doc.count()).toBeGreaterThan(0);
    expect(ctx.listenerCount).toBe(1);
    detach();
    expect(doc.count()).toBe(0);
    expect(ctx.listenerCount).toBe(0);
  });
});

describe("waitUntilReady", () => {
  it("準備ができたら true、できなければタイムアウトで false", async () => {
    let n = 0;
    const ticks: number[] = [];
    expect(await waitUntilReady(() => ++n >= 3, { pollMs: 1, onTick: (w) => ticks.push(w) })).toBe(true);
    expect(ticks.length).toBe(2);
    expect(await waitUntilReady(() => false, { pollMs: 1, timeoutMs: 5 })).toBe(false);
  });
});
