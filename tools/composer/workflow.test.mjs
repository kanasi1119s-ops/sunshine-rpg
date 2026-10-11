import { test } from "node:test";
import assert from "node:assert";
import { spawnSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";
import { judge, formatGate, measureWav, saveMeasurement } from "./gate.mjs";
import { checkPlan, PLAN_TEMPLATE } from "./plan-check.mjs";
import { describeSong, compareChoices, introOf, contourSimilarity, checkNovelty } from "./novelty.mjs";
import { formatRevision, appendRevision, hasRevision } from "./revision-log.mjs";
import { pickRecipes } from "./chord-pick.mjs";
import { collectFacts, isAvoid } from "../audio-check/score-facts.mjs";
import { chordPcs, estimateKey, barChords, parseNotes } from "../audio-check/score-lib.mjs";

const song = (over = {}) => ({
  title: "t", description: "", bpm: 100, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 2, autoAccompaniment: false, feel: "pop", tone: "rock",
  parts: [{ instrument: "lead", role: "メロディ", notes: "E5:4 C5:4 A4:4 B4:4 E5:4 D5:4 C5:4 B4:4" }],
  ...over,
});

test("合否表: 目安に合う数字は○、外れは要直しと直し方", () => {
  const ok = { lufs: -14.2, tp: -1.4, lra: 5.5, plr: 12.8, corr: 0.7, headVsMax: -3, midSilences: [], durationSec: 120 };
  assert.ok(judge(ok).every((r) => r.ok));
  const bad = { lufs: -8, tp: -0.1, lra: 0.9, plr: 7.9, corr: 0.97, headVsMax: 0, midSilences: [{ start: 40, end: 50 }], durationSec: 120 };
  const rows = judge(bad);
  assert.equal(rows.filter((r) => !r.ok).length, 7);
  const text = formatGate(bad, rows, "x.wav");
  assert.ok(text.includes("要直し 7件") && text.includes("ほぼモノラル") && text.includes("40秒"));
  assert.ok(judge(bad, { target: -8 })[0].ok);
});

test("合否表: ffmpeg でWAVを測る（相関・LUFS・無音）", { skip: spawnSync("ffmpeg", ["-version"]).error ? "ffmpeg なし" : false }, () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "gate-"));
  const f = path.join(dir, "a.wav");
  const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=f=220:d=5", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono:d=6", "-f", "lavfi", "-i", "sine=f=220:d=5", "-filter_complex", "[0]aformat=sample_rates=48000:channel_layouts=mono[a];[2]aformat=sample_rates=48000:channel_layouts=mono[c];[a][1][c]concat=n=3:v=0:a=1,aformat=channel_layouts=stereo", f]);
  assert.equal(r.status, 0);
  const m = measureWav(f);
  assert.ok(Number.isFinite(m.lufs) && m.lufs < -10);
  assert.ok(m.corr > 0.99, "同じ音を左右に入れたので相関はほぼ1");
  assert.equal(m.midSilences.length, 1);
  assert.ok(Math.abs(m.durationSec - 16) < 0.2);
  const s = saveMeasurement(dir, "test-song", m, judge(m), -14);
  assert.ok(fs.existsSync(s.file) && s.previous === null);
  assert.equal(saveMeasurement(dir, "test-song", m, judge(m), -14).previous.date.length, 10);
  assert.throws(() => saveMeasurement(dir, "Bad ID", m, judge(m), -14));
  fs.rmSync(dir, { recursive: true, force: true });
});

test("設計図の検査: 雛形は未記入を指摘し、整えると通る", () => {
  const r0 = checkPlan(JSON.parse(JSON.stringify(PLAN_TEMPLATE)));
  assert.equal(r0.errors.length, 0);
  assert.ok(r0.warnings.some((w) => w.includes("未記入")));
  const plan = JSON.parse(JSON.stringify(PLAN_TEMPLATE));
  plan.card.recipe = "borrowed-iv"; plan.card.soundSet = ""; plan.card.bannedChecked = true;
  assert.ok(!checkPlan(plan).warnings.some((w) => w.includes("未記入")));
  plan.sections.forEach((s) => (s.intensity = 5));
  assert.ok(checkPlan(plan).warnings.some((w) => w.includes("平ら")));
  plan.sections[1].change = "";
  assert.ok(checkPlan(plan).warnings.some((w) => w.includes("前との違い")));
  plan.sections[0].bars = 0;
  assert.ok(checkPlan(plan).errors.length > 0);
});

test("設計図の検査: 曲との食い違い（小節の合計・音域・計画にないパート）", () => {
  const plan = JSON.parse(JSON.stringify(PLAN_TEMPLATE));
  plan.card.bpm = 100; plan.card.beats = 4; plan.card.tonic = "C"; plan.card.mode = "major"; plan.card.bannedChecked = true; plan.card.recipe = "x";
  plan.card.ranges = { lead: ["C4", "C5"] };
  plan.sections = [{ name: "A", bars: 4, parts: ["lead"], intensity: 3, change: "-" }, { name: "B", bars: 4, parts: ["lead"], intensity: 8, change: "高く" }, { name: "C", bars: 4, parts: ["lead"], intensity: 4, change: "戻す" }];
  const r = checkPlan(plan, song());
  assert.ok(r.errors.some((e) => e.includes("合計（12）") && e.includes("8小節")));
  plan.sections = plan.sections.slice(0, 2);
  const r2 = checkPlan(plan, song());
  assert.equal(r2.errors.length, 0);
  assert.ok(r2.warnings.some((w) => w.includes("計画の音域") && w.includes("音")), r2.warnings.join("\n"));
  const r3 = checkPlan(plan, song({ parts: [...song().parts, { instrument: "piano", role: "ピアノ", notes: "C3:4 R:4" }] }));
  assert.ok(r3.warnings.some((w) => w.includes("計画にないパート") && w.includes("ピアノ")));
});

test("新しさ: 同じ選択を見つけ、違えば何も言わない", () => {
  const a = describeSong(song({ description: "入り方: 5。終わり方: 余韻" }), "a");
  const b = describeSong(song({ description: "入り方: 5。終わり方: 余韻" }), "b");
  const kinds = compareChoices(a, b).map((x) => x.kind);
  for (const k of ["調", "テンポ", "進行", "入り方", "終わり方", "主役の楽器"]) assert.ok(kinds.includes(k), k);
  const c = describeSong(song({ bpm: 140, chords: "Em D Bm G Em D Bm G", description: "入り方: 1。終わり方: ぴたりと止める", parts: [{ instrument: "leadGuitar", role: "メロディ", notes: "E4:8" }] }), "c");
  assert.deepEqual(compareChoices(c, a).map((x) => x.kind).filter((k) => k !== "調"), []);
  const w = checkNovelty(song(), "me", [{ name: "prev", song: song() }]).warnings;
  assert.ok(w.some((x) => x.includes("直前の曲「prev」")));
});

test("新しさ: 入り方の推測と、旋律の輪郭の重なり", () => {
  const drums = { instrument: "kick", role: "キック", notes: "x:1 R:3" };
  const bass = { instrument: "bass", role: "ベース", notes: "C2:1 R:3" };
  const pad = { instrument: "pad", role: "パッド", notes: "C3:8" };
  assert.equal(introOf(song({ parts: [drums, bass, pad, { instrument: "lead", role: "メロディ", notes: "C5:4" }] })).id, 1);
  assert.equal(introOf(song({ parts: [pad, { instrument: "kick", notes: "R:8" }, { instrument: "lead", role: "メロディ", notes: "R:8 C5:8" }] })).id, 5);
  assert.equal(introOf(song({ description: "入り方: 3", parts: [pad] })).declared, true);
  assert.equal(contourSimilarity("UUDDUDURRUDUUDDU", "UUDDUDURRUDUUDDU"), 1);
  assert.equal(contourSimilarity("UUDDUDURRUDU", "DDDDDDDDDDDD"), 0);
});

test("直しの記録: 1行の形式・追記・探せる", () => {
  assert.throws(() => formatRevision({ id: "a", before: "x", change: "", after: "y", ear: "z" }));
  assert.equal(formatRevision({ id: "a-b", before: "LRA 0.9", change: "Bメロを引く", after: "LRA 4.1", ear: "静けさが出た", date: "2026-10-11" }), "- 2026-10-11 a-b: LRA 0.9 → Bメロを引く → LRA 4.1 → 静けさが出た");
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "rev-"));
  assert.equal(hasRevision(dir, "a-b"), false);
  appendRevision(dir, { id: "a-b", before: "1", change: "2", after: "3", ear: "4" });
  assert.equal(hasRevision(dir, "a-b"), true);
  assert.equal(hasRevision(dir, "a"), false);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("進行の選択: 場面に合い、直近と違い、同じ種で同じ結果", () => {
  const recent = [{ name: "prev", chords: "Em C G D" }];
  const a = pickRecipes({ scene: "battle", recent, count: 3, seed: 7 });
  const b = pickRecipes({ scene: "battle", recent, count: 3, seed: 7 });
  assert.deepEqual(a, b);
  assert.equal(a.length, 3);
  assert.ok(a.every((x) => x.scenes.includes("battle") && x.id !== "royal"));
  assert.ok(a.every((x) => x.tonic.replace("m", "") !== "C" && x.tonic.replace("m", "") !== "E"), "直近の主音とC以外を選ぶ");
  assert.ok(pickRecipes({ scene: "boss", key: "Em", count: 1, seed: 1 })[0].tonic.startsWith("E"));
  assert.throws(() => pickRecipes({ key: "Q" }));
});

test("楽譜の事実: アヴォイドノート・音域外・拍の合計・同じ4小節の反復", () => {
  assert.ok(isAvoid(5, chordPcs("C"), new Set([0, 2, 4, 5, 7, 9, 11])), "C に対する F（3度の半音上）");
  assert.ok(!isAvoid(2, chordPcs("C"), new Set([0, 2, 4, 5, 7, 9, 11])));
  const s = song({ chords: "C", repeats: 12, parts: [{ instrument: "bass", role: "ベース", notes: "C1:4 R:4" }, { instrument: "lead", role: "メロディ", notes: "F4:4 E4:4 F4:2 E4:2 D4:4" }] });
  const { facts } = collectFacts(s);
  const by = (k) => facts.filter((f) => f.kind === k);
  assert.ok(by("アヴォイドノート").some((f) => f.bar === 1 && f.detail.includes("F4") && f.detail.includes("E")), JSON.stringify(by("アヴォイドノート")));
  assert.ok(by("音域外").some((f) => f.bar === 1 && f.detail.includes("C1")));
  assert.ok(by("同じ4小節の反復").length >= 1);
  const odd = collectFacts(song({ parts: [{ instrument: "lead", role: "メロディ", notes: "C5:3 D5:3" }] })).facts;
  assert.ok(odd.some((f) => f.kind === "拍の合計"));
  const long = collectFacts(song({ repeats: 1, parts: [{ instrument: "lead", role: "メロディ", notes: "C5:16 D5:8" }] })).facts;
  assert.ok(long.some((f) => f.kind === "拍の合計" && f.detail.includes("長い")));
});

test("楽譜の事実: 動機が現れないセクションと、変形のない反復", () => {
  const s = song({
    description: "動機: E4:1 G4:1 A4:2", chords: "C", repeats: 8,
    sections: [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }],
    parts: [{ instrument: "lead", role: "メロディ", notes: "E4:1 G4:1 A4:2 R:4 D5:8 C5:8 R:8" }],
  });
  const m = collectFacts(s).facts.filter((f) => f.kind === "動機");
  assert.ok(m.some((f) => f.detail.includes("chorus")), JSON.stringify(m));
  assert.ok(!m.some((f) => f.detail.includes("verse")));
});

test("コード名の読み: 分数・6・9・m7b5・add9", () => {
  const pcs = (n) => [...chordPcs(n).pcs].sort((a, b) => a - b).join(",");
  assert.equal(pcs("Bm7b5"), "2,5,9,11");
  assert.equal(pcs("Cadd9"), "0,2,4,7");
  assert.equal(pcs("Cmaj9"), "0,2,4,7,11");
  assert.equal(pcs("C6"), "0,4,7,9");
  assert.equal(pcs("G/B"), "2,7,11");
  assert.equal(estimateKey(["Am", "F", "C", "G"]).label, "A短調");
  assert.equal(estimateKey(["C", "Am", "F", "G"]).label, "C長調");
  assert.equal(barChords({ chords: "C G", barsPerChord: 2, repeats: 2 }).join(""), "CCGGCCGG");
  assert.equal(parseNotes("E5:1! R:0.5 g:X.x.", false).total, 1.5);
  assert.equal(parseNotes("g:X.x.", true).total, 1);
});
