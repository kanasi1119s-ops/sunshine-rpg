/**
 * Opus（小さくて音のよい圧縮）の音を、Ogg の入れ物（.ogg / .opus）に詰める。
 * 圧縮そのものは、ブラウザの WebCodecs（AudioEncoder）が行い、ここでは入れ物だけを作る。
 */
export interface OpusPacket {
  data: Uint8Array;
  /** このパケットの音の長さ（48kHzでのサンプル数。20ミリ秒なら960）。 */
  samples: number;
}

const CRC = new Uint32Array(256);
for (let i = 0; i < 256; i++) {
  let c = i << 24;
  for (let k = 0; k < 8; k++) c = c & 0x80000000 ? (c << 1) ^ 0x04c11db7 : c << 1;
  CRC[i] = c >>> 0;
}
export function oggCrc(b: Uint8Array): number {
  let c = 0;
  for (let i = 0; i < b.length; i++) c = ((c << 8) ^ CRC[((c >>> 24) ^ b[i]) & 255]) >>> 0;
  return c >>> 0;
}

function page(data: Uint8Array, granule: number, seq: number, serial: number, flags: number): Uint8Array {
  const lacing: number[] = [];
  let left = data.length;
  while (left >= 255) {
    lacing.push(255);
    left -= 255;
  }
  lacing.push(left);
  const out = new Uint8Array(27 + lacing.length + data.length);
  const v = new DataView(out.buffer);
  out.set([0x4f, 0x67, 0x67, 0x53], 0);
  v.setUint8(4, 0);
  v.setUint8(5, flags);
  v.setUint32(6, granule % 2 ** 32, true);
  v.setUint32(10, Math.floor(granule / 2 ** 32), true);
  v.setUint32(14, serial, true);
  v.setUint32(18, seq, true);
  v.setUint8(26, lacing.length);
  out.set(lacing, 27);
  out.set(data, 27 + lacing.length);
  v.setUint32(22, oggCrc(out), true);
  return out;
}

export function muxOggOpus(packets: OpusPacket[], opts: { channels: number; preSkip: number; inputSampleRate: number; totalSamples?: number; title?: string }): Uint8Array {
  const serial = 0x53554e53; // "SUNS"
  const head = new Uint8Array(19);
  const hv = new DataView(head.buffer);
  head.set([...new TextEncoder().encode("OpusHead")], 0);
  hv.setUint8(8, 1);
  hv.setUint8(9, opts.channels);
  hv.setUint16(10, opts.preSkip, true);
  hv.setUint32(12, opts.inputSampleRate, true);
  hv.setInt16(16, 0, true);
  hv.setUint8(18, 0);
  const vendor = new TextEncoder().encode("Sunshine Composer");
  const comments = opts.title ? [new TextEncoder().encode(`TITLE=${opts.title}`)] : [];
  const tags = new Uint8Array(8 + 4 + vendor.length + 4 + comments.reduce((s, c) => s + 4 + c.length, 0));
  const tv = new DataView(tags.buffer);
  tags.set([...new TextEncoder().encode("OpusTags")], 0);
  tv.setUint32(8, vendor.length, true);
  tags.set(vendor, 12);
  let at = 12 + vendor.length;
  tv.setUint32(at, comments.length, true);
  at += 4;
  for (const c of comments) {
    tv.setUint32(at, c.length, true);
    tags.set(c, at + 4);
    at += 4 + c.length;
  }
  const pages: Uint8Array[] = [page(head, 0, 0, serial, 0x02), page(tags, 0, 1, serial, 0)];
  let granule = opts.preSkip;
  const end = opts.totalSamples !== undefined ? opts.preSkip + opts.totalSamples : Infinity;
  packets.forEach((p, i) => {
    granule += p.samples;
    const last = i === packets.length - 1;
    pages.push(page(p.data, last ? Math.min(granule, end) : granule, i + 2, serial, last ? 0x04 : 0));
  });
  const out = new Uint8Array(pages.reduce((s, p) => s + p.length, 0));
  let o = 0;
  for (const p of pages) {
    out.set(p, o);
    o += p.length;
  }
  return out;
}
