/** WAVのビットの深さ。16・24は整数、32は小数（float）。 */
export type WavBits = 16 | 24 | 32;

/** 左右の音の並び（-1〜1）から、WAVファイル（ステレオ）を作る。 */
export function encodeWav(channels: Float32Array[], sampleRate: number, startFrame = 0, endFrame?: number, bits: WavBits = 16): Uint8Array {
  const left = channels[0];
  const right = channels[1] ?? channels[0];
  const end = Math.min(endFrame ?? left.length, left.length);
  const frames = Math.max(0, end - startFrame);
  const bytesPer = bits / 8;
  const block = bytesPer * 2;
  const bytes = new Uint8Array(44 + frames * block);
  const view = new DataView(bytes.buffer);
  const text = (at: number, str: string): void => {
    for (let i = 0; i < str.length; i++) view.setUint8(at + i, str.charCodeAt(i));
  };
  text(0, "RIFF");
  view.setUint32(4, 36 + frames * block, true);
  text(8, "WAVE");
  text(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, bits === 32 ? 3 : 1, true);
  view.setUint16(22, 2, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * block, true);
  view.setUint16(32, block, true);
  view.setUint16(34, bits, true);
  text(36, "data");
  view.setUint32(40, frames * block, true);
  const clamp = (x: number): number => Math.max(-1, Math.min(1, x));
  let at = 44;
  for (let i = 0; i < frames; i++) {
    for (const x of [left[startFrame + i], right[startFrame + i]]) {
      if (bits === 16) view.setInt16(at, Math.round(clamp(x) * 32767), true);
      else if (bits === 24) {
        const v = Math.round(clamp(x) * 8388607);
        view.setUint8(at, v & 255);
        view.setUint8(at + 1, (v >> 8) & 255);
        view.setUint8(at + 2, (v >> 16) & 255);
      } else view.setFloat32(at, x, true);
      at += bytesPer;
    }
  }
  return bytes;
}
