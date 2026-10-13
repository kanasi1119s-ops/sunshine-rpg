import { describe, expect, it } from "vitest";
import { analyzeChannels, BAND_IDS, BANDS, diagnoseMasking, familyBands, fftInPlace, MUD_COL, spectralTilt, WIN_COLS, type MaskStem } from "./auto-mix";
import { measureLufs } from "./loudness";
import { applyPlan, assignRoles, levelTargets, masterAdvice, planMix, type AiPartLike, type MixTargetsFile, type Unit } from "./auto-mix-plan";
import { GROUP_TARGETS, MASTER_FAMILIES, ROLE_SPECS } from "./auto-mix-targets";
import { describeDiff, formatReport, type ReportData } from "./auto-mix-report";

const SR = 22050;
const tone = (hz: number, amp: number, sec: number, pan = 0, sr = SR): [Float32Array, Float32Array] => {
  const n = Math.round(sec * sr);
  const l = new Float32Array(n), r = new Float32Array(n);
  const gl = Math.cos(((pan + 1) * Math.PI) / 4), gr = Math.sin(((pan + 1) * Math.PI) / 4);
  for (let i = 0; i < n; i++) { const v = amp * Math.sin((2 * Math.PI * hz * i) / sr); l[i] = v * gl; r[i] = v * gr; }
  return [l, r];
};
const noise = (amp: number, sec: number, seed = 1): [Float32Array, Float32Array] => {
  const n = Math.round(sec * SR);
  const l = new Float32Array(n), r = new Float32Array(n);
  let s = seed;
  for (let i = 0; i < n; i++) { s = (s * 1664525 + 1013904223) >>> 0; l[i] = amp * (s / 2147483648 - 1); s = (s * 1664525 + 1013904223) >>> 0; r[i] = amp * (s / 2147483648 - 1); }
  return [l, r];
};

describe("fftInPlace", () => {
  it("複素 FFT: 左=サイン波・右=0 を入れると、そのビンにだけ山が立つ", () => {
    const N = 64, re = new Float64Array(N), im = new Float64Array(N);
    for (let i = 0; i < N; i++) re[i] = Math.sin((2 * Math.PI * 4 * i) / N);
    fftInPlace(re, im);
    const mag = Array.from({ length: N }, (_, k) => Math.hypot(re[k], im[k]));
    expect(mag[4]).toBeCloseTo(N / 2, 3);
    expect(mag[7]).toBeLessThan(1e-9);
  });
});

describe("analyzeChannels（パート別の数値化）", () => {
  it("1kHz・振幅 0.5 の両ch同じサイン波: ピーク -6dB、LUFS は loudness.ts と一致、相関 1、重心 約1kHz、Mid 帯域に集まる", () => {
    const [l, r] = tone(1000, 0.5, 4);
    const a = analyzeChannels(l, r, SR);
    expect(a.samplePeakDb).toBeCloseTo(-9, 0); // tone() の pan=0 は左右とも 0.707 倍（-3dB）
    expect(a.lufsIntegrated).toBeCloseTo(measureLufs([l, r], SR), 0);
    expect(a.stereo.corr).toBeGreaterThan(0.99);
    expect(a.centroidHz).toBeGreaterThan(900);
    expect(a.centroidHz).toBeLessThan(1100);
    expect(a.bandShareDb.mid).toBeGreaterThan(-0.5);
    expect(a.bandShareDb.bass).toBeLessThan(-30);
    // サイン波のクレストは 3dB（ピーク − RMS）
    expect(a.crestDb).toBeGreaterThan(2.5);
    expect(a.crestDb).toBeLessThan(3.6);
  });
  it("帯域の振り分け: 40Hz=Sub、90Hz=Bass、180Hz=Low-mid、350Hz=Mud、1kHz=Mid、3kHz=Presence、8kHz=Air", () => {
    const cases: [number, string][] = [[40, "sub"], [90, "bass"], [180, "lowmid"], [350, "mud"], [1000, "mid"], [3000, "presence"], [8000, "air"]];
    for (const [hz, band] of cases) {
      const [l, r] = tone(hz, 0.3, 3);
      const a = analyzeChannels(l, r, SR);
      const best = BAND_IDS.reduce((m, b) => (a.bandShareDb[b] > a.bandShareDb[m] ? b : m), BAND_IDS[0]);
      expect(best, `${hz}Hz`).toBe(band);
    }
  });
  it("200-500Hz（濁り）の割合: 300Hz の音は約 0dB、1kHz の音は大きく負", () => {
    expect(analyzeChannels(...tone(300, 0.3, 3), SR).mudShareDb).toBeGreaterThan(-1);
    expect(analyzeChannels(...tone(1000, 0.3, 3), SR).mudShareDb).toBeLessThan(-25);
  });
  it("ステレオ: 逆相は相関 -1、片側だけなら左右バランスが大きくずれ、モノなら幅が小さい", () => {
    const [l, r] = tone(500, 0.4, 3);
    const inv = analyzeChannels(l, r.map((v) => -v), SR);
    expect(inv.stereo.corr).toBeLessThan(-0.99);
    expect(inv.stereo.widthDb).toBeGreaterThan(20);
    const left = analyzeChannels(...tone(500, 0.4, 3, -1), SR);
    expect(left.stereo.balanceDb).toBeLessThan(-20);
    const mono = analyzeChannels(l, new Float32Array(l), SR);
    expect(mono.stereo.widthDb).toBeLessThan(-40);
  });
  it("150Hz 以下の相関: 低い逆相の音は lowCorr が負、低い同相の音は 1 に近い", () => {
    const [l, r] = tone(80, 0.4, 3);
    expect(analyzeChannels(l, new Float32Array(l), SR).stereo.lowCorr).toBeGreaterThan(0.99);
    expect(analyzeChannels(l, r.map((v) => -v), SR).stereo.lowCorr).toBeLessThan(-0.99);
  });
  it("時間窓: 前半 100Hz・後半 3kHz の音は、窓ごとの帯域の強さが入れ替わる", () => {
    const [a1, b1] = tone(100, 0.4, 2), [a2, b2] = tone(3000, 0.4, 2);
    const l = new Float32Array([...a1, ...a2]), r = new Float32Array([...b1, ...b2]);
    const a = analyzeChannels(l, r, SR, { windowSec: 0.5 });
    expect(a.windows!.length).toBe(8);
    expect(a.windows![0].length).toBe(WIN_COLS);
    const bass = BAND_IDS.indexOf("bass"), pres = BAND_IDS.indexOf("presence");
    expect(a.windows![1][bass]).toBeGreaterThan(a.windows![1][pres] + 30);
    expect(a.windows![6][pres]).toBeGreaterThan(a.windows![6][bass] + 30);
  });
  it("鳴っている割合: 半分が無音なら約 0.5", () => {
    const [a1, b1] = tone(500, 0.4, 3);
    const l = new Float32Array(a1.length * 2), r = new Float32Array(a1.length * 2);
    l.set(a1); r.set(b1);
    const a = analyzeChannels(l, r, SR);
    expect(a.activity).toBeGreaterThan(0.4);
    expect(a.activity).toBeLessThan(0.6);
  });
  it("傾き: 白色ノイズは PSD の傾きがほぼ 0、1/3oct 幅の帯域では +3", () => {
    const [l, r] = noise(0.3, 6);
    const a = analyzeChannels(l, r, SR, { meanSpectrum: true });
    const t = spectralTilt(a.meanSpec!, SR);
    expect(Math.abs(t.psd)).toBeLessThan(0.7);
    expect(t.third).toBeCloseTo(t.psd + 3, 1);
    const fb = familyBands(a.meanSpec!, SR);
    // 白色ノイズなら帯域の幅の比（4k÷3k）だけ presence が大きい
    expect(fb.presence - fb.mid).toBeCloseTo(10 * Math.log10(4000 / 3000), 0);
  });
  it("帯域の定義は依頼どおりの 7 帯域", () => {
    expect(BANDS.map((b) => `${b.lo}-${b.hi}`)).toEqual(["20-60", "60-120", "120-250", "250-500", "500-2000", "2000-5000", "5000-20000"]);
    expect(MUD_COL).toBe(7);
  });
});

/** 窓ごとの帯域の強さが一定の人工のパート */
const flatStem = (id: string, role: string, perBand: Partial<Record<(typeof BAND_IDS)[number], number>>, windows = 40): MaskStem => {
  const row = Array.from({ length: WIN_COLS }, (_, c) => (c < BAND_IDS.length ? perBand[BAND_IDS[c]] ?? -90 : perBand.mud ?? -90));
  return { id, role, windows: Array.from({ length: windows }, () => [...row]), windowTotal: Array.from({ length: windows }, () => Math.max(...row)) };
};

describe("diagnoseMasking（パート間のマスキング）", () => {
  it("同じ帯域に 3 パートが同じ強さで鳴ると、混んでいる窓が 100%", () => {
    const r = diagnoseMasking([flatStem("g1", "guitarRhythm", { mid: -30 }), flatStem("g2", "guitarRhythm", { mid: -30 }), flatStem("k", "keys", { mid: -31 })]);
    expect(r.crowd.mid.crowdedPct).toBe(100);
    expect(r.crowd.mid.meanMajor).toBe(3);
  });
  it("帯域が分かれていれば、混まない", () => {
    const r = diagnoseMasking([flatStem("b", "bass", { bass: -30 }), flatStem("g", "guitarRhythm", { mid: -30 }), flatStem("h", "hihat", { air: -30 })]);
    expect(r.crowd.mid.crowdedPct).toBe(0);
    expect(r.crowd.mid.meanMajor).toBe(1);
  });
  it("キックとベースが Sub+Bass で同じ強さなら、ぶつかり 100%。差が大きければ 0%", () => {
    const same = diagnoseMasking([flatStem("k", "kick", { bass: -30 }), flatStem("b", "bass", { bass: -31 })]);
    expect(same.kickBass!.closePct).toBe(100);
    const apart = diagnoseMasking([flatStem("k", "kick", { bass: -30 }), flatStem("b", "bass", { bass: -45 })]);
    expect(apart.kickBass!.closePct).toBe(0);
  });
  it("キックが無ければ kickBass は null", () => {
    expect(diagnoseMasking([flatStem("b", "bass", { bass: -30 }), flatStem("g", "guitarRhythm", { mid: -30 })]).kickBass).toBeNull();
  });
  it("濁り: 200-500Hz に力が集まると超過が出て、寄与の大きいパートが先頭に並ぶ", () => {
    const heavy = diagnoseMasking([flatStem("g", "guitarRhythm", { mud: -20, mid: -40 }), flatStem("k", "keys", { mud: -35, mid: -40 })]);
    expect(heavy.mud.excessDb).toBeGreaterThan(5);
    expect(heavy.mud.top[0].id).toBe("g");
    const clean = diagnoseMasking([flatStem("g", "guitarRhythm", { mud: -60, mid: -20 }), flatStem("k", "keys", { mud: -60, mid: -22 })]);
    expect(clean.mud.excessDb).toBe(0);
    expect(heavy.mess.mud).toBeGreaterThan(clean.mess.mud);
  });
  it("リードの聞こえやすさ: 他が 10dB 大きければ負、10dB 小さければ正。埋もれ指数に反映", () => {
    const rules = [{ role: "lead", bands: ["mid", "presence"] as ("mid" | "presence")[] }];
    const buried = diagnoseMasking([flatStem("l", "lead", { mid: -40, presence: -40 }), flatStem("g", "guitarRhythm", { mid: -28, presence: -30 })], { clarity: rules, leadId: "l" });
    expect(buried.clarity[0].medianDb).toBeLessThan(-8);
    expect(buried.mess.leadBuried).toBeGreaterThan(80);
    const clear = diagnoseMasking([flatStem("l", "lead", { mid: -25, presence: -25 }), flatStem("g", "guitarRhythm", { mid: -38, presence: -40 })], { clarity: rules, leadId: "l" });
    expect(clear.clarity[0].medianDb).toBeGreaterThan(8);
    expect(clear.mess.leadBuried).toBe(0);
  });
  it("パートが無ければ空の結果", () => {
    expect(diagnoseMasking([]).windows).toBe(0);
  });
});

const PARTS: AiPartLike[] = [
  { instrument: "kick", role: "キック", volume: 0.22, pan: 0 },
  { instrument: "snare", role: "スネア", volume: 0.18, pan: 0 },
  { instrument: "hihat", role: "ハイハット", volume: 0.07, pan: 0 },
  { instrument: "crash", role: "ライドシンバル", volume: 0.07, pan: 0.15 },
  { instrument: "bass", role: "ベース（根音の8分）", volume: 0.18, pan: 0 },
  { instrument: "guitar", role: "歪みギターL（8分刻み）", volume: 0.17, pan: -0.7, amp: "loudrock", notes: "A3:1" },
  { instrument: "guitar", role: "歪みギターR（8分刻み）", volume: 0.17, pan: 0.7, amp: "loudrock", notes: "A3:1" },
  { instrument: "guitar", role: "クリーンのストローク（きらめき）", volume: 0.1, pan: 0, amp: "crystal", notes: "A3:1" },
  { instrument: "brass", patch: "trumpet", role: "メロディ（トランペット）", volume: 0.22, pan: 0.05, notes: "E5:1 A5:1" },
  { instrument: "piano", role: "ソロ（ピアノ）", volume: 0.2, pan: 0.1, notes: "E5:1 A5:1" },
  { instrument: "piano", role: "ピアノのアルペジオ", volume: 0.08, pan: -0.2, notes: "A3:0.5 E4:0.5" },
  { instrument: "brass", role: "ブラスの合いの手（Aメロ・アウトロだけ）", volume: 0.08, pan: 0.3, notes: "C#4:0.5" },
];

describe("assignRoles（役割の自動割り当て）", () => {
  const a = assignRoles(PARTS);
  it("楽器と role の文章から役割を決める", () => {
    expect(a.roles).toEqual(["kick", "snare", "hihat", "cymbal", "bass", "guitarRhythm", "guitarRhythm", "guitarClean", "lead", "leadDouble", "keys", "counter"]);
  });
  it("リードは「メロディ」の語があるパート。リードと同じ音符のピアノは重ね", () => {
    expect(a.leadIndex).toBe(8);
    expect(a.roles[9]).toBe("leadDouble");
  });
  it("mixRole と overrides で上書きできる", () => {
    const b = assignRoles(PARTS, { 3: "tom", 8: "lead" });
    expect(b.roles[3]).toBe("tom");
    const c = assignRoles(PARTS.map((p, i) => (i === 10 ? { ...p, mixRole: "strings" } : p)));
    expect(c.roles[10]).toBe("strings");
  });
  it("メロディの語が無ければリードギター、それも無ければ旋律でいちばん大きいパート", () => {
    const noWord = assignRoles([{ instrument: "bass", volume: 0.2 }, { instrument: "leadGuitar", volume: 0.1 }, { instrument: "brass", volume: 0.3 }]);
    expect(noWord.leadIndex).toBe(1);
    const loud = assignRoles([{ instrument: "bass", volume: 0.2 }, { instrument: "strings", volume: 0.1 }, { instrument: "brass", volume: 0.3 }]);
    expect(loud.leadIndex).toBe(2);
  });
});

const fakeAnalysis = (activeRmsDb: number, over: Partial<Parameters<typeof analyzeChannels>[0]> = {}): Unit["analysis"] => {
  void over;
  const base = analyzeChannels(...tone(1000, 0.1, 2), SR);
  return { ...base, activeRmsDb };
};
const unit = (id: string, role: Unit["role"], parts: number[], rms: number): Unit => ({ id, parts, role, label: id, analysis: fakeAnalysis(rms) });

describe("levelTargets（役割ごとの大きさの目標）", () => {
  it("グループの目標をグループ内の差で分ける: ギター 2 本は同じ値で、合計がグループの目標になる", () => {
    const units = [unit("lead", "lead", [0], -20), unit("g1", "guitarRhythm", [1], -20), unit("g2", "guitarRhythm", [2], -20)];
    const rows = levelTargets(units, "lead");
    expect(rows[1].targetRelDb).toBe(rows[2].targetRelDb);
    const sum = 10 * Math.log10(Math.pow(10, rows[1].targetRelDb / 10) + Math.pow(10, rows[2].targetRelDb / 10));
    expect(sum).toBeCloseTo(GROUP_TARGETS.guitar.relDb, 1);
  });
  it("ドラム: キックを基準にスネア -1.5・ハイハット -9 で、ドラム全体の目標に合計がそろう", () => {
    const units = [unit("lead", "lead", [0], -20), unit("k", "kick", [1], -20), unit("s", "snare", [2], -20), unit("h", "hihat", [3], -20)];
    const rows = levelTargets(units, "lead");
    expect(rows[2].targetRelDb - rows[1].targetRelDb).toBeCloseTo(ROLE_SPECS.snare.withinDb, 1);
    expect(rows[3].targetRelDb - rows[1].targetRelDb).toBeCloseTo(ROLE_SPECS.hihat.withinDb, 1);
    const sum = 10 * Math.log10(rows.slice(1).reduce((s, r) => s + Math.pow(10, r.targetRelDb / 10), 0));
    expect(sum).toBeCloseTo(GROUP_TARGETS.drums.relDb, 1);
  });
  it("目標より小さいパートには正の動かす量、大きいパートには負。許す幅の中なら動かさない", () => {
    const units = [unit("lead", "lead", [0], -20), unit("b", "bass", [1], -30), unit("k", "keys", [2], -10), unit("ok", "other", [3], -26)];
    const rows = levelTargets(units, "lead");
    expect(rows[1].stepDb).toBeGreaterThan(0);
    expect(rows[2].stepDb).toBeLessThan(0);
    expect(rows[3].stepDb).toBe(0);
    expect(rows[3].status).toBe("ok");
    expect(Math.abs(rows[1].stepDb)).toBeLessThanOrEqual(6);
  });
});

describe("planMix・applyPlan（調整案と反映）", () => {
  const roles = assignRoles(PARTS);
  const base = (rmsByRole: Record<string, number>): Unit[] => PARTS.map((_p, i) => unit(`p${i}`, roles.roles[i], [i], rmsByRole[roles.roles[i]] ?? -26)).filter((u) => !["kick", "snare", "hihat", "cymbal"].includes(String(u.role)));
  const plan = (units: Unit[], extra = {}) => planMix({ parts: PARTS, roles: roles.roles, leadIndex: roles.leadIndex, units, masking: null, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock", ...extra });

  it("ベースが目標より 8dB 小さければ gainDb を上げる（1 回の上限は 6dB）", () => {
    const p = plan(base({ lead: -20, bass: -29.1 }));
    const c = p.changes.find((x) => x.index === 4)!;
    expect(c.set.gainDb).toBeGreaterThan(0);
    expect(c.set.gainDb!).toBeLessThanOrEqual(6);
  });
  it("同じチャンネルを共有するパートは gainDb ではなく volume で動かす", () => {
    const shared = PARTS.map((_, i) => i === 4);
    const p = planMix({ parts: PARTS, roles: roles.roles, leadIndex: roles.leadIndex, units: base({ lead: -20, bass: -29.1 }), masking: null, sharedChannel: shared, bpm: 160, genre: "rock" });
    const c = p.changes.find((x) => x.index === 4)!;
    expect(c.set.volume).toBeGreaterThan(0.18);
    expect(c.set.gainDb).toBeUndefined();
  });
  it("ベースが左に寄っていれば中央へ。ギター 2 本が中央寄りなら左右へ", () => {
    const parts = PARTS.map((p, i) => (i === 4 ? { ...p, pan: -0.4 } : i === 5 ? { ...p, pan: -0.2 } : i === 6 ? { ...p, pan: 0.2 } : p));
    const p = planMix({ parts, roles: roles.roles, leadIndex: roles.leadIndex, units: base({ lead: -20 }), masking: null, sharedChannel: parts.map(() => false), bpm: 160, genre: "rock" });
    expect(p.changes.find((x) => x.index === 4)!.set.pan).toBe(0);
    expect(p.changes.find((x) => x.index === 5)!.set.pan).toBe(-0.75);
    expect(p.changes.find((x) => x.index === 6)!.set.pan).toBe(0.75);
  });
  it("低域が多いリズムギターにはハイパス、低域が少なければ何もしない。二重には足さない", () => {
    const lowUnits = base({ lead: -20 }).map((u) => (u.id === "p5" ? { ...u, analysis: { ...u.analysis, bandShareDb: { ...u.analysis.bandShareDb, sub: -12, bass: -8 } } } : u));
    const p = plan(lowUnits);
    const c = p.changes.find((x) => x.index === 5)!;
    expect(c.fx.some((f) => f.type === "filter" && f.kind === "highpass" && f.freq === 100)).toBe(true);
    const done = applyPlan({ parts: PARTS }, p.changes);
    const again = planMix({ parts: done.parts, roles: roles.roles, leadIndex: roles.leadIndex, units: lowUnits, masking: null, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock" });
    expect(again.changes.find((x) => x.index === 5)?.fx ?? []).toHaveLength(0);
    expect(again.advisories.length).toBeGreaterThan(0);
  });
  it("濁りの超過があれば、寄与の大きいギターの 350Hz を削る（合計 3dB まで）", () => {
    const masking = diagnoseMasking([flatStem("p5", "guitarRhythm", { mud: -20, mid: -30 }), flatStem("p6", "guitarRhythm", { mud: -30, mid: -30 }), flatStem("p8", "lead", { mud: -45, mid: -25 })]);
    const p = plan(base({ lead: -20 }), { masking });
    const c = p.changes.find((x) => x.index === 5)!;
    const eq = c.fx.find((f) => f.type === "eq")!;
    expect(eq.midHz).toBe(350);
    expect(eq.mid as number).toBeLessThan(0);
    // 反映を繰り返しても -3dB を超えない
    let song: { parts: AiPartLike[] } = { parts: PARTS };
    for (let i = 0; i < 4; i++) {
      const pp = planMix({ parts: song.parts, roles: roles.roles, leadIndex: roles.leadIndex, units: base({ lead: -20 }), masking, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock" });
      song = applyPlan(song, pp.changes);
    }
    const total = (song.parts[5].fx ?? []).filter((f) => f.automix === "mud").map((f) => f.mid as number);
    expect(total).toHaveLength(1);
    expect(total[0]).toBeGreaterThanOrEqual(-3);
  });
  it("キックとベースがぶつかっていればベースに duck（既にあれば足さない）", () => {
    const masking = diagnoseMasking([flatStem("k", "kick", { bass: -30 }), flatStem("b", "bass", { bass: -31 })]);
    const p = plan(base({ lead: -20 }), { masking });
    expect(p.changes.find((x) => x.index === 4)!.set.duck).toBeGreaterThan(0);
    const withDuck = PARTS.map((q, i) => (i === 4 ? { ...q, duck: 0.25 } : q));
    const p2 = planMix({ parts: withDuck, roles: roles.roles, leadIndex: roles.leadIndex, units: base({ lead: -20 }), masking, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock" });
    expect(p2.changes.find((x) => x.index === 4)?.set.duck).toBeUndefined();
  });
  it("applyPlan は元の曲を変えず、値を書き換えたコピーを返す。ドラムは volume を動かす", () => {
    const song = { parts: PARTS };
    const out = applyPlan(song, [{ index: 4, label: "x", set: { gainDb: 3, pan: 0 }, fx: [], reasons: [] }, { index: 0, label: "y", set: { volume: 0.3 }, fx: [], reasons: [] }]);
    expect(out.parts[4].gainDb).toBe(3);
    expect(out.parts[0].volume).toBe(0.3);
    expect(PARTS[4].gainDb).toBeUndefined();
    expect(PARTS[0].volume).toBe(0.22);
  });
  it("volume の目安: +6dB を volume に換算すると約 1.41 倍（2 乗則）", () => {
    const units = [unit("lead", "lead", [8], -20), unit("k", "kick", [0], -36)];
    const p = planMix({ parts: PARTS, roles: roles.roles, leadIndex: roles.leadIndex, units, masking: null, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock" });
    const c = p.changes.find((x) => x.index === 0)!;
    expect(c.set.volume!).toBeGreaterThan(0.22);
    expect(c.set.volume!).toBeLessThanOrEqual(0.5);
    expect(c.set.volume! / 0.22).toBeCloseTo(Math.pow(10, 6 / 40), 1);
  });
});

describe("masterAdvice（最後のまとめ）", () => {
  const mix: MixTargetsFile = { tolerance_dB: { bass: 2.5, lowmid: 2.5, mid: 2.5, presence: 4 }, families: { rock: { label: "ロック", bass: -4, lowmid: -6, mid: -8.5, presence: -17, tilt_dB_oct: -1.5 } } };
  const good = { lufs: -10, tpDb: -1.2, plr: 10, crestDb: 12, family: { bass: -4, lowmid: -6, mid: -8.5, presence: -17 }, tilt13: -1.5, corr: 0.7, widthDb: -5, lowCorr: 1, balanceDb: 0 };
  it("目標どおりなら全部 ○ で、EQ の追加案は出ない", () => {
    const a = masterAdvice(good, "rock", mix, MASTER_FAMILIES.rock, "rock-clean");
    expect(a.rows.filter((r) => r.status === "off")).toHaveLength(0);
    expect(a.eq).toHaveLength(0);
    expect(a.preset).toBe("rock-clean");
  });
  it("低中域が多ければ 300Hz を削る案、つぶれ気味なら軽い preset", () => {
    const a = masterAdvice({ ...good, family: { ...good.family, lowmid: -2 }, plr: 7, crestDb: 8, tpDb: -0.2 }, "rock", mix, MASTER_FAMILIES.rock, "rock-clean");
    expect(a.eq.find((e) => e.f === 300)!.g).toBeLessThan(0);
    expect(a.preset).toBe("rock-open");
    expect(a.rows.find((r) => r.name.startsWith("真のピーク"))!.status).toBe("off");
  });
  it("低域の相関が低いと警告の行が ×", () => {
    const a = masterAdvice({ ...good, lowCorr: 0.5 }, "rock", mix, MASTER_FAMILIES.rock);
    expect(a.rows.find((r) => r.name.startsWith("150Hz"))!.status).toBe("off");
  });
});

describe("formatReport（日本語レポート）", () => {
  it("耳で確認していないことと、7 つの節を必ず書く。差分の文章も出る", () => {
    const roles = assignRoles(PARTS);
    const units = PARTS.map((_p, i) => unit(`p${i}`, roles.roles[i], [i], -24)).filter((u) => !["kick", "snare", "hihat", "cymbal"].includes(String(u.role)));
    const masking = diagnoseMasking(units.map((u) => ({ id: u.id, role: u.role, windows: Array.from({ length: 10 }, () => Array(WIN_COLS).fill(-40)), windowTotal: Array(10).fill(-30) })));
    const pl = planMix({ parts: PARTS, roles: roles.roles, leadIndex: roles.leadIndex, units, masking, sharedChannel: PARTS.map(() => false), bpm: 160, genre: "rock" });
    const mm = { lufs: -10, tpDb: -1.2, plr: 10, crestDb: 12, family: { bass: -4, lowmid: -6, mid: -8.5, presence: -17 }, tilt13: -1.5, corr: 0.7, widthDb: -5, lowCorr: 1, balanceDb: 0 };
    const mix: MixTargetsFile = { tolerance_dB: { bass: 2.5, lowmid: 2.5, mid: 2.5, presence: 4 }, families: { rock: { label: "ロック", bass: -4, lowmid: -6, mid: -8.5, presence: -17, tilt_dB_oct: -1.5 } } };
    const advice = masterAdvice(mm, "rock", mix, MASTER_FAMILIES.rock, "rock-clean");
    const finalSong = applyPlan({ parts: PARTS }, pl.changes);
    const hist = { iteration: 0, mess: masking.mess, rows: pl.rows, master: mm, rep: "I -10.0", changes: pl.changes, advisories: pl.advisories, mud: masking.mud, lufsFinal: -10 };
    const data: ReportData = {
      title: "テスト曲", name: "t", songPath: "t.json", edition: "real", bpm: 160, seconds: 120, familyKey: "rock", familyLabel: "ロック", presetName: "rock-clean", spaceInfo: "", windowSec: 0.25, loop: false, loopDone: 0, history: [hist],
      final: { units, masking, plan: pl, masterMeasure: mm, advice, rep: { line: "I -10.0" }, split: false, sharedChannel: PARTS.map(() => false), warnings: [], gainDb: 0 },
      assignment: roles, parts: PARTS, proposalFile: "t.automix.json", buildFlags: "--bass pick", appliedTo: null, originalSong: { parts: PARTS }, finalSong,
    };
    const text = formatReport(data);
    expect(text).toContain("耳では確認していません");
    for (const h of ["## 1. 結果の要約", "## 2. パートごとの数値", "## 3. パート間のマスキング診断", "## 4. 最後のまとめ", "## 5. 調整案", "## 7. 直したこと・まだ残る問題"]) expect(text).toContain(h);
    expect(text).toContain("ぐじゃぐじゃ指数");
    expect(text).toContain("--master-preset rock-clean");
    const diff = describeDiff({ parts: PARTS }, finalSong, (i) => `p${i}`);
    expect(Array.isArray(diff)).toBe(true);
  });
});
