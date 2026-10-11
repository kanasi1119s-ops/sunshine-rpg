import { getScoreDurationSec, type BossPhase, type Score } from "./score";

/**
 * ゲーム用のBGM管理（docs/sound/game-music-guide.md §5.4・§10 の提案1・2・3、第1弾の積み残し「ボス戦の段階表」「ゲーム内ダッキング」）。
 * 再生エンジン（AudioEngine）の上に重ねる「指揮者」。曲を止めて次を鳴らすだけの切り替えを、次のように滑らかにする。
 *  ・曲の切り替えにフェード（前の曲を 0.3〜1秒で下げ、止めてから、次を小さい音から上げる。小節の頭まで待つ指定もできる）
 *  ・戦闘への切り替え（遭遇の一撃 ＋ フィールド曲を 0.3秒で下げる ＋ 戦闘曲は頭から）と、戦闘後に同じ位置から再開
 *  ・ダッキング（会話中は BGM を −5dB に 0.3秒で下げ、閉じたら 0.5秒で戻す。大きな効果音の一瞬は −3dB）
 *  ・ボス戦の段階表（HPの割合で、小節の頭で次の段階のループへ移る）
 *  ・ループ点（導入を1回だけ鳴らし、そのあと startBar〜endBar をくり返す。Score.meta.loop）
 * エンジンとの境目は BgmEngineLike だけなので、ゲーム側は AudioEngine をそのまま渡せる（rampBgmFade・rampBgmDuck を足してある）。
 */
export interface BgmEngineLike {
  playBgm(score: Score, offsetSec?: number): void;
  stopBgm(): void;
  getBgmPositionSec(): number;
  seekBgm(sec: number): void;
  /** 曲の切り替え用の音量（0〜1）を seconds かけて動かす。 */
  rampBgmFade(level: number, seconds: number): void;
  /** ダッキング用の音量（0〜1）を seconds かけて動かす。 */
  rampBgmDuck(level: number, seconds: number): void;
}

export interface Timers {
  setTimeout(fn: () => void, ms: number): unknown;
  clearTimeout(handle: unknown): void;
}
const realTimers: Timers = { setTimeout: (fn, ms) => setTimeout(fn, ms), clearTimeout: (h) => clearTimeout(h as ReturnType<typeof setTimeout>) };

export const dbToLinear = (db: number): number => Math.pow(10, db / 20);

/** ダッキングの標準値（game-music-guide.md §5.4・§8.1、synth-sfx-guide.md）。 */
export const DUCK_PRESETS = {
  /** 会話ウィンドウ: −5dB。0.3秒で下げ、0.5秒で戻す。 */
  dialogue: { db: -5, attackSec: 0.3, releaseSec: 0.5 },
  /** 大きな効果音（斬撃・魔法）: −3dB を一瞬。 */
  sfx: { db: -3, attackSec: 0.05, holdSec: 0.4, releaseSec: 0.5 },
  /** ファンファーレ・レベルアップ: −8dB を長めに。 */
  fanfare: { db: -8, attackSec: 0.1, holdSec: 2, releaseSec: 0.8 },
} as const;

export const BGM_DEFAULTS = {
  fadeOutSec: 0.6,
  fadeInSec: 0.8,
  /** 戦闘に入るとき。フィールド曲を 0.3秒で下げ、戦闘曲はほぼ頭から全員で鳴らす。 */
  battleFadeOutSec: 0.3,
  battleFadeInSec: 0.05,
  /** 戦闘のあとフィールドへ戻るとき。 */
  returnFadeOutSec: 0.4,
  returnFadeInSec: 1.0,
  /** 小節の頭まで待つ最長（秒）。これより遠いときは待たずに切り替える。 */
  alignMaxWaitSec: 1.5,
  /** ボスの段階の切り替えで、頭の一瞬だけ音量を落とす時間（秒）。 */
  phaseDipSec: 0.04,
} as const;

export interface ChangeOptions {
  /** 曲のID。いま鳴っている曲と同じIDなら何もしない（force で鳴らし直す）。 */
  id?: string;
  offsetSec?: number;
  fadeOutSec?: number;
  fadeInSec?: number;
  /** true なら、いま鳴っている曲の次の小節の頭まで待ってから切り替える（alignMaxWaitSec 以内のとき）。 */
  alignToBar?: boolean;
  force?: boolean;
}

interface Playing { id?: string; score: Score }
interface FieldMemory { id?: string; score: Score; positionSec: number }

/** いまの位置から次の小節の頭までの秒数（ちょうど小節の頭なら 0）。 */
export function secondsToNextBar(positionSec: number, bpm: number, beatsPerBar: number): number {
  const barSec = (beatsPerBar * 60) / bpm;
  if (!(barSec > 0)) return 0;
  const r = positionSec % barSec;
  return r < 1e-6 || barSec - r < 1e-6 ? 0 : barSec - r;
}

export const beatsPerBarOf = (score: Score): number => score.meta?.beatsPerBar ?? (score.timeSig?.num && score.timeSig.den ? (score.timeSig.num * 4) / score.timeSig.den : 4);

// ───────── ボス戦の段階 ─────────
export interface PhaseWindow { id: string; startSec: number; endSec: number; hpBelow: number }
export interface BossPlan { barSec: number; phases: PhaseWindow[] }

/** Score.meta.bossPhases から、秒で表した段階表を作る。段階表がなければ null。 */
export function planBossPhases(score: Score): BossPlan | null {
  const phases: BossPhase[] | undefined = score.meta?.bossPhases;
  if (!phases?.length) return null;
  const barSec = (beatsPerBarOf(score) * 60) / score.tempoBpm;
  return { barSec, phases: phases.map((p) => ({ id: p.id, startSec: (p.startBar - 1) * barSec, endSec: p.endBar * barSec, hpBelow: p.hpBelow })) };
}

/** HPの割合（0〜1）に対応する段階の番号。最初の段階は常に当てはまり、後の段階は hp が hpBelow を下回ったとき。 */
export function phaseIndexForHp(plan: BossPlan, hp: number): number {
  let idx = 0;
  plan.phases.forEach((p, k) => { if (k > 0 && hp < p.hpBelow) idx = k; });
  return idx;
}

export class BgmDirector {
  private timers: Timers;
  private current: Playing | null = null;
  private playing = false;
  private token = 0;
  private pending: unknown = null;
  private loopTimer: unknown = null;
  private field: FieldMemory | null = null;
  private battleActive = false;
  private ducks = new Map<string, number>();
  private pulseId = 0;
  private pulseTimers = new Map<string, unknown>();
  private boss: { plan: BossPlan; index: number; hp: number; switching: boolean; allowBack: boolean } | null = null;

  constructor(private engine: BgmEngineLike, opts: { timers?: Timers } = {}) {
    this.timers = opts.timers ?? realTimers;
  }

  // ───────── 状態 ─────────
  getState(): { id?: string; playing: boolean; battleActive: boolean; ducked: boolean; bossPhase: number | null; fieldMemory: { id?: string; positionSec: number } | null } {
    return { id: this.current?.id, playing: this.playing, battleActive: this.battleActive, ducked: this.ducks.size > 0, bossPhase: this.boss ? this.boss.index : null, fieldMemory: this.field ? { id: this.field.id, positionSec: this.field.positionSec } : null };
  }

  private clearPending(): void {
    if (this.pending !== null) { this.timers.clearTimeout(this.pending); this.pending = null; }
  }

  // ───────── 1. 曲の切り替えにフェード ─────────
  changeBgm(score: Score, o: ChangeOptions = {}): void {
    if (!o.force && this.playing && this.current && o.id !== undefined && this.current.id === o.id) return;
    const token = ++this.token;
    this.clearPending();
    this.disarmLoop();
    const fadeOut = Math.max(0, o.fadeOutSec ?? BGM_DEFAULTS.fadeOutSec);
    const fadeIn = Math.max(0, o.fadeInSec ?? BGM_DEFAULTS.fadeInSec);
    const start = (): void => {
      if (token !== this.token) return;
      this.pending = null;
      this.engine.stopBgm();
      this.engine.playBgm(score, o.offsetSec ?? 0);
      this.engine.rampBgmFade(0, 0); // 小さい音から（プチッという音を避ける）。最初の曲では playBgm が音の場を作るので、そのあとに指定する
      this.current = { id: o.id, score };
      this.playing = true;
      this.engine.rampBgmFade(1, fadeIn);
      this.armLoop();
    };
    if (!this.playing) { start(); return; }
    const begin = (): void => {
      if (token !== this.token) return;
      this.engine.rampBgmFade(0, fadeOut);
      this.pending = this.timers.setTimeout(start, fadeOut * 1000 + 20);
    };
    const wait = o.alignToBar && this.current ? secondsToNextBar(this.engine.getBgmPositionSec(), this.current.score.tempoBpm, beatsPerBarOf(this.current.score)) : 0;
    if (wait > 0 && wait <= (BGM_DEFAULTS.alignMaxWaitSec as number)) this.pending = this.timers.setTimeout(begin, wait * 1000);
    else begin();
  }

  /** フェードアウトして止める。 */
  stop(fadeOutSec: number = BGM_DEFAULTS.fadeOutSec): void {
    const token = ++this.token;
    this.clearPending();
    this.disarmLoop();
    this.boss = null;
    if (!this.playing) return;
    this.engine.rampBgmFade(0, fadeOutSec);
    this.pending = this.timers.setTimeout(() => {
      if (token !== this.token) return;
      this.pending = null;
      this.engine.stopBgm();
      this.engine.rampBgmFade(1, 0); // 止まっているうちに戻す（あとで engine.playBgm を直接呼んでも鳴る）
      this.playing = false;
      this.current = null;
    }, fadeOutSec * 1000 + 20);
  }

  // ───────── 3. 戦闘への切り替えと、戦闘後の再開 ─────────
  /** 戦闘に入る。フィールド曲の位置を覚え、遭遇の一撃（stinger）を鳴らし、フィールド曲を 0.3秒で下げて、戦闘曲を頭から鳴らす。 */
  enterBattle(battle: Score, o: { id?: string; stinger?: () => void; fadeOutSec?: number; offsetSec?: number } = {}): void {
    if (!this.battleActive && this.playing && this.current) {
      this.field = { id: this.current.id, score: this.current.score, positionSec: this.engine.getBgmPositionSec() };
    }
    this.battleActive = true;
    this.boss = null;
    o.stinger?.();
    this.changeBgm(battle, { id: o.id, force: true, offsetSec: o.offsetSec ?? 0, fadeOutSec: o.fadeOutSec ?? BGM_DEFAULTS.battleFadeOutSec, fadeInSec: BGM_DEFAULTS.battleFadeInSec });
  }

  /**
   * 戦闘が終わる。覚えておいたフィールド曲に戻る。
   * resume: "position"（同じ位置から。既定）／"head"（頭から）。rewindSec で少し戻して再開（耳が追いつく）。next を渡すと、フィールドではなくその曲へ（勝利のファンファーレなど）。
   */
  leaveBattle(o: { resume?: "position" | "head"; rewindSec?: number; fadeOutSec?: number; fadeInSec?: number; next?: { score: Score; id?: string } } = {}): void {
    const mem = this.field;
    this.battleActive = false;
    this.boss = null;
    if (o.next) {
      this.field = null;
      this.changeBgm(o.next.score, { id: o.next.id, force: true, fadeOutSec: o.fadeOutSec ?? BGM_DEFAULTS.returnFadeOutSec, fadeInSec: o.fadeInSec ?? BGM_DEFAULTS.returnFadeInSec });
      return;
    }
    if (!mem) { this.stop(o.fadeOutSec ?? BGM_DEFAULTS.returnFadeOutSec); return; }
    this.field = null;
    const dur = getScoreDurationSec(mem.score);
    const offset = o.resume === "head" || !(dur > 0) ? 0 : (((mem.positionSec - (o.rewindSec ?? 0)) % dur) + dur) % dur;
    this.changeBgm(mem.score, { id: mem.id, force: true, offsetSec: offset, fadeOutSec: o.fadeOutSec ?? BGM_DEFAULTS.returnFadeOutSec, fadeInSec: o.fadeInSec ?? BGM_DEFAULTS.returnFadeInSec });
  }

  // ───────── 2. ダッキング ─────────
  private applyDuck(seconds: number): void {
    const deepest = this.ducks.size ? Math.min(...this.ducks.values()) : 0;
    this.engine.rampBgmDuck(this.ducks.size ? dbToLinear(deepest) : 1, seconds);
  }
  /** key の理由でBGMを db（負の数）だけ下げ始める。同時に複数あれば、いちばん深いものに合わせる。 */
  beginDuck(key: string, db: number = DUCK_PRESETS.dialogue.db, attackSec: number = DUCK_PRESETS.dialogue.attackSec): void {
    this.ducks.set(key, Math.min(0, Math.max(-24, db)));
    this.applyDuck(attackSec);
  }
  endDuck(key: string, releaseSec: number = DUCK_PRESETS.dialogue.releaseSec): void {
    if (!this.ducks.delete(key)) return;
    this.applyDuck(releaseSec);
  }
  /** 会話ウィンドウを開く／閉じる。 */
  dialogOpen(): void { this.beginDuck("dialogue", DUCK_PRESETS.dialogue.db, DUCK_PRESETS.dialogue.attackSec); }
  dialogClose(): void { this.endDuck("dialogue", DUCK_PRESETS.dialogue.releaseSec); }
  /** 大きな効果音・ファンファーレの一瞬だけ下げて、自動で戻す。 */
  duckPulse(kind: "sfx" | "fanfare" = "sfx"): void {
    const p = DUCK_PRESETS[kind];
    const key = `pulse-${++this.pulseId}`;
    this.beginDuck(key, p.db, p.attackSec);
    this.pulseTimers.set(key, this.timers.setTimeout(() => { this.pulseTimers.delete(key); this.endDuck(key, p.releaseSec); }, (p.attackSec + p.holdSec) * 1000));
  }

  // ───────── ループ点・ボスの段階 ─────────
  /** いま鳴っている範囲（ループ点か、ボスの段階）。曲全体をくり返すだけなら null（エンジン任せ）。 */
  private loopWindow(): { startSec: number; endSec: number } | null {
    if (!this.current) return null;
    if (this.boss) { const p = this.boss.plan.phases[this.boss.index]; return { startSec: p.startSec, endSec: p.endSec }; }
    const lp = this.current.score.meta?.loop;
    if (!lp) return null;
    const dur = getScoreDurationSec(this.current.score);
    return lp.startSec > 0.01 || lp.endSec < dur - 0.01 ? { startSec: lp.startSec, endSec: lp.endSec } : null;
  }
  private disarmLoop(): void {
    if (this.loopTimer !== null) { this.timers.clearTimeout(this.loopTimer); this.loopTimer = null; }
  }
  /** 範囲の終わりに着いたら、始まりへ移す予約をする。 */
  private armLoop(): void {
    this.disarmLoop();
    const w = this.loopWindow();
    if (!w || !this.playing) return;
    const remaining = w.endSec - this.engine.getBgmPositionSec();
    const token = this.token;
    this.loopTimer = this.timers.setTimeout(() => {
      this.loopTimer = null;
      if (token !== this.token || !this.playing) return;
      const now = this.loopWindow();
      if (!now) return;
      this.engine.seekBgm(now.startSec);
      this.armLoop();
    }, Math.max(0, remaining * 1000 - 10));
  }
  /** ゲームの毎フレーム（または時々）呼ぶと、位置がずれたときに範囲へ戻す。予約だけでもループするので、呼ばなくてもよい。 */
  tick(): void {
    const w = this.loopWindow();
    if (!w || !this.playing) return;
    const pos = this.engine.getBgmPositionSec();
    if (pos >= w.endSec + 0.05) { this.engine.seekBgm(w.startSec); this.armLoop(); }
  }

  /** ボス戦を始める。score.meta.bossPhases の最初の段階から鳴らす。段階表がなければ、ふつうの戦闘曲として鳴らす。 */
  startBoss(score: Score, o: { id?: string; stinger?: () => void; allowBack?: boolean } = {}): void {
    const plan = planBossPhases(score);
    this.enterBattle(score, { id: o.id, stinger: o.stinger, offsetSec: plan?.phases[0].startSec ?? 0 });
    if (!plan) { this.boss = null; return; }
    this.boss = { plan, index: 0, hp: 1, switching: false, allowBack: o.allowBack === true };
    if (this.playing) this.armLoop(); // すぐ鳴り始めた場合は、段階のループを予約する（フェード待ちのときは鳴り始めに予約される）
  }

  /** ボスのHPの割合（0〜1）を知らせる。段階が上がるなら、次の小節の頭で切り替える（短く音量を落として、頭に着地）。 */
  setBossHp(hp: number): void {
    const b = this.boss;
    if (!b) return;
    b.hp = hp;
    if (b.switching) return;
    const target = phaseIndexForHp(b.plan, hp);
    if (target === b.index || (target < b.index && !b.allowBack)) return;
    b.switching = true;
    const dip = BGM_DEFAULTS.phaseDipSec;
    const wait = secondsToNextBar(this.engine.getBgmPositionSec(), this.current ? this.current.score.tempoBpm : 120, this.current ? beatsPerBarOf(this.current.score) : 4);
    const token = this.token;
    this.disarmLoop();
    const dipAt = Math.max(0, wait - dip);
    this.timers.setTimeout(() => {
      if (token !== this.token || !this.boss) return;
      this.engine.rampBgmFade(0, dip);
      this.timers.setTimeout(() => {
        if (token !== this.token || !this.boss) return;
        // 待っているあいだにHPがさらに減っていたら、最新の段階へ
        const now = this.boss;
        const idx = Math.max(phaseIndexForHp(now.plan, now.hp), now.allowBack ? 0 : now.index);
        now.index = idx;
        now.switching = false;
        this.engine.seekBgm(now.plan.phases[idx].startSec);
        this.engine.rampBgmFade(1, dip * 2);
        this.armLoop();
      }, dip * 1000);
    }, dipAt * 1000);
  }
}
