// リズム・グルーヴの点検（docs/sound/rhythm-groove-guide.md §10 の提案10）。AIソング形式のJSON（オブジェクト）を調べて、{ level, msg } の並びを返す。
// level: "error"（直さないと小節がずれる）／"warn"（わざとなら無視してよい）。数字は同ガイドの出発点（耳で最終確認すること）。
const DRUM = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const RHYTHM_FOR_SYNC = new Set(["kick", "snare", "bass", "slap", "sub808", "guitar", "crunch", "distGuitar", "keys", "piano"]);
// human の上限（ジャンルの目安。ガイド §7.2）。表にないジャンルは 0.6
const HUMAN_LIMIT = { metal: 0.2, boss: 0.25, trap: 0.15, dnb: 0.15, dubstep: 0.15, house: 0.2, disco: 0.25, vocaloid: 0.25, battle: 0.3, punk: 0.45, rock: 0.45, hardrock: 0.4, pop: 0.45, jpop: 0.45, hiphop: 0.45, funk: 0.55, rnb: 0.55, bossa: 0.55, field: 0.55, ballad: 0.6, reggae: 0.6, jazz: 0.6 };
const MAX_MS = 30; // 楽器の「最大のずれ」がこれを超えると外れて聞こえる（ガイド §7.1）
const num = (x) => (x === undefined || x === null || x === "" ? NaN : Number(x));

/** パートの notes を、{ start, dur, rest } の並びに読む（g:・t:・音名:拍）。まちがいは issues に足す。 */
export function readOnsets(text, label, issues, cells) {
  const out = [];
  let at = 0;
  let total = 0;
  const gridTokens = [];
  for (const t of String(text ?? "").trim().split(/\s+/).filter(Boolean)) {
    if (/^g:/i.test(t)) {
      const g = t.slice(2);
      if (g.length % 4 !== 0) issues.push({ level: "error", msg: `${label}: ${t} は ${g.length} 文字です（1拍＝4文字の倍数に。1小節＝${cells}文字）` });
      gridTokens.push(g);
      for (const c of g) { if (!/[.\-]/.test(c)) out.push({ start: at, dur: 0.25, c }); at += 0.25; }
      continue;
    }
    if (/^t:/i.test(t)) {
      const g = t.slice(2);
      if (g.length % 3 !== 0) issues.push({ level: "error", msg: `${label}: ${t} は ${g.length} 文字です（三連は3文字で1拍。4/4の1小節は12文字）` });
      for (const c of g) { if (!/[.\-]/.test(c)) out.push({ start: at, dur: 1 / 3, c }); at += 1 / 3; }
      continue;
    }
    const m = /^([^:]+):(\d+(?:\.\d+)?)/.exec(t);
    if (!m) continue;
    const d = Number(m[2]);
    if (!/^[Rr]$/.test(m[1])) out.push({ start: at, dur: d, c: m[1] });
    at += d;
  }
  total = at;
  return { onsets: out, total, gridTokens };
}

/**
 * @param {any} song AIソング形式のJSON
 * @param {{ edition?: "modern"|"real" }} [opts]
 */
export function checkGroove(song, opts = {}) {
  const issues = [];
  const bpm = num(song.bpm) || 120;
  const beats = Math.round(num(song.beats) || 4);
  const cells = beats * 4;
  const genre = song.drumGenre;
  const edition = opts.edition === "real" ? 1.6 : 1;
  const parts = Array.isArray(song.parts) ? song.parts : [];
  const pushBeats = (p) => (Number.isFinite(num(p.push)) ? num(p.push) : 0) + (Number.isFinite(num(p.pushMs)) ? (num(p.pushMs) * bpm) / 60000 : 0);

  // 1. push の大きさ・キックとベースの push
  parts.forEach((p, i) => {
    const label = `parts[${i}]（${p?.role ?? p?.instrument ?? "?"}）`;
    const pb = pushBeats(p);
    if (Math.abs(pb) > 0.05 + 1e-9) issues.push({ level: "warn", msg: `${label}: push が ${pb.toFixed(3)} 拍（${((pb * 60000) / bpm).toFixed(0)}ms）です。±0.05 拍（120bpm で約 30ms）以内にしてください。意図的なら無視` });
    if (p?.instrument === "kick" && Math.abs(pb) > 1e-9) issues.push({ level: "warn", msg: `${label}: キックの push は 0 が基準です（スネアを＋、ハットを−に）` });
    if ((p?.instrument === "bass" || p?.instrument === "slap") && (pb < -1e-9 || pb > 0.015 + 1e-9)) issues.push({ level: "warn", msg: `${label}: ベースの push は 0〜+0.01 拍にしてください（キックとのロックイン。${pb.toFixed(3)} 拍）。lockToKick: true も使えます` });
  });

  // 2. human の上限
  const human = num(song.human);
  if (Number.isFinite(human) && human > 0) {
    const limit = genre && HUMAN_LIMIT[genre] !== undefined ? HUMAN_LIMIT[genre] : 0.6;
    if (human > limit + 1e-9) issues.push({ level: "warn", msg: `human ${human} は ${genre ?? "標準"} の目安（${limit}）を超えています` });
    const ms = 4.9 * edition * (1 + 4 * Math.min(1, human)) * (125 / bpm) * 1.0;
    if (ms > MAX_MS) issues.push({ level: "warn", msg: `human ${human}（bpm ${bpm}${edition > 1 ? "・real版" : ""}）だと楽器の最大のずれが約 ${ms.toFixed(0)}ms で、${MAX_MS}ms を超えて外れて聞こえます。human を下げてください` });
  }

  // 3. ドラムの volume
  parts.forEach((p, i) => {
    if (DRUM.has(p?.instrument) && num(p.volume) > 0.18 + 1e-9) issues.push({ level: "warn", msg: `parts[${i}]（${p.role ?? p.instrument}）: ドラムの volume ${p.volume} は 0.18 を超えています。X が 127 に張りつき、x との差が消えます（目安 0.10〜0.15）` });
  });

  // 4. 6拍子（複合拍子）の swing
  const sw = num(song.swing);
  if (beats === 6 && Number.isFinite(sw) && sw > 0) issues.push({ level: "warn", msg: `beats 6（6/8 系）に swing ${sw} がかかっています。3つ1組が崩れます。三連の感じは音の長さで書いてください` });
  parts.forEach((p, i) => { if (beats === 6 && num(p?.swing) > 0) issues.push({ level: "warn", msg: `parts[${i}]: beats 6 のパートに swing がかかっています` }); });

  // 5. 格子の長さ・ベタ打ち・同じ小節のコピー・シンコペ率
  const syncAll = [];
  parts.forEach((p, i) => {
    if (!p || typeof p.instrument !== "string") return;
    const label = `parts[${i}]（${p.role ?? p.instrument}）`;
    const { onsets, total, gridTokens } = readOnsets(p.notes, label, issues, cells);
    if (DRUM.has(p.instrument) && gridTokens.length && total > 0 && Math.abs((total % beats) - 0) > 1e-6 && Math.abs((total % beats) - beats) > 1e-6) issues.push({ level: "error", msg: `${label}: 格子・音符の合計が ${total} 拍で、小節（${beats}拍）の倍数になりません。そのあとの小節がずれます` });
    const bars = [];
    for (const g of gridTokens) if (g.length % cells === 0) for (let k = 0; k < g.length; k += cells) bars.push(g.slice(k, k + cells));
    if (bars.length && p.instrument === "hihat" && cells === 16 && bars.every((b) => /^x+$/.test(b))) issues.push({ level: "warn", msg: `${label}: 全部 x のベタ打ちです。X（強く）と o（弱く）で強弱をつけてください` });
    let run = 1, max = 1;
    for (let k = 1; k < bars.length; k++) { run = bars[k] === bars[k - 1] ? run + 1 : 1; max = Math.max(max, run); }
    if (max >= 8) issues.push({ level: "warn", msg: `${label}: 同じ小節が ${max} 回続きます。2〜4小節ごとに型を変えてください` });
    if (RHYTHM_FOR_SYNC.has(p.instrument)) for (const o of onsets) syncAll.push(o.start);
  });
  if (syncAll.length >= 16) {
    const off = syncAll.filter((b) => Math.abs(b - Math.round(b)) > 1e-3).length;
    const rate = off / syncAll.length;
    if (rate === 0) issues.push({ level: "warn", msg: `シンコペ率が 0%（リズムのパートが全部、拍の頭に鳴る）です。機械的に聞こえます。裏拍や先取りを少し足してください（0.2〜0.7 が目安）` });
    else if (rate > 0.9) issues.push({ level: "warn", msg: `シンコペ率が ${(rate * 100).toFixed(0)}% です。拍の感じが分からなくなるので、拍の頭の音を残してください` });
  }
  return issues;
}
