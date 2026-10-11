import { describe, expect, it } from "vitest";
// @ts-ignore 点検の道具は .mjs（型なし）
import { checkGroove, readOnsets } from "../../tools/audio-check/groove-lib.mjs";
import { ROCK_SONG } from "./rhythm-fixtures";

type Issue = { level: string; msg: string };
const part = (instrument: string, notes: string, extra: Record<string, unknown> = {}): Record<string, unknown> => ({ instrument, role: instrument, volume: 0.12, pan: 0, notes, ...extra });
const check = (song: Record<string, unknown>, opts?: { edition?: string }): Issue[] => checkGroove({ bpm: 120, beats: 4, ...song }, opts);
const has = (issues: Issue[], text: string): boolean => issues.some((i) => i.msg.includes(text));
const bar = "g:x.x.x.x.x.x.x.x.";

describe("check-groove（提案10）", () => {
  it("気になる点がない曲は空", () => {
    expect(check({ parts: [part("kick", "g:X.......X.x....."), part("snare", "g:....X.......X..."), part("hihat", "g:X.x.X.x.X.x.X.x.")], human: 0.3, swing: 0 })).toEqual([]);
  });
  it("push が ±0.05 拍を超える（pushMs はミリ秒を拍に直して）", () => {
    expect(has(check({ parts: [part("snare", bar, { push: 0.08 })] }), "push")).toBe(true);
    expect(has(check({ parts: [part("snare", bar, { push: 0.04 })] }), "push")).toBe(false);
    // 60ms は 120bpm で 0.12 拍
    expect(has(check({ parts: [part("snare", bar, { pushMs: 60 })] }), "push")).toBe(true);
    expect(has(check({ parts: [part("snare", bar, { pushMs: 10 })] }), "push")).toBe(false);
    // 同じ ms でも bpm が高いと拍数が増える: 同じ ms でも bpm 200 では拍数が増える（12ms＝0.04 拍は大丈夫、50ms＝0.17 拍は超える）
    expect(has(check({ bpm: 200, parts: [part("snare", bar, { pushMs: 12 })] }), "±0.05")).toBe(false);
    expect(has(check({ bpm: 200, parts: [part("snare", bar, { pushMs: 50 })] }), "±0.05")).toBe(true);
  });
  it("キックの push が 0 でない／ベースの push が 0〜+0.01 拍の外", () => {
    expect(has(check({ parts: [part("kick", bar, { push: 0.02 })] }), "キックの push")).toBe(true);
    expect(has(check({ parts: [part("kick", bar)] }), "キックの push")).toBe(false);
    expect(has(check({ parts: [part("bass", "E2:4", { push: 0.04 })] }), "ベースの push")).toBe(true);
    expect(has(check({ parts: [part("bass", "E2:4", { push: -0.02 })] }), "ベースの push")).toBe(true);
    expect(has(check({ parts: [part("bass", "E2:4", { push: 0.008 })] }), "ベースの push")).toBe(false);
  });
  it("human がジャンルの上限や 30ms を超える", () => {
    expect(has(check({ drumGenre: "metal", human: 0.4, parts: [] }), "目安（0.2）")).toBe(true);
    expect(has(check({ drumGenre: "metal", human: 0.15, parts: [] }), "目安")).toBe(false);
    expect(has(check({ human: 0.9, parts: [] }), "目安（0.6）")).toBe(true);
    // 80bpm は ms が約1.5倍: modern で human 0.7 → 約 4.9×3.8×1.56=29ms、real 版では 47ms
    expect(has(check({ bpm: 80, human: 0.5, drumGenre: "ballad", parts: [] }, { edition: "real" }), "30ms")).toBe(true);
    expect(has(check({ bpm: 120, human: 0.3, parts: [] }), "30ms")).toBe(false);
  });
  it("ドラムの volume が 0.18 を超える", () => {
    expect(has(check({ parts: [part("kick", bar, { volume: 0.25 })] }), "0.18")).toBe(true);
    expect(has(check({ parts: [part("bass", "E2:4", { volume: 0.25 })] }), "0.18")).toBe(false);
  });
  it("beats 6 に swing", () => {
    expect(has(check({ beats: 6, swing: 0.5, parts: [] }), "6/8")).toBe(true);
    expect(has(check({ beats: 4, swing: 0.5, parts: [] }), "6/8")).toBe(false);
    expect(has(check({ beats: 6, parts: [part("hihat", "g:xxxxxxxxxxxxxxxxxxxxxxxx", { swing: 0.4 })] }), "swing")).toBe(true);
  });
  it("g: が4の倍数でない・合計が小節の倍数でない（エラー）、t: が3の倍数でない（エラー）", () => {
    const e1 = check({ parts: [part("kick", "g:x...x...x...x..")] });
    expect(e1.some((i) => i.level === "error" && i.msg.includes("15 文字"))).toBe(true);
    expect(check({ parts: [part("kick", "g:x...x...x...x...x...")] }).some((i) => i.level === "error" && i.msg.includes("倍数"))).toBe(true);
    expect(check({ parts: [part("hihat", "t:xxxx")] }).some((i) => i.level === "error" && i.msg.includes("三連"))).toBe(true);
    expect(check({ parts: [part("hihat", "t:xxxxxxxxxxxx t:x.xx.xx.xx.x")] }).filter((i) => i.level === "error")).toEqual([]);
    // 変拍子: beats 7 なら 28 文字が1小節
    expect(check({ beats: 7, parts: [part("kick", "g:x...x...x...x...x...x...x...")] }).filter((i) => i.level === "error" && i.msg.includes("倍数"))).toEqual([]);
  });
  it("ハイハットが全部 x のベタ打ち／同じ小節が8回以上", () => {
    expect(has(check({ parts: [part("hihat", "g:xxxxxxxxxxxxxxxx g:xxxxxxxxxxxxxxxx")] }), "ベタ打ち")).toBe(true);
    expect(has(check({ parts: [part("hihat", "g:X.x.X.x.X.x.X.x.")] }), "ベタ打ち")).toBe(false);
    expect(has(check({ parts: [part("snare", Array(9).fill("g:....X.......X...").join(" "))] }), "9 回続きます")).toBe(true);
    expect(has(check({ parts: [part("snare", Array(7).fill("g:....X.......X...").join(" "))] }), "回続きます")).toBe(false);
  });
  it("シンコペ率: 0%（全部拍の頭）と90%超", () => {
    const straight = part("bass", "E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1 E2:1");
    expect(has(check({ parts: [straight] }), "0%")).toBe(true);
    const off = part("bass", Array(20).fill("R:0.5 E2:0.5").join(" "));
    expect(has(check({ parts: [off] }), "シンコペ率")).toBe(true);
    const mixed = part("bass", Array(8).fill("E2:1 E2:0.5 E2:0.5 E2:1 E2:1").join(" "));
    expect(has(check({ parts: [mixed] }), "シンコペ率")).toBe(false);
    // 打点が少ないときは見ない
    expect(has(check({ parts: [part("bass", "E2:1 E2:1")] }), "シンコペ率")).toBe(false);
  });
  it("readOnsets: g:・t:・音名:拍を打点にする", () => {
    const issues: Issue[] = [];
    const r = readOnsets("g:x.x. t:x.x R:1 E2:0.5", "l", issues, 16);
    expect(r.onsets.map((o: { start: number }) => Math.round(o.start * 1000) / 1000)).toEqual([0, 0.5, 1, 1.667, 3]);
    expect(r.total).toBeCloseTo(3.5, 6);
    expect(issues).toEqual([]);
  });
  it("見本曲 ROCK_SONG は、ドラムの volume が小さいので volume の注意が出ない", () => {
    expect(has(check(ROCK_SONG as unknown as Record<string, unknown>), "0.18")).toBe(false);
  });
});
