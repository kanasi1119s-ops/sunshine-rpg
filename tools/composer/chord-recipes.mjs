// コード進行の型（docs/sound/data/chord-recipes.json）を読み、ローマ数字の度数を、実際のコード名にする。
// chord-variety.mjs（型ラベル）と chord-pick.mjs（進行の選択ツール）が使う。
import fs from "fs";

const FILE = new URL("../../docs/sound/data/chord-recipes.json", import.meta.url);
export const DEGREE = { I: 0, II: 2, III: 4, IV: 5, V: 7, VI: 9, VII: 11 };
const SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
const ROMAN = /^([b#]?)(VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i)(.*)$/;

export function loadRecipes() {
  return JSON.parse(fs.readFileSync(FILE, "utf8"));
}

/** 主音（0〜11）と長短から、フラット表記かどうか。 */
export function useFlats(tonic, minor) {
  return minor ? [2, 7, 0, 5, 10, 3, 8].includes(tonic) : [5, 10, 3, 8, 1, 6].includes(tonic);
}
export const pcName = (pc, flats) => (flats ? FLAT : SHARP)[((pc % 12) + 12) % 12];

/** "bVII" "iv" "V7" "IV/1" "i(maj7)" → { root(0〜11, 主音から), name(接尾辞つき), bassOffset } 。読めなければ null。 */
export function parseRoman(tok) {
  const m = ROMAN.exec(tok);
  if (!m) return null;
  const upper = m[2] === m[2].toUpperCase();
  const off = (DEGREE[m[2].toUpperCase()] + (m[1] === "b" ? -1 : m[1] === "#" ? 1 : 0) + 12) % 12;
  let [suffix, bass] = m[3].split("/");
  let bassOff = null;
  if (bass !== undefined) {
    const b = /^([b#]?)([1-7])$/.exec(bass);
    if (!b) return null;
    bassOff = ([0, 2, 4, 5, 7, 9, 11][Number(b[2]) - 1] + (b[1] === "b" ? -1 : b[1] === "#" ? 1 : 0) + 12) % 12;
  }
  const keepsOwn = /^(dim|m7b5|aug)/.test(suffix);
  return { off, acc: m[1], quality: (upper || keepsOwn ? "" : "m") + suffix, bassOff };
}

/** ローマ数字の並び（"I V vi IV"）を、主音 tonic（0〜11）のコード名の並びにする。 */
export function realize(roman, tonic, { minor = false, flats = useFlats(tonic, minor) } = {}) {
  return String(roman).split(/\s+/).filter(Boolean).map((tok) => {
    const r = parseRoman(tok);
    if (!r) throw new Error(`度数が読めません「${tok}」`);
    const fl = r.acc === "b" ? true : r.acc === "#" ? false : flats; // 半音下げの度数（bVII など）はフラットで書く
    const root = pcName(tonic + r.off, fl);
    return root + r.quality + (r.bassOff === null ? "" : `/${pcName(tonic + r.bassOff, flats)}`);
  });
}
