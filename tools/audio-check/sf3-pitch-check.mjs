// 使い方: node tools/audio-check/sf3-pitch-check.mjs <音源.sf3>   （リポジトリの直下で実行）
// SF3 の各サンプルについて、根音(originalKey)の周波数 f0 の近く(±60セント)に基音の山があるか、無音でないかを調べる。基音が極端に弱い低音は "no-f0" と出ることがある（倍音が整数倍に乗っているかは別に確かめる）。 デチューンした重ね音の高音域は、うなりで基音が弱く出て誤検出になる（作曲ソフトと同じ描画での検査 sf3-render-check は短い窓で測るので影響されにくい）。
import fs from "fs";
import {execFileSync} from "child_process";
import { SoundBankLoader, BasicSoundBank } from "spessasynth_core";
await BasicSoundBank.isSF3DecoderReady;
const f=process.argv[2];
const b=SoundBankLoader.fromArrayBuffer(fs.readFileSync(f).buffer.slice(0));
const dec=(s)=>{const buf=execFileSync("ffmpeg",["-v","error","-f","ogg","-i","pipe:0","-f","f32le","-ac","1","-"],{input:Buffer.from(s.compressedData),maxBuffer:1<<28});return new Float32Array(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength));};
const goert=(x,fr,sr)=>{const w=2*Math.PI*fr/sr;const c=2*Math.cos(w);let s0=0,s1=0,s2=0;for(let i=0;i<x.length;i++){s0=x[i]+c*s1-s2;s2=s1;s1=s0}return Math.sqrt(s1*s1+s2*s2-c*s1*s2)/x.length};
const seen=new Set();let n=0,silent=0,peak=0;const flags=[],shown=[];
for(const inst of b.instruments)for(const z of inst.zones){const s=z.sample;if(seen.has(s))continue;seen.add(s);
 if(s.sampleType===4)continue; // right of pair: skip
 const a=dec(s),sr=s.sampleRate;
 let pk=0;for(let i=0;i<a.length;i++){const v=Math.abs(a[i]);if(v>pk)pk=v}
 if(pk<0.003){silent++;continue}
 peak=Math.max(peak,pk);
 const len=Math.min(Math.floor(0.45*sr),a.length);const st=Math.min(Math.floor(0.04*sr),a.length-len);const w0=a.subarray(st,st+len);
 const win=Float32Array.from(w0,(v,i)=>v*(0.5-0.5*Math.cos(2*Math.PI*i/w0.length)));
 const tune=(((z.generators?.find?.(g=>g.generatorType===51)?.generatorValue)||0)*100)+((z.generators?.find?.(g=>g.generatorType===52)?.generatorValue)||0)+(s.samplePitchCorrection||0);
 const f0=440*2**((s.originalKey-69)/12)*2**(tune/1200);
 // 0.45 f0 .. 4.2 f0 を 10 セント刻みで走査
 const pts=[];for(let c=-1380;c<=2500;c+=10){const fr=f0*2**(c/1200);if(fr>sr/2.1)break;pts.push([c,goert(win,fr,sr)])}
 const mx=Math.max(...pts.map(p=>p[1]));
 let near=0,nc=0;for(const [c,v] of pts){if(Math.abs(c)<=60&&v>near){near=v;nc=c}}
 const ok=near>=0.3*mx; n++;
 if(!ok){ // 最も強いピークの比
   const top=pts.reduce((a,p)=>p[1]>a[1]?p:a);flags.push(`${s.name.slice(0,18)}(k${s.originalKey}) near/max=${(near/mx).toFixed(2)} top@${top[0]}c`);}
 else if(Math.abs(nc)>35)shown.push(`${s.name.slice(0,14)}:${nc}c`);
}
console.log(f.split("/").pop().padEnd(28),"samples",n,"silent",silent,"peak",peak.toFixed(2),"| no-f0 flags",flags.length,flags.slice(0,6).join("; "),"| detune>35c:",shown.length,shown.slice(0,4).join(" "));
