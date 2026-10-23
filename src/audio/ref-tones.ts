/**
 * 参考の音（2026-10-23、人間「音源はソフトでも使えるようにしてね」）。
 * 人間が渡した参考録音を音源分離（demucs htdemucs_6s）して楽器ごとに 1/3 オクターブで測り、こちらの音（聞き比べ G）との差を埋める EQ を計算した数値。
 * 録音の音そのものは取り込んでいない（数値だけ）。名前は音の特徴にする（CLAUDE.md 1-1）。出どころは source に書く。
 * 使い方: 書き出しで `--ref-tone <id>`、作曲ソフトでは「参考の音」で選ぶ。ギター・ベース・ドラムの fx の EQ とフィルターを、この値に置きかえる
 *   （ほかの fx＝ルーム・ディレイ・コンプなどは残す）。guitarWide なら、左右に分かれた歪みギターを左右いっぱいにする。
 * 計算の道具: tools/audio-check/guitar-ref-analyze.py・guitar-ref-fit.py。
 */
import type { FxSpec } from "./fx-chain";
import type { Score, Track } from "./score";

export interface RefTone {
  id: string;
  label: string;
  description: string;
  source: string;
  /** 左右に分かれた歪みギターを左右いっぱい（±1）にする。 */
  guitarWide: boolean;
  guitar: FxSpec[];
  bass: FxSpec[];
  drums: FxSpec[];
  /** 歌の代わりの旋律（歌・リードなど、帯域の目安は参考の歌）。無いときは当てない。 */
  vocal?: FxSpec[];
  /** そのほかの楽器（シンセ・民族楽器・空気の層など）。無いときは当てない。 */
  other?: FxSpec[];
  /**
   * 楽器どうしの大きさの比を参考に合わせるために、パートの音量に掛ける量（dB。ギターが基準）。2026-10-23 人間「楽器同士の大きさの比も保存して」。
   * こちらの音（聞き比べ G＝ラウド25曲の土台）にこの EQ を当てたあとの大きさと、参考録音の楽器ごとの大きさ（音源分離）の差から計算した。
   */
  /** 2026-10-23 人間「個人的にベースを50ぐらい上げてほしい」→ bass は計算値に +3.5dB（1.5倍）→ 人間「全部に 1.5 は強いかな…1.2 にしよう」で +1.6dB（音量 1.2倍）にした値。 */
  balanceDb?: { bass: number; drums: number; vocal: number; other: number };
  /** リフ（role が「看板リフ」で始まる歪みギター）の音量に掛ける量（dB）。2026-10-23 人間「bmth のリフの音量 1.1倍にしよう」。書き出し（曲の JSON）でだけ効く。 */
  riffDb?: number;
  /** 参考録音そのものの楽器ごとの大きさ（ギターを 0dB とした dB。音源分離 demucs htdemucs_6s。曲の音量のつり合いの目安）。 */
  refLevelsDb?: { bass: number; drums: number; vocals: number; piano: number; other: number };
}

export const REF_TONES: Record<string, RefTone> = {
  "wide-dark-wall": {
    "id": "wide-dark-wall",
    "riffDb": 0.83,
    "label": "左右いっぱいの暗く太い壁（参考1）",
    "description": "低い中域（160〜250Hz）が太く、400〜800Hz を深くえぐり、4kHz から上を丸める。リフ・リズムは左右いっぱいの別テイク。",
    "source": "人間が渡した参考録音（Bring Me The Horizon）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": true,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 60.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 11.21,
        "midHz": 258.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 491.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 5.35,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.95,
        "midHz": 4353.8,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11989.0,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11989.0,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 31.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 8.94,
        "mid": -8.93,
        "midHz": 349.8,
        "high": 7.51
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.95,
        "midHz": 764.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 828.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 2251.2,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11718.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11718.3,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 6.7,
        "midHz": 200.0,
        "high": 8.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -0.66,
        "midHz": 900.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -4.22,
        "midHz": 916.1,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 2.74,
        "midHz": 2248.7,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11775.0,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11775.0,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 199.9,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -11.96,
        "mid": -11.99,
        "midHz": 294.9,
        "high": 11.96
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 566.1,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 4250.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11994.5,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11994.5,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 40.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 4.97,
        "mid": 3.48,
        "midHz": 293.4,
        "high": -5.27
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 614.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -10.29,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 6000.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -15.7,
      "drums": -2.2,
      "vocal": 12.2,
      "other": 12.6
    },
    "refLevelsDb": {
      "bass": -13.3,
      "drums": -3.1,
      "vocals": -2.6,
      "piano": -51.5,
      "other": -13.7
    }
  },
  "bright-pop-rock": {
    "id": "bright-pop-rock",
    "label": "明るいポップロック（参考2）",
    "description": "明るさの中心 2.2kHz。中域を少し削り、高域は残す。左右は普通の広さ。",
    "source": "人間が渡した参考録音（Mrs. GREEN APPLE）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": false,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 180.9,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 0.7,
        "mid": -3.28,
        "midHz": 350.0,
        "high": 5.21
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.95,
        "midHz": 569.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.72,
        "midHz": 2499.9,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 5258.8,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 12000.0,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 12000.0,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 6.3,
        "mid": 9.0,
        "midHz": 200.0,
        "high": 8.79
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 708.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 1249.6,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.95,
        "midHz": 5229.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11697.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11697.3,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 7.7,
        "midHz": 200.0,
        "high": 8.86
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 2.21,
        "midHz": 899.6,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.93,
        "midHz": 700.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.98,
        "midHz": 4154.8,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11732.8,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11732.8,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 159.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -7.21,
        "mid": 12.0,
        "midHz": 200.0,
        "high": 11.96
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 528.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 3993.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11487.6,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11487.6,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 140.1,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 11.96,
        "mid": -10.48,
        "midHz": 200.0,
        "high": 11.97
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -9.59,
        "midHz": 581.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2499.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 5802.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11460.1,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11460.1,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -16.4,
      "drums": -15.7,
      "vocal": -1.7,
      "other": -2.1
    },
    "refLevelsDb": {
      "bass": -2.2,
      "drums": -5.0,
      "vocals": 0.8,
      "piano": -52.3,
      "other": -16.4
    }
  },
  "deep-scoop-djent": {
    "id": "deep-scoop-djent",
    "label": "中域を深くえぐる低い刻み（参考3）",
    "description": "160Hz に集中し、400〜800Hz を大きく削る。3kHz から上は急に落とす。乾いて締まった刻み向き。",
    "source": "人間が渡した参考録音（Meshuggah）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": false,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 60.2,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 9.14,
        "mid": 10.87,
        "midHz": 223.3,
        "high": -2.11
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 493.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 4.43,
        "midHz": 2069.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 5412.3,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 30.1,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 8.93,
        "mid": -8.93,
        "midHz": 349.8,
        "high": 8.62
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.95,
        "midHz": 732.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 807.9,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 1855.4,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11731.4,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11731.4,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 1.99,
        "midHz": 200.3,
        "high": 8.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.78,
        "midHz": 350.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.17,
        "midHz": 700.2,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 8.95,
        "midHz": 2012.1,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11685.2,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11685.2,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 194.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -11.26,
        "mid": -11.99,
        "midHz": 349.6,
        "high": 11.96
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 510.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 4325.7,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11723.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11723.3,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 115.4,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 11.96,
        "mid": 11.68,
        "midHz": 200.0,
        "high": 11.24
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -6.64,
        "midHz": 381.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 4647.5,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11451.0,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11451.0,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -13.0,
      "drums": 0.1,
      "vocal": 13.3,
      "other": -5.7
    },
    "refLevelsDb": {
      "bass": -13.9,
      "drums": -5.5,
      "vocals": -4.3,
      "piano": -63.8,
      "other": -26.5
    }
  },
  "dark-electro-rock": {
    "id": "dark-electro-rock",
    "label": "暗い電子ロック（参考4）",
    "description": "一番暗い（明るさの中心 1kHz）。強弱の幅が大きい。電子音が主役でギターは後ろ。",
    "source": "人間が渡した参考録音（BOOM BOOM SATELLITES）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": false,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 60.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 3.53,
        "mid": -2.98,
        "midHz": 200.0,
        "high": -10.92
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -15.0,
        "midHz": 532.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -9.79,
        "midHz": 2017.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 5875.5,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11991.0,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11991.0,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 5.21,
        "mid": 7.81,
        "midHz": 200.0,
        "high": 3.91
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.24,
        "midHz": 522.8,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.62,
        "midHz": 822.8,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 1607.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11994.8,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11994.8,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 8.09,
        "midHz": 200.1,
        "high": 8.88
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.55,
        "midHz": 359.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -5.07,
        "midHz": 772.2,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": 3.45,
        "midHz": 2315.1,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 8930.1,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 8930.1,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 199.7,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -11.93,
        "mid": -5.69,
        "midHz": 344.5,
        "high": 11.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.95,
        "midHz": 487.2,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.95,
        "midHz": 2496.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.94,
        "midHz": 3927.0,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11677.4,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11677.4,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 40.1,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 11.96,
        "mid": 5.48,
        "midHz": 200.0,
        "high": -8.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.07,
        "midHz": 458.7,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -12.0,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 5403.7,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -7.0,
      "drums": -0.4,
      "vocal": 18.0,
      "other": 18.0
    },
    "refLevelsDb": {
      "bass": 7.6,
      "drums": 6.0,
      "vocals": 16.8,
      "piano": -5.5,
      "other": 13.8
    }
  },
  "bright-nu-wall": {
    "id": "bright-nu-wall",
    "label": "明るいニューメタルの壁（参考5）",
    "description": "明るさの中心 2.35kHz で、こちらの音に一番近い形。左右やや広め。",
    "source": "人間が渡した参考録音（Linkin Park）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": false,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 180.3,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 5.62,
        "mid": -4.64,
        "midHz": 200.0,
        "high": -7.35
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 565.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -7.93,
        "midHz": 1552.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.64,
        "midHz": 3969.4,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11990.8,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11990.8,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 8.94,
        "mid": -2.35,
        "midHz": 349.5,
        "high": 7.34
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.37,
        "midHz": 602.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 1572.3,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 5181.9,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.3,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 2.79,
        "midHz": 258.7,
        "high": 8.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -7.67,
        "midHz": 398.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -4.43,
        "midHz": 752.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -3.85,
        "midHz": 4695.1,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11996.6,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11996.6,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 167.8,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -6.9,
        "mid": -7.62,
        "midHz": 349.6,
        "high": 11.96
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.95,
        "midHz": 564.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.95,
        "midHz": 2494.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.94,
        "midHz": 3997.1,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11515.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11515.9,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 81.7,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 10.77,
        "mid": -7.18,
        "midHz": 204.6,
        "high": -8.3
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.03,
        "midHz": 509.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -12.0,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 4800.3,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11999.9,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -16.4,
      "drums": -12.5,
      "vocal": 4.7,
      "other": 9.0
    },
    "refLevelsDb": {
      "bass": -7.8,
      "drums": -4.8,
      "vocals": 2.2,
      "piano": -13.2,
      "other": -7.1
    }
  },
  "glossy-jrock": {
    "id": "glossy-jrock",
    "label": "つやのある J ロック（参考6）",
    "description": "明るさの中心 2.3kHz。500〜700Hz と 4.5kHz を削った、つやのある重ね。",
    "source": "人間が渡した参考録音（TRiDENT）を音源分離（demucs htdemucs_6s）して1/3オクターブごとに測り、聞き比べ G との差を埋める EQ を計算した数値（tools/audio-check/guitar-ref-fit.py。2026-10-23）。音そのものは取り込んでいない",
    "guitarWide": false,
    "guitar": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 199.9,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 6.63,
        "mid": -2.66,
        "midHz": 350.0,
        "high": -5.3
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -10.7,
        "midHz": 494.5,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -12.62,
        "midHz": 700.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -14.94,
        "midHz": 4512.9,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11998.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11998.3,
        "q": 0.7
      }
    ],
    "bass": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -2.22,
        "mid": -8.95,
        "midHz": 350.0,
        "high": 8.95
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 525.2,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -8.94,
        "midHz": 700.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -7.39,
        "midHz": 5999.9,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11755.7,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11755.7,
        "q": 0.7
      }
    ],
    "drums": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 45.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -8.94,
        "mid": 5.99,
        "midHz": 236.9,
        "high": 8.94
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -7.87,
        "midHz": 529.4,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -3.44,
        "midHz": 700.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -3.69,
        "midHz": 4646.3,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11689.2,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11689.2,
        "q": 0.7
      }
    ],
    "vocal": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 200.0,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": -11.96,
        "mid": -1.7,
        "midHz": 350.0,
        "high": 11.96
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 517.1,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.91,
        "midHz": 2500.0,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 4470.6,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11546.9,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11546.9,
        "q": 0.7
      }
    ],
    "other": [
      {
        "type": "filter",
        "kind": "highpass",
        "freq": 65.3,
        "q": 0.7
      },
      {
        "type": "eq",
        "low": 11.11,
        "mid": 7.57,
        "midHz": 200.1,
        "high": 6.03
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.93,
        "midHz": 570.8,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.96,
        "midHz": 2490.6,
        "high": 0
      },
      {
        "type": "eq",
        "low": 0,
        "mid": -11.94,
        "midHz": 4267.9,
        "high": 0
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11497.3,
        "q": 0.7
      },
      {
        "type": "filter",
        "kind": "lowpass",
        "freq": 11497.3,
        "q": 0.7
      }
    ],
    "balanceDb": {
      "bass": -12.2,
      "drums": -11.0,
      "vocal": 3.0,
      "other": -1.7
    },
    "refLevelsDb": {
      "bass": -7.0,
      "drums": -2.6,
      "vocals": 1.5,
      "piano": -34.6,
      "other": -12.0
    }
  }
} as unknown as Record<string, RefTone>;

export const REF_TONE_IDS = Object.keys(REF_TONES);

const GUITARS = new Set(["distGuitar", "crunch", "leadGuitar", "echoGuitar", "guitar"]);
const DRUMS = new Set(["kick", "snare", "hihat", "tom", "crash", "cymbal", "kickTrigger"]);
const BASSES = new Set(["bass", "slap", "sub808"]);
const VOCALS = new Set(["voice", "vocal", "choir", "lead"]);

/** EQ・フィルター以外の fx（ルーム・ディレイ・コンプなど）は残し、EQ とフィルターだけを参考の値に置きかえる。 */
function withEq(t: Track, eq: FxSpec[]): Track {
  const keep = (t.fx ?? []).filter((f) => f.type !== "eq" && f.type !== "filter");
  return { ...t, fx: [...eq.map((f) => ({ ...f })), ...keep] };
}

const dbGain = (db: number | undefined): number => Math.pow(10, (db ?? 0) / 20);
const scaled = <T extends { volume?: number }>(t: T, db: number | undefined): T => (db ? { ...t, volume: Math.round((t.volume ?? 0) * dbGain(db) * 10000) / 10000 } : t);

type Group = "guitar" | "bass" | "drums" | "vocal" | "other";
/** パートの役割を決める。歌の代わりのリード（role が「リード」で始まる歪みギター）は vocal。やまびこの付いたギター（空気の層）は other。 */
function groupOf(ins: string, fx: FxSpec[] | undefined, role?: string, patch?: string): Group {
  if (patch === "cymbalFx") return "drums";
  if (GUITARS.has(ins)) {
    if ((fx ?? []).some((f) => f.type === "delay" || f.type === "pingpong") || /空気の層/.test(role ?? "")) return "other";
    if (/^リード/.test(role ?? "")) return "vocal";
    return "guitar";
  }
  if (BASSES.has(ins)) return "bass";
  if (DRUMS.has(ins)) return "drums";
  if (VOCALS.has(ins)) return "vocal";
  return "other";
}

/**
 * 曲に参考の音を当てる（組み立てたあとの曲。作曲ソフトの「参考の音」）。元の曲は変えず、新しい曲を返す。
 * 組み立てたあとは役割（role）が分からないので、歪みギターのリードは「ギター」として扱う（書き出しの --ref-tone は役割まで見る applyRefToneToSong）。
 * 音量のつり合い（balanceDb）は、ベース・ドラム・歌の楽器・そのほかに掛ける。
 */
export function applyRefTone(score: Score, tone: RefTone): Score {
  // 選びなおしても音量が重ならないように、前に当てた参考の音の大きさの比をいったん戻してから当てる
  const prev = REF_TONES[(score as Score & { refTone?: string }).refTone ?? ""];
  const tracks = score.tracks.map((t0) => {
    const ins = t0.instrument ?? "";
    const g = groupOf(ins, t0.fx);
    const t = prev && g !== "guitar" ? scaled(t0, -(prev.balanceDb?.[g] ?? 0)) : t0;
    if (g === "guitar") {
      const n = withEq(t, tone.guitar);
      if (tone.guitarWide && ins !== "guitar" && t.pan !== undefined && Math.abs(t.pan) >= 0.3) n.pan = Math.sign(t.pan);
      return n;
    }
    const eq = { bass: tone.bass, drums: tone.drums, vocal: tone.vocal, other: tone.other }[g];
    return scaled(eq ? withEq(t, eq) : t, tone.balanceDb?.[g]);
  });
  return { ...score, tracks, refTone: tone.id } as Score;
}

/**
 * リードギター専用の音作り（6つの参考の音で共通。2026-10-23 の聞き比べで人間が選んだ③）。
 * 参考の音の「歌の EQ」は 2.5k・3.9k を深く削り 4.5k より上を持ち上げるため、リードギターでは抜ける帯域が消えてザラつきだけが残った
 * （人間「歪があるんだけど透き通るような伸びが欲しくて、余韻も感じたい」「歪が汚い」）。
 * アンプは PRS Archon のリード1（手元だけのモデル。無い環境ではマーシャル系で代わりに鳴る）を浅い歪み（0.45）で。
 * 濁り（350Hz）を少し削り、歌う帯域（1.6kHz）を出し、刺さる 4.2kHz だけを細く削って、11.5kHz までの空気感は残す。付点8分の薄いやまびこと残響の送りで余韻。
 */
export const LEAD_GUITAR = {
  amp: "namArchonL1",
  ampDrive: 0.38, // 2026-10-23 人間「歪がちょっと濁っている」→ 0.45 から浅く。低い中域（濁りの帯域）も少し多めに削る
  ampGate: 3,
  fx: [
    { type: "filter", kind: "highpass", freq: 150, q: 0.7 },
    { type: "eq", low: 0, mid: -3.5, midHz: 320, high: 0 },
    { type: "eq", low: 0, mid: 2.0, midHz: 1600, high: 0 },
    { type: "eq", low: 0, mid: -2.0, midHz: 4200, high: 0 },
    { type: "filter", kind: "lowpass", freq: 11500, q: 0.6 },
    { type: "delay", beats: 0.75, mix: 0.16, feedback: 0.3 },
  ] as FxSpec[],
};

/** AIソング形式のパート（JSON）。 */
interface SongPart { role?: string; instrument?: string; patch?: string; volume?: number; fx?: FxSpec[]; double?: unknown; [k: string]: unknown }

/**
 * 曲（AIソング形式の JSON）に参考の音を当てる（書き出しの --ref-tone。2026-10-23 の「再現2」と同じ処理）。役割まで見る:
 * 歪みギター（リフ・リズム・分散和音・速弾き）＝ギターの EQ、「リード」で始まる歪みギター＝歌の EQ と大きさ、空気の層・民族楽器・鍵盤など＝そのほかの EQ と大きさ、
 * ベース・ドラム＝それぞれの EQ と大きさ。guitarWide なら、リフ・リズムを左右いっぱいの別テイクにする。EQ とフィルター以外の fx（ルーム・やまびこなど）は残す。
 */
export function applyRefToneToSong<T extends { parts?: SongPart[] }>(song: T, tone: RefTone): T {
  if (!Array.isArray(song.parts)) return song;
  const eqOnly = (fx: FxSpec[] | undefined, eq: FxSpec[] | undefined): FxSpec[] | undefined =>
    eq ? [...eq.map((f) => ({ ...f })), ...(fx ?? []).filter((f) => f.type !== "eq" && f.type !== "filter")] : fx;
  const parts = song.parts.map((p) => {
    const ins = p.instrument ?? "";
    const g = groupOf(ins, p.fx, p.role, p.patch);
    // 歪みギターと歌の代わりのリードは、EQ のあとにルーム（小さな部屋の鳴り）だけを残す（再現2と同じ。プレートなどの残響は外す）
    const roomOnly = (eq: FxSpec[] | undefined): FxSpec[] | undefined => (eq ? [...eq.map((f) => ({ ...f })), ...(p.fx ?? []).filter((f) => f.type === "room")] : p.fx);
    if (g === "guitar") {
      const n: SongPart = scaled({ ...p, fx: roomOnly(tone.guitar) }, /^看板リフ/.test(p.role ?? "") ? tone.riffDb : undefined);
      if (tone.guitarWide && ins === "distGuitar" && /^(看板リフ|リズム)/.test(p.role ?? "")) {
        const base = typeof p.double === "object" && p.double ? (p.double as Record<string, unknown>) : {};
        n.double = { ...(/^リズム/.test(p.role ?? "") ? { irR: "jd-greenback-4x12-01" } : {}), ...base, spread: 1.0 };
      }
      return n;
    }
    if (p.patch === "cymbalFx" || p.patch === "guitarFx") return p;   // 本物のシンバル・ギターの効果音は変えない
    // リードギター（歌の代わり）は、歌の EQ ではなくリード専用の音作り（LEAD_GUITAR）。6つの参考の音で共通（2026-10-23 人間「これで音源6個を合わせて」）
    if (g === "vocal" && GUITARS.has(ins)) return scaled({ ...p, ...LEAD_GUITAR, fx: LEAD_GUITAR.fx.map((f) => ({ ...f })), sustain: Math.max(Number(p.sustain ?? 0), 2), mono: true, release: 0.35, reverb: Math.max(Number(p.reverb ?? 0), 0.25) }, tone.balanceDb?.vocal);
    if (g === "vocal") return scaled({ ...p, fx: roomOnly(tone.vocal) }, tone.balanceDb?.vocal);
    // ベースは、アンプのあとの圧縮などを先に、EQ をあとに（再現2と同じ順番）
    if (g === "bass") return scaled({ ...p, fx: [...(p.fx ?? []).filter((f) => f.type !== "eq" && f.type !== "filter"), ...tone.bass.map((f) => ({ ...f }))] }, tone.balanceDb?.bass);
    const eq = { bass: tone.bass, drums: tone.drums, other: tone.other }[g];
    return scaled({ ...p, fx: eqOnly(p.fx, eq) }, tone.balanceDb?.[g]);
  });
  return { ...song, parts };
}
