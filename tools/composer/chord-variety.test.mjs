import { test } from "node:test";
import assert from "node:assert";
import { signature, similarity, checkChordVariety, parseChord, recipeOf } from "./chord-variety.mjs";
import { realize, parseRoman, loadRecipes } from "./chord-recipes.mjs";

test("基本の和音だけを見つける", () => {
  assert.ok(checkChordVariety("Am F C G Am F C G", []).some((x) => x.includes("基本の和音")));
  assert.ok(!checkChordVariety("Am7 Fmaj7 Cadd9 G/B Dm7 E7 Am7 Fmaj7 Bb Gsus4", []).some((x) => x.includes("基本の和音")));
});
test("キーが違っても同じ形なら似ている", () => {
  const a = signature("Am F C G Am F C G").seq, b = signature("Em C G D Em C G D").seq;
  assert.equal(similarity(a, b), 1);
  assert.ok(similarity(a, signature("Dm Bb Gm A7 Dm Bb Gm A7 Dm Em F G").seq) < 0.7);
});
test("回して書いても同じと判定する（回転不変）", () => {
  assert.equal(similarity(signature("C G Am F").seq, signature("Am F C G").seq), 1);
  assert.equal(similarity(signature("C G Am F").seq, signature("F C G Am").seq), 1);
  assert.equal(similarity(signature("C G Am F").seq, signature("D A Bm G").seq), 1);
  assert.ok(checkChordVariety("Am F C G", [{ name: "前の曲", chords: "C G Am F C G Am F" }]).some((x) => x.includes("前の曲") && x.includes("100%")));
});
test("別の進行は似ていない", () => {
  assert.ok(similarity(signature("Am F C G").seq, signature("Em D A E").seq) < 0.7);
  assert.equal(similarity([], signature("C").seq), 0);
});
test("分数コード・6・9・m7b5・mmaj7・小節数つきを読む", () => {
  assert.deepEqual(parseChord("G/B"), { root: 7, minor: false, plain: false, bass: 11, quality: "" });
  assert.equal(parseChord("Am*2").root, 9);
  assert.equal(parseChord("Bm7b5").minor, true);
  assert.equal(parseChord("Am(maj7)").minor, true);
  assert.equal(parseChord("C6").plain, false);
  assert.equal(parseChord("Cadd9").plain, false);
  assert.equal(parseChord("Xm"), null);
  assert.ok(!checkChordVariety("C G/B Am*2 F Dm7b5 E7", []).some((x) => x.includes("基本の和音")));
});
test("型ラベル: 既知の型を見つける（調や回しが違っても）", () => {
  assert.equal(recipeOf("Em C G D")?.id, "royal");
  assert.ok(checkChordVariety("Am F C G", []).some((x) => x.includes("使いすぎ注意")));
  assert.equal(recipeOf("E D A E")?.roman.startsWith("I bVII"), true);
  assert.equal(recipeOf("Dm Gm7 Cm9 Em"), null);
});
test("同じ型を使った他の曲を知らせる", () => {
  const w = checkChordVariety("E D A E", [{ name: "別の曲", chords: "A G D A" }]);
  assert.ok(w.some((x) => x.includes("別の曲")));
});
test("ローマ数字を主音のコード名にする", () => {
  assert.deepEqual(realize("I V/7 vi I/5 IV", 7), ["G", "D/F#", "Em", "G/D", "C"]);
  assert.deepEqual(realize("i bVII bVI V", 2, { minor: true }), ["Dm", "C", "Bb", "A"]);
  assert.deepEqual(realize("IVmaj7 III7 vi7 I7", 7), ["Cmaj7", "B7", "Em7", "G7"]);
  assert.deepEqual(realize("i i(maj7) i7 i6", 9, { minor: true }), ["Am", "Am(maj7)", "Am7", "Am6"]);
  assert.equal(parseRoman("Q"), null);
});
test("すべての型が読め、コード名がアプリ側で読める書式になっている", () => {
  for (const r of loadRecipes().recipes) {
    const cs = realize(r.roman, 0, { minor: r.mode === "minor" });
    for (const c of cs) assert.ok(parseChord(c), `${r.id}: ${c}`);
  }
});
