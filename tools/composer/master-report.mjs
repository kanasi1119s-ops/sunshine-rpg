// 書き出しの合否表（master-report）とループの継ぎ目。docs/sound/mastering-guide.md の提案 10・11 を入れたもの。
//   masterReport(wav, {lufs, tp, loop}) … I・TP・LRA・PLR・PSR・左右の相関・100Hz 以下の相関・継ぎ目・雑音を 1 行で ○／要直し
//   loopCheck(wav)                     … 先頭・末尾の段差、継ぎ目の前後の大きさの差
//   loopTailWrap(wav, T)               … 書き出しの末尾（T 秒より後ろ＝残響の尾）を先頭に重ねて T 秒に切る（テールラップ）
import { execSync } from "child_process";
import fs from "fs";
import { spectralMetrics } from "./spectral-metrics.mjs";
import { genreJudge } from "./genre-targets.mjs";
import { fileURLToPath } from "url";

/** 雑音の検知（tools/audio-check/noise-check.py。音割れ・直流・超低域・プチッ）。Python がないなどで測れないときは null */
export function noiseCheck(file, { vocal = false, notes = "", bpm = NaN } = {}) {
  try {
    const py = fileURLToPath(new URL("../audio-check/noise-check.py", import.meta.url));
    const extra = `${vocal ? " --vocal" : ""}${notes ? ` --notes "${notes}"` : ""}${Number.isFinite(bpm) ? ` --bpm ${bpm}` : ""}`;
    return JSON.parse(sh(`python3 "${py}" "${file}" --json${extra}`).trim().split("\n").pop());
  } catch { return null; }
}

const sh = (cmd) => execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], maxBuffer: 1 << 28 });

/** wav を f32 のステレオで読む（filter があれば先にかける） */
export function readPcm(file, { filter = "", sr = 48000 } = {}) {
  const buf = execSync(`ffmpeg -v error -i "${file}" ${filter ? `-af "${filter}"` : ""} -ac 2 -ar ${sr} -f f32le -`, { maxBuffer: 1 << 29 });
  const a = new Float32Array(buf.buffer, buf.byteOffset, Math.floor(buf.byteLength / 4));
  const n = a.length >> 1, L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = a[2 * i]; R[i] = a[2 * i + 1]; }
  return { L, R, sr, n };
}

/** 2 つの波形の相関（-1〜1）。どちらかが無音なら 1 */
export function correlation(a, b) {
  let sa = 0, sb = 0, sab = 0;
  for (let i = 0; i < a.length; i++) { sa += a[i] * a[i]; sb += b[i] * b[i]; sab += a[i] * b[i]; }
  return sa < 1e-12 || sb < 1e-12 ? 1 : sab / Math.sqrt(sa * sb);
}

/** I・LRA・True Peak・Short-term の最大（PSR 用）を ebur128 で測る */
export function measureAll(file) {
  const out = sh(`ffmpeg -hide_banner -nostats -i "${file}" -af ebur128=peak=true -f null - 2>&1`);
  const last = (re) => { const m = [...out.matchAll(re)].pop(); return m ? Number(m[1]) : NaN; };
  const shorts = [...out.matchAll(/\bS:\s+(-?[\d.]+)/g)].map((m) => Number(m[1])).filter((v) => v > -100);
  return { I: last(/\bI:\s+(-?[\d.]+) LUFS/g), LRA: last(/\bLRA:\s+(-?[\d.]+) LU/g), TP: last(/\bPeak:\s+(-?[\d.]+) dBFS/g), shortMax: shorts.length ? Math.max(...shorts) : NaN };
}

const rmsDb = (L, R, a, b) => {
  let s = 0;
  for (let i = a; i < b; i++) s += (L[i] * L[i] + R[i] * R[i]) / 2;
  return 10 * Math.log10(s / Math.max(1, b - a) + 1e-14);
};

/** 低域（cutoff Hz 以下）が全体に対して何 dB か。モノ化の前後で比べると、逆相気味の低音が消えたかが分かる */
export function lowShareDb(file, cutoff = 100) {
  const low = readPcm(file, { filter: `lowpass=f=${cutoff}:poles=2` }), all = readPcm(file);
  return rmsDb(low.L, low.R, 0, low.n) - rmsDb(all.L, all.R, 0, all.n);
}

/**
 * ループの継ぎ目の検査（末尾から先頭へ戻るところ）。
 * step: 末尾の最後の音と先頭の最初の音の段差を、末尾 20ms の「となりの音との差」で割ったもの（8 を超えたらプチッと鳴る恐れ）
 * jump100／jump400: 継ぎ目の前後 100ms／400ms の大きさの差（dB。6／4 を超えたら、つなぎ目で急に大きさが変わる）
 */
export function loopCheck(file, pcm = null) {
  const { L, R, sr, n } = pcm ?? readPcm(file);
  const warnings = [];
  if (n < sr) return { ok: true, step: 0, jump100: 0, jump400: 0, warnings: ["短いので継ぎ目は見ていません"] };
  const w20 = Math.round(sr * 0.02);
  let dsum = 0;
  for (let i = n - w20 + 1; i < n; i++) dsum += (((L[i] - L[i - 1]) ** 2) + ((R[i] - R[i - 1]) ** 2)) / 2;
  const diffRms = Math.sqrt(dsum / w20) + 1e-5;
  const jumpAbs = Math.max(Math.abs(L[n - 1] - L[0]), Math.abs(R[n - 1] - R[0]));
  const step = jumpAbs / diffRms;
  const seamDb = (win) => {
    const w = Math.round(sr * win);
    const a = rmsDb(L, R, n - w, n), b = rmsDb(L, R, 0, w);
    return a < -70 && b < -70 ? 0 : Math.abs(a - b);
  };
  const jump100 = seamDb(0.1), jump400 = seamDb(0.4);
  if (step > 8 && jumpAbs > 0.003) warnings.push(`継ぎ目に段差があります（波形の飛びが普段の ${step.toFixed(0)} 倍。プチッと鳴る恐れ）`);
  if (jump100 > 6) warnings.push(`継ぎ目の前後 100ms の大きさが ${jump100.toFixed(1)}dB ちがいます（曲の頭と終わりの大きさをそろえる）`);
  if (jump400 > 4) warnings.push(`継ぎ目の前後 400ms の大きさが ${jump400.toFixed(1)}dB ちがいます（残響の尾を先頭に重ねる --loop-tail を試す）`);
  return { ok: warnings.length === 0, step: Math.round(step * 10) / 10, jump100: Math.round(jump100 * 10) / 10, jump400: Math.round(jump400 * 10) / 10, warnings };
}

/**
 * テールラップ: T 秒より後ろ（残響の尾）を先頭に重ねて、T 秒の長さに切る。
 * 戻り値: { wrapped, tailSec }。尾が 0.2 秒に満たなければ何もせず wrapped=false。
 */
export function loopTailWrap(file, T) {
  const dur = Number(sh(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${file}"`).trim());
  const tailSec = dur - T;
  if (!(T > 1) || tailSec < 0.2) return { wrapped: false, tailSec: Math.max(0, tailSec) };
  const tmp = file + ".loop.wav";
  // 同じファイルを 2 つの入力にして渡す（1 つの入力を asplit で分ける書き方は、ffmpeg 6.1 で 0.02 秒で切れる）
  sh(`ffmpeg -y -loglevel error -i "${file}" -i "${file}" -filter_complex "[0]atrim=0:${T.toFixed(4)},asetpts=PTS-STARTPTS[body];[1]atrim=start=${T.toFixed(4)},asetpts=PTS-STARTPTS[tail];[body][tail]amix=inputs=2:normalize=0:duration=longest,atrim=0:${T.toFixed(4)}" -c:a pcm_s16le -map_metadata -1 -fflags +bitexact -flags:a +bitexact "${tmp}"`);
  fs.renameSync(tmp, file);
  return { wrapped: true, tailSec };
}

/**
 * 書き出しの合否表。opts: lufs（目標）・tp（天井 dBTP。既定 -1）・loop（継ぎ目を見るか）・plrMin・psrMin・lowCutoff（低域相関を測る上限 Hz。既定 100）。
 * 戻り値: { ok, line, metrics, issues }
 */
export function masterReport(file, { lufs = null, tp = -1, loop = false, plrMin = null, psrMin = null, lowCutoff = 100, genre = null, bpm = NaN, noise = true } = {}) {
  const m = measureAll(file);
  const pcm = readPcm(file);
  const corr = correlation(pcm.L, pcm.R);
  const low = readPcm(file, { filter: `lowpass=f=${lowCutoff}:poles=2` }); // 低域モノ化の周波数が 200Hz 未満のときは、その半分（モノ化の境目は少し漏れるため。song-lib が渡す）
  // 低域が全体よりずっと小さい曲（-30dB より下、または -55dBFS より小さい）は、残響の余りやディザの雑音の相関を測るだけになるので 1 とみなす
  const lowDb = rmsDb(low.L, low.R, 0, low.n), allDb = rmsDb(pcm.L, pcm.R, 0, pcm.n);
  const lowCorr = lowDb < -55 || lowDb - allDb < -30 ? 1 : correlation(low.L, low.R);
  const seam = loop ? loopCheck(file, pcm) : null;
  const PLR = m.TP - m.I, PSR = m.TP - m.shortMax;
  // つぶれの下限は、目標の大きさで 3 段（大きい仕上げほど甘く。mastering-guide §2-2 の「9〜12 が健全」は静かな側の値）
  const tier = lufs === null ? 2 : lufs >= -10 ? 0 : lufs >= -13 ? 1 : 2;
  const plrLo = plrMin ?? [6, 7.5, 9][tier], psrLo = psrMin ?? [4, 5, 6.5][tier];
  const issues = [];
  if (lufs !== null && Math.abs(m.I - lufs) > 0.5) issues.push(`音量が目標 ${lufs} から ${(m.I - lufs).toFixed(1)}LU ずれ`);
  if (m.TP > tp + 0.1) issues.push(`真のピーク ${m.TP.toFixed(1)}dBTP が天井 ${tp} を超えている`);
  if (PLR < plrLo) issues.push(`PLR ${PLR.toFixed(1)} が ${plrLo} 未満（つぶれ気味）`);
  if (PSR < psrLo) issues.push(`PSR ${PSR.toFixed(1)} が ${psrLo} 未満（つぶれ気味）`);
  if (corr < 0.3) issues.push(`左右の相関 ${corr.toFixed(2)} が 0.3 未満（モノで薄くなる恐れ）`);
  if (lowCorr < 0.9) issues.push(`${lowCutoff}Hz 以下の左右の相関 ${lowCorr.toFixed(2)} が 0.9 未満（低音がモノで痩せる）`);
  if (seam && !seam.ok) issues.push(...seam.warnings);
  // 雑音（2026-10-16、人間の指示「雑音検知する項目欲しい」）
  const nz = noise ? noiseCheck(file, { bpm }) : null;
  if (nz && !nz.ok) for (const it of nz.items.filter((x) => !x.ok)) issues.push(`雑音「${it.name}」${it.times.length ? it.times.length + "か所（" + it.times.slice(0, 3).map((t) => t.toFixed(2) + "秒").join("・") + "…）" : it.note}`);
  const f1 = (v) => (Number.isFinite(v) ? v.toFixed(1) : "-");
  // ざらつき(flat・2〜8kHz)と空気(8kHz以上)。ジャンルを渡すと、そのジャンルの目安（p10〜p90）からの外れを「ジャンル注意」として添える（合否には入れない）
  const sp = spectralMetrics(pcm.L, pcm.R, pcm.sr);
  let genreNote = "";
  const g = genre ? genreJudge({ lra: m.LRA, plr: PLR, corr, flat: sp.flat, air: sp.air, intro: sp.intro, tail: sp.tail }, genre, { bpm }) : null;
  if (genre && !g) genreNote = `  [ジャンル「${genre}」の目標がありません]`;
  else if (g) { const ng = g.rows.filter((r) => !r.ok); genreNote = `  [ジャンル「${g.target.label}」${ng.length ? "注意: " + ng.map((r) => `${r.label} ${r.value}（目安 ${r.goal.split("（")[0]}）`).join("；") : "の目安に収まっています"}]`; }
  const line = `${issues.length ? "要直し" : "○"} I ${f1(m.I)} / TP ${f1(m.TP)} / LRA ${f1(m.LRA)} / PLR ${f1(PLR)} / PSR ${f1(PSR)} / 相関 ${corr.toFixed(2)} / 低域相関 ${lowCorr.toFixed(2)} / 継ぎ目 ${seam ? (seam.ok ? "○" : "要直し") : "-"} / flat ${Number.isFinite(sp.flat) ? sp.flat.toFixed(2) : "-"} / 空気 ${f1(sp.air)} / 雑音 ${nz ? (nz.ok ? "○" : "要直し") : "-"}${issues.length ? "  → " + issues.join("；") : ""}${genreNote}`;
  return { ok: issues.length === 0, line, issues, genre: g, metrics: { ...m, PLR, PSR, corr, lowCorr, seam, flat: sp.flat, air: sp.air, presence: sp.presence, intro: sp.intro, tail: sp.tail, noise: nz } };
}
