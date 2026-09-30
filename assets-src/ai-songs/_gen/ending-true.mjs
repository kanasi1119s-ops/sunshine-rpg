// 真エンディング「灯りの環（わ）、ふたたび」— ラスト裏ボス撃破後の、オーケストラ約5分の曲を書き出す（度数で書いて、調ごとに移調する）。
// 使い方: node assets-src/ai-songs/_gen/ending-true.mjs  →  assets-src/ai-songs/ending-true.json
import fs from "node:fs";
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const STEPS = [0, 2, 4, 5, 7, 9, 11];
const KEYS = { D: 2, E: 4, Fs: 6 };
const RANGE = { strings: [36, 96], pad: [36, 84], choir: [48, 84], brass: [40, 84], bell: [60, 96], piano: [21, 108] };
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const degSemi = (d) => Math.floor((d - 1) / 7) * 12 + STEPS[(((d - 1) % 7) + 7) % 7];
const midi = (key, d, oct = 4) => 12 * (oct + 1) + KEYS[key] + degSemi(d);
const fit = (m, ins) => { const [lo, hi] = RANGE[ins]; while (m > hi) m -= 12; while (m < lo) m += 12; return m; };
// ---- 旋律の書き方: "^3:1.5 ^^2:0.5 6:2" ＝ ^ で1オクターブ上、_ で1オクターブ下、数字は度数、R は休み。小節は | で区切る。
function parseMel(str) {
  const bars = str.split("|").map((b) => b.trim().split(/\s+/).map((t) => { const [p, b2] = t.split(":"); const beats = Number(b2); if (p === "R") return { rest: true, beats }; const up = (p.match(/\^/g) || []).length - (p.match(/_/g) || []).length; return { deg: Number(p.replace(/[\^_]/g, "")), up, beats }; }));
  bars.forEach((b, i) => { const s = b.reduce((a, n) => a + n.beats, 0); if (Math.abs(s - 4) > 1e-9) throw new Error(`旋律の小節${i + 1}が${s}拍: ${str}`); });
  return bars;
}
const T = (s) => parseMel(s);
// 主題A（灯りの動機）
const A1 = T("5:2 ^1:1 ^2:1 | ^3:3 ^2:1 | ^1:1.5 7:0.5 6:1 5:1 | 5:4 | 3:2 5:1 6:1 | ^1:3 7:1 | ^2:1.5 ^1:0.5 7:1 6:1 | 5:3 R:1");
const A2 = T("5:2 ^1:1 ^2:1 | ^3:2 ^5:2 | ^6:1.5 ^5:0.5 ^3:1 ^2:1 | ^3:4 | ^1:2 ^3:1 ^2:1 | ^1:1 7:1 6:1 ^1:1 | ^2:2 7:1 ^2:1 | ^1:4");
// 主題B（のびやかな第2主題）
const B1 = T("6:2 ^1:2 | ^2:3 ^1:1 | ^3:2 ^5:1 ^3:1 | ^6:2 ^5:1 ^3:1 | ^4:2 ^3:1 ^2:1 | ^2:1 ^3:1 ^5:2 | ^6:1 ^5:1 ^3:2 | ^2:3 R:1");
const B2 = T("^6:2 ^^1:2 | ^^2:3 ^^1:1 | ^^3:2 ^^5:1 ^^3:1 | ^^1:2 ^7:1 ^6:1 | ^^4:2 ^^3:1 ^^2:1 | ^^2:1 ^^3:1 ^^5:2 | ^^6:1 ^^5:1 ^^3:2 | ^^2:2 ^7:1 ^5:1");
const INT = T("^3:4 | ^4:2 ^3:2 | ^5:3 ^3:1 | ^2:4 | ^3:2 ^5:2 | ^6:3 ^5:1 | ^7:2 ^5:2 | ^3:4");
const FIN = T("^3:1.5 ^3:0.5 ^5:2 | ^^2:2 ^7:1 ^5:1 | ^^1:2 ^6:1 ^3:1 | ^7:1 ^5:1 ^3:2 | ^6:1.5 ^^1:0.5 ^^4:2 | ^^3:2 ^^1:1 ^5:1 | ^^2:1 ^7:1 ^^2:2 | ^^1:4");
const REL = T("^3:4 | ^2:2 ^1:2 | ^7:3 ^5:1 | ^6:4 | ^4:2 ^6:2 | ^5:3 ^2:1 | ^3:2 ^5:2 | ^3:4");
const CODA = T("5:2 ^1:1 ^2:1 | ^3:3 ^2:1 | ^1:2 7:1 6:1 | 5:4 | ^1:2 ^3:2 | ^2:3 ^1:1 | 7:2 ^2:2 | ^1:4");
// コード進行（度数。1〜7）
const P = {
  A1: [1, 6, 4, 5, 1, 4, 5, 1], A2: [1, 6, 4, 3, 6, 4, 5, 1],
  B: [4, 5, 3, 6, 4, 5, 1, 5], INT: [6, 4, 1, 5, 6, 4, 5, "B7"],
  REL: [1, 5, 6, 3, 4, 1, 5, "C#7"],
  FIN: [1, 5, 6, 3, 4, 1, 5, 1], CODA: [1, 6, 4, 5, 1, 4, 5, 1],
};
// ---- 曲の構成（小節数の合計 104 小節 ＝ ♩84 で約4分57秒）
// act: そのセクションで鳴らすパート（tex は音の厚さ 0〜3）
const SECTIONS = [
  { name: "序 灯りのともる前に", key: "D", ph: [{ mel: A1, prog: P.A1, mv: "bell" }], tex: 0, act: ["bell", "piano", "pad", "cello", "tom0"] },
  { name: "主題A 静かな行進", key: "D", ph: [{ mel: A1, prog: P.A1 }, { mel: A2, prog: P.A2 }], tex: 1, act: ["vln", "vla", "cello", "piano", "pad", "tom1"] },
  { name: "主題B のびやかに", key: "D", ph: [{ mel: B1, prog: P.B }, { mel: B2, prog: P.B, build: true }], tex: 2, act: ["vln", "vla", "cello", "piano", "pad", "hn", "hn2", "tom2", "snbuild", "crashEnd"] },
  { name: "間奏 祈り", key: "D", ph: [{ mel: INT, prog: P.INT, mv: "choir" }], tex: 0, act: ["choir", "piano", "pad", "cello", "bell"] },
  { name: "大いなる主題（ホ長調）", key: "E", ph: [{ mel: A1, prog: P.A1 }, { mel: A2, prog: P.A2 }, { mel: REL, prog: P.REL, build: true }], tex: 3, act: ["vln", "vla", "cello", "piano", "pad", "choir", "hn", "hn2", "bell", "tom3", "kick", "crash", "snbuild"] },
  { name: "終幕（嬰ヘ長調）", key: "Fs", ph: [{ mel: A1, prog: P.A1 }, { mel: B1, prog: P.B }, { mel: FIN, prog: P.FIN, build: true }], tex: 3, act: ["vln", "vla", "cello", "piano", "pad", "choir", "hn", "hn2", "bell", "tom3", "kick", "crash", "snbuild", "snare"] },
  { name: "後奏 灯りのゆくえ", key: "D", ph: [{ mel: CODA, prog: P.CODA, mv: "vln" }], tex: 0, act: ["vln", "piano", "pad", "cello", "bell", "coda"] },
];
const ROLES = { vln: "第1ヴァイオリン（旋律）", vla: "ヴィオラ（内声の分散和音）", cello: "チェロ・コントラバス（低音）", pad: "弦のロングトーン（3度）", choir: "合唱", piano: "ピアノ", hn: "ホルン・トランペット（旋律）", hn2: "ホルン（ハモリ）", bell: "鐘・チューブラーベル", tom: "ティンパニ", kick: "大太鼓", snare: "スネア", crash: "シンバル" };
const parts = { vln: [], vla: [], cello: [], pad: [], choir: [], piano: [], hn: [], hn2: [], bell: [], tom: [], kick: [], snare: [], crash: [] };
const chords = [];
const R = (n) => `R:${n}`;
let bar = 0;
const chordName = (key, r) => { if (typeof r === "string") return r; const root = KEYS[key] + degSemi(r); const minor = [2, 3, 6].includes(r); return NAMES[root % 12] + (minor ? "m" : ""); };
const triad = (key, r) => [r, r + 2, r + 4];
for (const sec of SECTIONS) {
  const has = (x) => sec.act.includes(x);
  let ib = 0;
  sec.ph.forEach((ph, pi) => {
    for (let i = 0; i < 8; i++, bar++, ib++) {
      const key = sec.key, r = ph.prog[i], isStr = typeof r === "string";
      chords.push(chordName(key, r));
      const rd = isStr ? (r === "B7" ? 6 : 6) : r;        // 特別コード（B7・C#7）は根音を6度扱いにする（伴奏の音の選び方用）
      const tri = isStr ? (r === "B7" ? [5, 7, 2] : [6, 8, 10]) : triad(key, rd);
      const bm = ph.mel[i];
      const last = i === 7, lastPh = pi === sec.ph.length - 1;
      const mel = (ins, up = 0, shift = 0) => bm.map((n) => n.rest ? R(n.beats) : `${nm(fit(midi(key, n.deg + shift, 4 + n.up + up), ins))}:${n.beats}`).join(" ");
      const put = (id, s) => parts[id].push(s);
      // 旋律
      const mvId = ph.mv ?? "vln";
      put("vln", (has("vln") && (mvId === "vln" || sec.tex >= 1)) ? mel("strings", 0) : R(4));
      put("choir", has("choir") ? (mvId === "choir" ? mel("choir", -1) : `${nm(fit(midi(key, tri[2], 4), "choir"))}:4`) : R(4));
      put("bell", has("bell") ? (mvId === "bell" ? mel("bell", 1) : sec.tex === 3 ? `${nm(fit(midi(key, tri[2], 6), "bell"))}:2 ${nm(fit(midi(key, tri[0], 6), "bell"))}:2` : (i % 2 === 0 ? `${nm(fit(midi(key, tri[2], 6), "bell"))}:1 R:3` : R(4))) : R(4));
      put("hn", has("hn") && (sec.tex >= 2) && !(sec.tex === 2 && pi === 0 && !ph.build && false) ? (sec.tex === 2 && pi === 0 ? R(4) : mel("brass", -1)) : R(4));
      put("hn2", has("hn2") && !(sec.tex === 2 && pi === 0) ? bm.map((n) => n.rest ? R(n.beats) : `${nm(fit(midi(key, n.deg - 2, 4 + n.up - 1), "brass"))}:${n.beats}`).join(" ") : R(4));
      // 低音
      const rootN = nm(fit(midi(key, tri[0], 2), "strings"));
      let cello;
      if (!has("cello")) cello = R(4);
      else if (sec.tex === 0) cello = `${rootN}:4`;
      else if (sec.tex === 1) cello = `${rootN}:3 ${nm(fit(midi(key, tri[2], 2), "strings"))}:1`;
      else cello = `${rootN}:1.5 ${rootN}:0.5 ${nm(fit(midi(key, tri[2], 2), "strings"))}:1 ${nm(fit(midi(key, tri[0], 3), "strings"))}:1`;
      put("cello", cello);
      // 内声
      const arp = [0, 1, 2, 3, 2, 1, 0, 1].map((k) => tri[k % 3] + 7 * Math.floor(k / 3));
      put("vla", has("vla") && sec.tex >= 1 ? arp.map((d) => `${nm(fit(midi(key, d, 3), "strings"))}:0.5`).join(" ") : R(4));
      put("pad", has("pad") ? `${nm(fit(midi(key, tri[1], 3), "pad"))}:4` : R(4));
      // ピアノ（分散和音）
      const pa = [tri[0], tri[2], tri[0] + 7, tri[1] + 7, tri[0] + 7, tri[2], tri[1], tri[2]];
      put("piano", has("piano") ? (sec.tex === 3 ? [tri[0] - 7, tri[0], tri[2], tri[0] + 7, tri[2], tri[0] + 7, tri[1] + 7, tri[2] + 7].map((d) => `${nm(fit(midi(key, d, 4), "piano"))}:0.5`).join(" ") : pa.map((d) => `${nm(fit(midi(key, d, 4), "piano"))}:0.5`).join(" ")) : R(4));
      // 打楽器
      const roll = Array(16).fill("x:0.25").join(" ");
      const isBuildEnd = ph.build && i >= 6, isBuildLast = ph.build && last;
      const tomOn = has("tom0") || has("tom1") || has("tom2") || has("tom3");
      let tom = R(4);
      if (tomOn) {
        if (isBuildLast) tom = roll;
        else if (sec.tex === 0) tom = last && lastPh && sec.name.startsWith("序") ? "x:2 R:2" : R(4);
        else if (sec.tex === 1) tom = i % 4 === 0 ? "x:1 R:3" : (last ? "x:0.5 x:0.5 x:1 R:2" : R(4));
        else if (sec.tex === 2) tom = isBuildEnd ? "x:0.5 x:0.5 x:0.5 x:0.5 x:1 x:1" : i % 2 === 0 ? "x:1 R:1 x:1 R:1" : "R:2 x:0.5 x:0.5 x:1";
        else tom = isBuildEnd ? "x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5" : "x:1 x:0.5 x:0.5 x:1 x:1";
      }
      put("tom", tom);
      put("kick", has("kick") && sec.tex === 3 && !isBuildLast ? (isBuildEnd ? "x:1 x:1 x:1 x:1" : "x:1 R:1 x:1 R:1") : R(4));
      let sn = R(4);
      if (has("snbuild") && ph.build) sn = isBuildLast ? "x:0.25 ".repeat(16).trim() : i === 6 ? "R:2 x:0.5 x:0.5 x:0.5 x:0.5" : R(4);
      if (has("snare") && sec.name.startsWith("終幕") && !ph.build) sn = "R:1 x:1 R:1 x:1";
      put("snare", sn);
      let cr = R(4);
      if (has("crash") && sec.tex === 3 && i === 0) cr = "x:4";
      if (has("crashEnd") && last && lastPh) cr = R(4);
      put("crash", cr);
    }
  });
  // 章の切れ目の頭にシンバル（大いなる主題・終幕）は上で入れた。コーダの最後は長い余韻。
}
const total = chords.length;
// 最後の小節を長い和音で締める（後奏の最終小節）
const lastIdx = total - 1;
parts.vln[lastIdx] = parts.vln[lastIdx].replace(/\S+$/, (m) => m); // 旋律は書いたまま（^1:4）
parts.crash[lastIdx] = "x:4"; parts.tom[lastIdx] = "x:2 R:2";
// 序の終わりのクレッシェンド代わりの鐘、間奏の最後のティンパニ
const spec = [
  ["strings", "第1ヴァイオリン（旋律）", "vln", 0.27, -0.25], ["strings", ROLES.vla, "vla", 0.15, 0.3], ["strings", ROLES.cello, "cello", 0.2, -0.05], ["pad", ROLES.pad, "pad", 0.12, 0.1],
  ["choir", ROLES.choir, "choir", 0.2, 0.0], ["piano", ROLES.piano, "piano", 0.2, 0.2], ["brass", ROLES.hn, "hn", 0.24, -0.35], ["brass", ROLES.hn2, "hn2", 0.16, 0.35], ["bell", ROLES.bell, "bell", 0.16, 0.4],
  ["tom", ROLES.tom, "tom", 0.24, -0.1], ["kick", ROLES.kick, "kick", 0.22, 0], ["snare", ROLES.snare, "snare", 0.16, 0.1], ["crash", ROLES.crash, "crash", 0.2, -0.2],
];
const song = {
  title: "灯りの環、ふたたび",
  description: "【仮】ラスト裏ボス撃破後の真エンディング用。オーケストラの大編成、約5分。鐘とピアノの静かな導入（序）から、弦の主題A、ホルンが加わる主題B、合唱の祈りの間奏を経て、ホ長調（大いなる主題）、嬰ヘ長調（終幕）と2度転調しながらティンパニ・大太鼓・シンバルで盛り上がり、最後はニ長調に戻って鐘とピアノで静かに終わる。",
  bpm: 84, beats: 4, chords: chords.join(" "), barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "ballad", tone: "prs",
  parts: spec.map(([instrument, role, id, volume, pan]) => ({ instrument, role, volume, pan, amp: "auto", notes: parts[id].join("  ") })),
};
fs.writeFileSync(new URL("../ending-true.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節数", total, "→", (total * 4 / 84 * 60).toFixed(0), "秒");
