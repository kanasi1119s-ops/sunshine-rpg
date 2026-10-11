// 対旋律・カノン・保持音の生成（docs/sound/counterpoint-voicing-guide.md §9 の提案 7・8・10。9 の pedalLine は tools/audio-check/voice-lint.mjs）。
// どれも「音名:拍」の文字列 → 文字列の純粋関数。結果は拍の合計が元の旋律とそろう。
// CLI: node tools/composer/song.mjs counter <曲.json> [--part 番号] [--above] [--enter 小節] / canon "<notes>" --delay 4 [--transpose 7] [--invert] [--factor 2]
import { parseNotes, midi, midiName, chordPcs, estimateKey } from "../audio-check/score-lib.mjs";

const fmt = (x) => String(+x.toFixed(4));

/** 音の並び（休符は pitch=null）を文字列へ */
export function formatNotes(list) {
  return list.map((n) => `${n.pitch == null ? "R" : midiName(n.pitch)}:${fmt(n.dur)}${n.mark ?? ""}`).join(" ");
}

/** notes の文字列の拍の合計 */
export const notesTotal = (str) => parseNotes(str).total;

// ---- 提案8: カノン／模倣 ----------------------------------------------------

/**
 * canonOf: notes 列をもとに、遅れて入る模倣のパートを返す。
 *   delay     … 遅れ幅（拍）。先頭に R:delay を置く
 *   transpose … 移調（半音）。5度上なら 7
 *   invert    … true で反行（最初の音を軸にして上下を反転）
 *   factor    … 拡大（2）・縮小（0.5）の倍率
 *   total     … 合計の拍数（省略は元の列の合計）。末尾を R で埋める。長すぎるときは切る
 */
export function canonOf(str, { delay = 0, transpose = 0, invert = false, factor = 1, total } = {}) {
  const { notes, total: orig } = parseNotes(str);
  const want = total ?? orig;
  const firstPitch = notes.find((n) => !n.rest)?.pitch;
  const out = [];
  if (delay > 0) out.push({ pitch: null, dur: delay, mark: "" });
  for (const n of notes) {
    let pitch = n.rest ? null : n.pitch;
    if (pitch != null) {
      if (invert && firstPitch != null) pitch = 2 * firstPitch - pitch;
      pitch += transpose;
    }
    out.push({ pitch, dur: n.dur * factor, mark: n.mark });
  }
  // 合計をそろえる: 長ければ後ろを切り、短ければ末尾に休符
  let sum = 0;
  const fitted = [];
  for (const n of out) {
    if (sum + n.dur > want + 1e-9) {
      const rest = want - sum;
      if (rest > 1e-9) fitted.push({ ...n, dur: rest });
      sum = want;
      break;
    }
    fitted.push(n);
    sum += n.dur;
  }
  if (want - sum > 1e-9) fitted.push({ pitch: null, dur: want - sum, mark: "" });
  return formatNotes(fitted);
}

// ---- 提案7: 対旋律の自動生成 ------------------------------------------------

const SCALE_MAJ = [0, 2, 4, 5, 7, 9, 11], SCALE_MIN = [0, 2, 3, 5, 7, 8, 10];

function gridFor(total) {
  for (const g of [0.5, 0.25, 0.125]) if (Math.abs(total / g - Math.round(total / g)) < 1e-6) return g;
  return 0.125;
}

/** 旋律をスロットに分ける: 各スロットで鳴っている音の高さ（なければ null）と、そのスロットが音の頭かどうか */
function slotsOfMelody(notes, total, grid) {
  const n = Math.round(total / grid);
  const slots = Array.from({ length: n }, () => ({ pitch: null, onset: false }));
  for (const m of notes) {
    if (m.rest) continue;
    const a = Math.round(m.t / grid), b = Math.round((m.t + m.dur) / grid);
    for (let i = a; i < b && i < n; i++) slots[i] = { pitch: m.pitch, onset: i === a };
  }
  return slots;
}

/**
 * generateCounter: 旋律と和音から、対旋律を1本つくる（動的計画法で全体のコストが最小の道を選ぶ）。
 *   melody … 旋律の notes 文字列
 *   chords … 小節ごとのコード名の配列（旋律の小節数ぶん。足りなければ最後をくり返す）
 *   options.beats … 1小節の拍数（既定4）
 *   options.place … "below"（旋律の下。既定）か "above"
 *   options.lo / hi … 音域（音名）。既定 below は C3〜C5、above は C4〜C6
 * 評価: ①旋律と逆向きに動く ②旋律が動かない所で動く（長い所は短く、短い所は保つ）
 *       ③強拍は和音の構成音 ④旋律との音程が協和（3度・6度が最良、完全5度・8度はやや減点、2度・7度・4度は減点）
 *       ⑤平行5度・8度は大きく減点 ⑥動きは順次が基本。返り値は notes の記法の文字列と、点検用の情報。
 */
export function generateCounter(melody, chords, { beats = 4, place = "below", lo, hi } = {}) {
  const { notes, total } = parseNotes(melody);
  if (total <= 0) throw new Error("旋律が空です");
  const grid = gridFor(total);
  const slots = slotsOfMelody(notes, total, grid);
  const bars = Math.ceil(total / beats - 1e-9);
  const chordList = Array.from({ length: bars }, (_, i) => chords[Math.min(chords.length - 1, i)]);
  const cps = chordList.map((c) => chordPcs(c));
  if (cps.some((c) => !c)) throw new Error("読めないコードがあります");
  const key = estimateKey(chordList);
  const scaleSet = new Set((key?.minor ? SCALE_MIN : SCALE_MAJ).map((x) => ((key?.tonic ?? 0) + x) % 12));
  const above = place === "above";
  const LO = midi(lo ?? (above ? "C4" : "C3")), HI = midi(hi ?? (above ? "C6" : "C5"));

  const strongAt = (i) => i % Math.round(1 / grid) === 0; // 拍の頭
  const bigStrong = (i) => i % Math.round((beats / 2) / grid) === 0; // 小節の頭と中央
  const cand = (i) => {
    const bar = Math.min(bars - 1, Math.floor((i * grid) / beats + 1e-9));
    const cp = cps[bar];
    const out = [{ p: null }];
    for (let p = LO; p <= HI; p++) {
      const isChord = cp.pcs.has(p % 12);
      if (!isChord && !scaleSet.has(p % 12)) continue;
      const m = slots[i].pitch;
      if (m != null) {
        const d = above ? p - m : m - p;
        if (d < 3) continue; // 旋律と同じ高さ・近すぎる・追い越しは使わない
        if (d > 19) continue;
      }
      out.push({ p, chord: isChord });
    }
    return out;
  };
  const harmonic = (p, m, i) => {
    if (p == null || m == null) return 0;
    const iv = Math.abs(m - p) % 12;
    const strong = strongAt(i);
    switch (iv) {
      case 3: case 4: case 8: case 9: return 0;
      case 0: return 2;
      case 7: return 0.6;
      case 5: return 1.2;
      default: return strong ? 4 : 1.4; // 2度・7度・トライトーンは強拍で強く減点
    }
  };

  const n = slots.length;
  const layers = [];
  for (let i = 0; i < n; i++) layers.push(cand(i));
  const CAP = Math.max(2, Math.round(2.5 / grid)); // 同じ音が続いた長さ（スロット数）の上限。これを状態に持つ
  const MINRUN = Math.max(1, Math.round(1 / grid)); // 1拍より短く動きつづけない
  const HOLDMAX = Math.max(2, Math.round(2 / grid)); // 2拍を超えて保持すると減点
  // 状態 = (候補 k, 続いた長さ run)。best[i] は Map(キー k*100+run → {cost, prev})
  const best = layers.map(() => new Map());
  const unary = (c, i) => {
    const m = slots[i].pitch;
    let cost = harmonic(c.p, m, i);
    if (c.p == null) cost += m != null ? 1.3 : 0.2;
    else {
      if (strongAt(i) && !c.chord) cost += bigStrong(i) ? 6 : 3;
      else if (!c.chord) cost += 0.6;
      if (m == null) cost += 0.3;
    }
    return cost;
  };
  layers[0].forEach((c, k) => best[0].set(k * 100 + 1, { cost: unary(c, 0), prev: null }));
  for (let i = 1; i < n; i++) {
    const m = slots[i].pitch, mPrev = slots[i - 1].pitch;
    layers[i].forEach((c, k) => {
      const base = unary(c, i);
      for (const [pkey, pst] of best[i - 1]) {
        const kp = Math.floor(pkey / 100), run = pkey % 100;
        const q = layers[i - 1][kp].p, p = c.p;
        let cost = pst.cost + base;
        let nextRun;
        if (p === q) {
          nextRun = Math.min(CAP, run + 1);
          if (run + 1 > HOLDMAX) cost += 0.4; // 長すぎる保持
          if (p != null && !slots[i].onset && m != null) cost += 0.05;
        } else {
          nextRun = 1;
          if (run < MINRUN) cost += 0.7; // 動きすぎ（1拍未満で次の音）
          if (p != null && q != null) {
            const step = Math.abs(p - q);
            cost += step <= 2 ? 0.1 : step <= 4 ? 0.6 : step <= 7 ? 1.8 : 4;
            if (m != null && mPrev != null && m !== mPrev) {
              const dm = Math.sign(m - mPrev), dc = Math.sign(p - q);
              if (dm !== dc) cost -= 0.8;
              else {
                const ivNow = Math.abs(m - p) % 12, ivPrev = Math.abs(mPrev - q) % 12;
                cost += 0.3;
                if ((ivNow === 7 || ivNow === 0) && ivNow === ivPrev) cost += 12; // 平行5度・8度
                else if (ivNow === 7 || ivNow === 0) cost += 3; // 隠れ5度・8度
              }
            }
          } else if (p != null && q == null) cost += 0.2;
          if (slots[i].onset) cost += 0.9; // 旋律が音を出す瞬間に動くと重なって聞こえる
        }
        const key = k * 100 + nextRun;
        const cur = best[i].get(key);
        if (!cur || cost < cur.cost) best[i].set(key, { cost, prev: pkey });
      }
    });
  }
  // 逆にたどる
  let sk = null, bc = Infinity;
  for (const [kk, st] of best[n - 1]) if (st.cost < bc) { bc = st.cost; sk = kk; }
  const picked = new Array(n);
  for (let i = n - 1; i >= 0; i--) {
    picked[i] = layers[i][Math.floor(sk / 100)].p;
    sk = best[i].get(sk).prev;
  }
  // 同じ高さのつづきを1つの音にまとめる
  const out = [];
  for (let i = 0; i < n; i++) {
    const last = out[out.length - 1];
    if (last && last.pitch === picked[i]) last.dur += grid;
    else out.push({ pitch: picked[i], dur: grid, mark: "" });
  }
  return { notes: formatNotes(out), total, grid };
}

// ---- 提案10: 「入り」の自動セクション ----------------------------------------

/**
 * 曲の sections（[{kind, bars}]）から、対旋律が入る小節（0から数える）を決める。
 * 同じ種類が2回出たら、その2回目の頭。なければ全体の後ろ半分の頭。
 */
export function enterBarFromSections(sections, totalBars) {
  if (Array.isArray(sections)) {
    let bar = 0;
    const seen = new Set();
    for (const s of sections) {
      if (s.kind === "intro" || s.kind === "outro") { bar += s.bars; continue; }
      if (seen.has(s.kind)) return bar;
      seen.add(s.kind);
      bar += s.bars;
    }
  }
  return Math.floor(totalBars / 2);
}

/**
 * counterEntering: 1周目は休み、enterBar 小節目から入る対旋律のパートを返す。
 * 旋律の enterBar 以降だけに generateCounter をかけ、前に R を置く。拍の合計は旋律と同じ。
 * 戻り値は song.parts に足せる { instrument, role, notes, volume, pan }。
 */
export function counterEntering(melody, chords, { beats = 4, enterBar, instrument = "strings", role = "対旋律（2周目から）", place = "below", volume = 0.5, pan = 0.4 } = {}) {
  const { notes, total } = parseNotes(melody);
  const totalBars = Math.ceil(total / beats - 1e-9);
  const enter = Math.max(0, Math.min(totalBars - 1, enterBar ?? Math.floor(totalBars / 2)));
  const from = enter * beats;
  // 入り以降の旋律を切り出す（途中をまたぐ音は入りの位置で切る）
  const tail = [];
  for (const n of notes) {
    const end = n.t + n.dur;
    if (end <= from + 1e-9) continue;
    const t0 = Math.max(n.t, from);
    tail.push({ pitch: n.rest ? null : n.pitch, dur: end - t0, mark: n.mark });
  }
  const tailStr = formatNotes(tail);
  const gen = generateCounter(tailStr, chords.slice(enter), { beats, place });
  const lead = from > 0 ? `R:${fmt(from)} ` : "";
  return { instrument, role, notes: lead + gen.notes, volume, pan, enterBar: enter };
}
