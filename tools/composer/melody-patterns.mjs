// 旋律の型ライブラリ（docs/sound/melody-craft-guide.md §8 の提案 P9）。
// ガイドの見本（型1〜型38）を機械可読にし、条件に合う型を指定の調へ移高して「下書き」として出す。
//   node tools/composer/melody-patterns.mjs build         … ガイドから docs/sound/data/melody-patterns.json を作り直す
//   node tools/composer/song.mjs pattern --scene 町 --key D [--beats 4] [--record <曲ID>] [--history <ファイル>]
// 直前の曲で使った型は選ばない（履歴は docs/sound/data/pattern-history.json に --record で残す）。
// 出した下書きは、リズムか音を2か所以上変えてから使うこと（changeCount で確かめられる）。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { parseNotes } from "../audio-check/score-lib.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
export const GUIDE_PATH = path.join(ROOT, "docs/sound/melody-craft-guide.md");
export const PATTERNS_PATH = path.join(ROOT, "docs/sound/data/melody-patterns.json");
export const HISTORY_PATH = path.join(ROOT, "docs/sound/data/pattern-history.json");

const JP = { イ: 9, ロ: 11, ハ: 0, ニ: 2, ホ: 4, ヘ: 5, ト: 7 };
const LATIN = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** "G長調"・"変ホ長調"・"イ短調"・"イ（フリジアン風）" → { tonic(0-11), minor(true/false/null), label } */
export function parseKeyLabel(s) {
  const m = /^(変|嬰)?([イロハニホヘト]|[A-G])([#b]?)/.exec(s.trim());
  if (!m) return null;
  const base = JP[m[2]] ?? LATIN[m[2]];
  const acc = (m[1] === "変" ? -1 : m[1] === "嬰" ? 1 : 0) + (m[3] === "#" ? 1 : m[3] === "b" ? -1 : 0);
  const rest = s.slice(m[0].length);
  const minor = rest.startsWith("短調") ? true : rest.startsWith("長調") ? false : null;
  return { tonic: (base + acc + 12) % 12, minor, label: s.trim() };
}

const TAGS = [
  ["町", /町/], ["フィールド", /フィールド/], ["ダンジョン", /ダンジョン/], ["戦闘", /戦闘/], ["ボス", /ボス/], ["ロック", /ロック/],
  ["ポップ", /ポップ|J-POP/], ["バラード", /バラード|子守歌/], ["ジャズ", /ジャズ/], ["ブルース", /ブルース/], ["和", /民謡|都節|琉球|律音階/],
  ["ケルト", /ケルト/], ["チップチューン", /チップチューン/], ["ファンファーレ", /ファンファーレ/], ["悲しい", /悲しい/], ["神秘", /神秘|謎解き/],
  ["エンディング", /エンディング/], ["サビ", /サビ/], ["コミカル", /コミカル/], ["夕焼け", /夕焼け/], ["ファンク", /ファンク/], ["子守歌", /子守歌/], ["掛留", /掛留|倚音/],
];

/** ガイドの Markdown から型の一覧を取り出す。 */
export function parsePatternsFromGuide(md) {
  const out = [];
  const re = /\*\*型(\d+)\s+([^*]+)\*\*（([^）]*(?:（[^）]*）[^）]*)*)）\s*\n+(?:コード（1小節ずつ）:\s*`([^`]+)`\s*\n+)?```\n([\s\S]*?)```/g;
  let m;
  while ((m = re.exec(md))) {
    const [, id, title, meta, chordLine, body] = m;
    const parts = meta.split("・");
    const keyLabel = parts[0].trim();
    const beats = Number((/(\d+)拍子/.exec(meta) ?? [])[1]);
    const bpm = Number((/bpm\s*(\d+)/.exec(meta) ?? [])[1]);
    const bars = Number((/(\d+)小節/.exec(meta) ?? [])[1]);
    const key = parseKeyLabel(keyLabel);
    const notes = body.trim().split("\n").map((l) => l.trim()).filter(Boolean).join(" ");
    const chords = chordLine ? chordLine.split("|").map((c) => c.trim()).filter(Boolean) : [];
    const tags = TAGS.filter(([, r]) => r.test(title)).map(([t]) => t);
    out.push({ id: Number(id), title: title.trim(), scene: tags[0] ?? "", key: keyLabel, tonic: key?.tonic ?? null, minor: key?.minor ?? null, beats, bpm, bars, chords, notes, tags });
  }
  return out;
}

export function loadPatterns(file = PATTERNS_PATH) {
  return JSON.parse(fs.readFileSync(file, "utf8")).patterns;
}

// ---- 移高 -------------------------------------------------------------------

const FLAT_KEYS = new Set([5, 10, 3, 8, 1, 6]); // F・Bb・Eb・Ab・Db・Gb（長調の主音）
const useFlats = (tonic, minor) => FLAT_KEYS.has(minor ? (tonic + 3) % 12 : tonic);
const SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const FLAT_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];

function nameOf(pitch, flats) {
  return `${(flats ? FLAT_NAMES : SHARP_NAMES)[((pitch % 12) + 12) % 12]}${Math.floor(pitch / 12) - 1}`;
}

/** コード名の根音（と分数の低音）を semis 半音動かす。 */
export function transposeChord(name, semis, flats) {
  const tr = (s) => {
    const m = /^([A-G])([#b]?)/.exec(s);
    if (!m) return s;
    const pc = (LATIN[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + semis + 120) % 12;
    return (flats ? FLAT_NAMES : SHARP_NAMES)[pc] + s.slice(m[0].length);
  };
  const [head, bass] = name.split("/");
  return bass ? `${tr(head)}/${tr(bass)}` : tr(head);
}

/** 型を targetTonic（0〜11 の主音）へ移高する。いちばん近い向き（-6〜+5半音）で動かし、音域の変化を小さくする。 */
export function transposePattern(pat, targetTonic) {
  if (pat.tonic == null || targetTonic == null) return { ...pat, semis: 0 };
  let semis = (((targetTonic - pat.tonic) % 12) + 12) % 12;
  if (semis > 6) semis -= 12;
  const flats = useFlats(targetTonic, pat.minor === true);
  const { notes } = parseNotes(pat.notes);
  const text = notes.map((n) => {
    const tail = `:${+n.dur.toFixed(4)}${n.mark}`;
    return n.rest ? `R${tail}` : `${nameOf(n.pitch + semis, flats)}${tail}`;
  }).join(" ");
  return { ...pat, notes: text, chords: pat.chords.map((c) => transposeChord(c, semis, flats)), semis, tonic: targetTonic };
}

/** 主音名（"D"・"Bb"・"ニ"）→ 0〜11 */
export function parseTonicArg(s) {
  const k = parseKeyLabel(String(s));
  return k ? k.tonic : null;
}

// ---- 選ぶ -------------------------------------------------------------------

export function readHistory(file = HISTORY_PATH) {
  try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return []; }
}
export function recordHistory(songId, patternId, file = HISTORY_PATH) {
  const h = readHistory(file);
  h.push({ song: songId, pattern: patternId, date: new Date().toISOString().slice(0, 10) });
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(h, null, 1) + "\n");
  return h;
}

/**
 * 条件に合う型を探す。scene は場面名かタグ（"町"・"戦闘"・"バラード" など。型の題名にも当てる）。
 * beats を指定すると拍子で絞る。exclude の id と、履歴の直前 avoidLast 曲の型は選ばない。
 * 戻り値は候補の配列（先頭が第一候補。同条件なら id が小さい順）。
 */
export function selectPatterns(patterns, { scene, beats, exclude = [], history = [], avoidLast = 2, mode } = {}) {
  const recent = new Set(history.slice(-avoidLast).map((h) => h.pattern));
  const ban = new Set([...exclude, ...recent]);
  return patterns.filter((p) => {
    if (ban.has(p.id)) return false;
    if (scene && !(p.tags.includes(scene) || p.scene === scene || p.title.includes(scene))) return false;
    if (beats && p.beats !== Number(beats)) return false;
    if (mode === "minor" && p.minor !== true) return false;
    if (mode === "major" && p.minor !== false) return false;
    return true;
  });
}

/** 下書きから何か所変えたか（音の高さ・長さ・休符の違い。長さが同じ位置の音を 1 トークンずつ比べ、数の違いも足す）。 */
export function changeCount(draft, final) {
  const a = parseNotes(draft).notes, b = parseNotes(final).notes;
  let n = Math.abs(a.length - b.length);
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i].pitch !== b[i].pitch || Math.abs(a[i].dur - b[i].dur) > 1e-9 || a[i].rest !== b[i].rest) n++;
  }
  return n;
}

export const DRAFT_RULE = "下書きです。そのまま使わず、リズムか音を2か所以上変えてから曲に入れてください（同じ型を続けて使わない）。";

/** CLI: pattern の本体。args は ["pattern", "--scene", ...] */
export function runPatternCommand(args) {
  const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
  const histFile = opt("--history", HISTORY_PATH);
  const patterns = loadPatterns();
  const scene = opt("--scene");
  const keyArg = opt("--key");
  const target = keyArg !== undefined ? parseTonicArg(keyArg) : null;
  if (keyArg !== undefined && target === null) throw new Error(`調が読めません: ${keyArg}（D・Bb・ニ など）`);
  const list = selectPatterns(patterns, { scene, beats: opt("--beats"), history: readHistory(histFile), mode: opt("--mode") });
  if (!list.length) return "条件に合う型がありません（直前の曲で使った型は除いています）。--scene を替えるか、--history を確かめてください。";
  const pick = opt("--id") ? list.find((p) => p.id === Number(opt("--id"))) ?? list[0] : list[0];
  const t = target === null ? pick : transposePattern(pick, target);
  const lines = [
    `型${pick.id}「${pick.title}」（原曲 ${pick.key}・${pick.beats}拍子・bpm ${pick.bpm}・${pick.bars}小節）${target === null ? "" : `→ ${keyArg} へ ${t.semis >= 0 ? "+" : ""}${t.semis}半音`}`,
    `コード: ${t.chords.join(" | ")}`,
    t.notes,
    `他の候補: ${list.filter((p) => p.id !== pick.id).slice(0, 5).map((p) => `型${p.id}`).join("・") || "なし"}`,
    DRAFT_RULE,
  ];
  const rec = opt("--record");
  if (rec) { recordHistory(rec, pick.id, histFile); lines.push(`履歴に記録: ${rec} → 型${pick.id}`); }
  return lines.join("\n");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url) && process.argv[2] === "build") {
  const patterns = parsePatternsFromGuide(fs.readFileSync(GUIDE_PATH, "utf8"));
  fs.mkdirSync(path.dirname(PATTERNS_PATH), { recursive: true });
  fs.writeFileSync(PATTERNS_PATH, JSON.stringify({ source: "docs/sound/melody-craft-guide.md §4（node tools/composer/melody-patterns.mjs build で作り直す）", patterns }, null, 1) + "\n");
  console.log(`${patterns.length}個の型を ${path.relative(ROOT, PATTERNS_PATH)} に書きました`);
}
