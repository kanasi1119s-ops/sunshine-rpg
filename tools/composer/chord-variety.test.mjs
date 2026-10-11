import { test } from "node:test";
import assert from "node:assert";
import { signature, similarity, checkChordVariety } from "./chord-variety.mjs";
test("基本の和音だけを見つける", () => {
  assert.ok(checkChordVariety("Am F C G Am F C G", []).some((x) => x.includes("基本の和音")));
  assert.ok(!checkChordVariety("Am7 Fmaj7 Cadd9 G/B Dm7 E7 Am7 Fmaj7 Bb Gsus4", []).some((x) => x.includes("基本の和音")));
});
test("キーが違っても同じ形なら似ている", () => {
  const a = signature("Am F C G Am F C G").seq, b = signature("Em C G D Em C G D").seq;
  assert.equal(similarity(a, b), 1);
  assert.ok(similarity(a, signature("Dm Bb Gm A7 Dm Bb Gm A7 Dm Em F G").seq) < 0.7);
});
