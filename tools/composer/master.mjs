// 書き出しの仕上げ（マスタリング）。docs/sound/mastering-guide.md の提案 1〜9 を入れたもの（実装状況は同書の末尾）。
//   1) 掃除（HPF・LPF）→ 広い EQ・ティルト・マッチング EQ（任意）→ 軽く圧縮（接着。natural の曲はやさしく）→ 低域だけの圧縮（マルチバンド、任意）
//   2) 140Hz 前後より下をモノにして、それより上だけ左右に広げる。広げ方は 2 種類:
//        widen のみ … extrastereo（従来。game/rock/loud/calm プリセットはこれ。出力を変えない）
//        sideHpf あり … M/S ワイド（サイドだけを HPF してから slev で持ち上げる。低音が広がらない）
//   3) 目標の大きさ（LUFS）に合わせ、ソフトクリップ（任意）→ トゥルーピーク対応のリミッター（192kHz で処理）で山を止める
//   4) 書き出し後にもう一度測り、目標とのずれ（strictTp のときは天井超えも）が大きければ補正して、最大 3 回までやり直す
//   5) 16bit への最終変換にディザ
// ffmpeg 6.1 の注意（検証済み）: asoftclip の oversample は 2 以上にすると約 6dB 小さくなるので 1 のまま使い、前後に自前で aresample=192000／48000 を挟む。
//   adynamicequalizer は 6.1 では threshold の効きが連続でなく（0 で無効、1 以上で全域が一定に切れる）、動的 EQ としては使えないので使わない。
import { execSync } from "child_process";
import fs from "fs";
import path from "path";

const run = (cmd) => execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], maxBuffer: 1 << 26 });
const HERE = path.dirname(new URL(import.meta.url).pathname);

export function measureLufs(file) {
  const out = execSync(`ffmpeg -nostats -i "${file}" -af ebur128=peak=true -f null - 2>&1`, { encoding: "utf8", maxBuffer: 1 << 26 });
  const m = [...out.matchAll(/\bI:\s+(-?[\d.]+) LUFS/g)].pop();
  const p = [...out.matchAll(/\bPeak:\s+(-?[\d.]+) dBFS/g)].pop();
  return { lufs: m ? Number(m[1]) : NaN, peak: p ? Number(p[1]) : NaN };
}

/** 圧縮（接着）の強さ。gentle・normal・strong は従来のまま（出力を変えない）。light・bus2・bus3 は mastering-guide R4 の接着用。off は圧縮なし */
export const GLUE = {
  gentle: "acompressor=threshold=0.2:ratio=2.2:attack=8:release=140:makeup=1.5",
  normal: "acompressor=threshold=0.12:ratio=4:attack=4:release=90:makeup=2",
  strong: "acompressor=threshold=0.09:ratio=3.2:attack=10:release=110:makeup=3,acompressor=threshold=0.18:ratio=2:attack=3:release=60:makeup=1.5",
  light: "acompressor=threshold=0.3:ratio=1.5:attack=30:release=200:knee=4:makeup=1",
  bus2: "acompressor=threshold=0.18:ratio=2:attack=30:release=200:knee=4:makeup=1:detection=rms:link=average",
  bus3: "acompressor=threshold=0.15:ratio=3:attack=30:release=150:knee=4:makeup=1.5:detection=rms:link=average",
  off: "",
};

/**
 * 書き出しのプリセット（--master-preset）。
 *   lufs 目標の大きさ／tp 真のピークの天井(dBTP)／widen 広がり(1=そのまま)／glue 圧縮の強さ／lowmono 〜Hz をモノに(0=切る)
 *   sideHpf サイドの HPF(Hz)。あると M/S ワイド／hpf・lpf 掃除(Hz)／tilt 明るさの傾き(dB/oct)／eq [{type:"peak"|"hs"|"ls",f,g,o}]
 *   air サイドの高域(10kHz〜)を足す量(dB)／mb 低域だけの圧縮 {split,thr,ratio}／clip ソフトクリップ(dB分のゲイン)／rel リミッターのリリース(ms)
 *   match マッチング EQ の家族名（docs/sound/data/mix-targets.json）と matchAmount／strictTp 天井超えも補正のやり直しに使う
 * game・rock・loud・calm は従来の出力を変えない（テストで固定）。それ以外は mastering-guide §3-1 の表の数字。
 */
export const MASTER_PRESETS = {
  game: { lufs: -14, widen: 1.5, glue: "gentle" },
  rock: { lufs: -10, widen: 2.4, glue: "normal" },
  loud: { lufs: -8, widen: 2.2, glue: "strong" },
  calm: { lufs: -16, widen: 1.4, glue: "gentle" },
  // ここから新しい仕上げ（M/S ワイド・掃除・トゥルーピーク補正つき）
  metal: { lufs: -9.5, tp: -1, widen: 1.2, sideHpf: 130, lowmono: 150, hpf: 28, lpf: 19000, glue: "bus3", clip: 1.5, rel: 60, mb: { split: 150, thr: -26, ratio: 2.5 }, eq: [{ type: "peak", f: 320, g: -1.5, o: 1.5 }], strictTp: true },
  punk: { lufs: -10, tp: -1.5, widen: 1.2, sideHpf: 150, lowmono: 140, hpf: 28, lpf: 19000, glue: "bus2", clip: 1, rel: 60, eq: [{ type: "hs", f: 6000, g: 1 }], strictTp: true },
  "rock-clean": { lufs: -10, tp: -1, widen: 1.25, sideHpf: 150, lowmono: 140, hpf: 25, lpf: 19000, glue: "bus2", clip: 0.5, rel: 80, eq: [{ type: "peak", f: 100, g: 0.5, o: 2 }, { type: "peak", f: 300, g: -1, o: 1.5 }, { type: "hs", f: 6000, g: 1 }], strictTp: true },
  "jpop-band": { lufs: -10, tp: -1, widen: 1.25, sideHpf: 150, lowmono: 140, hpf: 25, lpf: 19000, glue: "bus2", clip: 0.5, rel: 80, eq: [{ type: "peak", f: 100, g: 0.5, o: 2 }, { type: "peak", f: 300, g: -1, o: 1.5 }, { type: "hs", f: 6000, g: 1 }, { type: "peak", f: 250, g: -1, o: 1.5 }, { type: "peak", f: 2000, g: 0.5, o: 1.5 }, { type: "hs", f: 8000, g: 1.5 }], strictTp: true },  // jpop-band: rock-clean に 250Hz -1・2kHz +0.5・8kHz 高域 +1.5 を足した、バンド編成のJ-POP（クリーンのギター主体）向け。数字は jpop-clean-guitar-guide.md 提案11（未測定の出発点。analyze.py --bands で前後を測って決める）
  pop: { lufs: -11, tp: -1, widen: 1.3, sideHpf: 150, lowmono: 130, hpf: 25, lpf: 19000, glue: "bus2", clip: 0.5, rel: 70, eq: [{ type: "peak", f: 300, g: -1, o: 1.5 }, { type: "peak", f: 3000, g: 0.5, o: 1.5 }, { type: "hs", f: 10000, g: 1 }], strictTp: true },
  jazz: { lufs: -16, tp: -1, widen: 1.05, sideHpf: 100, lowmono: 100, hpf: 25, lpf: 19000, glue: "light", rel: 120, strictTp: true },
  orch: { lufs: -18, tp: -1.5, widen: 1.0, sideHpf: 100, lowmono: 100, hpf: 25, lpf: 19500, tilt: -0.5, glue: "light", rel: 120, strictTp: true },
  edm: { lufs: -9, tp: -1, widen: 1.4, sideHpf: 150, lowmono: 150, hpf: 28, lpf: 19000, glue: "bus2", clip: 2, rel: 50, air: 2, strictTp: true },
  hiphop: { lufs: -10, tp: -1, widen: 1.0, sideHpf: 140, lowmono: 140, hpf: 28, lpf: 19000, glue: "bus3", clip: 1.5, rel: 60, eq: [{ type: "peak", f: 300, g: -1, o: 1.5 }], strictTp: true },
  lofi: { lufs: -13, tp: -1.5, widen: 0.95, sideHpf: 150, lowmono: 150, hpf: 30, lpf: 10000, glue: "light", clip: 1, rel: 100, eq: [{ type: "peak", f: 300, g: 1, o: 1.5 }], strictTp: true },
  ambient: { lufs: -16, tp: -2, widen: 1.4, sideHpf: 120, lowmono: 120, hpf: 25, lpf: 16000, glue: "off", rel: 150, eq: [{ type: "peak", f: 250, g: -1.5, o: 1.5 }], strictTp: true },
  "game-field": { lufs: -16.5, tp: -1.5, widen: 1.15, sideHpf: 150, lowmono: 140, hpf: 25, lpf: 19000, glue: "light", rel: 100, eq: [{ type: "peak", f: 2000, g: -1, o: 1.5 }], strictTp: true },
  "game-battle": { lufs: -14.5, tp: -1.5, widen: 1.2, sideHpf: 150, lowmono: 150, hpf: 28, lpf: 19000, glue: "bus3", clip: 1, rel: 60, mb: { split: 150, thr: -26, ratio: 2.5 }, eq: [{ type: "peak", f: 400, g: -1.5, o: 1.5 }, { type: "peak", f: 2500, g: -1.5, o: 1.5 }], strictTp: true },
  "game-boss": { lufs: -14.5, tp: -1.5, widen: 1.3, sideHpf: 150, lowmono: 150, hpf: 28, lpf: 19500, glue: "bus2", clip: 1, rel: 70, air: 1, mb: { split: 150, thr: -26, ratio: 2 }, strictTp: true },
  "game-dungeon": { lufs: -18, tp: -2, widen: 1.3, sideHpf: 120, lowmono: 120, hpf: 25, lpf: 15000, glue: "light", rel: 150, eq: [{ type: "peak", f: 250, g: -1, o: 1.5 }], strictTp: true },
  retro: { lufs: -16, tp: -1.5, widen: 0.8, sideHpf: 150, lowmono: 150, hpf: 30, lpf: 12000, glue: "off", rel: 80, strictTp: true },
  wafu: { lufs: -16, tp: -1.5, widen: 1.1, sideHpf: 140, lowmono: 120, hpf: 25, lpf: 19000, glue: "light", rel: 100, eq: [{ type: "peak", f: 4000, g: -1, o: 1.5 }], strictTp: true },
  solo: { lufs: -17, tp: -2, widen: 1.1, sideHpf: 100, lowmono: 100, hpf: 25, lpf: 19000, glue: "off", rel: 150, eq: [{ type: "peak", f: 3000, g: -1, o: 1.5 }], strictTp: true },
};

/** プリセットの別名（mastering-guide §3-1 の呼び名） */
export const MASTER_PRESET_ALIASES = { "rock-pop": "rock-clean", "game-town": "game-field", "game-title": "game-boss" };

export function resolvePreset(name) {
  const key = MASTER_PRESET_ALIASES[name] ?? name;
  const p = MASTER_PRESETS[key];
  if (!p) throw new Error(`master-preset は ${Object.keys(MASTER_PRESETS).join("・")} のどれか（${name}）`);
  return { id: key, ...p };
}

/** リミッターの limit（線形）。16bit への丸めとディザで少し上がるぶん 0.3dB 余裕を見る */
export const limitFor = (tp) => Math.pow(10, (tp - 0.3) / 20);

/** 低域だけの圧縮（mcompand の 2 帯域。上の帯域は素通し）。thr(dB) より上を ratio:1 で縮める */
export function mbFilter({ split = 150, thr = -26, ratio = 2.5 } = {}) {
  const out0 = (thr + (0 - thr) / ratio).toFixed(2);
  return `mcompand=args='0.02\\,0.2 6 -70/-70\\,${thr}/${thr}\\,0/${out0} ${split} | 0.01\\,0.1 6 -70/-70\\,0/0 20000'`;
}

/** 明るさの傾き（650Hz 軸、1 オクターブごとに dB。負で暗く） */
export const tiltFilter = (db) => `firequalizer=gain='${(-db).toFixed(3)}*log(max(f\\,20)/650)/log(2)':zero_phase=on`;

/** EQ 1 つぶんのフィルター */
export function eqFilter(e) {
  if (e.type === "hs") return `treble=g=${e.g}:f=${e.f}`;
  if (e.type === "ls") return `bass=g=${e.g}:f=${e.f}`;
  return `equalizer=f=${e.f}:t=o:w=${e.o ?? 1.5}:g=${e.g}`;
}

/** マッチング EQ（tools/audio-check/match-eq.py）が作る gain_entry を firequalizer に */
export function matchEqFilter(file, family, amount = 0.4) {
  const entries = run(`python3 "${path.join(HERE, "../audio-check/match-eq.py")}" "${file}" --family ${family} --amount ${amount}`).trim();
  return entries ? `firequalizer=gain_entry='${entries}':zero_phase=on:delay=0.05` : "";
}

/**
 * 前段（圧縮の前に通す掃除と EQ）と、圧縮・低域マルチバンドのフィルター列を作る。
 * 何も指定しなければ従来と同じ（圧縮だけ）。
 */
export function buildFrontChain({ comp, hpf = 0, lpf = 0, tilt = 0, eq = [], matchFilter = "", mb = null }) {
  const parts = [];
  if (hpf > 0) parts.push(`highpass=f=${hpf}:poles=2`);
  if (lpf > 0) parts.push(`lowpass=f=${lpf}:poles=2`);
  if (tilt) parts.push(tiltFilter(tilt));
  for (const e of eq) parts.push(eqFilter(e));
  if (matchFilter) parts.push(matchFilter);
  if (comp) parts.push(comp);
  if (mb) parts.push(mbFilter(mb));
  return parts.length ? parts.join(",") : "anull";
}

/** 低域モノ化と広げ方（filter_complex の断片。入力 [c]、出力 [o]） */
export function buildStereoStage({ lowmono = 140, widen = 1, sideHpf = 0, air = 0 }) {
  const w = Math.max(0.5, Math.min(3, Number(widen) || 1));
  // 広げ方: sideHpf があれば M/S（サイドだけ HPF してから slev。FL=Mid・FR=Side）、なければ従来の extrastereo
  const widenOf = (inp, outp) => sideHpf > 0
    ? `[${inp}]stereotools=mode=lr>ms,highpass=f=${sideHpf}:poles=2:channels=FR${air ? `,equalizer=f=10000:t=h:w=2000:g=${air}:channels=FR` : ""},stereotools=slev=${w}:mode=ms>lr[${outp}]`
    : `[${inp}]extrastereo=m=${Math.max(1, w)}[${outp}]`; // 従来どおり 1 未満にはしない
  return lowmono > 0
    ? `[c]acrossover=split=${lowmono}:order=4th[lo][hi];[lo]pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1[lom];${widenOf("hi", "hiw")};[lom][hiw]amix=inputs=2:normalize=0[o]`
    : widenOf("c", "o");
}

/** ゲイン→（ソフトクリップ）→リミッターのフィルター列 */
export function buildLimitChain({ gain, clip = 0, limit, rel = 60, attack = 3, clipType = "tanh" }) {
  const lim = `alimiter=limit=${limit.toFixed(4)}:attack=${attack}:release=${rel}:level=false`;
  if (clip > 0) {
    // クリップ分のゲインを足して丸め、同じだけ戻す。大きさは、このあと閉ループで測り直して合わせる
    return `volume=${(gain + clip).toFixed(2)}dB,aresample=192000,asoftclip=type=${clipType}:threshold=1:oversample=1,volume=${(-clip).toFixed(2)}dB,${lim},aresample=48000`;
  }
  return `volume=${gain.toFixed(2)}dB,aresample=192000,${lim},aresample=48000`;
}

/** file を上書きして仕上げる。戻り値: { lufs, peak, passes } */
export function masterFile(file, { lufs, widen = 1, natural = false, glue, lowmono = 140, tp = -1.5, sideHpf = 0, air = 0, hpf = 0, lpf = 0, tilt = 0, eq = [], mb = null, clip = 0, rel = 60, match = "", matchAmount = 0.4, strictTp = false } = {}) {
  const pre = file + ".pre.wav", tmp = file + ".master.wav";
  const comp = GLUE[glue ?? (natural ? "gentle" : "normal")] ?? GLUE.normal;
  const matchFilter = match ? matchEqFilter(file, match, Math.min(0.5, matchAmount)) : "";
  const front = buildFrontChain({ comp, hpf, lpf, tilt, eq, matchFilter, mb });
  const split = buildStereoStage({ lowmono, widen, sideHpf, air });
  run(`ffmpeg -y -loglevel error -i "${file}" -filter_complex "[0]${front}[c];${split}" -map "[o]" -ar 48000 -ac 2 -c:a pcm_f32le "${pre}"`);
  const before = measureLufs(pre).lufs;
  let limit = limitFor(tp);
  let gain = Number.isFinite(before) ? Math.min(18, Math.max(-18, lufs - before)) : 0;
  let result = { lufs: NaN, peak: NaN }, passes = 0;
  for (; passes < 3; passes++) {
    // トゥルーピーク対応: 192kHz に上げてからリミッターをかけ、48kHz に戻す。最後にディザ
    run(`ffmpeg -y -loglevel error -i "${pre}" -af "${buildLimitChain({ gain, clip, limit, rel })}" -ar 48000 -ac 2 -c:a pcm_f32le "${tmp}.f32.wav"`);
    run(`ffmpeg -y -loglevel error -i "${tmp}.f32.wav" -af "aresample=48000:osf=s16:dither_method=triangular_hp" -ar 48000 -ac 2 -c:a pcm_s16le -map_metadata -1 -fflags +bitexact -flags:a +bitexact "${tmp}"`);
    result = measureLufs(tmp);
    if (!Number.isFinite(result.lufs)) { passes++; break; }
    const lufsOk = Math.abs(result.lufs - lufs) <= 0.3;
    const over = strictTp && Number.isFinite(result.peak) && result.peak > tp + 0.05; // 真のピークが天井を超えたら、超えたぶん limit を下げてやり直す
    if (lufsOk && !over) { passes++; break; }
    if (over) limit *= Math.pow(10, -(result.peak - tp + 0.05) / 20);
    if (!lufsOk) gain += lufs - result.lufs;
  }
  fs.renameSync(tmp, file);
  for (const f of [pre, tmp + ".f32.wav"]) fs.rmSync(f, { force: true });
  return { ...result, passes };
}
