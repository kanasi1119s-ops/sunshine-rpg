// 使い方: node tools/audio-check/sf3-render-check.mjs <overlay.sf3> <GMの番号> [鍵,鍵,...] [保持秒]   （リポジトリの直下で実行）
// 追加音源（SF3）を作曲ソフトと同じ描画（spessasynth）で鳴らし、鍵ごとに 音量(RMS・ピーク)・基音が合っているか(f0ok)・保持中の音量の落ち込み(hold/early)・サンプル間の飛び(jump/rms) を表示する。耳の代わりではない。
import fs from "fs";
import { SpessaSynthProcessor, SoundBankLoader, BasicSoundBank } from "spessasynth_core";
const [ov, prog, keysArg, holdArg] = process.argv.slice(2);
await BasicSoundBank.isSF3DecoderReady;
const SR = 44100;
const proc = new SpessaSynthProcessor(SR, { effectsEnabled: false, maxBufferSize: 512 });
await proc.processorInitialized;
proc.soundBankManager.addSoundBank(SoundBankLoader.fromArrayBuffer(fs.readFileSync("src/audio/soundfont/game.sf3").buffer.slice(0)), "main");
proc.soundBankManager.addSoundBank(SoundBankLoader.fromArrayBuffer(fs.readFileSync(ov).buffer.slice(0)), "ov");
proc.soundBankManager.priorityOrder = ["ov", "main"];
proc.programChange(0, Number(prog));
const keys = (keysArg || "36,48,60,72,84").split(",").map(Number);
const hold = Number(holdArg || 1.2);
const goert=(x,fr)=>{const w=2*Math.PI*fr/SR;const c=2*Math.cos(w);let s0=0,s1=0,s2=0;for(let i=0;i<x.length;i++){s0=x[i]+c*s1-s2;s2=s1;s1=s0}return Math.sqrt(s1*s1+s2*s2-c*s1*s2)/x.length};
const out=[];
for (const k of keys) {
  const total = Math.ceil((hold + 0.6) * SR); const L = new Float32Array(total), R = new Float32Array(total);
  proc.noteOn(0, k, 100); let off=false;
  for (let pos = 0; pos < total; pos += 512) { if (!off && pos/SR >= hold) { proc.noteOff(0, k); off=true; } proc.process(L, R, pos, Math.min(512, total - pos)); }
  const m = new Float32Array(total); for (let i=0;i<total;i++) m[i]=(L[i]+R[i])/2;
  let pk=0; for (const v of m) pk=Math.max(pk,Math.abs(v));
  const f0=440*2**((k-69)/12); const wl=f0>600?0.1:0.45; const st=Math.floor(0.2*SR), w0=m.subarray(st, st+Math.floor(wl*SR));
  const win=Float32Array.from(w0,(v,i)=>v*(0.5-0.5*Math.cos(2*Math.PI*i/w0.length)));
  const pts=[];for(let c=-1380;c<=2500;c+=10){const fr=f0*2**(c/1200);if(fr>SR/2.1)break;pts.push([c,goert(win,fr)])}
  const mx=Math.max(...pts.map(p=>p[1]));let near=0,nc=0;for(const [c,v] of pts){if(Math.abs(c)<=100&&v>near){near=v;nc=c}}
  // 後半(保持中)と前半の音量(ループの落ち込み確認)
  const rms=(a,b)=>{let s=0,n=0;for(let i=Math.floor(a*SR);i<Math.floor(b*SR)&&i<total;i++){s+=m[i]*m[i];n++}return Math.sqrt(s/Math.max(1,n))};
  const r1=rms(0.15,0.5), r2=rms(hold-0.4,hold-0.05);
  // 最大のサンプル間ジャンプ(プチッの検出): 保持区間の 1階差分の最大 / rms
  let mj=0;for(let i=Math.floor(0.3*SR);i<Math.floor((hold-0.05)*SR);i++){mj=Math.max(mj,Math.abs(m[i+1]-m[i]))}
  const rr=rms(0.2,Math.min(hold,1.0)); out.push(`k${k}:rms${(20*Math.log10(rr+1e-9)).toFixed(1)}dB pk${(20*Math.log10(pk+1e-9)).toFixed(0)}dB f0ok=${near/mx>=0.3?"Y":"?"}(${nc}c,${(near/mx).toFixed(2)}) hold/early=${(20*Math.log10((r2+1e-9)/(r1+1e-9))).toFixed(1)}dB jump/rms=${(mj/(r2+1e-9)).toFixed(1)}`);
}
console.log(ov.split("/").pop(), "prog", prog, "\n  "+out.join("\n  "));
