#!/usr/bin/env python3
"""4 段階目: 曲を聴いて「何が鳴っているか」を言い当てる（2026-11-17 人間「曲を聴いて学習して、使ってる楽器、コード、音の種類、ジャンルなどあらゆるものがわかる用にしましょう」）。
やり方: AudioSet（YouTube の音 200 万本に 527 種類の名前をつけたデータ）で学んだ聞き分けモデル AST（MIT・BSD-3 ライセンス。Hugging Face から取る）に、
        曲を 10 秒ずつ聞かせて、527 種類それぞれの「鳴っていそうな度合い（0〜1）」を出す。
        曲全体（ジャンル・ふんいき）と、Demucs で分けた音（歌・ドラム・ベース・ギター・ピアノ・そのほか）のそれぞれに聞かせて、分けた音の中身（シンセか弦か、歪んだギターか生ギターか、など）を出す。
使い方: python3 tools/song-analyzer/stage4.py <曲のファイル> [出力 JSON]   … 1 曲だけ調べる（分ける所から）
        analyze.py からは run(stems, sr) を呼ぶ
数字の読み方: このモデルの度合いは全体に小さく出る（お手本のロックの曲でも「ロック 0.17」くらい）。大きさそのものより、順番と、ほかの曲とのくらべで読む。
気をつけること: このモデルは「名前を当てる」だけで、音符や音色の数字は出さない（それは 2・3 段階目）。当たり具合は eval4.py（自分の曲＝正解がわかっている曲）で確かめる。"""
import sys, os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
MODEL = "MIT/ast-finetuned-audioset-10-10-0.4593"
_M = {}

# AudioSet の名前 → 日本語（使うものだけ）。グループごとに並べる
GENRE = {"Pop music": "ポップ", "Rock music": "ロック", "Heavy metal": "ヘビーメタル", "Punk rock": "パンク", "Grunge": "グランジ", "Progressive rock": "プログレ", "Rock and roll": "ロックンロール", "Psychedelic rock": "サイケ",
         "Hip hop music": "ヒップホップ", "Rhythm and blues": "R&B", "Soul music": "ソウル", "Funk": "ファンク", "Disco": "ディスコ", "Reggae": "レゲエ", "Ska": "スカ", "Country": "カントリー", "Folk music": "フォーク", "Blues": "ブルース", "Jazz": "ジャズ", "Swing music": "スウィング", "Bluegrass": "ブルーグラス",
         "Classical music": "クラシック", "Opera": "オペラ", "Electronic music": "電子音楽", "House music": "ハウス", "Techno": "テクノ", "Dubstep": "ダブステップ", "Drum and bass": "ドラムンベース", "Electronica": "エレクトロニカ", "Electronic dance music": "EDM", "Ambient music": "アンビエント", "Trance music": "トランス",
         "Music of Latin America": "ラテン", "Salsa music": "サルサ", "Flamenco": "フラメンコ", "Music of Asia": "アジアの音楽", "Music of Bollywood": "ボリウッド", "Carnatic music": "インド古典", "Music of Africa": "アフリカの音楽", "Afrobeat": "アフロビート", "Christian music": "クリスチャン", "Gospel music": "ゴスペル",
         "New-age music": "ニューエイジ", "Vocal music": "声の音楽", "A capella": "アカペラ", "Independent music": "インディー", "Traditional music": "伝統音楽", "Middle Eastern music": "中東の音楽", "Video game music": "ゲーム音楽", "Soundtrack music": "サントラ", "Theme music": "テーマ曲", "Jingle (music)": "ジングル", "Dance music": "ダンス音楽", "Lullaby": "子守歌", "Christmas music": "クリスマス", "Wedding music": "結婚式の音楽"}
MOOD = {"Happy music": "明るい", "Funny music": "おどけた", "Sad music": "悲しい", "Tender music": "やさしい", "Exciting music": "わくわく", "Angry music": "怒った", "Scary music": "こわい"}
INST = {"Guitar": "ギター", "Electric guitar": "エレキギター", "Bass guitar": "ベースギター", "Acoustic guitar": "アコースティックギター", "Steel guitar, slide guitar": "スライドギター", "Tapping (guitar technique)": "タッピング（ギター）", "Strum": "かき鳴らし", "Distortion": "歪み", "Banjo": "バンジョー", "Sitar": "シタール", "Mandolin": "マンドリン", "Zither": "ツィター", "Ukulele": "ウクレレ",
        "Keyboard (musical)": "鍵盤", "Piano": "ピアノ", "Electric piano": "エレピ", "Organ": "オルガン", "Electronic organ": "電子オルガン", "Hammond organ": "ハモンドオルガン", "Synthesizer": "シンセサイザー", "Sampler": "サンプラー", "Harpsichord": "チェンバロ",
        "Percussion": "打楽器", "Drum kit": "ドラムセット", "Drum machine": "ドラムマシン", "Drum": "太鼓", "Snare drum": "スネア", "Rimshot": "リムショット", "Drum roll": "ドラムロール", "Bass drum": "バスドラム", "Timpani": "ティンパニ", "Tabla": "タブラ", "Cymbal": "シンバル", "Hi-hat": "ハイハット", "Wood block": "ウッドブロック", "Tambourine": "タンバリン", "Rattle (instrument)": "ガラガラ", "Maraca": "マラカス", "Gong": "ゴング", "Tubular bells": "チューブラーベル", "Mallet percussion": "鍵盤打楽器", "Marimba, xylophone": "マリンバ・木琴", "Glockenspiel": "グロッケン", "Vibraphone": "ビブラフォン", "Steelpan": "スチールパン", "Clapping": "手拍子", "Cowbell": "カウベル",
        "Orchestra": "オーケストラ", "Brass instrument": "金管", "French horn": "ホルン", "Trumpet": "トランペット", "Trombone": "トロンボーン", "Bowed string instrument": "弓の弦楽器", "String section": "ストリングス", "Violin, fiddle": "バイオリン", "Pizzicato": "ピチカート", "Cello": "チェロ", "Double bass": "コントラバス",
        "Wind instrument, woodwind instrument": "木管", "Flute": "フルート", "Saxophone": "サックス", "Clarinet": "クラリネット", "Harp": "ハープ", "Bell": "ベル", "Church bell": "教会の鐘", "Jingle bell": "鈴", "Chime": "チャイム", "Wind chime": "ウィンドチャイム", "Harmonica": "ハーモニカ", "Accordion": "アコーディオン", "Bagpipes": "バグパイプ", "Didgeridoo": "ディジュリドゥ", "Shofar": "角笛", "Theremin": "テルミン", "Singing bowl": "シンギングボウル", "Scratching (performance technique)": "スクラッチ", "Music box": "オルゴール", "Whistle": "ホイッスル", "Whistling": "口笛"}
VOICE = {"Singing": "歌", "Female singing": "女の人の歌", "Male singing": "男の人の歌", "Child singing": "子どもの歌", "Choir": "合唱", "Chant": "となえ声", "Rapping": "ラップ", "Humming": "ハミング", "Yodeling": "ヨーデル", "Synthetic singing": "歌声合成", "Vocal music": "声の音楽", "A capella": "アカペラ", "Speech": "話し声", "Shout": "さけび", "Screaming": "絶叫", "Whispering": "ささやき", "Beatboxing": "ボイパ", "Background music": "うしろの音楽"}
SOUND = {"Distortion": "歪み", "Reverberation": "響き", "Echo": "やまびこ", "Effects unit": "エフェクター", "Chorus effect": "コーラス", "Noise": "ノイズ", "Static": "ザーッという音", "White noise": "ホワイトノイズ", "Pink noise": "ピンクノイズ", "Hum": "うなり", "Sine wave": "サイン波", "Chirp tone": "チャープ", "Sound effect": "効果音", "Pulse": "パルス", "Buzz": "ブザー", "Beep, bleep": "ピッという音", "Ding": "チーン", "Ping": "ピン", "Clang": "カーン", "Whoosh, swoosh, swish": "ヒュッという音", "Boom": "ドーン", "Thump, thud": "ドスン", "Sidetone": "側音", "Cacophony": "ごちゃごちゃ", "Environmental noise": "環境音", "Silence": "無音", "Zing": "キーン", "Boing": "ビヨーン", "Crunch": "ザクッ", "Bass (frequency range)": "低音"}
GROUPS = {"ジャンル": GENRE, "ふんいき": MOOD, "楽器": INST, "声": VOICE, "音の種類": SOUND}

def _model():
    if "m" not in _M:
        import torch
        from transformers import ASTFeatureExtractor, ASTForAudioClassification
        os.environ.setdefault("HF_HOME", "/tmp/hf"); torch.set_num_threads(max(1, (os.cpu_count() or 2)))
        _M["fe"] = ASTFeatureExtractor.from_pretrained(MODEL); _M["m"] = ASTForAudioClassification.from_pretrained(MODEL).eval(); _M["lab"] = [_M["m"].config.id2label[i] for i in range(len(_M["m"].config.id2label))]
    return _M["fe"], _M["m"], _M["lab"]

def listen(mono, sr, win=10.0, hop=10.0):
    """mono（1 本の音）を win 秒ずつ聞かせる。返すもの: (時刻の並び, 度合い[窓の数 × 527], 名前の並び, その窓の大きさ dB)"""
    import torch, librosa
    fe, m, lab = _model()
    if sr != 16000: mono = librosa.resample(np.asarray(mono, dtype=np.float32), orig_sr=sr, target_sr=16000)
    n = len(mono); W, H = int(win * 16000), int(hop * 16000); ts, P, L = [], [], []
    peak = float(np.abs(mono).max()) + 1e-9
    for a in range(0, max(1, n - W // 2), H):
        seg = mono[a:a + W]
        if len(seg) < 16000: break
        lv = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9); L.append(lv); ts.append(a / 16000)
        x = fe(seg / peak * 0.5, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad(): P.append(torch.sigmoid(m(**x).logits)[0].numpy())
    return np.array(ts), np.array(P), lab, np.array(L)

def top(P, lab, table, k=6, floor=0.02, w=None):
    """table（英語の名前 → 日本語）の中で、度合いの高い順に k 個。w: 窓ごとの重み（鳴っている窓だけ数える）"""
    if len(P) == 0: return []
    w = np.ones(len(P)) if w is None else np.asarray(w, float)
    if w.sum() <= 0: return []
    mean = (P * w[:, None]).sum(0) / w.sum(); out = []
    for en, ja in table.items():
        if en in lab:
            v = float(mean[lab.index(en)])
            if v >= floor: out.append((ja, round(v, 3)))
    return sorted(out, key=lambda z: -z[1])[:k]

STEM_TABLE = {"vocals": ("歌", VOICE), "drums": ("ドラム", {k: v for k, v in INST.items() if k in ("Drum kit", "Drum machine", "Snare drum", "Bass drum", "Cymbal", "Hi-hat", "Tambourine", "Clapping", "Cowbell", "Rimshot", "Drum roll", "Percussion", "Wood block", "Maraca", "Timpani", "Tabla")}),
              "bass": ("ベース", {"Bass guitar": "ベースギター", "Double bass": "コントラバス", "Synthesizer": "シンセサイザー", "Bass (frequency range)": "低音", "Distortion": "歪み", "Electronic music": "電子音", "Guitar": "ギター"}),
              "guitar": ("ギター", {k: v for k, v in INST.items() if k in ("Guitar", "Electric guitar", "Acoustic guitar", "Steel guitar, slide guitar", "Tapping (guitar technique)", "Strum", "Distortion", "Banjo", "Mandolin", "Ukulele", "Synthesizer", "Piano", "Electric piano", "Harp", "Sitar")}),
              "piano": ("ピアノ", {k: v for k, v in INST.items() if k in ("Piano", "Electric piano", "Keyboard (musical)", "Organ", "Hammond organ", "Electronic organ", "Synthesizer", "Harpsichord", "Marimba, xylophone", "Glockenspiel", "Vibraphone", "Music box", "Harp", "Guitar")}),
              "other": ("そのほか", {k: v for k, v in INST.items() if k not in ("Drum kit", "Drum machine", "Snare drum", "Bass drum", "Cymbal", "Hi-hat", "Drum", "Percussion")})}

def run(stems, sr, bar_t=None, only=None):
    """stems: {"vocals"・"drums"・"bass"・"guitar"・"piano"・"other": 音（[2, n] か [n]）}。返すもの: 日本語のまとめ（辞書）"""
    mono = {k: (np.asarray(v).mean(0) if np.asarray(v).ndim > 1 else np.asarray(v)) for k, v in stems.items()}
    mix = sum(mono.values()); out = {"モデル": MODEL}
    ts, P, lab, L = listen(mix, sr)
    for g, tb in GROUPS.items(): out[g] = top(P, lab, tb, k=8 if g in ("楽器", "ジャンル") else 5)
    # 時間ごとの上位（30 秒ごと）: どこで何が鳴っているか
    tl = []
    for a in np.arange(0, ts[-1] + 5 if len(ts) else 0, 30.0):
        w = ((ts >= a - 5) & (ts < a + 25)).astype(float)
        if w.sum(): tl.append({"秒": float(a), "ジャンル": top(P, lab, GENRE, 3, w=w), "楽器": top(P, lab, INST, 5, w=w), "声": top(P, lab, VOICE, 2, 0.03, w=w)})
    out["時間ごと"] = tl
    ref = 20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-9); parts = {}
    for k, (ja, tb) in STEM_TABLE.items():
        if k not in mono or (only and k not in only): continue
        ts2, P2, _, L2 = listen(mono[k], sr); w = (L2 > ref - 30).astype(float)       # その音が鳴っている窓だけ
        parts[ja] = {"鳴っている時間の割合": round(float(w.mean()) if len(w) else 0.0, 2), "中身": top(P2, lab, tb, 6, 0.03, w=w) if w.sum() else []}
    out["分けた音の中身"] = parts
    return out

def show(o):
    f = lambda v: "・".join(f"{a} {b:.2f}" for a, b in v) if v else "—"
    for g in GROUPS: print(f"  {g}: {f(o[g])}")
    for ja, d in o["分けた音の中身"].items(): print(f"  分けた音「{ja}」（鳴っている時間 {int(d['鳴っている時間の割合']*100)}%）: {f(d['中身'])}")
    for r in o["時間ごと"]: print(f"    {int(r['秒']//60)}:{int(r['秒']%60):02d}〜 ジャンル {f(r['ジャンル'])} ／ 楽器 {f(r['楽器'])} ／ 声 {f(r['声'])}")

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import analyze as A, gc
    st = A.separate(A.load_audio(sys.argv[1])); st = {k: np.asarray(v, dtype=np.float32).mean(0) if np.asarray(v).ndim > 1 else np.asarray(v, dtype=np.float32) for k, v in st.items()}; gc.collect()
    o = run(st, A.SR); print("■", os.path.basename(sys.argv[1])); show(o)
    if len(sys.argv) > 2: json.dump(o, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
