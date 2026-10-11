import type { NamHost } from "./nam/nam-host";
import { SampledBgm, SampledSe } from "./sampled-engine";
import { createBgmBus, createHallImpulse, scheduleInstrumentNote, type Source } from "./voices";
import { noteNameToMidi } from "./note";
import { DUCK_DB, RoundRobin, SeThrottle, duckBgmForSe, duckLevelOf, makeVariants, playSfx, recipeDuration, tuneSe, type DuckLevel, type SfxRecipe } from "./sfx-synth";
import { flattenScore, getScoreDurationSec, type Score, type ScheduledNote } from "./score";

/** `?synth` をつけて開くと、録音音源を使わず合成音だけで鳴らす（音の比較・不具合の切り分け用）。 */
const SYNTH_ONLY_FROM_URL = typeof location !== "undefined" && new URLSearchParams(location.search).has("synth");
const SCHEDULE_AHEAD_SEC = 2.5;
const SCHEDULE_INTERVAL_MS = 250;

/**
 * Web Audio APIでBGM・効果音を鳴らす。
 * ブラウザの決まりで、最初の操作（クリック・キー入力・タップ）があるまで音は出せないため、
 * AudioContextの生成は最初のユーザー操作まで遅らせる（`ensureContext` を参照）。
 */
export class AudioEngine {
  private ctx: AudioContext | null = null;
  private bgmGain: GainNode | null = null;
  /** 曲の切り替え（フェード）とダッキング用の音量。bgmGain のあとに直列でつなぐ（bgm-director.ts が動かす）。 */
  private bgmDuck: GainNode | null = null;
  private bgmFade: GainNode | null = null;
  private seGain: GainNode | null = null;
  private sfxThrottle = new SeThrottle();
  private sfxRobin = new RoundRobin();
  private sfxVariants = new Map<string, SfxRecipe[]>();
  /** BGM の調（主音 0〜11 と音階名）。※調 の SE をここへ寄せる。 */
  private sfxKey: { tonic: number; scale: string } | null = null;

  private bgmVolume = 0.6;
  /** 曲ごとの音量補正（倍率。`Score.trimDb` から。曲を鳴らすたびに更新）。 */
  private bgmTrim = 1;
  private seVolume = 0.8;
  private muted = false;

  private bgmLoopHandle: number | null = null;
  private activeBgmNodes = new Set<Source>();
  /** BGMだけに、ほんのり残響をかけるための入り口（`ensureContext`で用意する）。 */
  private bgmBus: GainNode | null = null;
  /** 録音音源（サウンドフォント）のBGM再生。準備ができるまでは合成音で鳴らす。 */
  private sampled = new SampledBgm();
  private sampledBus: GainNode | null = null;
  /** 効果音: 残響の出口と、録音音源のシンセサイザー。 */
  private seBus: GainNode | null = null;
  private sampledSe = new SampledSe();
  private currentBgm: Score | null = null;
  /** 版（modern/ps2）に応じた、高音の丸めとホール残響の段。 */
  private profileLp: BiquadFilterNode | null = null;
  private hallSend: GainNode | null = null;
  private synthOnly = SYNTH_ONLY_FROM_URL;
  private bgmLoopStart = 0;
  private bgmDurationSec = 0;

  /** 最初のユーザー操作のタイミングで呼ぶ。AudioContextを用意し、一時停止も解除する。 */
  private ensureContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.bgmGain = this.ctx.createGain();
      this.applyBgmGain();
      this.bgmDuck = this.ctx.createGain();
      this.bgmFade = this.ctx.createGain();
      this.bgmGain.connect(this.bgmDuck);
      this.bgmDuck.connect(this.bgmFade);
      this.bgmFade.connect(this.ctx.destination);
      this.bgmBus = createBgmBus(this.ctx, this.bgmGain);
      // 録音音源は、ほんの少しだけ残響を足して、同じ出口（音量・仕上げ）を通す
      // 録音音源の出口には「版」の段を挟む: 高音を丸める低域通過フィルターと、ホール残響（PS2世代の音）
      const lp = this.ctx.createBiquadFilter();
      lp.type = "lowpass";
      lp.frequency.value = 22000;
      lp.Q.value = 0.6;
      lp.connect(this.bgmGain);
      const hall = this.ctx.createConvolver();
      hall.buffer = createHallImpulse(this.ctx);
      const send = this.ctx.createGain();
      send.gain.value = 0;
      lp.connect(send);
      send.connect(hall);
      hall.connect(this.bgmGain);
      this.profileLp = lp;
      this.hallSend = send;
      this.sampledBus = createBgmBus(this.ctx, lp, 0.1);
      if (!this.synthOnly) {
        void this.sampled.load(this.ctx, this.sampledBus).then(async (ok) => {
          if (ok && this.ctx && this.seBus) {
            await this.sampledSe.load(this.sampled, this.seBus);
          }
          if (ok && this.currentBgm && this.bgmLoopHandle !== null) {
            // 準備ができたら、いま合成音で鳴っている曲を、同じ位置から録音音源に切り替える
            this.playBgm(this.currentBgm, this.getBgmPositionSec());
          }
        });
      }

      this.seGain = this.ctx.createGain();
      this.seGain.gain.value = this.muted ? 0 : this.seVolume;
      this.seGain.connect(this.ctx.destination);
      // 効果音にも仕上げをかける。残響は短く軽く（間延びせず、鋭く聞こえるように）
      this.seBus = createBgmBus(this.ctx, this.seGain, 0.16, 1.0, 1);
    }
    if (this.ctx.state === "suspended") {
      void this.ctx.resume();
    }
    return this.ctx;
  }

  /**
   * 音を1つ予約する。`rich`（BGM用）のときは、少しだけ音程をずらした2つ目の音を重ねて厚みを出し、
   * 立ち上がりに軽いアタック、鳴っている間にゆるやかな減衰をつけて、電子音の平らさをやわらげる。
   * 効果音は従来どおり（`rich`なし）。
   */
  private scheduleNote(
    ctx: AudioContext,
    destination: AudioNode,
    event: ScheduledNote,
    when: number,
    rich = false,
  ): Source[] {
    const instrumental = scheduleInstrumentNote(ctx, destination, event, when);
    if (instrumental.length > 0) {
      return instrumental;
    }
    const gain = ctx.createGain();
    const attack = rich ? 0.012 : 0.005;
    const release = Math.min(rich ? 0.12 : 0.05, event.durationSec * 0.3);
    const peak = event.volume;
    gain.gain.setValueAtTime(0, when);
    gain.gain.linearRampToValueAtTime(peak, when + attack);
    if (rich) {
      // 鳴らし始めは少し強く、すぐ7割ほどに落ち着く（ゆるやかな減衰）
      gain.gain.linearRampToValueAtTime(peak * 0.72, when + Math.min(0.18, event.durationSec * 0.5));
    }
    const holdLevel = rich ? peak * 0.72 : peak;
    gain.gain.setValueAtTime(holdLevel, Math.max(when + attack, when + event.durationSec - release));
    gain.gain.linearRampToValueAtTime(0, when + event.durationSec);
    gain.connect(destination);

    const detunes = rich && event.waveform !== "sine" ? [-6, 6] : [0];
    const oscillators: OscillatorNode[] = [];
    for (const cents of detunes) {
      const osc = ctx.createOscillator();
      osc.type = event.waveform;
      osc.frequency.value = event.frequency;
      osc.detune.value = cents;
      if (detunes.length > 1) {
        const half = ctx.createGain();
        half.gain.value = 0.5;
        osc.connect(half);
        half.connect(gain);
      } else {
        osc.connect(gain);
      }
      osc.start(when);
      osc.stop(when + event.durationSec + 0.02);
      oscillators.push(osc);
    }
    return oscillators;
  }

  /**
   * 効果音を鳴らす。`gm`つきのパートは録音音源で、それ以外（と、録音音源の準備前）は合成音で鳴らす。
   * 音の始まりの時刻（startSec）どおりに、順番に鳴らす。
   */
  playSe(score: Score): void {
    const ctx = this.ensureContext();
    const secPerBeat = 60 / score.tempoBpm;
    const synthTracks: Score["tracks"] = [];
    for (const track of score.tracks) {
      if (track.gm !== undefined && this.sampledSe.isReady() && !this.synthOnly) {
        let beat = 0;
        for (const n of track.notes) {
          if (n.note !== "R") {
            const midi = noteNameToMidi(n.note);
            const velocity = Math.max(18, Math.min(127, Math.round(34 + track.volume * (n.velocity ?? 1) * 430)));
            this.sampledSe.note(track.gm, track.gmDrum === true, midi, velocity, beat * secPerBeat, n.durationBeats * secPerBeat);
          }
          beat += n.durationBeats;
        }
      } else {
        synthTracks.push(track);
      }
    }
    const bus = this.seBus ?? this.seGain!;
    for (const event of flattenScore({ ...score, tracks: synthTracks })) {
      this.scheduleNote(ctx, bus, event, ctx.currentTime + event.startSec);
    }
  }

  /** BGM の調を知らせる（主音 0〜11・音階名）。以後の playSfx で ※調 の SE がこの音階へ寄る。null で解除。 */
  setSfxKey(key: { tonic: number; scale: string } | null): void {
    this.sfxKey = key;
    this.sfxVariants.clear();
  }

  /**
   * 合成の SE（sfx-synth.ts のレシピ）を鳴らす。同じ SE の連打は throttleMs で間引き、vary のある SE は 4 変種を順に回す。
   * 通知・ファンファーレ・警告の SE は、鳴っている間だけ BGM を下げる（−2/−4/−8dB）。鳴らしたら true、間引かれたら false。
   */
  playSfx(recipe: SfxRecipe, opts: { duck?: DuckLevel; gainDb?: number; pan?: number } = {}): boolean {
    const ctx = this.ensureContext();
    if (!this.sfxThrottle.allow(recipe.id, ctx.currentTime * 1000, recipe.throttleMs ?? 0)) return false;
    let r = recipe;
    if (this.sfxKey) r = tuneSe(r, this.sfxKey.tonic, this.sfxKey.scale);
    let cacheKey = this.sfxKey ? `${recipe.id}@${this.sfxKey.tonic}${this.sfxKey.scale}` : recipe.id;
    if (r.vary) {
      let vs = this.sfxVariants.get(recipe.id);
      if (!vs) this.sfxVariants.set(recipe.id, (vs = makeVariants(r, 4, 1)));
      const i = this.sfxRobin.next(recipe.id, vs.length);
      r = vs[i];
      cacheKey += `#${i}`;
    }
    playSfx(ctx, this.seBus ?? this.seGain!, r, ctx.currentTime, { gainDb: opts.gainDb, pan: opts.pan, cacheKey });
    this.duckBgm(opts.duck ?? duckLevelOf(recipe), recipeDuration(recipe));
    return true;
  }

  /** BGM を level の分だけ一時的に下げ、holdSec 秒後に戻す。 */
  duckBgm(level: DuckLevel, holdSec: number): void {
    if (!this.ctx || !this.bgmDuck || !DUCK_DB[level]) return;
    duckBgmForSe(this.bgmDuck.gain, level, this.ctx.currentTime, holdSec);
  }

  /** `offsetSec`: 曲の途中（この秒数の位置）から鳴らす。BGMプレイヤーの「聴きたい部分から再生」用。 */
  playBgm(score: Score, offsetSec = 0): void {
    this.stopBgm();
    this.bgmTrim = Math.pow(10, (score.trimDb ?? 0) / 20);
    this.applyBgmGain();
    const ctx = this.ensureContext();
    const durationSec = getScoreDurationSec(score);
    if (durationSec <= 0) {
      return;
    }
    this.currentBgm = score;
    this.applyEdition(score.edition ?? "modern");
    if (this.sampled.isReady() && !this.synthOnly) {
      this.sampled.play(score, offsetSec);
      // シーケンサーが位置を返せないとき（音が1つもない曲など）のための、目安の時計
      this.bgmLoopStart = ctx.currentTime - offsetSec;
      this.bgmDurationSec = durationSec;
      this.bgmLoopHandle = -1; // 「鳴っている」印（録音音源はシーケンサーが自分でループする）
      return;
    }

    // 曲全体を一度に予約すると、長い曲では数千個の音を一気に作ってしまい、音が途切れたり出なくなる。
    // そこで、先の数秒ぶんだけを少しずつ予約する（次の周回も同じ要領でつなぐ）。
    const events = flattenScore(score).sort((x, y) => x.startSec - y.startSec);
    const offset = Math.max(0, Math.min(offsetSec, durationSec - 0.01));
    let loopStart = ctx.currentTime + 0.08 - offset;
    let index = 0;
    while (index < events.length && events[index].startSec < offset) {
      index++;
    }
    this.bgmLoopStart = loopStart;
    this.bgmDurationSec = durationSec;

    const scheduleAhead = (): void => {
      const horizon = ctx.currentTime + SCHEDULE_AHEAD_SEC;
      if (events.length === 0) {
        // 音が1つもない曲（1から作りはじめた曲など）: 位置だけ進める
        while (score.loop && ctx.currentTime > loopStart + durationSec) loopStart += durationSec;
        this.bgmLoopStart = loopStart;
        return;
      }
      for (;;) {
        if (index >= events.length) {
          if (!score.loop) {
            return;
          }
          index = 0;
          loopStart += durationSec;
          this.bgmLoopStart = loopStart;
        }
        const event = events[index];
        const when = loopStart + event.startSec;
        if (when > horizon) {
          return;
        }
        const nodes = this.scheduleNote(ctx, this.bgmBus!, event, Math.max(when, ctx.currentTime), true);
        for (const node of nodes) {
          this.activeBgmNodes.add(node);
          node.onended = () => this.activeBgmNodes.delete(node);
        }
        index++;
      }
    };

    scheduleAhead();
    this.bgmLoopHandle = window.setInterval(scheduleAhead, SCHEDULE_INTERVAL_MS);
  }

  /** NAM（実際のアンプを学習したモデル）を使えるようにする（作曲ソフトだけ）。 */
  setNamHost(host: NamHost | null): void {
    this.sampled.setNam(host);
  }

  /** 作曲ソフト用: 録音音源（サウンドフォント）を入れかえる。 */
  swapSoundfont(buf: ArrayBuffer): Promise<void> {
    return this.sampled.swapSoundfont(buf);
  }

  /** 作曲ソフト用: ベース・ドラムの追加の音源を入れる／はずす（slot は "bass"・"drums"・"synth"・"guitar"。null ではずす）。 */
  setOverlaySoundfont(slot: "bass" | "drums" | "synth" | "guitar", buf: ArrayBuffer | null): Promise<void> {
    return this.sampled.setOverlay(slot, buf);
  }

  /** 作曲ソフト用: 音の場（AudioContext）。録音トラックの再生や録音に使う。 */
  audioContext(): AudioContext {
    return this.ensureContext();
  }

  /** 作曲ソフト用: 録音トラックの出口（録音音源と同じ仕上げ・版の段・BGMの音量を通る）。 */
  clipDestination(): AudioNode {
    this.ensureContext();
    return this.sampledBus!;
  }

  /** 版に合わせて、高音の丸めとホール残響の量を切り替える。 */
  private applyEdition(edition: "modern" | "ps2" | "real"): void {
    if (!this.ctx || !this.profileLp || !this.hallSend) {
      return;
    }
    const t = this.ctx.currentTime;
    this.profileLp.frequency.setTargetAtTime(edition === "ps2" ? 15500 : edition === "real" ? 19000 : 22000, t, 0.02);
    // 実楽器版は、自然なホール（生のオーケストラやバンドの録音のような響き）を薄く
    this.hallSend.gain.setTargetAtTime(edition === "ps2" ? 0.34 : edition === "real" ? 0.15 : 0, t, 0.02);
  }

  /** true にすると、録音音源を使わず合成音だけで鳴らす（音の聴き比べ用）。鳴っている曲は同じ位置から切り替える。 */
  setSynthOnly(value: boolean): void {
    if (this.synthOnly === value) {
      return;
    }
    this.synthOnly = value;
    if (this.currentBgm && this.bgmLoopHandle !== null) {
      this.playBgm(this.currentBgm, this.getBgmPositionSec());
    }
  }

  /** 録音音源の準備ができているか（BGMプレイヤーの表示用）。 */
  isSampledReady(): boolean {
    return this.sampled.isReady();
  }

  /** いま鳴っているBGMを、曲の中の指定位置へ移す（曲の頭に戻さず、その場で移動）。区間リピートなどに使う。 */
  seekBgm(sec: number): void {
    if (this.sampled.isPlaying()) {
      this.sampled.seek(sec);
      return;
    }
    if (this.currentBgm && this.bgmLoopHandle !== null) {
      this.playBgm(this.currentBgm, sec);
    }
  }

  /** いま鳴っているBGMの、曲の中での位置（秒）。鳴っていなければ0。 */
  getBgmPositionSec(): number {
    if (this.sampled.isPlaying()) {
      const p = this.sampled.positionSec();
      if (Number.isFinite(p) && p >= 0) return p;
    }
    if (!this.ctx || this.bgmLoopHandle === null || this.bgmDurationSec <= 0) {
      return 0;
    }
    const pos = this.ctx.currentTime - this.bgmLoopStart;
    return Math.max(0, pos % this.bgmDurationSec);
  }

  stopBgm(): void {
    this.sampled.stop();
    if (this.bgmLoopHandle !== null) {
      if (this.bgmLoopHandle >= 0) {
        window.clearInterval(this.bgmLoopHandle);
      }
      this.bgmLoopHandle = null;
    }
    for (const node of this.activeBgmNodes) {
      try {
        node.stop();
      } catch {
        // すでに再生が終わっているノードは無視する。
      }
    }
    this.activeBgmNodes.clear();
  }

  /** 音量ノードごとの、直前の動き（いまの値を自分で計算するため。同じ瞬間に2回呼ばれても、前の指定を引き継げる）。 */
  private gainRamps = new Map<GainNode, { from: number; to: number; t0: number; t1: number }>();

  /** 音量ノードを seconds かけて level（0〜1）へ動かす（いまの値から。途中で呼び直してもプチッとならない）。 */
  private rampGain(node: GainNode | null, level: number, seconds: number): void {
    if (!node || !this.ctx) return;
    const p = node.gain;
    const t = this.ctx.currentTime;
    const prev = this.gainRamps.get(node);
    const now = prev ? (t >= prev.t1 ? prev.to : prev.from + ((prev.to - prev.from) * (t - prev.t0)) / Math.max(1e-6, prev.t1 - prev.t0)) : p.value;
    p.cancelScheduledValues(t);
    p.setValueAtTime(now, t);
    if (seconds <= 0.001) { p.setValueAtTime(level, t); this.gainRamps.set(node, { from: level, to: level, t0: t, t1: t }); }
    else { p.linearRampToValueAtTime(level, t + seconds); this.gainRamps.set(node, { from: now, to: level, t0: t, t1: t + seconds }); }
  }

  /** 曲の切り替え用の音量（0〜1）を動かす。bgm-director.ts のフェード用。 */
  rampBgmFade(level: number, seconds: number): void {
    this.rampGain(this.bgmFade, level, seconds);
  }

  /** ダッキング用の音量（0〜1）を動かす。bgm-director.ts の会話・効果音の一瞬の音量下げ用。 */
  rampBgmDuck(level: number, seconds: number): void {
    this.rampGain(this.bgmDuck, level, seconds);
  }

  /** BGMの音量（プレイヤーが決めた音量 × 曲ごとの補正。ミュート中は0）を反映する。 */
  private applyBgmGain(): void {
    if (this.bgmGain) {
      this.bgmGain.gain.value = this.muted ? 0 : this.bgmVolume * this.bgmTrim;
    }
  }

  setBgmVolume(volume: number): void {
    this.bgmVolume = volume;
    if (this.bgmGain) {
      this.applyBgmGain();
    }
  }

  setSeVolume(volume: number): void {
    this.seVolume = volume;
    if (this.seGain) {
      this.seGain.gain.value = this.muted ? 0 : volume;
    }
  }

  setMuted(muted: boolean): void {
    this.muted = muted;
    this.applyBgmGain();
    if (this.seGain) {
      this.seGain.gain.value = muted ? 0 : this.seVolume;
    }
  }

  isMuted(): boolean {
    return this.muted;
  }
}
