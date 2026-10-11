import { test } from "node:test";
import assert from "node:assert";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { GLUE, MASTER_PRESETS, buildFrontChain, buildLimitChain, buildStereoStage, eqFilter, limitFor, masterFile, mbFilter, measureLufs, resolvePreset, tiltFilter } from "./master.mjs";
import { correlation, loopCheck, loopTailWrap, masterReport, readPcm } from "./master-report.mjs";

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "master-test-"));
const sh = (c) => execSync(c, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
process.on("exit", () => fs.rmSync(tmp, { recursive: true, force: true }));

/** 合成の「曲」: 左右別のピンクノイズ（高域を落とす）＋ 脈打つ 60Hz のサイン（左右逆相）＋ 1kHz のサイン。8 秒。 */
function makeTone(name, { seconds = 8, antiphaseLow = true } = {}) {
  const f = path.join(tmp, name);
  const low = antiphaseLow ? "c0=0.25*c0|c1=-0.25*c0" : "c0=0.25*c0|c1=0.25*c0";
  sh(`ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=d=${seconds}:c=pink:r=48000:a=0.08:seed=1" -f lavfi -i "anoisesrc=d=${seconds}:c=pink:r=48000:a=0.08:seed=2" -f lavfi -i "sine=f=60:d=${seconds}:r=48000" -f lavfi -i "sine=f=1000:d=${seconds}:r=48000" -filter_complex "[0][1]amerge=inputs=2[n];[2]pan=stereo|${low}[l];[3]volume=0.05,pan=stereo|c0=c0|c1=c0[m];[n][l]amix=inputs=2:normalize=0[a];[a][m]amix=inputs=2:normalize=0,aformat=sample_fmts=s16:channel_layouts=stereo" -ar 48000 "${f}"`);
  return f;
}

test("従来の 4 プリセットは、フィルターの文字列が変わっていない（出力を固定する）", () => {
  assert.equal(buildFrontChain({ comp: GLUE.gentle }), GLUE.gentle);
  assert.equal(buildStereoStage({ lowmono: 140, widen: 1.5 }), "[c]acrossover=split=140:order=4th[lo][hi];[lo]pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1[lom];[hi]extrastereo=m=1.5[hiw];[lom][hiw]amix=inputs=2:normalize=0[o]");
  assert.equal(buildStereoStage({ lowmono: 0, widen: 2 }), "[c]extrastereo=m=2[o]");
  assert.equal(buildLimitChain({ gain: 3.2, limit: limitFor(-1.5) }), "volume=3.20dB,aresample=192000,alimiter=limit=0.8128:attack=3:release=60:level=false,aresample=48000");
  for (const id of ["game", "rock", "loud", "calm"]) {
    const p = MASTER_PRESETS[id];
    assert.deepEqual(Object.keys(p).sort(), ["glue", "lufs", "widen"], id);
  }
  assert.deepEqual([MASTER_PRESETS.game.lufs, MASTER_PRESETS.rock.lufs, MASTER_PRESETS.loud.lufs, MASTER_PRESETS.calm.lufs], [-14, -10, -8, -16]);
});

test("部品のフィルター文字列", () => {
  assert.equal(eqFilter({ type: "peak", f: 300, g: -1, o: 1.5 }), "equalizer=f=300:t=o:w=1.5:g=-1");
  assert.equal(eqFilter({ type: "hs", f: 6000, g: 1 }), "treble=g=1:f=6000");
  assert.ok(tiltFilter(-0.5).includes("0.500*log(max(f\\,20)/650)"));
  assert.ok(mbFilter({ split: 150, thr: -26, ratio: 2.5 }).startsWith("mcompand=args='0.02\\,0.2 6 -70/-70\\,-26/-26\\,0/-15.60 150 |"));
  assert.ok(buildStereoStage({ lowmono: 0, widen: 1.3, sideHpf: 150, air: 2 }).includes("highpass=f=150:poles=2:channels=FR,equalizer=f=10000"));
  assert.ok(buildLimitChain({ gain: 2, clip: 1.5, limit: 0.8, rel: 80 }).includes("asoftclip=type=tanh:threshold=1:oversample=1"));
});

test("別名とプリセットの解決", () => {
  assert.equal(resolvePreset("game-town").id, "game-field");
  assert.throws(() => resolvePreset("nothing"), /master-preset/);
  assert.ok(Object.keys(MASTER_PRESETS).length >= 20);
});

test("すべての新プリセットが書き出せて、目標の大きさ（±0.6）と天井（+0.1）に収まる", { timeout: 600000 }, () => {
  const src = makeTone("src.wav");
  for (const [id, p] of Object.entries(MASTER_PRESETS)) {
    const f = path.join(tmp, `p-${id}.wav`);
    fs.copyFileSync(src, f);
    const { lufs, ...rest } = p;
    masterFile(f, { ...rest, lufs });
    const m = measureLufs(f);
    assert.ok(Math.abs(m.lufs - lufs) <= 0.6, `${id}: ${m.lufs} LUFS（目標 ${lufs}）`);
    if (p.strictTp) assert.ok(m.peak <= (p.tp ?? -1.5) + 0.1, `${id}: TP ${m.peak}`);
    fs.rmSync(f);
  }
});

test("逆相の 60Hz は、低域モノ化で 100Hz 以下の左右の相関が0.9 以上になる", () => {
  const src = makeTone("anti.wav");
  const before = readPcm(src, { filter: "lowpass=f=100:poles=2" });
  assert.ok(correlation(before.L, before.R) < 0.5);
  const f = path.join(tmp, "anti-m.wav");
  fs.copyFileSync(src, f);
  masterFile(f, { ...MASTER_PRESETS.pop, lufs: -14 });
  const after = readPcm(f, { filter: "lowpass=f=100:poles=2" });
  assert.ok(correlation(after.L, after.R) > 0.9, `低域相関 ${correlation(after.L, after.R)}`);
});

test("M/S ワイドは低音を広げない（サイドの HPF）が、従来の extrastereo は広げる", () => {
  // 50Hz の逆相（サイドだけの成分）と 2kHz の逆相を作り、サイドの量を測る
  const f0 = path.join(tmp, "side.wav");
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=50:d=5:r=48000" -f lavfi -i "sine=f=2000:d=5:r=48000" -filter_complex "[0]volume=0.1,pan=stereo|c0=c0|c1=-1*c0[a];[1]volume=0.1,pan=stereo|c0=c0|c1=-1*c0[b];[a][b]amix=inputs=2:normalize=0,aformat=sample_fmts=s16" -ar 48000 "${f0}"`);
  const sideRms = (file, filter) => {
    const p = readPcm(file, { filter });
    let s = 0;
    for (let i = 0; i < p.n; i++) s += ((p.L[i] - p.R[i]) / 2) ** 2;
    return Math.sqrt(s / p.n);
  };
  const fa = path.join(tmp, "side-ms.wav"), fb = path.join(tmp, "side-ex.wav");
  fs.copyFileSync(f0, fa); fs.copyFileSync(f0, fb);
  masterFile(fa, { lufs: -20, widen: 1.5, glue: "off", lowmono: 0, sideHpf: 150, tp: -1.5 });
  masterFile(fb, { lufs: -20, widen: 1.5, glue: "off", lowmono: 0, tp: -1.5 });
  const low = "lowpass=f=100:poles=2";
  assert.ok(sideRms(fa, low) < sideRms(fb, low) * 0.2, `M/S のサイド ${sideRms(fa, low)} vs ${sideRms(fb, low)}`);
  const high = "highpass=f=1000:poles=2";
  assert.ok(sideRms(fa, high) > 0.01, "高域のサイドは残る");
});

test("真のピーク: 12kHz の山を、天井 -1.5dBTP 以下にする（strictTp）", () => {
  const f = path.join(tmp, "tp.wav");
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=12000:d=4:r=48000" -af "volume=0.95,aformat=sample_fmts=s16:channel_layouts=stereo" -ar 48000 "${f}"`);
  masterFile(f, { lufs: -9, widen: 1, glue: "off", lowmono: 0, sideHpf: 100, tp: -1.5, rel: 60, strictTp: true });
  assert.ok(measureLufs(f).peak <= -1.4, `TP ${measureLufs(f).peak}`);
});

test("マッチング EQ は amount 0.5 を超えず、各帯域 ±1.5dB 以内（3dB × 0.5）", () => {
  const src = makeTone("match.wav");
  const out = sh(`python3 ${path.join(import.meta.dirname, "../audio-check/match-eq.py")} "${src}" --family rock --amount 1`).trim();
  const gains = [...out.matchAll(/entry\((\d+),(-?[\d.]+)\)/g)].map((m) => ({ f: Number(m[1]), g: Number(m[2]) }));
  assert.ok(gains.length >= 25);
  for (const { f, g } of gains) {
    assert.ok(Math.abs(g) <= 1.5 + 1e-9, `${f}Hz ${g}`);
    if (f < 80 || f > 12500) assert.equal(g, 0, `${f}Hz は触らない`);
  }
  const f = path.join(tmp, "match-m.wav");
  fs.copyFileSync(src, f);
  masterFile(f, { ...MASTER_PRESETS.pop, lufs: -14, match: "rock", matchAmount: 0.4 }); // 構文が通って書き出せる
  assert.ok(Math.abs(measureLufs(f).lufs + 14) <= 0.6);
});

test("低域だけの圧縮（mb）は、低域のラウドな曲で低域だけを縮める", () => {
  const f0 = path.join(tmp, "mb-src.wav");
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=80:d=5:r=48000" -f lavfi -i "sine=f=2000:d=5:r=48000" -filter_complex "[0]volume=0.5[a];[1]volume=0.05[b];[a][b]amix=inputs=2:normalize=0,pan=stereo|c0=c0|c1=c0,aformat=sample_fmts=s16" -ar 48000 "${f0}"`);
  const band = (file, filt) => measureLufs(Object.assign(file, {}) && (() => { const t = file + ".b.wav"; sh(`ffmpeg -y -loglevel error -i "${file}" -af "${filt}" "${t}"`); return t; })()).lufs;
  const a = path.join(tmp, "mb-a.wav"), b = path.join(tmp, "mb-b.wav");
  fs.copyFileSync(f0, a); fs.copyFileSync(f0, b);
  masterFile(a, { lufs: -20, glue: "off", lowmono: 0, widen: 1, tp: -1.5, sideHpf: 150 });
  masterFile(b, { lufs: -20, glue: "off", lowmono: 0, widen: 1, tp: -1.5, sideHpf: 150, mb: { split: 150, thr: -26, ratio: 4 } });
  const lowA = band(a, "lowpass=f=150"), lowB = band(b, "lowpass=f=150"), hiA = band(a, "highpass=f=1000"), hiB = band(b, "highpass=f=1000");
  // 同じ全体の大きさに合わせるので、低域が縮んだぶん高域は相対的に上がる
  assert.ok(hiB - lowB > hiA - lowA + 1, `低域/高域の差が縮む: A ${lowA - hiA} → B ${lowB - hiB}`);
});

test("テールラップ: 尾を先頭に重ねて T 秒に切る。尾が無ければ何もしない", () => {
  const f = path.join(tmp, "tail.wav");
  // 3 秒の本体（1 秒のところに 440Hz の音）＋ 2 秒の尾（消えていく 440Hz）
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=440:d=5:r=44100" -af "volume=0.3,afade=t=out:st=3:d=2,aformat=sample_fmts=s16:channel_layouts=stereo" -ar 44100 "${f}"`);
  const r = loopTailWrap(f, 3);
  assert.equal(r.wrapped, true);
  const dur = Number(sh(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${f}"`).trim());
  assert.ok(Math.abs(dur - 3) < 0.02, `長さ ${dur}`);
  assert.deepEqual(loopTailWrap(f, 3).wrapped, false);
});

test("継ぎ目の検査: 先頭と末尾の大きさが違うと警告、なじんでいれば通る", () => {
  const ok = path.join(tmp, "seam-ok.wav"), bad = path.join(tmp, "seam-bad.wav");
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=220:d=4:r=48000" -af "volume=0.3,aformat=sample_fmts=s16:channel_layouts=stereo" -ar 48000 "${ok}"`);
  sh(`ffmpeg -y -loglevel error -f lavfi -i "sine=f=220:d=4:r=48000" -af "volume=0.3,afade=t=out:st=3:d=1,aformat=sample_fmts=s16:channel_layouts=stereo" -ar 48000 "${bad}"`);
  assert.equal(loopCheck(ok).ok, true, JSON.stringify(loopCheck(ok)));
  const b = loopCheck(bad);
  assert.equal(b.ok, false);
  assert.ok(b.warnings.some((w) => w.includes("大きさ")));
});

test("master-report は 1 行で ○／要直し を返す", () => {
  const f = path.join(tmp, "rep.wav");
  fs.copyFileSync(makeTone("rep-src.wav", { antiphaseLow: false }), f);
  masterFile(f, { ...MASTER_PRESETS.jazz, lufs: -16 });
  const r = masterReport(f, { lufs: -16, tp: -1, loop: false });
  assert.match(r.line, /^(○|要直し) I -?[\d.]+ \/ TP -?[\d.]+ \/ LRA [\d.]+ \/ PLR [\d.]+ \/ PSR [\d.]+ \/ 相関 [\d.-]+ \/ 低域相関 [\d.-]+ \/ 継ぎ目 -/);
  assert.ok(Number.isFinite(r.metrics.PSR) && r.metrics.PLR > 0);
  const off = masterReport(f, { lufs: -10, tp: -1, loop: false });
  assert.equal(off.ok, false);
  assert.ok(off.issues.some((i) => i.includes("目標")));
});

test("analyze.py --roles は席の重なりを警告し、--family は家族別の目標で帯域を診断する", () => {
  const proj = path.join(tmp, "p.sunshine-song.json");
  const notes = (n) => Array.from({ length: 8 }, () => ({ note: n, durationBeats: 1 }));
  fs.writeFileSync(proj, JSON.stringify({ score: { tracks: [
    { instrument: "kick", volume: 0.1, pan: 0.5, notes: notes("C2") },
    { instrument: "bass", volume: 0.1, pan: 0, notes: notes("C1") },
    { instrument: "piano", volume: 0.1, notes: notes("C4") },
    { instrument: "strings", volume: 0.1, notes: notes("D4") },
  ] } }));
  const out = sh(`python3 ${path.join(import.meta.dirname, "../audio-check/analyze.py")} --roles "${proj}"`);
  assert.ok(out.includes("体の席"), out);
  assert.ok(out.includes("キック") || out.includes("重心"), out);
  assert.ok(out.includes("中央でない"), out);
  const res = path.join(tmp, "res.json");
  fs.writeFileSync(res, JSON.stringify({ "x.wav": { band_dB: { sub: -8.8, bass: -2, lowmid: -8, mid: -12, presence: -20, air: -27 }, side_minus_mid_dB: {}, corr: 0.7, centroid_Hz: 400 } }));
  const out2 = sh(`python3 ${path.join(import.meta.dirname, "../audio-check/analyze.py")} --bands "${res}" --family edm`);
  assert.ok(out2.includes("EDM"), out2);
  assert.ok(out2.includes("○ mid"), out2); // EDM の中は -12 なので ○
  const out3 = sh(`python3 ${path.join(import.meta.dirname, "../audio-check/analyze.py")} --bands "${res}" --family rock`);
  assert.ok(out3.includes("△ mid"), out3); // ロックの中は -8.5 なので、-12 は 3.5 低くて △
});

test("bgm-trim-report は -16 軸の補正量を出し、TP の余裕で止まる曲を警告する", () => {
  const f = path.join(tmp, "loud.json");
  fs.writeFileSync(f, JSON.stringify({ quiet: { I: -22, TP: -8 }, quietPeaky: { I: -22, TP: -2.5 }, hot: { I: -8, TP: -1 }, "battle-x": { I: -14, TP: -1 } }));
  const out = sh(`python3 ${path.join(import.meta.dirname, "../audio-check/bgm-trim-report.py")} --bgm-loudness "${f}" --json "${path.join(tmp, "o.json")}"`);
  const j = JSON.parse(fs.readFileSync(path.join(tmp, "o.json"), "utf8"));
  assert.equal(j.quiet, 6);        // -22 → -16
  assert.equal(j.quietPeaky, 1.5); // 上げたいのは 6 だが TP -2.5 → 天井 -1 までの 1.5 で止まる
  assert.equal(j.hot, -8);
  assert.equal(j["battle-x"], -0.5); // 戦闘は軸 +1.5 → 目標 -14.5。-14 から -0.5
  assert.ok(out.includes("TP の余裕"), out);
});
