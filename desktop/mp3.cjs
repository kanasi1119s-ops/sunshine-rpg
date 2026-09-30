// MP3 の書き出し（デスクトップ版だけ）。
// MP3 の変換には LAME（lamejs。LGPL-3.0）を使う。LGPL の条件を守るため、
// - 本体のプログラムに混ぜず、別のファイルのまま置く（配布物では app.asar.unpacked/node_modules/@breezystack/lamejs。利用者が差し替えられる）
// - LAME を使っていることと入手先を、ライセンスの画面に書く（licenses/README.txt・licenses/LAME-NOTICE.txt）
// - LAME そのものは改変しない
let lame = null;
async function load() {
  lame ??= await import("@breezystack/lamejs");
  return lame;
}

/** 左右（または1つ）の音の並び（-1〜1）を、MP3 にする。kbps は 128〜320。 */
async function encodeMp3(channels, sampleRate, kbps = 256) {
  const { Mp3Encoder } = await load();
  const nch = channels.length >= 2 ? 2 : 1;
  const toInt = (f) => {
    const out = new Int16Array(f.length);
    for (let i = 0; i < f.length; i++) out[i] = Math.max(-32768, Math.min(32767, Math.round(f[i] * 32767)));
    return out;
  };
  const L = toInt(channels[0]);
  const R = nch === 2 ? toInt(channels[1]) : null;
  const enc = new Mp3Encoder(nch, sampleRate, Math.max(128, Math.min(320, kbps)));
  const parts = [];
  const block = 1152;
  for (let i = 0; i < L.length; i += block) {
    const b = R ? enc.encodeBuffer(L.subarray(i, i + block), R.subarray(i, i + block)) : enc.encodeBuffer(L.subarray(i, i + block));
    if (b.length) parts.push(Buffer.from(b.buffer, b.byteOffset, b.length));
  }
  const tail = enc.flush();
  if (tail.length) parts.push(Buffer.from(tail.buffer, tail.byteOffset, tail.length));
  return new Uint8Array(Buffer.concat(parts));
}

module.exports = { encodeMp3 };
