// 書き出しの仕上げ（マスタリング）。docs/sound/mastering-guide.md の提案 3・4・5・7 を入れたもの。
//   1) 軽く圧縮（natural の曲はやさしく） 2) 140Hz 以下をモノにして、それより上だけ左右に広げる（widen）
//   3) 目標の大きさ（LUFS）に合わせ、トゥルーピーク対応のリミッターで山を止める  4) 書き出し後にもう一度測り、目標とのずれが大きければ補正して1回だけやり直す
//   5) 16bit への最終変換にディザ
import { execSync } from "child_process";
import fs from "fs";

const run = (cmd) => execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], maxBuffer: 1 << 26 });

export function measureLufs(file) {
  const out = execSync(`ffmpeg -nostats -i "${file}" -af ebur128=peak=true -f null - 2>&1`, { encoding: "utf8", maxBuffer: 1 << 26 });
  const m = [...out.matchAll(/\bI:\s+(-?[\d.]+) LUFS/g)].pop();
  const p = [...out.matchAll(/\bPeak:\s+(-?[\d.]+) dBFS/g)].pop();
  return { lufs: m ? Number(m[1]) : NaN, peak: p ? Number(p[1]) : NaN };
}

/** file を上書きして仕上げる。戻り値: { lufs, peak, passes } */
// 圧縮（接着）の強さ: gentle＝起伏を残す／normal／strong＝録音のように密度を上げる
const GLUE = {
  gentle: "acompressor=threshold=0.2:ratio=2.2:attack=8:release=140:makeup=1.5",
  normal: "acompressor=threshold=0.12:ratio=4:attack=4:release=90:makeup=2",
  strong: "acompressor=threshold=0.09:ratio=3.2:attack=10:release=110:makeup=3,acompressor=threshold=0.18:ratio=2:attack=3:release=60:makeup=1.5",
};
/** 書き出しのプリセット（--master-preset）。lufs・widen・glue の組み合わせ */
export const MASTER_PRESETS = {
  game: { lufs: -14, widen: 1.5, glue: "gentle" },
  rock: { lufs: -10, widen: 2.4, glue: "normal" },
  loud: { lufs: -8, widen: 2.2, glue: "strong" },
  calm: { lufs: -16, widen: 1.4, glue: "gentle" },
};

export function masterFile(file, { lufs, widen = 1, natural = false, glue, lowmono = 140, tp = -1.5 } = {}) {
  const pre = file + ".pre.wav", tmp = file + ".master.wav";
  const comp = GLUE[glue ?? (natural ? "gentle" : "normal")] ?? GLUE.normal;
  const w = Math.max(1, Math.min(3, Number(widen) || 1));
  const split = lowmono > 0
    ? `[c]acrossover=split=${lowmono}:order=4th[lo][hi];[lo]pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1[lom];[hi]extrastereo=m=${w}[hiw];[lom][hiw]amix=inputs=2:normalize=0[o]`
    : `[c]extrastereo=m=${w}[o]`;
  run(`ffmpeg -y -loglevel error -i "${file}" -filter_complex "[0]${comp}[c];${split}" -map "[o]" -ar 48000 -ac 2 -c:a pcm_f32le "${pre}"`);
  const before = measureLufs(pre).lufs;
  const limit = Math.pow(10, (tp - 0.3) / 20).toFixed(4); // 16bit への丸めとディザで少し上がるぶん、0.3dB 余裕を見る
  let gain = Number.isFinite(before) ? Math.min(18, Math.max(-18, lufs - before)) : 0;
  let result = { lufs: NaN, peak: NaN }, passes = 0;
  for (; passes < 3; passes++) {
    // トゥルーピーク対応: 192kHz に上げてからリミッターをかけ、48kHz に戻す。最後にディザ
    run(`ffmpeg -y -loglevel error -i "${pre}" -af "volume=${gain.toFixed(2)}dB,aresample=192000,alimiter=limit=${limit}:attack=3:release=60:level=false,aresample=48000" -ar 48000 -ac 2 -c:a pcm_f32le "${tmp}.f32.wav"`);
    run(`ffmpeg -y -loglevel error -i "${tmp}.f32.wav" -af "aresample=48000:osf=s16:dither_method=triangular_hp" -ar 48000 -ac 2 -c:a pcm_s16le -map_metadata -1 -fflags +bitexact -flags:a +bitexact "${tmp}"`);
    result = measureLufs(tmp);
    if (!Number.isFinite(result.lufs) || Math.abs(result.lufs - lufs) <= 0.3) { passes++; break; }
    gain += lufs - result.lufs;
  }
  fs.renameSync(tmp, file);
  for (const f of [pre, tmp + ".f32.wav"]) fs.rmSync(f, { force: true });
  return { ...result, passes };
}
