import { describe, expect, it } from "vitest";
import { BgmDirector, BGM_DEFAULTS, DUCK_PRESETS, beatsPerBarOf, dbToLinear, phaseIndexForHp, planBossPhases, secondsToNextBar, type BgmEngineLike, type Timers } from "./bgm-director";
import type { Score } from "./score";

class Clock implements Timers {
  now = 0;
  private q: { at: number; fn: () => void; id: number }[] = [];
  private n = 0;
  setTimeout(fn: () => void, ms: number): unknown { const id = ++this.n; this.q.push({ at: this.now + ms / 1000, fn, id }); return id; }
  clearTimeout(h: unknown): void { this.q = this.q.filter((x) => x.id !== h); }
  advance(sec: number): void {
    const end = this.now + sec;
    for (;;) {
      this.q.sort((a, b) => a.at - b.at || a.id - b.id);
      const next = this.q[0];
      if (!next || next.at > end + 1e-9) break;
      this.q.shift();
      this.now = Math.max(this.now, next.at);
      next.fn();
    }
    this.now = end;
  }
  get pending(): number { return this.q.length; }
}

class FakeEngine implements BgmEngineLike {
  log: string[] = [];
  fade: { t: number; level: number; sec: number }[] = [];
  duck: { t: number; level: number; sec: number }[] = [];
  playing: Score | null = null;
  private startAt = 0;
  private startOffset = 0;
  constructor(private clock: Clock) {}
  playBgm(score: Score, offsetSec = 0): void { this.log.push(`play:${score.tempoBpm}@${offsetSec.toFixed(2)}`); this.playing = score; this.startAt = this.clock.now; this.startOffset = offsetSec; }
  stopBgm(): void { this.log.push("stop"); this.playing = null; }
  getBgmPositionSec(): number {
    if (!this.playing) return 0;
    const dur = this.playing.tracks[0].notes.reduce((a, n) => a + n.durationBeats, 0) * (60 / this.playing.tempoBpm);
    return (this.startOffset + (this.clock.now - this.startAt)) % dur;
  }
  seekBgm(sec: number): void { this.log.push(`seek:${sec.toFixed(2)}`); this.startAt = this.clock.now; this.startOffset = sec; }
  rampBgmFade(level: number, seconds: number): void { this.fade.push({ t: this.clock.now, level, sec: seconds }); }
  rampBgmDuck(level: number, seconds: number): void { this.duck.push({ t: this.clock.now, level, sec: seconds }); }
}

/** bpm 120・4/4 なら 1小節 2秒。bars 小節ぶんの曲。 */
const song = (bars: number, bpm = 120, meta?: Score["meta"]): Score => ({
  tempoBpm: bpm, loop: true, ...(meta ? { meta } : {}),
  tracks: [{ waveform: "sine", instrument: "lead", volume: 0.2, notes: [{ note: "C4", durationBeats: bars * 4 }] }],
});
const setup = () => { const clock = new Clock(); const eng = new FakeEngine(clock); return { clock, eng, dir: new BgmDirector(eng, { timers: clock }) }; };

describe("計算の部品", () => {
  it("dB → 倍率、次の小節の頭までの秒数", () => {
    expect(dbToLinear(0)).toBe(1);
    expect(dbToLinear(-6)).toBeCloseTo(0.501, 2);
    expect(secondsToNextBar(0, 120, 4)).toBe(0);
    expect(secondsToNextBar(2, 120, 4)).toBe(0);
    expect(secondsToNextBar(2.5, 120, 4)).toBeCloseTo(1.5);
    expect(secondsToNextBar(1.999999, 120, 4)).toBe(0);
  });
  it("標準の値はガイドどおり（会話 −5dB・0.3秒／0.5秒、効果音 −3dB・0.5秒）", () => {
    expect(DUCK_PRESETS.dialogue).toMatchObject({ db: -5, attackSec: 0.3, releaseSec: 0.5 });
    expect(DUCK_PRESETS.sfx.db).toBe(-3);
    expect(DUCK_PRESETS.sfx.attackSec + DUCK_PRESETS.sfx.holdSec).toBeCloseTo(0.45);
    expect(BGM_DEFAULTS.battleFadeOutSec).toBe(0.3);
  });
  it("拍子は meta・timeSig・既定の4", () => {
    expect(beatsPerBarOf(song(4))).toBe(4);
    expect(beatsPerBarOf({ ...song(4), timeSig: { num: 7, den: 4 } })).toBe(7);
    expect(beatsPerBarOf({ ...song(4), meta: { beatsPerBar: 6 } })).toBe(6);
  });
});

describe("曲の切り替えにフェード", () => {
  it("最初の曲は、小さい音から上げる", () => {
    const { dir, eng } = setup();
    dir.changeBgm(song(8), { id: "a" });
    expect(eng.log).toEqual(["stop", "play:120@0.00"]);
    expect(eng.fade).toEqual([{ t: 0, level: 0, sec: 0 }, { t: 0, level: 1, sec: BGM_DEFAULTS.fadeInSec }]);
  });

  it("2曲目: 前の曲を下げ、下がり切ってから止めて、次を小さい音から上げる", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8), { id: "a" });
    eng.log.length = 0; eng.fade.length = 0;
    clock.advance(5);
    dir.changeBgm(song(8, 100), { id: "b", fadeOutSec: 0.5, fadeInSec: 0.7 });
    expect(eng.fade).toEqual([{ t: 5, level: 0, sec: 0.5 }]);
    expect(eng.log).toEqual([]); // まだ止めない
    clock.advance(0.4);
    expect(eng.log).toEqual([]);
    clock.advance(0.2);
    expect(eng.log).toEqual(["stop", "play:100@0.00"]);
    expect(eng.fade.slice(-2)).toEqual([{ t: expect.closeTo(5.52, 2), level: 0, sec: 0 }, { t: expect.closeTo(5.52, 2), level: 1, sec: 0.7 }]);
    expect(dir.getState().id).toBe("b");
  });

  it("同じIDの曲は鳴らし直さない（force なら鳴らし直す）", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8), { id: "a" });
    clock.advance(1);
    eng.log.length = 0;
    dir.changeBgm(song(8), { id: "a" });
    clock.advance(2);
    expect(eng.log).toEqual([]);
    dir.changeBgm(song(8), { id: "a", force: true });
    clock.advance(2);
    expect(eng.log).toEqual(["stop", "play:120@0.00"]);
  });

  it("切り替え中にもう一度呼ぶと、最後の指定だけが鳴る", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8), { id: "a" });
    clock.advance(1);
    dir.changeBgm(song(8, 90), { id: "b" });
    clock.advance(0.2);
    dir.changeBgm(song(8, 150), { id: "c" });
    clock.advance(3);
    expect(eng.log.filter((l) => l.startsWith("play"))).toEqual(["play:120@0.00", "play:150@0.00"]);
    expect(dir.getState().id).toBe("c");
  });

  it("alignToBar: 次の小節の頭まで待ってから下げ始める（遠すぎれば待たない）", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8), { id: "a" });
    clock.advance(0.5); // 小節の途中（2秒で1小節）→ 次の頭まで1.5秒
    eng.fade.length = 0;
    dir.changeBgm(song(8, 100), { id: "b", alignToBar: true, fadeOutSec: 0.3 });
    expect(eng.fade).toEqual([]);
    clock.advance(1.49);
    expect(eng.fade).toEqual([]);
    clock.advance(0.02);
    expect(eng.fade[0]).toMatchObject({ level: 0, sec: 0.3 });
    // 遠いとき（0.3秒進めると 1.7秒待ち → 上限 1.5 を超える）
    const t2 = setup();
    t2.dir.changeBgm(song(8), { id: "a" });
    t2.clock.advance(0.3);
    t2.eng.fade.length = 0;
    t2.dir.changeBgm(song(8, 100), { id: "b", alignToBar: true });
    expect(t2.eng.fade[0]).toMatchObject({ level: 0 });
  });

  it("stop はフェードアウトしてから止め、音量を戻す", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8), { id: "a" });
    clock.advance(1);
    eng.fade.length = 0;
    dir.stop(0.5);
    expect(eng.fade).toEqual([{ t: 1, level: 0, sec: 0.5 }]);
    clock.advance(0.6);
    expect(eng.log.at(-1)).toBe("stop");
    expect(eng.fade.at(-1)).toMatchObject({ level: 1, sec: 0 });
    expect(dir.getState().playing).toBe(false);
  });
});

describe("戦闘への切り替えと再開", () => {
  it("遭遇の一撃 → フィールド曲を0.3秒で下げる → 戦闘曲を頭から", () => {
    const { dir, eng, clock } = setup();
    const order: string[] = [];
    dir.changeBgm(song(16), { id: "field" });
    clock.advance(10);
    eng.fade.length = 0; eng.log.length = 0;
    dir.enterBattle(song(8, 180), { id: "battle", stinger: () => order.push("stinger") });
    expect(order).toEqual(["stinger"]);
    expect(eng.fade[0]).toEqual({ t: 10, level: 0, sec: BGM_DEFAULTS.battleFadeOutSec });
    clock.advance(0.4);
    expect(eng.log).toEqual(["stop", "play:180@0.00"]);
    expect(eng.fade.at(-1)).toMatchObject({ level: 1, sec: BGM_DEFAULTS.battleFadeInSec });
    expect(dir.getState()).toMatchObject({ battleActive: true, id: "battle" });
    expect(dir.getState().fieldMemory?.positionSec).toBeCloseTo(10);
  });

  it("戦闘後はフィールド曲の同じ位置から再開する", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16), { id: "field" }); // 32秒の曲
    clock.advance(10);
    dir.enterBattle(song(8, 180), { id: "battle" });
    clock.advance(20);
    eng.log.length = 0;
    dir.leaveBattle();
    clock.advance(1);
    expect(eng.log).toEqual(["stop", "play:120@10.00"]);
    expect(dir.getState()).toMatchObject({ battleActive: false, id: "field", fieldMemory: null });
  });

  it("rewindSec で少し戻す（頭を越えたら曲の長さで回り込む）／head で頭から", () => {
    const a = setup();
    a.dir.changeBgm(song(16), { id: "field" });
    a.clock.advance(1);
    a.dir.enterBattle(song(8, 180), { id: "b" });
    a.clock.advance(5); a.eng.log.length = 0;
    a.dir.leaveBattle({ rewindSec: 3 });
    a.clock.advance(1);
    expect(a.eng.log).toEqual(["stop", "play:120@30.00"]);
    const b = setup();
    b.dir.changeBgm(song(16), { id: "field" });
    b.clock.advance(7);
    b.dir.enterBattle(song(8, 180), { id: "b" });
    b.clock.advance(5); b.eng.log.length = 0;
    b.dir.leaveBattle({ resume: "head" });
    b.clock.advance(1);
    expect(b.eng.log).toEqual(["stop", "play:120@0.00"]);
  });

  it("戦闘が連続しても、最初のフィールド位置を覚えたまま", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16), { id: "field" });
    clock.advance(8);
    dir.enterBattle(song(8, 180), { id: "b1" });
    clock.advance(3);
    dir.enterBattle(song(8, 170), { id: "b2" });
    clock.advance(3);
    eng.log.length = 0;
    dir.leaveBattle();
    clock.advance(1);
    expect(eng.log).toEqual(["stop", "play:120@8.00"]);
  });

  it("next を渡すと、フィールドの代わりにその曲（勝利のファンファーレなど）", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16), { id: "field" });
    clock.advance(2);
    dir.enterBattle(song(8, 180), { id: "b" });
    clock.advance(5); eng.log.length = 0;
    dir.leaveBattle({ next: { score: song(2, 140), id: "victory" } });
    clock.advance(1);
    expect(eng.log).toEqual(["stop", "play:140@0.00"]);
    expect(dir.getState().fieldMemory).toBeNull();
  });

  it("フィールド曲を覚えていなければ、フェードして止める", () => {
    const { dir, eng, clock } = setup();
    dir.enterBattle(song(8, 180), { id: "b" });
    clock.advance(2);
    dir.leaveBattle();
    clock.advance(1);
    expect(eng.log.at(-1)).toBe("stop");
    expect(dir.getState().playing).toBe(false);
  });
});

describe("ダッキング", () => {
  it("会話を開くと −5dB・0.3秒、閉じると 0.5秒で戻す", () => {
    const { dir, eng } = setup();
    dir.dialogOpen();
    expect(eng.duck[0].level).toBeCloseTo(dbToLinear(-5));
    expect(eng.duck[0].sec).toBe(0.3);
    expect(dir.getState().ducked).toBe(true);
    dir.dialogClose();
    expect(eng.duck[1]).toMatchObject({ level: 1, sec: 0.5 });
    expect(dir.getState().ducked).toBe(false);
  });

  it("重なったときは深いほうに合わせ、全部閉じたら戻る", () => {
    const { dir, eng } = setup();
    dir.beginDuck("a", -4); dir.beginDuck("b", -9);
    expect(eng.duck.at(-1)!.level).toBeCloseTo(dbToLinear(-9));
    dir.endDuck("b");
    expect(eng.duck.at(-1)!.level).toBeCloseTo(dbToLinear(-4));
    dir.endDuck("a");
    expect(eng.duck.at(-1)!.level).toBe(1);
    const n = eng.duck.length;
    dir.endDuck("none"); // 開いていないものを閉じても何も起きない
    expect(eng.duck.length).toBe(n);
  });

  it("duckPulse: 効果音の一瞬だけ −3dB で、自動で戻る", () => {
    const { dir, eng, clock } = setup();
    dir.duckPulse("sfx");
    expect(eng.duck[0].level).toBeCloseTo(dbToLinear(-3));
    clock.advance(0.4);
    expect(eng.duck).toHaveLength(1);
    clock.advance(0.1);
    expect(eng.duck[1]).toMatchObject({ level: 1, sec: 0.5 });
    dir.duckPulse("fanfare");
    expect(eng.duck.at(-1)!.level).toBeCloseTo(dbToLinear(-8));
    clock.advance(2.2);
    expect(eng.duck.at(-1)!.level).toBe(1);
  });

  it("会話中に効果音の一瞬があっても、会話が閉じるまで下がったまま", () => {
    const { dir, eng, clock } = setup();
    dir.dialogOpen();
    dir.duckPulse("sfx");
    clock.advance(1);
    expect(eng.duck.at(-1)!.level).toBeCloseTo(dbToLinear(-5));
    dir.dialogClose();
    expect(eng.duck.at(-1)!.level).toBe(1);
  });

  it("曲の切り替えのフェードとは別の音量を動かす", () => {
    const { dir, eng } = setup();
    dir.changeBgm(song(8), { id: "a" });
    dir.dialogOpen();
    expect(eng.fade.every((f) => f.level === 0 || f.level === 1)).toBe(true);
    expect(eng.duck).toHaveLength(1);
  });
});

describe("ループ点（導入を1回だけ）", () => {
  const loopMeta = (startBar: number, endBar: number, bpm = 120, bpb = 4): NonNullable<Score["meta"]> => ({ beatsPerBar: bpb, loop: { startBar, endBar, startSec: ((startBar - 1) * bpb * 60) / bpm, endSec: (endBar * bpb * 60) / bpm } });

  it("5〜12小節（8〜24秒）をくり返す。導入の8秒は最初の1回だけ", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16, 120, loopMeta(5, 12)), { id: "a" }); // 全体は32秒
    clock.advance(23.9);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
    clock.advance(0.2);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual(["seek:8.00"]);
    clock.advance(16);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual(["seek:8.00", "seek:8.00"]);
  });

  it("曲全体のループ（meta.loop が全体）はエンジンに任せる", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(8, 120, loopMeta(1, 8)), { id: "a" });
    clock.advance(60);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
    expect(clock.pending).toBe(0);
  });

  it("tick: 位置が範囲を外れていたら始まりへ戻す", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16, 120, loopMeta(5, 12)), { id: "a" });
    clock.advance(1);
    // 導入の途中は範囲の前なので戻さない
    dir.tick();
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
  });

  it("曲を替えたら前の曲のループ予約は消える", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16, 120, loopMeta(5, 12)), { id: "a" });
    clock.advance(1);
    dir.changeBgm(song(16), { id: "b" });
    clock.advance(60);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
  });
});

describe("ボス戦の段階表", () => {
  // bpm 120 → 1小節2秒。48小節（96秒）。段階: 1〜16（0〜32秒）・17〜32（32〜64秒）・33〜48（64〜96秒）
  const phases = [{ id: "p1", startBar: 1, endBar: 16, hpBelow: 1 }, { id: "p2", startBar: 17, endBar: 32, hpBelow: 0.6 }, { id: "p3", startBar: 33, endBar: 48, hpBelow: 0.3 }];
  const boss = (): Score => song(48, 120, { bossPhases: phases });

  it("段階表を秒にする／HPから段階を選ぶ", () => {
    const plan = planBossPhases(boss())!;
    expect(plan.barSec).toBe(2);
    expect(plan.phases.map((p) => [p.startSec, p.endSec])).toEqual([[0, 32], [32, 64], [64, 96]]);
    expect(planBossPhases(song(8))).toBeNull();
    expect([1, 0.7, 0.6, 0.59, 0.3, 0.29, 0].map((hp) => phaseIndexForHp(plan, hp))).toEqual([0, 0, 0, 1, 1, 2, 2]);
  });

  it("第1段階のループ（0〜32秒）をくり返す", () => {
    const { dir, eng, clock } = setup();
    dir.startBoss(boss(), { id: "boss" });
    expect(dir.getState()).toMatchObject({ battleActive: true, bossPhase: 0 });
    clock.advance(33);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual(["seek:0.00"]);
  });

  it("HPが閾値を下回ると、次の小節の頭で第2段階の頭へ移る", () => {
    const { dir, eng, clock } = setup();
    dir.startBoss(boss(), { id: "boss" });
    clock.advance(10.5); // 小節の途中（次の頭は 12秒）
    eng.log.length = 0; eng.fade.length = 0;
    dir.setBossHp(0.55);
    clock.advance(1.4);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
    clock.advance(0.2);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual(["seek:32.00"]);
    expect(dir.getState().bossPhase).toBe(1);
    // 切り替えの頭で、ごく短く音量を落として戻す
    expect(eng.fade[0]).toMatchObject({ level: 0, sec: BGM_DEFAULTS.phaseDipSec });
    expect(eng.fade.at(-1)).toMatchObject({ level: 1 });
    // 第2段階のループは 32〜64秒
    clock.advance(33);
    expect(eng.log.filter((l) => l.startsWith("seek"))).toEqual(["seek:32.00", "seek:32.00"]);
  });

  it("待っているあいだにさらにHPが減ったら、最新の段階へ飛ぶ。HPが戻っても後戻りしない", () => {
    const { dir, eng, clock } = setup();
    dir.startBoss(boss(), { id: "boss" });
    clock.advance(10.5);
    dir.setBossHp(0.55);
    clock.advance(0.5);
    dir.setBossHp(0.2);
    clock.advance(2);
    expect(dir.getState().bossPhase).toBe(2);
    expect(eng.log.filter((l) => l.startsWith("seek")).at(-1)).toBe("seek:64.00");
    dir.setBossHp(0.9); // 回復
    clock.advance(5);
    expect(dir.getState().bossPhase).toBe(2);
  });

  it("allowBack なら回復で前の段階へ戻れる", () => {
    const { dir, clock } = setup();
    dir.startBoss(boss(), { id: "boss", allowBack: true });
    clock.advance(1);
    dir.setBossHp(0.2);
    clock.advance(3);
    expect(dir.getState().bossPhase).toBe(2);
    dir.setBossHp(0.9);
    clock.advance(3);
    expect(dir.getState().bossPhase).toBe(0);
  });

  it("段階表のない曲では setBossHp は何もしない／戦闘が終わると段階は解除", () => {
    const a = setup();
    a.dir.startBoss(song(8), { id: "x" });
    a.dir.setBossHp(0.1);
    a.clock.advance(5);
    expect(a.eng.log.filter((l) => l.startsWith("seek"))).toEqual([]);
    expect(a.dir.getState().bossPhase).toBeNull();
    const b = setup();
    b.dir.startBoss(boss(), { id: "boss" });
    b.clock.advance(1);
    b.dir.leaveBattle();
    expect(b.dir.getState().bossPhase).toBeNull();
  });

  it("ボス戦の前のフィールド曲の位置を覚えていて、戻れる", () => {
    const { dir, eng, clock } = setup();
    dir.changeBgm(song(16), { id: "field" });
    clock.advance(6);
    dir.startBoss(boss(), { id: "boss" });
    clock.advance(40);
    eng.log.length = 0;
    dir.leaveBattle();
    clock.advance(1);
    expect(eng.log).toEqual(["stop", "play:120@6.00"]);
  });
});
