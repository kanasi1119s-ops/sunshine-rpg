// 作曲ソフト用の追加の録音音源（ベース・ドラム）を、SFZなどの元素材からSoundFont（.sf2）に変換するための共通の道具。
import fs from "fs";
import os from "os";
import path from "path";
import { execFileSync } from "child_process";
import { SoundBankLoader, BasicSoundBank, BasicSample, GeneratorTypes, SampleTypes } from "spessasynth_core";

export const SR = 44100;
/** 音声ファイル（FLAC/WAV）を、モノラル32bit浮動小数で読む（ffmpeg を使う）。 */
export function decodeMono(file, seconds, filter) {
  const args = ["-v", "error", "-i", file, ...(seconds ? ["-t", String(seconds)] : []), "-ac", "1", "-ar", String(SR), ...(filter ? ["-af", filter] : []), "-f", "f32le", "-"];
  const buf = execFileSync("ffmpeg", args, { maxBuffer: 1 << 30 });
  return new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
}
export function loadBank(file) {
  return SoundBankLoader.fromArrayBuffer(fs.readFileSync(file).buffer.slice(0));
}
export function monoSample(name, data, key) {
  const s = new BasicSample(name, SR, key, 0, SampleTypes.monoSample, 0, 0);
  s.setAudioData(data, SR);
  return s;
}
/** 左右の2つのサンプルを、ステレオの組にする。 */
export function stereoPair(name, left, right, key) {
  const l = new BasicSample(name + " L", SR, key, 0, SampleTypes.leftSample, 0, 0);
  const r = new BasicSample(name + " R", SR, key, 0, SampleTypes.rightSample, 0, 0);
  l.setAudioData(left, SR);
  r.setAudioData(right, SR);
  l.setLinkedSample(r, SampleTypes.leftSample);
  return [l, r];
}
export const timecents = (sec) => Math.round(1200 * Math.log2(sec));
export { BasicSoundBank, GeneratorTypes };
/** 元の音源の、ある楽器（GMの番号）の入れものを新しい音源に写し、中の音の割りあて（ゾーン）をすべて空にして返す。 */
export function emptyPresetFrom(base, out, { program, drum = false }) {
  const preset = base.presets.find((p) => (drum ? p.isGMGSDrum && p.program === program : !p.isGMGSDrum && p.bankMSB === 0 && p.program === program));
  if (!preset) throw new Error(`元の音源に楽器がありません: ${drum ? "drum" : ""}${program}`);
  const copy = out.clonePreset(preset);
  return copy;
}

/** サンプルを Vorbis（OGG）に圧縮して、SF3 にする（ffmpeg の libvorbis を使う）。品質 q は -1〜10（4≒128kbps相当）。 */
export async function compressBank(bank, q = 4) {
  const encode = async (audio, rate) => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "sf3-"));
    const raw = path.join(tmp, "in.f32"), ogg = path.join(tmp, "out.ogg");
    fs.writeFileSync(raw, Buffer.from(audio.buffer, audio.byteOffset, audio.byteLength));
    execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "f32le", "-ar", String(rate), "-ac", "1", "-i", raw, "-c:a", "libvorbis", "-q:a", String(q), ogg]);
    const data = new Uint8Array(fs.readFileSync(ogg));
    fs.rmSync(tmp, { recursive: true });
    return data;
  };
  await bank.setSampleFormat({ format: "compressed", compressionFunction: encode });
}

/** 音声ファイルを、左右2つの32bit浮動小数で読む（モノラルなら左右とも同じ）。 */
export function decodeStereo(file, seconds) {
  const args = ["-v", "error", "-i", file, ...(seconds ? ["-t", String(seconds)] : []), "-ac", "2", "-ar", String(SR), "-f", "f32le", "-"];
  const buf = execFileSync("ffmpeg", args, { maxBuffer: 1 << 30 });
  const all = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  const n = all.length >> 1;
  const L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = all[2 * i]; R[i] = all[2 * i + 1]; }
  return [L, R];
}
/** 左右の波形に、ffmpegのフィルター（イコライザー・コンプレッサーなど）をかける。 */
export function filterStereo(L, R, filter) {
  if (!filter) return [L, R];
  const n = L.length;
  const inter = new Float32Array(n * 2);
  for (let i = 0; i < n; i++) { inter[2 * i] = L[i]; inter[2 * i + 1] = R[i]; }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "flt-"));
  const raw = path.join(tmp, "in.f32");
  fs.writeFileSync(raw, Buffer.from(inter.buffer));
  const out = execFileSync("ffmpeg", ["-v", "error", "-f", "f32le", "-ar", String(SR), "-ac", "2", "-i", raw, "-af", filter, "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  fs.rmSync(tmp, { recursive: true });
  const all = new Float32Array(out.buffer.slice(out.byteOffset, out.byteOffset + out.byteLength));
  const L2 = new Float32Array(n), R2 = new Float32Array(n);
  for (let i = 0; i < n; i++) { L2[i] = all[2 * i] ?? 0; R2[i] = all[2 * i + 1] ?? 0; }
  return [L2, R2];
}
