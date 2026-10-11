// ギターのソロ・表現の過多・音域の検査（解析だけ。曲は変えない）。docs/sound/guitar-technique-deep-guide.md §10 の提案 6・7・8。
// 使い方: node tools/audio-check/guitar-lint.mjs <曲.json> […]    または score-check.mjs から自動で呼ばれる。
// 数値の目安は同ガイドの §2（ソロ）・§8（失敗）・§6.4（推奨ポジション）。【推測】を含む。警告が出ても、わざとなら直さなくてよい。
import fs from "fs";
import { DRUMS, midi, chordPcs, barChords } from "./score-lib.mjs";

const GUITARS = new Set(["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"]);
const SUGAR = { gallop: [0.5, 0.25, 0.25], rgallop: [0.25, 0.25, 0.5], trem: [0.125], trem16: [0.25] };

/** 音の並び（"E5:1! D5:0.5~ R:0.5"）を読む。@gallop などの糖衣は展開し、記号は rawMarks に残す。戻り値は { t, dur, name, pitch, marks }。 */
export function readNotes(text) {
  const out = [];
  let t = 0;
  for (const raw of String(text ?? "").trim().split(/\s+/)) {
    if (!raw) continue;
    const m = /^([^:@\s]+):(\d+(?:\.\d+)?)([^@\s]*?)(?:@(gallop|rgallop|trem|trem16))?$/.exec(raw);
    if (!m) continue;
    const name = m[1];
    const dur = Number(m[2]);
    if (!(dur > 0)) continue;
    const marks = m[3].replace(/u\([^)]*\)/, "");
    const pitch = name === "R" || name === "r" ? null : name === "x" || name === "X" ? null : midi(name);
    const dead = name === "x" || name === "X";
    if (m[4] && pitch !== null) {
      const unit = SUGAR[m[4]];
      const total = unit.reduce((a, b) => a + b, 0);
      const count = Math.max(1, Math.floor(dur / total + 1e-9));
      for (let u = 0; u < count; u++) for (const d of unit) { out.push({ t, dur: d, name, pitch, marks: "", fig: true }); t += d; }
      const rem = dur - count * total;
      if (rem > 1e-9) { out.push({ t, dur: rem, name, pitch, marks: "", fig: true }); t += rem; }
      continue;
    }
    out.push({ t, dur, name, pitch, marks, dead, rest: name === "R" || name === "r" });
    t += dur;
  }
  return { notes: out, total: t };
}

/** くり返しで曲の長さまで広げた、休符を含む音の並び。 */
function expandTo(text, totalBeats) {
  const { notes, total } = readNotes(text);
  if (!(total > 0)) return [];
  const out = [];
  for (let base = 0; base < totalBeats - 1e-9; base += total) for (const n of notes) if (base + n.t < totalBeats - 1e-9) out.push({ ...n, t: base + n.t });
  return out;
}

const pct = (x) => `${Math.round(x * 100)}%`;
const barOf = (t, beats) => Math.floor(t / beats + 1e-9) + 1;
const joinBars = (list, beats, max = 5) => {
  const u = [...new Set(list.map((t) => barOf(t, beats)))];
  return u.slice(0, max).join("・") + (u.length > max ? `…ほか${u.length - max}か所` : "") + "小節目";
};
const count = (s, ch) => (s.match(new RegExp(`\\${ch}`, "g")) ?? []).length;

/**
 * 検査の本体。song はAIソング形式のJSON、opts は { beats, totalBeats, chords（小節ごとのコード名） }（省略は song から求める）。
 * 戻り値は { level: "warn" | "ok" | "info", msg } の並び。
 */
export function guitarLint(song, opts = {}) {
  const beats = opts.beats ?? song.beats ?? 4;
  const chords = opts.chords ?? barChords(song);
  const totalBeats = opts.totalBeats ?? chords.length * beats;
  const res = [];
  const warn = (ok, okMsg, ngMsg) => { if (ok) { if (okMsg) res.push({ level: "ok", msg: okMsg }); } else res.push({ level: "warn", msg: ngMsg }); };
  const info = (msg) => res.push({ level: "info", msg });
  const parts = (song.parts ?? []).filter((p) => p && !DRUMS.has(p.instrument)).map((p) => ({ p, seq: expandTo(p.notes, totalBeats) }));
  const hasMelody = parts.some(({ p }) => /メロディ|旋律/.test(p.role ?? "") && !GUITARS.has(p.instrument));

  // ───── 1. ソロの検査（leadGuitar、または役割に「ソロ」を含むギター） ─────
  const solos = parts.filter(({ p, seq }) => GUITARS.has(p.instrument) && seq.some((n) => n.pitch !== null) && (p.instrument === "leadGuitar" || /ソロ|solo/i.test(p.role ?? "")));
  for (const { p, seq } of solos) {
    const label = `${/ソロ|solo/i.test(p.role ?? "") ? "ソロ" : "リード"}「${p.role ?? p.instrument}」`;
    const snd = seq.filter((n) => n.pitch !== null);
    const first = snd[0].t;
    const last = snd[snd.length - 1];
    const span = last.t + last.dur - first;
    if (span < beats * 4) { info(`${label}: 4小節未満なので、ソロの検査は省きました`); continue; }
    // 休符の割合（鳴っている範囲の中）
    const sounding = snd.reduce((s, n) => s + n.dur, 0);
    const restRate = Math.max(0, 1 - sounding / span);
    warn(restRate >= 0.12, `${label}: 休符の割合 ${pct(restRate)}（目安 20〜30%）`, `${label}: 休符が ${pct(restRate)} しかありません（目安 20〜30%。空間を埋めすぎ。フレーズの内側にも休符を）`);
    if (restRate > 0.5) res.push({ level: "warn", msg: `${label}: 休符が ${pct(restRate)} と多すぎます（目安 20〜30%）` });
    // 最高音: 位置と回数
    const top = Math.max(...snd.map((n) => n.pitch));
    const tops = snd.filter((n) => n.pitch === top);
    const pos = (tops[0].t - first) / span;
    const posLast = (tops[tops.length - 1].t - first) / span;
    warn(posLast >= 0.55, `${label}: 最高音は後ろ寄り（${pct(posLast)} の位置）`, `${label}: 最高音（${tops[0].name}）が前半（${pct(pos)}）にしかありません（頂点は後ろ3分の1に置くのが目安）`);
    const bars8 = Math.max(1, span / (beats * 8));
    warn(tops.length <= Math.max(2, Math.ceil(2 * bars8)), `${label}: 最高音 ${tops[0].name} は ${tops.length}回`, `${label}: 最高音 ${tops[0].name} が ${tops.length}回（頂点は1回が目安。${joinBars(tops.map((n) => n.t), beats)}）`);
    // 表現の予算（8小節あたり）
    const vib = snd.filter((n) => n.marks.includes("~")).length / bars8;
    const bnd = snd.filter((n) => n.marks.includes("^")).length / bars8;
    const slp = snd.filter((n) => /[/\\]/.test(n.marks)).length / bars8;
    warn(vib <= 6, `${label}: ~ は8小節あたり ${vib.toFixed(1)}音`, `${label}: ~（ビブラート）が8小節あたり ${vib.toFixed(1)}音（目安 4〜5。毎小節に載せない）`);
    warn(bnd <= 3, `${label}: ^ は8小節あたり ${bnd.toFixed(1)}音`, `${label}: ^（ベンド）が8小節あたり ${bnd.toFixed(1)}音（目安 1〜2。頂点のために取っておく）`);
    warn(slp <= 4, `${label}: / \\ は8小節あたり ${slp.toFixed(1)}か所`, `${label}: /（しゃくり）・\\（フォール）が8小節あたり ${slp.toFixed(1)}か所（目安 2〜3）`);
    // モチーフの反復（3つの音程の並びが2回以上出る割合）
    if (snd.length >= 12) {
      const iv = [];
      for (let i = 1; i < snd.length; i++) iv.push(snd[i].pitch - snd[i - 1].pitch);
      const grams = new Map();
      for (let i = 0; i + 3 <= iv.length; i++) { const k = iv.slice(i, i + 3).join(","); grams.set(k, (grams.get(k) ?? 0) + 1); }
      let rep = 0;
      let all = 0;
      for (const c of grams.values()) { all += c; if (c >= 2) rep += c; }
      const rate = all ? rep / all : 0;
      warn(rate >= 0.15, `${label}: 音型の反復 ${pct(rate)}`, `${label}: 同じ音型（3つの音程の並び）の反復が ${pct(rate)} しかありません（動機を決めて育てると覚えやすい）`);
    }
    // 拍頭が和音の構成音である割合
    let onBeat = 0;
    let chordTone = 0;
    for (const n of snd) {
      if (Math.abs(n.t - Math.round(n.t)) > 1e-6 || n.dead) continue;
      const c = chordPcs(chords[Math.min(chords.length - 1, Math.floor(n.t / beats))]);
      if (!c) continue;
      onBeat++;
      if (c.pcs.has(n.pitch % 12)) chordTone++;
    }
    if (onBeat >= 6) warn(chordTone / onBeat >= 0.5, `${label}: 拍頭の構成音 ${pct(chordTone / onBeat)}`, `${label}: 拍頭の音が和音の構成音なのは ${pct(chordTone / onBeat)} だけ（目安 6割以上。拍頭は構成音、間を音階の音でつなぐ）`);
  }

  // ───── 2. 表現の過多・無効 ─────
  for (const { p, seq } of parts) {
    if (!GUITARS.has(p.instrument)) continue;
    const label = `「${p.role ?? p.instrument}」`;
    const snd = seq.filter((n) => n.pitch !== null && !n.fig);
    const shortVib = snd.filter((n) => n.marks.includes("~") && n.dur < 0.4);
    if (shortVib.length) warn(false, "", `${label}: 0.4拍未満の音に ~ があります（効きません）: ${joinBars(shortVib.map((n) => n.t), beats)}`);
    const shortBend = snd.filter((n) => n.marks.includes("^") && n.dur < 0.25);
    if (shortBend.length) warn(false, "", `${label}: 0.25拍未満の音に ^ があります（0.125拍未満は効かず、短いベンドは一瞬）: ${joinBars(shortBend.map((n) => n.t), beats)}`);
    const longNotes = snd.filter((n) => n.dur >= 0.4);
    const vibNotes = snd.filter((n) => n.marks.includes("~"));
    if (vibNotes.length >= 5 && longNotes.length && vibNotes.length / longNotes.length > 0.8) warn(false, "", `${label}: 長い音のほぼ全部（${vibNotes.length}/${longNotes.length}）に ~ があります。付けない長音も混ぜる`);
    else if (vibNotes.length >= 6 && vibNotes.length / snd.length > 0.5) warn(false, "", `${label}: 音の ${pct(vibNotes.length / snd.length)} に ~ があります（毎音には付けない）`);
    // 同じ深さの ~ の連続（3音以上）
    let run = 0;
    let runMark = "";
    let worst = null;
    for (const n of snd) {
      const k = n.marks.includes("~") ? (n.marks.match(/~\.?/g) ?? []).join("") : "";
      if (k && k === runMark) run++;
      else { run = k ? 1 : 0; runMark = k; }
      if (run >= 3 && !worst) worst = n.t;
    }
    if (worst !== null) warn(false, "", `${label}: 同じ深さの ~ が3音以上つづきます（${barOf(worst, beats)}小節目。~ と ~~ を使い分ける）`);
    // autoArticulation と手書きの ~ の重複
    const autoOn = p.autoArticulation === true || (song.autoArticulation === true && p.autoArticulation !== false);
    if (autoOn && vibNotes.length && ["guitar", "leadGuitar"].includes(p.instrument)) warn(false, "", `${label}: autoArticulation が長音の終わりに ~ を自動で付けるのに、手書きの ~ も ${vibNotes.length}音あります（重なる。どちらかに）`);
    // 自動しゃくり
    if (["guitar", "leadGuitar"].includes(p.instrument) && song.autoScoop !== false && p.autoScoop !== false) {
      const scooped = snd.filter((n) => n.dur >= 1 && n.t > 0 && !/[\^/\\]/.test(n.marks));
      if (scooped.length >= 6) warn(false, "", `${label}: 1拍以上の音 ${scooped.length}音に自動しゃくり（毎回「キュッ」と下から入る）がかかります。曲かパートに autoScoop:false を（必要な所だけ / を書く）`);
    }
    if (p.strum && p.strum.scoop === true && song.autoScoop !== false && p.autoScoop !== false) warn(false, "", `${label}: strum.scoop:true でストロークの和音にも自動しゃくりがかかります（「キュインキュイン」の原因。外すか autoScoop:false を）`);
    // 短い同音の連打（禁止の音 1）。ギャロップ・トレモロの糖衣は意図した使い方なので数えない
    let same = 1;
    let sameBar = null;
    for (let i = 1; i < snd.length; i++) {
      const a = snd[i - 1];
      const b = snd[i];
      if (b.pitch === a.pitch && b.dur <= 0.25 && a.dur <= 0.25 && b.marks.includes("'") && a.marks.includes("'")) { same++; if (same === 4) sameBar = b.t; } else same = 1;
    }
    if (sameBar !== null && !p.rhythm && !p.tremolo) warn(false, "", `${label}: スタッカート（'）の短い同音の連打が4つ以上あります（${barOf(sameBar, beats)}小節目。banned-sounds.md の「ピ、ピ」。音程を動かすか、sustain を伸ばして和音に）`);
  }

  // ───── 3. 音域（推奨ポジション。guitar-technique-deep-guide.md §6.4） ─────
  for (const { p, seq } of parts) {
    if (!GUITARS.has(p.instrument)) continue;
    const label = `「${p.role ?? p.instrument}」`;
    const snd = seq.filter((n) => n.pitch !== null && !n.dead && !n.fig);
    const totalDur = snd.reduce((s, n) => s + n.dur, 0);
    if (!totalDur) continue;
    const durWhere = (f) => snd.filter(f).reduce((s, n) => s + n.dur, 0);
    if (p.instrument === "distGuitar") {
      const hi = durWhere((n) => n.pitch > midi("A3"));
      warn(hi / totalDur <= 0.2, "", `${label}: 歪みの刻みが A3 より高い音を ${pct(hi / totalDur)} 使っています（推奨 E2〜A3。高いと刺さる・割れる）`);
    }
    if (p.instrument === "leadGuitar") {
      const hi = snd.filter((n) => n.dur >= 1 && n.pitch > midi("C6"));
      if (hi.length) warn(false, "", `${label}: C6 より高い長音が ${hi.length}か所あります（${joinBars(hi.map((n) => n.t), beats)}。頂点でも A5〜C6 まで。6kHz 以上は刺さる）`);
      const over = durWhere((n) => n.pitch > midi("E5"));
      if (over / totalDur > 0.15) warn(false, "", `${label}: E5 より高い音が ${pct(over / totalDur)} あります（頂点の1音以外は E5 以下が目安）`);
    }
    if ((p.instrument === "guitar" || p.instrument === "crunch") && hasMelody) {
      const mid = durWhere((n) => n.pitch >= midi("C4") && n.pitch <= midi("B4"));
      if (mid / totalDur > 0.6 && !/旋律|メロ|ソロ|オブリ|リード/.test(p.role ?? "")) warn(false, "", `${label}: C4〜B4 に ${pct(mid / totalDur)} います。メロディと同じ帯域でぶつかります（リズムギターは C3〜G4 が目安）`);
    }
  }
  return res;
}

const label = (r) => (r.level === "warn" ? "△ " : r.level === "info" ? "  ・" : "○ ") + r.msg;
// 単独で使う: node tools/audio-check/guitar-lint.mjs 曲.json
if (process.argv[1] && process.argv[1].endsWith("guitar-lint.mjs")) {
  let warns = 0;
  for (const f of process.argv.slice(2).filter((a) => !a.startsWith("--"))) {
    const song = JSON.parse(fs.readFileSync(f, "utf8"));
    console.log(`■ ${song.title ?? f}`);
    const r = guitarLint(song);
    for (const x of r) { console.log(label(x)); if (x.level === "warn") warns++; }
    if (!r.length) console.log("  ・検査の対象（ギターのパート）がありません");
  }
  console.log(`\n警告 ${warns}件（目安。耳で確かめて決める）`);
}
export { label as guitarLintLabel };
