import type { Direction } from "../input/direction";
import type { PlayerState } from "./player";

/**
 * 仲間が主人公の後ろをついて歩く（王道RPGの隊列）。主人公が通った道すじを「パンくず」（2ドットおき）として覚え、
 * 仲間は、そのパンくずの上を、決まった間隔（1人ぶん約20ドット）をあけて追いかける。立ち止まると追いついて止まる。
 * 見た目だけで、当たり判定や会話には関わらない。
 */
export interface Crumb {
  x: number;
  y: number;
  dir: Direction;
}

export interface FollowerState {
  /** 今いるパンくずの通し番号（小数。進むほど新しい）。 */
  seq: number;
  moving: boolean;
  animMs: number;
  /** 動いていない時間（ms）。 */
  idleMs?: number;
}

/** パンくずの間隔（ドット）。細かくして、仲間の位置を毎フレームなめらかに動かす（粗いと、2ドットずつカクカクして見える）。 */
export const CRUMB_SPACING = 0.5;
/** 仲間どうしの間隔（パンくずの数。40個＝20ドット）。 */
export const GAP_CRUMBS = 40;
/** 追いかける速さ（パンくず／秒）。主人公の歩く速さ（約64ドット/秒＝128個/秒）より少し速い。 */
const CHASE_SPEED = 150;
/** 止まったと見なすまでの時間（ms）。歩いている途中で、歩く絵が止まっては動くのをくり返さないための余裕。 */
const STOP_GRACE_MS = 90;

const MAX_CRUMBS = 2400;

export class PartyTrail {
  private crumbs: Crumb[] = [];
  /** crumbs[0] の通し番号。 */
  private base = 0;
  private followers: FollowerState[] = [];

  private get latestSeq(): number {
    return this.base + this.crumbs.length - 1;
  }

  reset(player: PlayerState): void {
    this.crumbs = [{ x: player.x, y: player.y, dir: player.direction }];
    this.base = 0;
    this.followers = this.followers.map(() => ({ seq: 0, moving: false, animMs: 0 }));
  }

  /** つながる地図の端をまたいだとき、道すじ全体をずらして、仲間がとんで見えないようにする。 */
  shift(dx: number, dy: number): void {
    for (const c of this.crumbs) {
      c.x += dx;
      c.y += dy;
    }
  }

  /** 毎フレーム呼ぶ。`count` は、ついてくる仲間の人数。`speed` は、主人公の歩く速さの倍率（速く歩くとき、仲間も同じだけ速く追いかける）。 */
  update(player: PlayerState, dtMs: number, count: number, speed = 1): void {
    if (this.crumbs.length === 0) {
      this.reset(player);
    }
    const last = this.crumbs[this.crumbs.length - 1];
    const dx = player.x - last.x;
    const dy = player.y - last.y;
    const dist = Math.hypot(dx, dy);
    if (dist > 40) {
      this.reset(player); // 場面の切り替えなどで、とつぜん遠くへ移った
    } else if (dist >= CRUMB_SPACING) {
      const n = Math.floor(dist / CRUMB_SPACING);
      for (let i = 1; i <= n; i++) {
        this.crumbs.push({ x: last.x + (dx * i * CRUMB_SPACING) / dist, y: last.y + (dy * i * CRUMB_SPACING) / dist, dir: player.direction });
      }
      if (this.crumbs.length > MAX_CRUMBS) {
        const drop = this.crumbs.length - MAX_CRUMBS;
        this.crumbs.splice(0, drop);
        this.base += drop;
      }
    }
    while (this.followers.length < count) {
      this.followers.push({ seq: Math.max(this.base, this.latestSeq - GAP_CRUMBS * (this.followers.length + 1)), moving: false, animMs: 0 });
    }
    this.followers.length = count;
    this.followers.forEach((f, i) => {
      const target = Math.max(this.base, this.latestSeq - GAP_CRUMBS * (i + 1));
      f.seq = Math.max(this.base, f.seq);
      if (f.seq < target) {
        f.seq = Math.min(target, f.seq + (CHASE_SPEED * speed * dtMs) / 1000);
        f.idleMs = 0;
        f.moving = true;
        f.animMs += dtMs * speed;
      } else {
        f.idleMs = (f.idleMs ?? 0) + dtMs;
        if (f.idleMs >= STOP_GRACE_MS) {
          f.moving = false;
          f.animMs = 0;
        } else if (f.moving) {
          f.animMs += dtMs;
        }
      }
    });
  }

  /** i番目（0から）の仲間の今の位置と向き。 */
  followerAt(i: number): { x: number; y: number; dir: Direction; moving: boolean; animMs: number } | null {
    const f = this.followers[i];
    if (!f || this.crumbs.length === 0) {
      return null;
    }
    const index = Math.min(this.crumbs.length - 1, Math.max(0, Math.round(f.seq - this.base)));
    const c = this.crumbs[index];
    return { x: c.x, y: c.y, dir: c.dir, moving: f.moving, animMs: f.animMs };
  }

  get count(): number {
    return this.followers.length;
  }
}
