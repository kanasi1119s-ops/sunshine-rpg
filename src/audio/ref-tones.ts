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
}

export const REF_TONES: Record<string, RefTone> = {
  "wide-dark-wall": {
    "id": "wide-dark-wall",
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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

/** 曲に参考の音を当てる（元の曲は変えず、新しい曲を返す）。何度当てても同じ結果。 */
export function applyRefTone(score: Score, tone: RefTone): Score {
  const tracks = score.tracks.map((t) => {
    const ins = t.instrument ?? "";
    if (GUITARS.has(ins)) {
      const isAmbient = (t.fx ?? []).some((f) => f.type === "delay" || f.type === "pingpong");   // 空気の層（やまびこ付き）は「そのほか」
      if (isAmbient) return tone.other ? withEq(t, tone.other) : t;
      const n = withEq(t, tone.guitar);
      if (tone.guitarWide && ins !== "guitar" && t.pan !== undefined && Math.abs(t.pan) >= 0.3) n.pan = Math.sign(t.pan);
      return n;
    }
    if (BASSES.has(ins)) return withEq(t, tone.bass);
    if (DRUMS.has(ins)) return withEq(t, tone.drums);
    if (VOCALS.has(ins)) return tone.vocal ? withEq(t, tone.vocal) : t;
    return tone.other ? withEq(t, tone.other) : t;
  });
  return { ...score, tracks };
}
