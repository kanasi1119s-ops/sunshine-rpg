// 書き出したWAVの合否表（docs/sound/ai-composition-workflow.md の提案 4・5）。
//   node tools/composer/song.mjs gate <曲.wav> [--target -14] [--save <曲ID>] [--json]
//   node tools/composer/song.mjs gate-compare <曲.wav> <基準.wav>   … 音量（LUFS）をそろえてから、帯域ごとの差を数字で出す
// ffmpeg の ebur128 で、統合ラウドネス（LUFS）・真のピーク・ラウドネスレンジ（LRA）・PLR・頭の大きさ・途中の無音を測り、左右の相関も出して、
// 目安（ai-composition-workflow.md の C-3 の表）と比べて「○／要直し」を日本語で出す。数字だけを保存する（曲の音は入れない）。
import { spawnSync } from "child_process";
import fs from "fs";
import path from "path";

/** 判定表。値は measureWav の戻り値。target は目標の統合ラウドネス。 */
export function judge(m, { target = -14 } = {}) {
  const rows = [];
  const add = (key, label, value, unit, goal, ok, hint) => rows.push({ key, label, value, unit, goal, ok, hint: ok ? "" : hint });
  const f = (x, d = 1) => (Number.isFinite(x) ? Number(x.toFixed(d)) : null);
  add("lufs", "統合ラウドネス", f(m.lufs), "LUFS", `${target} ±1.5`, Number.isFinite(m.lufs) && Math.abs(m.lufs - target) <= 1.5, "volume の合計を調整する。リミッターだけで稼がない（--master で目標にそろえられる）。");
  add("tp", "真のピーク", f(m.tp), "dBTP", "-1.0 以下", Number.isFinite(m.tp) && m.tp <= -1.0, "全体の音量を下げる。歪みギターの volume を下げる。");
  add("lra", "ラウドネスレンジ", f(m.lra), "LU", "4〜8", Number.isFinite(m.lra) && m.lra >= 4 && m.lra <= 8, m.lra < 4 ? "セクション表の強さ差を広げる。dynamics: \"natural\"。サビ前に引く。" : "大きすぎる。静かな所を持ち上げるか、山を少し下げる（ゲーム中の音量差に注意）。");
  add("plr", "PLR（ピーク−ラウドネス）", f(m.plr), "dB", "9 以上", Number.isFinite(m.plr) && m.plr >= 9, "潰れ気味。圧縮を浅く、パートの足しすぎをやめる。");
  add("corr", "左右の相関", f(m.corr, 2), "", "0.4〜0.88", Number.isFinite(m.corr) && m.corr >= 0.4 && m.corr <= 0.88, m.corr > 0.88 ? "ほぼモノラル。和音の楽器を左右に振る（pan）。--widen。" : "左右がばらけすぎ。低音とリードは中央に。");
  add("head", "頭の大きさ（最初の10秒−曲のいちばん大きい所）", f(m.headVsMax), "LU", "-1.5 以下", Number.isFinite(m.headVsMax) && m.headVsMax <= -1.5, "頭が最大音量と同じ。小さく始めるなら導入の volume を下げる（「いきなり全員」の曲なら意図どおりで可）。");
  add("silence", "途中の無音（4秒以上）", m.midSilences.length, "か所", "0", m.midSilences.length === 0, `無音の位置: ${m.midSilences.map((s) => `${s.start.toFixed(0)}秒〜`).join("・")}。意図したものでなければ、パートの入りを確かめる。`);
  return rows;
}

export function formatGate(m, rows, name = "") {
  const ng = rows.filter((r) => !r.ok);
  const out = [`■ 合否表${name ? `「${name}」` : ""}（${m.durationSec.toFixed(0)}秒）: ${ng.length ? `要直し ${ng.length}件` : "すべて○"}`];
  for (const r of rows) out.push(`  ${r.ok ? "○" : "要直し"}　${r.label}: ${r.value ?? "測れず"}${r.unit ? " " + r.unit : ""}（目安 ${r.goal}）${r.hint ? "\n        → " + r.hint : ""}`);
  out.push("  ※ 数字は耳の代わりにならない。直したら同じ測定をもう一度回し、結果を song.mjs log で1行残す。タイミングのずれ・帯域は analyze.py／realism.py（tools/audio-check）。");
  return out.join("\n");
}

const run = (args, input) => spawnSync("ffmpeg", args, { encoding: "utf8", maxBuffer: 1 << 28, input });

/** WAV を測る（ffmpeg が必要）。 */
export function measureWav(file) {
  if (!fs.existsSync(file)) throw new Error(`ファイルがありません: ${file}`);
  const r = run(["-nostats", "-i", file, "-af", "ebur128=peak=true,silencedetect=n=-60dB:d=4", "-f", "null", "-"]);
  if (r.error) throw new Error("ffmpeg が使えません（インストールしてください）");
  const text = r.stderr ?? "";
  const sum = text.slice(text.lastIndexOf("Summary:"));
  const num = (re, s = sum) => { const m = re.exec(s); return m ? Number(m[1]) : NaN; };
  const lufs = num(/I:\s+(-?[\d.]+) LUFS/), lra = num(/LRA:\s+(-?[\d.]+) LU/), tp = num(/True peak:\s*\n\s*Peak:\s+(-?[\d.]+) dBFS/);
  const durM = /Duration: (\d+):(\d+):([\d.]+)/.exec(text);
  const durationSec = durM ? Number(durM[1]) * 3600 + Number(durM[2]) * 60 + Number(durM[3]) : NaN;
  // 短時間ラウドネス（S）の推移
  const frames = [...text.matchAll(/t:\s*([\d.]+)\s+TARGET.*?S:\s*(-?[\d.]+|-inf)\s/g)].map((m) => ({ t: Number(m[1]), s: m[2] === "-inf" ? -120 : Number(m[2]) }));
  const maxS = Math.max(...frames.filter((x) => x.t >= 3).map((x) => x.s), -120);
  const headS = Math.max(...frames.filter((x) => x.t >= 3 && x.t <= 10).map((x) => x.s), -120);
  // 無音（曲の頭と終わりの余韻は数えない）
  const sil = [...text.matchAll(/silence_start: ([\d.]+)/g)].map((m) => Number(m[1]));
  const ends = [...text.matchAll(/silence_end: ([\d.]+)/g)].map((m) => Number(m[1]));
  const midSilences = sil.map((start, i) => ({ start, end: ends[i] ?? NaN })).filter((s) => s.start > 1 && Number.isFinite(s.end) && s.end < durationSec - 1);
  // 左右の相関（ピアソン）
  const pcm = spawnSync("ffmpeg", ["-v", "error", "-i", file, "-f", "f32le", "-ac", "2", "-ar", "48000", "-"], { maxBuffer: 1 << 30 });
  let corr = NaN;
  if (pcm.stdout?.length >= 8) {
    const buf = pcm.stdout;
    const n = Math.floor(buf.length / 8);
    let sl = 0, sr = 0, sll = 0, srr = 0, slr = 0;
    for (let i = 0; i < n; i++) { const l = buf.readFloatLE(i * 8), rr = buf.readFloatLE(i * 8 + 4); sl += l; sr += rr; sll += l * l; srr += rr * rr; slr += l * rr; }
    const cov = slr / n - (sl / n) * (sr / n), vl = sll / n - (sl / n) ** 2, vr = srr / n - (sr / n) ** 2;
    corr = vl > 0 && vr > 0 ? cov / Math.sqrt(vl * vr) : NaN;
  }
  return { lufs, tp, lra, plr: tp - lufs, corr, headVsMax: headS - maxS, midSilences, durationSec };
}

/** 数字だけを docs/sound/data/ours/<ID>.json に保存する（過去の曲との比較・推移用）。 */
export function saveMeasurement(root, id, m, rows, target) {
  if (!/^[a-z0-9][a-z0-9-]*$/.test(id)) throw new Error(`曲IDは英小文字・数字・「-」だけ（${id}）`);
  const dir = path.join(root, "docs", "sound", "data", "ours");
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `${id}.json`);
  const prev = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : { id, history: [] };
  const entry = { date: new Date().toISOString().slice(0, 10), target, lufs: rows[0].value, tp: rows[1].value, lra: rows[2].value, plr: rows[3].value, corr: rows[4].value, headVsMax: rows[5].value, midSilences: rows[6].value, ng: rows.filter((r) => !r.ok).map((r) => r.key) };
  prev.history.push(entry);
  fs.writeFileSync(file, JSON.stringify(prev, null, 1) + "\n");
  return { file, previous: prev.history.length > 1 ? prev.history[prev.history.length - 2] : null, entry };
}

export const BANDS = [["sub", 20, 60], ["bass", 60, 250], ["lowmid", 250, 500], ["mid", 500, 2000], ["highmid", 2000, 5000], ["high", 5000, 16000]];

function bandDb(file, lo, hi, gainDb) {
  const r = run(["-nostats", "-i", file, "-af", `volume=${gainDb.toFixed(2)}dB,highpass=f=${lo}:poles=2,lowpass=f=${hi}:poles=2,astats=metadata=0:reset=0`, "-f", "null", "-"]);
  const all = [...(r.stderr ?? "").matchAll(/RMS level dB:\s*(-?[\d.]+|-inf)/g)];
  const last = all[all.length - 1]; // 末尾は全体
  return last ? Number(last[1]) : NaN;
}

/** 音量（LUFS）をそろえてから、帯域ごとのRMSの差（a − b）を出す。 */
export function compareBands(a, b) {
  const la = measureWav(a).lufs, lb = measureWav(b).lufs;
  const gain = lb - la; // a を b の大きさにそろえる
  const rows = BANDS.map(([name, lo, hi]) => {
    const da = bandDb(a, lo, hi, gain), db = bandDb(b, lo, hi, 0);
    return { band: name, range: `${lo}〜${hi}Hz`, a: da, b: db, diff: da - db };
  });
  return { gain, lufsA: la, lufsB: lb, rows };
}

export function formatCompare(c, nameA = "曲", nameB = "基準") {
  const out = [`■ 帯域の比較（${nameA} を ${nameB} の大きさ ${c.lufsB.toFixed(1)} LUFS にそろえて ${c.gain >= 0 ? "+" : ""}${c.gain.toFixed(1)} dB。差=${nameA}−${nameB}）`];
  for (const r of c.rows) out.push(`  ${r.band.padEnd(8)} ${r.range.padEnd(14)} ${nameA} ${r.a.toFixed(1)} / ${nameB} ${r.b.toFixed(1)} dB　差 ${r.diff >= 0 ? "+" : ""}${r.diff.toFixed(1)} dB${Math.abs(r.diff) >= 4 ? "　← 偏り" : ""}`);
  out.push("  ※ 曲を真似るためでなく、帯域・ダイナミクスの偏りを見つけるために使う。同ジャンルの基準を選ぶ。");
  return out.join("\n");
}
