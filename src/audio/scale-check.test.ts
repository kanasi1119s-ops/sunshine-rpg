import guideText from "../../docs/sound/scales-world-guide.md?raw";
import { describe, expect, it } from "vitest";
import { parseNotes } from "./ai-song";
import { checkScaleUsage } from "./scale-check";
import { findScale, pitchClassOf } from "./scales";

const doc = guideText.split("\n");
interface Example { n: number; scaleName: string; tonic: string; beats: number; notes: string }
const examples: Example[] = [];
doc.forEach((l, i) => {
  const m = /^\*\*例(\d+)　.*\*\*（(.+)・主音 ([A-G][b#]?)・beats (\d+)・bpm/.exec(l);
  if (!m) return;
  const notes = doc.slice(i + 1, i + 8).find((x) => x.startsWith("notes: "))!.slice(7);
  examples.push({ n: Number(m[1]), scaleName: m[2].replace(/（.*$/, ""), tonic: m[3], beats: Number(m[4]), notes });
});
const track = (notes: string) => ({ instrument: "lead" as const, role: "メロディ", notes: parseNotes(notes, false, [], "t") });

describe("checkScaleUsage（ガイド 6-3 の旋律 24 例）", () => {
  it("24 例を全部読めている", () => {
    expect(examples.length).toBe(24);
    for (const e of examples) {
      expect(findScale(e.scaleName), `例${e.n} ${e.scaleName}`).toBeTruthy();
      const total = parseNotes(e.notes, false, [], "t").reduce((s, x) => s + x.durationBeats, 0);
      expect(total % e.beats, `例${e.n} 拍の合計`).toBe(0);
    }
  });
  it.each(examples.map((e) => [e.n, e] as const))("例%i: 警告ゼロ", (_n, e) => {
    const w = checkScaleUsage([track(e.notes)], findScale(e.scaleName)!, pitchClassOf(e.tonic)!, { beatsPerBar: e.beats });
    expect(w).toEqual([]);
  });
  it.each(examples.filter((e) => !["全音音階", "ディミニッシュ"].some((s) => e.scaleName.startsWith(s))).map((e) => [e.n, e] as const))("例%i: 小節頭の音を 1 つ外すと警告が出る", (_n, e) => {
    const scale = findScale(e.scaleName)!;
    const tonic = pitchClassOf(e.tonic)!;
    const set = new Set(scale.semis.map((s) => (s + tonic) % 12));
    const events = parseNotes(e.notes, false, [], "t");
    // 先頭の音を、音階の外へ半音ずらす（上か下、どちらかが外れる）
    const first = events[0];
    const midi = Number(0) + (({ C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 } as Record<string, number>)[first.note[0]] + (first.note.includes("#") ? 1 : first.note.includes("b") ? -1 : 0) + (Number(first.note.slice(-1)) + 1) * 12);
    const shifted = [midi + 1, midi - 1].find((m) => !set.has(m % 12));
    if (shifted === undefined) return; // 半音の隣がすべて音階内（半音階に近い音階）
    const names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    events[0] = { ...first, note: `${names[shifted % 12]}${Math.floor(shifted / 12) - 1}` };
    const w = checkScaleUsage([{ instrument: "lead", role: "メロディ", notes: events }], scale, tonic, { beatsPerBar: e.beats, maxOffRatio: 0 });
    expect(w.length).toBeGreaterThan(0);
  });
  it("ベンドの付いた音（ブルーノート）は外れとして数えない", () => {
    const scale = findScale("minor-pentatonic")!;
    const w = checkScaleUsage([track("A4:1 C5:1 Eb5:1^ E5:1")], scale, 9, { beatsPerBar: 4, maxOffRatio: 0 });
    expect(w.join()).not.toContain("外の音が");
  });
  it("低音・ドラムのパートは点検しない", () => {
    const w = checkScaleUsage([{ instrument: "bass", role: "ベース", notes: parseNotes("C#2:4", false, [], "t") }], findScale("miyako")!, 0, { beatsPerBar: 4 });
    expect(w).toEqual([]);
  });
  it("転調のあとは、上がった主音で判定する", () => {
    const scale = findScale("ro")!; // C D E G A
    const ok = checkScaleUsage([track("C4:4 C4:4 Db4:4 Eb4:4 Ab4:4 Bb4:4")], scale, 0, { beatsPerBar: 4, modulate: { semitones: 1, atBeat: 8 }, maxOffRatio: 0.2 });
    expect(ok.join()).not.toContain("外の音が");
  });
});
