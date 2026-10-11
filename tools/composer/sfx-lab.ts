// SE ラボ（synth-sfx-guide.md §10 の 10）。58 種の合成 SE を一覧で鳴らし、スライダーで調整し、WAV と JSON に書き出す。
// 純 JS の合成（sfx-synth.ts）なので、ゲーム本体・Node のテスト・この画面で同じ音になる。
import { SFX_RECIPES } from "../../src/audio/sfx-recipes";
import { DUCK_DB, SE_MAX_SEC, adjustSe, checkSe, duckLevelOf, makeVariants, renderSfx, tuneSe, type SfxRecipe } from "../../src/audio/sfx-synth";
import { analyzeSamples, toWav16 } from "../../src/audio/synth-dsp";
import { SCALES } from "../../src/audio/scales";

const SR = 44100;
const $ = <T extends HTMLElement>(id: string): T => document.getElementById(id) as T;
let ctx: AudioContext | null = null;
let current: SfxRecipe = SFX_RECIPES[0];
let lastSamples: Float32Array | null = null;
let variantIndex = -1;

const NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
const val = (id: string): number => Number($<HTMLInputElement>(id).value);

function adjusted(): SfxRecipe {
  let r = current;
  const key = $<HTMLSelectElement>("tonic").value;
  if (key !== "") r = tuneSe(r, Number(key), $<HTMLSelectElement>("scale").value);
  if (variantIndex >= 0) r = makeVariants(r, 4, 1)[variantIndex];
  return adjustSe(r, { pitch: 2 ** (val("pitch") / 12), time: val("time"), attack: val("attack"), release: val("release"), peakDb: val("peak") });
}

function show(): void {
  const r = adjusted();
  const x = renderSfx(r, SR);
  lastSamples = x;
  const a = analyzeSamples(x, SR);
  const w = checkSe(a, r);
  $("stats").textContent = `山 ${a.peakDb.toFixed(1)}dBFS ／ RMS ${a.rmsDb.toFixed(1)}dB ／ 長さ ${a.lengthSec.toFixed(2)}秒（${r.kind} の上限 ${SE_MAX_SEC[r.kind]}秒）／ 立ち上がり ${a.attackMs.toFixed(0)}ms ／ 重心 ${a.centroidHz.toFixed(0)}Hz ／ 1〜4kHz ${(a.band1to4k * 100).toFixed(0)}% ／ BGM を ${DUCK_DB[duckLevelOf(r)]}dB`;
  $("warn").textContent = w.length ? w.join("\n") : "検査: 問題なし";
  $("warn").className = w.length ? "warn" : "ok";
  draw(x);
  $("json").textContent = JSON.stringify(r, null, 1);
}

function draw(x: Float32Array): void {
  const c = $<HTMLCanvasElement>("wave");
  const g = c.getContext("2d")!;
  g.clearRect(0, 0, c.width, c.height);
  g.strokeStyle = "#19d9ff";
  g.beginPath();
  const step = Math.max(1, Math.floor(x.length / c.width));
  for (let px = 0; px < c.width; px++) {
    let mx = 0;
    for (let i = px * step; i < Math.min(x.length, (px + 1) * step); i++) mx = Math.max(mx, Math.abs(x[i]));
    g.moveTo(px, c.height / 2 - mx * c.height / 2);
    g.lineTo(px, c.height / 2 + mx * c.height / 2);
  }
  g.stroke();
}

function play(): void {
  if (!lastSamples) show();
  ctx ??= new AudioContext();
  void ctx.resume();
  const b = ctx.createBuffer(1, lastSamples!.length, SR);
  b.getChannelData(0).set(lastSamples!);
  const s = ctx.createBufferSource();
  s.buffer = b;
  s.connect(ctx.destination);
  s.start();
}

function download(name: string, data: BlobPart, type: string): void {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([data], { type }));
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

function select(r: SfxRecipe): void {
  current = r;
  variantIndex = -1;
  document.querySelectorAll(".se").forEach((e) => e.classList.toggle("on", (e as HTMLElement).dataset.id === r.id));
  $("title").textContent = `${r.name}（${r.id}）— ${r.group}`;
  show();
  play();
}

function init(): void {
  const list = $("list");
  let group = "";
  for (const r of SFX_RECIPES) {
    if (r.group !== group) {
      group = r.group;
      const h = document.createElement("h3");
      h.textContent = group;
      list.appendChild(h);
    }
    const b = document.createElement("button");
    b.className = "se";
    b.dataset.id = r.id;
    b.textContent = r.name;
    b.onclick = () => select(r);
    list.appendChild(b);
  }
  const tonic = $<HTMLSelectElement>("tonic");
  tonic.innerHTML = `<option value="">調に合わせない</option>` + NOTE_NAMES.map((n, i) => `<option value="${i}">${n}</option>`).join("");
  const scale = $<HTMLSelectElement>("scale");
  scale.innerHTML = SCALES.map((s) => `<option value="${s.id}">${s.name}</option>`).join("");
  scale.value = "ionian";
  for (const id of ["pitch", "time", "attack", "release", "peak", "tonic", "scale"]) $(id).addEventListener("input", () => { show(); });
  $("play").onclick = () => { show(); play(); };
  $("variant").onclick = () => { variantIndex = (variantIndex + 1) % 4; $("variant").textContent = `変種 ${variantIndex + 1}/4 を鳴らす`; show(); play(); };
  $("reset").onclick = () => { $<HTMLInputElement>("pitch").value = "0"; $<HTMLInputElement>("time").value = "1"; $<HTMLInputElement>("attack").value = "1"; $<HTMLInputElement>("release").value = "1"; $<HTMLInputElement>("peak").value = String(current.peakDb ?? (current.kind === "ui" ? -6 : -4.5)); variantIndex = -1; show(); };
  $("wav").onclick = () => { show(); download(`${current.id}.wav`, toWav16(lastSamples!, SR) as BlobPart, "audio/wav"); };
  $("save").onclick = () => { show(); download(`${current.id}.sfx.json`, JSON.stringify(adjusted(), null, 2), "application/json"); };
  select(SFX_RECIPES[0]);
}
init();
