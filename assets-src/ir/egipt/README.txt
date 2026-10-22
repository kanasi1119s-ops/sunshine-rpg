4x12 キャビネット（スピーカー V30）の IR（2026-10-22 作成）

元: EG-IPT Dataset（Electric Guitar Instrumental Playing Techniques）
    M. Fiorini, N. Brochec, J. Borg, R. Pasini (2025). doi:10.5281/zenodo.15205644
    https://zenodo.org/records/15205644 ／ CC BY 4.0（クレジット必要。規約の本文は assets-src/soundfont/extra/src/licenses/CC-BY-4.0-legalcode.txt）
作り方: 同じ演奏の DI 録音と、アンプ（つまみはすべて中央）→ 4x12（V30）をマイクで録った音の組 32 個から、
        tools/soundfont/egipt-cab-ir.py で計算した（ウィーナーの推定 → 大きさをならす → 端の処理 → 最小位相 → 48kHz・100ms）。
        アンプの線形な音色（EQ）・箱・マイクを含む。録音そのものではなく、録音から計算した加工物。
ファイル: 412-v30-dyn（ダイナミックマイク）・412-v30-cond（コンデンサーマイク）・412-v30-rib（リボンマイク）・412-v30-mix（dyn と rib を半分ずつ）
確かめ: DI にこの IR を畳み込んだ音とマイク録音の大きさの差は、100Hz〜4kHz の 1/3 オクターブごとに ±1dB 前後（rib は ±2.3dB）。
        6.3kHz 以上はマイク側がほぼ雑音（DI とのコヒーレンス 0.1 以下）なので、IR は −24dB/オクターブで下げている。
クレジット: 「Cabinet IRs computed from EG-IPT Dataset by M. Fiorini, N. Brochec, J. Borg, R. Pasini (CC BY 4.0)。DI とマイク録音から計算した加工あり」
