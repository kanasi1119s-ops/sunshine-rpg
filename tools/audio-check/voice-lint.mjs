// 声部の点検（docs/sound/counterpoint-voicing-guide.md §9 の提案 1・2・3・6・9）。
// score-check.mjs から呼ぶ。純粋関数だけで、ファイルは読まない。警告のみで、曲の生成は止めない。
// parts は [{ instrument, role, seq: [{t, dur, pitch, name}] }]（ドラムは含めない。score-lib.mjs の expand の結果）。
import { chordPcs, midiName, pcName } from "./score-lib.mjs";

const label = (p, i) => `${p.role || p.instrument}（${i + 1}番目・${p.instrument}）`;
const barOf = (t, beats) => Math.floor(t / beats + 1e-9) + 1;

/** 時刻 t に鳴っている音（なければ null）。seq は t の昇順。 */
export function soundingAt(seq, t) {
  let cur = null;
  for (const n of seq) {
    if (n.t > t + 1e-9) break;
    if (n.t + n.dur > t + 1e-9) cur = n;
  }
  return cur;
}

/** 拍の頭（1拍ごと）の音を、パートごとに並べる。戻り値: parts と同じ長さの配列で、各要素は拍ごとの音（なければ null）。 */
export function sampleBeats(parts, totalBeats, step = 1) {
  const cols = [];
  for (let t = 0; t < totalBeats - 1e-9; t += step) cols.push(t);
  return { times: cols, rows: parts.map((p) => cols.map((t) => soundingAt(p.seq, t))) };
}

const dir = (x) => (x > 0 ? 1 : x < 0 ? -1 : 0);

/** 意図した重ねか: 役割に「重ね」「下で」「ハモ」「パワー」を含む */
const intentionalRole = (p) => /重ね|下で|ハモ|パワー|オクターブ/.test(p.role ?? "");

/**
 * 提案1: 平行5度・8度の検出（全ペア）。拍の頭の音で、前後2点とも両方が動き、同じ向きで、
 * 音程が完全5度（7半音）またはオクターブ（12の倍数）。ペアの中でその音程が6割以上を占めるときは
 * 「重ね」「パワーコード」とみなして除外する。同じペアで minCount 回以上あれば警告に入れる。
 * skip は除外するペアの判定 (i, j) => boolean（旋律×ベースが別の点検にあるときなど）。
 */
export function findParallels(parts, totalBeats, { minCount = 4, skip = () => false } = {}) {
  const { times, rows } = sampleBeats(parts, totalBeats);
  const out = [];
  for (let i = 0; i < parts.length; i++) {
    for (let j = i + 1; j < parts.length; j++) {
      if (skip(i, j) || intentionalRole(parts[i]) || intentionalRole(parts[j])) continue;
      let count = 0, same = 0, total = 0, first = null;
      let prev = null;
      for (let k = 0; k < times.length; k++) {
        const a = rows[i][k], b = rows[j][k];
        if (!a || !b) { prev = null; continue; }
        const iv = Math.abs(a.pitch - b.pitch);
        const cls = iv % 12 === 7 ? 7 : iv % 12 === 0 && iv > 0 ? 0 : -1;
        total++;
        if (cls >= 0) same++;
        if (prev && cls >= 0 && prev.cls === cls) {
          const da = a.pitch - prev.a, db = b.pitch - prev.b;
          if (da !== 0 && db !== 0 && dir(da) === dir(db)) { count++; first ??= times[k]; }
        }
        prev = { a: a.pitch, b: b.pitch, cls };
      }
      if (total && same / total >= 0.6) continue; // 重ね・パワーコード（意図）
      if (count >= minCount) out.push({ a: i, b: j, count, bar: first, nameA: label(parts[i], i), nameB: label(parts[j], j) });
    }
  }
  return out;
}

/**
 * 提案2: 声部交差の検出。同じ楽器名が複数のパートにあるとき、平均の高さの低い順を基準の並びとして、
 * 拍の頭に並びが入れ替わった回数を数える。意図した交差もあるので警告のみ。
 */
export function findVoiceCrossings(parts, totalBeats, { minCount = 2 } = {}) {
  const byInst = new Map();
  parts.forEach((p, i) => { if (!byInst.has(p.instrument)) byInst.set(p.instrument, []); byInst.get(p.instrument).push(i); });
  const out = [];
  for (const [inst, idxs] of byInst) {
    if (idxs.length < 2) continue;
    const mean = idxs.map((i) => parts[i].seq.reduce((s, n) => s + n.pitch, 0) / Math.max(1, parts[i].seq.length));
    const order = idxs.map((_, k) => k).sort((a, b) => mean[a] - mean[b]).map((k) => idxs[k]); // 低→高
    const sub = order.map((i) => parts[i]);
    const { times, rows } = sampleBeats(sub, totalBeats);
    let count = 0, first = null;
    for (let k = 0; k < times.length; k++) {
      let crossed = false;
      for (let x = 0; x < sub.length && !crossed; x++) {
        for (let y = x + 1; y < sub.length; y++) {
          const lo = rows[x][k], hi = rows[y][k];
          if (lo && hi && lo.pitch > hi.pitch) { crossed = true; break; }
        }
      }
      if (crossed) { count++; first ??= times[k]; }
    }
    if (count >= minCount) out.push({ instrument: inst, count, bar: first, parts: order.map((i) => label(parts[i], i)) });
  }
  return out;
}

/**
 * 提案3: 隠れ5度・8度（外声）。最高声（outer の top）と最低声（bottom）が、同じ向きに動いて
 * 完全5度・8度に着く。ただし最高声が順次（2半音以下）なら除外。すでに完全音程だった（平行）ものも除く。
 */
export function findHiddenPerfects(top, bottom, totalBeats, { minCount = 4 } = {}) {
  const { times, rows } = sampleBeats([top, bottom], totalBeats);
  let count = 0, first = null;
  for (let k = 1; k < times.length; k++) {
    const [t0, t1] = [rows[0][k - 1], rows[0][k]], [b0, b1] = [rows[1][k - 1], rows[1][k]];
    if (!t0 || !t1 || !b0 || !b1) continue;
    const dt = t1.pitch - t0.pitch, db = b1.pitch - b0.pitch;
    if (dt === 0 || db === 0 || dir(dt) !== dir(db)) continue;
    if (Math.abs(dt) <= 2) continue; // 最高声が順次
    const ivNow = Math.abs(t1.pitch - b1.pitch) % 12, ivPrev = Math.abs(t0.pitch - b0.pitch) % 12;
    const perfectNow = (ivNow === 7 || ivNow === 0) && t1.pitch !== b1.pitch;
    const perfectPrev = ivPrev === 7 || ivPrev === 0;
    if (perfectNow && !perfectPrev) { count++; first ??= times[k]; }
  }
  return { count, bar: first, warn: count >= minCount };
}

/**
 * 提案6: 低音域の間隔チェック。拍の頭に同時に鳴っている音を、高さ順に隣どうし比べ、
 * C3（MIDI 48）より下で3度（3〜4半音）、E3（52）より下で2度（1〜2半音）のものを数えて、パート名を挙げる。
 */
export function findLowMuddy(parts, totalBeats) {
  const { times, rows } = sampleBeats(parts, totalBeats);
  const hits = new Map();
  for (let k = 0; k < times.length; k++) {
    const ns = rows.map((r, i) => (r[k] ? { i, p: r[k].pitch } : null)).filter(Boolean).sort((a, b) => a.p - b.p);
    for (let x = 0; x + 1 < ns.length; x++) {
      const lo = ns[x], hi = ns[x + 1];
      const iv = hi.p - lo.p;
      if (iv === 0 || lo.i === hi.i) continue;
      const third = lo.p < 48 && iv >= 3 && iv <= 4;
      const second = lo.p < 52 && iv >= 1 && iv <= 2;
      if (!third && !second) continue;
      const key = `${lo.i}-${hi.i}-${third ? "3" : "2"}`;
      const h = hits.get(key) ?? { count: 0, bar: times[k], kind: third ? "3度" : "2度", lo: lo.i, hi: hi.i, pitch: lo.p };
      h.count++;
      hits.set(key, h);
    }
  }
  return [...hits.values()].map((h) => ({ ...h, nameLo: label(parts[h.lo], h.lo), nameHi: label(parts[h.hi], h.hi) }));
}

/**
 * 提案9: 保持音（ペダル）の補助。和音列（小節ごとのコード名）と度数（"root" か "fifth"）から、
 * 最初の和音のその度数を保持する長い音の列（notes の記法）を返す。和音が替わって保持音が和音外になる小節は warnings に出す。
 * octave は保持音の高さ（既定 2 = 低い所）。同じ高さがつづく間は1つの長い音にまとめ、全体の拍数は小節数×beats。
 */
export function pedalLine(chordNames, { degree = "root", beats = 4, octave = 2 } = {}) {
  const first = chordPcs(chordNames[0]);
  if (!first) throw new Error(`読めないコードです: ${chordNames[0]}`);
  const pc = degree === "fifth" ? (first.root + 7) % 12 : first.root;
  const name = `${pcName(pc)}${octave}`;
  const warnings = [];
  chordNames.forEach((c, i) => {
    const cp = chordPcs(c);
    if (cp && !cp.pcs.has(pc)) warnings.push(`${i + 1}小節目（${c}）で保持音 ${pcName(pc)} が和音の外になる。解決するか、保持音を替える`);
  });
  const total = chordNames.length * beats;
  return { notes: `${name}:${total}`, pitch: name, warnings, total };
}

/** 点検をまとめて実行する。skipPairs は findParallels の skip。戻り値は score-check と同じ { level, msg } の配列。 */
export function voiceLint(parts, { beats = 4, totalBeats, melodyIndex = -1, bassIndex = -1 } = {}) {
  const res = [];
  const skip = (i, j) => melodyIndex >= 0 && bassIndex >= 0 && ((i === melodyIndex && j === bassIndex) || (i === bassIndex && j === melodyIndex));
  const par = findParallels(parts, totalBeats, { skip });
  if (par.length) for (const p of par.slice(0, 4)) res.push({ id: "C1", level: "warn", msg: `平行5度・8度: ${p.nameA} と ${p.nameB} で${p.count}回（${barOf(p.bar, beats)}小節目から。拍の頭で判定）` });
  else res.push({ id: "C1", level: "ok", msg: "ほかのパートの組み合わせに平行5度・8度のまとまった連続なし" });
  const cr = findVoiceCrossings(parts, totalBeats);
  if (cr.length) for (const c of cr) res.push({ id: "C2", level: "warn", msg: `声部交差: 同じ楽器（${c.instrument}）のパートの上下が${c.count}回入れ替わる（${barOf(c.bar, beats)}小節目から）。意図したハモリの入れ替えならそのまま` });
  else res.push({ id: "C2", level: "ok", msg: "同じ楽器のパートで声部交差なし" });
  if (melodyIndex >= 0 && bassIndex >= 0) {
    const h = findHiddenPerfects(parts[melodyIndex], parts[bassIndex], totalBeats);
    res.push(h.warn ? { id: "C3", level: "warn", msg: `隠れ5度・8度: 旋律とベースが同じ向きに跳んで完全5度・8度に着く所が${h.count}回（${barOf(h.bar, beats)}小節目から。ロック系では許容されることも多い）` } : { id: "C3", level: "ok", msg: "旋律とベースの隠れ5度・8度は少ない" });
  }
  const low = findLowMuddy(parts, totalBeats);
  if (low.length) for (const l of low.slice(0, 3)) res.push({ id: "C6", level: "warn", msg: `低音域の${l.kind}: ${l.nameLo} と ${l.nameHi} が ${midiName(l.pitch)} 付近でぶつかる（${l.count}回・${barOf(l.bar, beats)}小節目から）。低い所は5度かオクターブに` });
  else res.push({ id: "C6", level: "ok", msg: "C3より下の3度・E3より下の2度の濁りなし" });
  return res;
}
