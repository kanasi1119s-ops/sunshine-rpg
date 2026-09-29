/** 左右の音の並び（-1〜1）から、16ビットのWAVファイル（ステレオ）を作る。 */
export function encodeWav(channels: Float32Array[], sampleRate: number, startFrame = 0, endFrame?: number): Uint8Array {
  const left = channels[0];
  const right = channels[1] ?? channels[0];
  const end = Math.min(endFrame ?? left.length, left.length);
  const frames = Math.max(0, end - startFrame);
  const bytes = new Uint8Array(44 + frames * 4);
  const view = new DataView(bytes.buffer);
  const text = (at: number, str: string): void => {
    for (let i = 0; i < str.length; i++) view.setUint8(at + i, str.charCodeAt(i));
  };
  text(0, "RIFF");
  view.setUint32(4, 36 + frames * 4, true);
  text(8, "WAVE");
  text(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 2, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 4, true);
  view.setUint16(32, 4, true);
  view.setUint16(34, 16, true);
  text(36, "data");
  view.setUint32(40, frames * 4, true);
  const clamp = (x: number): number => Math.round(Math.max(-1, Math.min(1, x)) * 32767);
  for (let i = 0; i < frames; i++) {
    view.setInt16(44 + i * 4, clamp(left[startFrame + i]), true);
    view.setInt16(46 + i * 4, clamp(right[startFrame + i]), true);
  }
  return bytes;
}
