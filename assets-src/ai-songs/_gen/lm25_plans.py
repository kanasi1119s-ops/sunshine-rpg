# ラウド26曲の「展開の型」（2026-10-23 人間「展開が全曲同じ」「始まり終わりまでの流れってそれぞれ違う」「サビから始まる曲だっていい」
# 「前奏から」「同じギターリフで旋律だけ変わる」「ドラムから・ベースから始まってもいい」「最後イントロがゆっくりフェードアウトしてもいい」
# 「オリジナル性を」「ドラムはいろんなテクニック・プログレの部分も」「1曲4分から5分」）
# 曲ごとに、始まり方・流れ・ドラムの感じ・終わり方を変える。並べかえの仕組みは lm25_lib.rearrange。
# drums の既定は "lib"（学んだドラムのフレーズ集から区間ごとに選ぶ）。half / double / ride / sparse / toms もフレーズ集から、
# tribal（タムの太鼓）・kick4（4つ打ち）・build（スネアがだんだん細かく）・heart（心臓の音）・solo（ドラムソロ）・none・own（曲のもとの手書き）は手で作る型。

def alt(src_a, src_b, n, step, opt_a, opt_b, name_a="a", name_b="b", start=0):
    """かけ合い: src_a と src_b を step 小節ずつ交互に（同じ小節の位置を進めながら）"""
    out, i = [], start
    while i < start + n:
        j = min(i + step, start + n)
        out.append((name_a, (src_a, i, j), dict(opt_a)))
        if j >= start + n: break
        k = min(j + step, start + n)
        out.append((name_b, (src_b, j, k), dict(opt_b)))
        i = k
    return out


PLANS = {}
DESC = {}
FADE = {}

# 01 路地裏の灯（96）: ロンド「路地の角を曲がるたびに、同じ看板（サビ）に出会う」。ベースだけで始まり、サックスだけ残ってフェードアウト
DESC["01"] = "展開: ロンド（看板＝サビに4回戻り、毎回ようすが違う: 眩しい・サックスと重なる・傷ついて欠ける・サックスと同じ旋律）。雨のクリーンとベースで始まり、夜明けにサックスだけ残ってフェードアウト。"
PLANS["01"] = [   # 2026-10-24 素材から作り直し。FORM の順のまま、場面ごとのドラムと強さ（lv）だけを決める
    ("rain", "rain", {"drums": "own", "lv": 0, "kind": "intro"}),
    ("neon", "neon", {"drums": "lib", "lv": 2, "kind": "chorus"}),
    ("alley", "alley", {"drums": "half", "lv": 1, "kind": "verse", "fills": None}),
    ("neon2", "neon2", {"drums": "lib", "lv": 2, "kind": "chorus", "from": "stopBeat"}),
    ("fight", ("fight", 0, 6), {"drums": "double", "lv": 3, "kind": "break"}),
    ("fight2", ("fight", 6, 12), {"drums": "half", "lv": 3, "kind": "break", "stop": True}),
    ("neon3", "neon3", {"drums": "sparse", "lv": 1, "kind": "chorus"}),
    ("backdoor", ("backdoor", 0, 8), {"drums": "own", "lv": 1, "kind": "solo"}),
    ("backdoor2", ("backdoor", 8, 16), {"drums": "shuffle", "lv": 2, "kind": "solo"}),
    ("neon4", ("neon4", 0, 8), {"drums": "lib", "lv": 2, "kind": "chorus", "from": "break1bar"}),
    ("tag", ("neon4", 8, 12), {"drums": "double", "lv": 3, "kind": "chorus"}),
    ("dawn", "dawn", {"drums": "own", "lv": 0, "kind": "outro"}),
]
FADE["01"] = (0, 14)

# 02 白い螺旋（128・7拍子）: 転調の階段（螺旋を上る）。ドラムだけで始まり、半音ずつ4回上がる。終わりはドラムとシタールでフェードアウト
DESC["02"] = "展開: 螺旋（サビという区切りなし。同じ16小節が半音ずつ上がって4周。3周目のはじめで全部消え、4周目で全開、最後はタッピングが螺旋を描く）。シタールだけで始まり、ドラムとシタールでフェードアウト。"
PLANS["02"] = [   # 2026-10-24 素材から作り直し: 同じ16小節を半音ずつ上げて4周する螺旋
    ("intro", "intro", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("lap1", "lap1", {"drums": "sparse", "lv": 1, "kind": "verse"}),
    ("lap2", "lap2", {"drums": "lib", "lv": 2, "kind": "chorus", "semi": 1, "from": "stopBeat"}),
    ("void", ("lap3", 0, 4), {"drums": "heart", "lv": 0, "kind": "bridge", "semi": 2}),
    ("return", ("lap3", 4, 12), {"drums": "sparse", "lv": 1, "kind": "bridge", "semi": 2}),
    ("return2", ("lap3", 12, 16), {"drums": "build", "lv": 2, "kind": "pre", "semi": 2}),
    ("lap4", ("lap4", 0, 12), {"drums": "double", "lv": 3, "kind": "chorus", "semi": 3, "from": "break1bar"}),
    ("spiral", ("lap4", 12, 16), {"drums": "half", "lv": 3, "kind": "chorus", "semi": 3}),
    ("outro", "outro", {"drums": "lib", "lv": 1, "kind": "outro"}),
]
FADE["02"] = (0, 12)

# 03 嵐の背骨（138）: 積み上げと「嵐の目」。チェロ1本から始まり、少しずつ楽器が増えて嵐になり、途中で全部が止んで目に入り、雷のドラムソロ、最後はいきなり切れる
DESC["03"] = "展開: 台風の通過（外側の暴風の壁＝速いスラッシュ → 目＝72 に落ちて完全な静けさ → 背後の壁＝100 のドゥームで前半より重い。サビは背後の壁の頂点に1回だけ）。チェロのトレモロで近づき、拍の頭で突然切れて終わる。"
PLANS["03"] = [   # 2026-10-24 素材から作り直し: 台風の通過（外側の壁・目・背後の壁）
    ("approach", "approach", {"drums": "own", "lv": [0, 0, 0, 0, 1, 1, 1, 1], "kind": "intro"}),
    ("wall1", ("wall1", 0, 8), {"drums": "double", "lv": 2, "kind": "chorus"}),
    ("wall1b", ("wall1", 8, 24), {"drums": "double", "lv": 3, "kind": "chorus"}),
    ("wall1c", ("wall1", 24, 32), {"drums": "lib", "lv": 3, "kind": "chorus", "stop": True}),
    ("eye", "eye", {"drums": "own", "lv": 0, "kind": "bridge", "bpm": 72}),
    ("wall2", ("wall2", 0, 16), {"drums": "half", "lv": 3, "kind": "break", "bpm": 100, "from": "break1bar"}),
    ("peak", ("wall2", 16, 32), {"drums": "lib", "lv": 3, "kind": "chorus"}),
    ("tail", ("wall2", 32, 40), {"drums": "half", "lv": 3, "kind": "break"}),
]

# 04 沈黙の掟（88）: 沈黙（全休止）が主役。ピアノ1人で始まり、重い音の間に「何も鳴らない小節」が入る。最後もピアノだけで、ぷつりと終わる
DESC["04"] = "展開: 一筆書き（葬儀・密談・裏切り・処刑・沈黙。同じ区間を2度使わない。5小節の句）。ピアノだけで始まり、処刑のあと全員が黙り、ピアノの単音でぷつりと終わる。"
PLANS["04"] = [   # 2026-10-24 素材から作り直し: 葬儀・密談・裏切り・処刑・沈黙の一筆書き（5小節の句）
    ("funeral", "funeral", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("meeting", "meeting", {"drums": "sparse", "lv": 1, "kind": "verse", "crash": False}),
    ("betrayal", "betrayal", {"drums": "half", "lv": 2, "kind": "chorus", "from": "stopBeat"}),
    ("execution", ("execution", 0, 6), {"drums": "double", "lv": 3, "kind": "break"}),
    ("execution2", ("execution", 6, 13), {"drums": "half", "lv": 3, "kind": "break"}),
    ("hush", ("execution", 13, 15), {"drums": "none", "lv": 0, "kind": "break"}),
    ("silence", "silence", {"drums": "none", "lv": 0, "kind": "outro"}),
]

# 05 七つの角（112・5拍子）: ブレイクダウンが主役。2回目のブレイクダウンはテンポが落ちていき、決めで止まってから元の速さで戻る
DESC["05"] = "展開: 呪文（三味線の呼びかけ4小節とバンドの答え8小節を7回。答えるたびに旋律の音が1つ増え、5回目は全部消える罠、7回目で七本の角がそろう）。三味線の一打で始まり、全員の一撃と三味線の一打で終わる。"
PLANS["05"] = [   # 2026-10-24 素材から作り直し: 呪文（三味線の呼びかけ＋バンドの答え）×7。5回目は罠
    ("summon", "summon", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("call1", "call1", {"drums": "none", "lv": 0, "kind": "interlude", "crash": False}),
    ("answer1", "answer1", {"drums": "half", "lv": 1, "kind": "chorus"}),
    ("call2", "call2", {"drums": "tribal", "lv": 1, "kind": "interlude", "crash": False}),
    ("answer2", "answer2", {"drums": "lib", "lv": 1, "kind": "chorus"}),
    ("call3", "call3", {"drums": "tribal", "lv": 1, "kind": "interlude", "crash": False}),
    ("answer3", "answer3", {"drums": "lib", "lv": 2, "kind": "chorus"}),
    ("call4", "call4", {"drums": "tribal", "lv": 2, "kind": "interlude", "crash": False}),
    ("answer4", "answer4", {"drums": "double", "lv": [2, 2, 2, 2, 3, 3, 3, 3], "kind": "chorus"}),
    ("call5", "call5", {"drums": "heart", "lv": 0, "kind": "interlude", "crash": False}),
    ("answer5", "answer5", {"drums": "heart", "lv": 0, "kind": "bridge"}),
    ("call6", "call6", {"drums": "tribal", "lv": 2, "kind": "interlude", "crash": False}),
    ("answer6", "answer6", {"drums": "double", "lv": 3, "kind": "chorus", "from": "stopBeat"}),
    ("call7", "call7", {"drums": "tribal", "lv": 2, "kind": "interlude", "crash": False}),
    ("answer7", "answer7", {"drums": "double", "lv": 3, "kind": "chorus"}),
    ("crown", "crown", {"drums": "double", "lv": 3, "kind": "outro", "stop": True}),
]

# 06 鐘と偶像（84・6拍子）: 二部構成。前半はドラムなしの賛美歌（72）、鐘の一打で区切り、後半は偶像が崩れる重い曲（96）。最後はオルガンだけが遅くなって消える
DESC["06"] = "展開: 聖歌の行進（遅く重い）→ 説教 → 二度目の行進 → ひび → 崩落（144 の倍の速さ・ブラスト）→ 瓦礫。オルガンの和音で始まり、オルガンの1音で終わる。"
PLANS["06"] = [   # 2026-10-24 素材から作り直し: 聖歌の行進 → 崩落（倍の速さ）→ 瓦礫
    ("bells", "bells", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("procession", "procession", {"drums": "tribal", "lv": 2, "kind": "chorus"}),
    ("sermon", "sermon", {"drums": "sparse", "lv": 1, "kind": "verse"}),
    ("procession2", "procession2", {"drums": "half", "lv": 2, "kind": "chorus", "from": "stopBeat"}),
    ("crack", "crack", {"drums": "build", "lv": [2, 2, 3, 3], "kind": "pre"}),
    ("collapse", "collapse", {"drums": "double", "lv": 3, "kind": "break", "bpm": 144, "from": "break1bar"}),
    ("rubble", "rubble", {"drums": "none", "lv": 0, "kind": "outro", "bpm": 72}),
]
FADE["06"] = (0, 8)

# 07 羽の落ちる速さ（120）: 逆さ構成。いきなり最後のサビから始まり、だんだん楽器が減り、テンポも落ちて、ハープだけが舞い落ちて終わる
DESC["07"] = "展開: 一本の長い落下（成層圏・雲・風・急降下・地面の直前と、速さは 100 のまま、ドラムの感じがハーフ→ふつう→倍と詰まり、音域は低く、厚みは重く）。ハープだけで始まり、着地の1小節の無音のあと、ハープだけで終わる。"
PLANS["07"] = [   # 2026-10-24 素材から作り直し: 一本の長い落下（速く・低く・重くなる）
    ("strato", "strato", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("cloud", "cloud", {"drums": "sparse", "lv": 1, "kind": "verse"}),
    ("wind", "wind", {"drums": "half", "lv": 2, "kind": "pre"}),
    ("dive", "dive", {"drums": "lib", "lv": 3, "kind": "chorus"}),
    ("ground", "ground", {"drums": "double", "lv": 3, "kind": "solo"}),
    ("impact", "impact", {"drums": "none", "lv": 0, "kind": "interlude"}),
    ("feather", "feather", {"drums": "none", "lv": 0, "kind": "outro"}),
]
FADE["07"] = (0, 6)

# 08 鼓動の前（100・7拍子）: 加速する鼓動。心臓の音だけで始まり、区間ごとにテンポが 80→88→96→104→112→120 と上がり、一瞬止まって（心停止）、ゆっくりの心臓で終わる
DESC["08"] = "展開: 速さが物語（鼓動 80 → 早まる 96 → 走る 120 → 動悸 144 → 限界 160 → 停止（心電図の平らな音）→ 蘇生 60）。心音とバイオリンの「ドクン」で始まり、蘇生がいちばん大きな歌になり、全員の「ドクン」の一打で切れて終わる。"
PLANS["08"] = [   # 2026-10-24 素材から作り直し: 速さそのものが物語（80→160→停止→60）
    ("pulse", "pulse", {"drums": "own", "lv": [0, 0, 0, 1, 1, 1], "kind": "intro"}),
    ("quicken", "quicken", {"drums": "sparse", "lv": 1, "kind": "verse", "bpm": 96}),
    ("race", "race", {"drums": "lib", "lv": 2, "kind": "pre", "bpm": 120}),
    ("panic", "panic", {"drums": "double", "lv": 3, "kind": "chorus", "bpm": 144}),
    ("peak", "peak", {"drums": "double", "lv": 3, "kind": "break", "bpm": 160, "stop": True}),
    ("flat", "flat", {"drums": "none", "lv": 0, "kind": "interlude"}),
    ("revive", "revive", {"drums": "half", "lv": [1, 1, 2, 2, 2, 2, 3, 3, 3, 3], "kind": "chorus", "bpm": 60}),
    ("beat", "beat", {"drums": "own", "lv": 3, "kind": "break"}),
]
FADE["08"] = (0, 5)

# 09 罰の階段（92）: 下る転調。チェンバロ1人で始まり、区間ごとに半音ずつ下がって（地下へ降りる階段）、一番下で決めの一撃
DESC["09"] = "展開: 9段の階段（パッサカリア。低音が C から E まで半音ずつ下り続け、段ごとに主題を変奏。重さが段ごとに増し、8段目がいちばん遅く重く、9段目で主題が逆さに上る）。チェンバロの主題で始まり、判決の槌の一撃とチェンバロの1音で終わる。"
PLANS["09"] = [   # 2026-10-24 素材から作り直し: 9段の階段（低音が半音ずつ下り続けるパッサカリア）
    ("door", "door", {"drums": "none", "lv": 0, "kind": "intro"}),
    ("step1", "step1", {"drums": "none", "lv": 0}),
    ("step2", "step2", {"drums": "none", "lv": 1}),
    ("step3", "step3", {"drums": "sparse", "lv": 1}),
    ("step4", "step4", {"drums": "half", "lv": 2}),
    ("step5", "step5", {"drums": "lib", "lv": 2}),
    ("step6", "step6", {"drums": "lib", "lv": [2, 2, 2, 2, 2, 3, 3, 3, 3, 3]}),
    ("step7", "step7", {"drums": "double", "lv": 3}),
    ("step8", "step8", {"drums": "half", "lv": 3}),
    ("step9", "step9", {"drums": "lib", "lv": 3}),
    ("verdict", "verdict", {"drums": "own", "lv": 3, "kind": "outro"}),
]

# 10 成層圏の手紙（132）: 一本道（同じ区間をそのままくり返さない）。サビの旋律を途中で馬頭琴が引き継ぎ、全音上がって成層圏へ、最後は馬頭琴だけが飛んでいく
DESC["10"] = "展開: 手紙を読む（いま）と回想（あの日）を3回くり返し、三通目でたどり着いた一言を、最後に一度だけのサビでぶちまける。クリーンのギターと話すようなリードで始まり、追伸の馬頭琴だけで終わる。"
PLANS["10"] = [   # 2026-10-24 素材から作り直し: 手紙を読む／回想の交互、サビは最後に一度だけ
    ("read1", "read1", {"drums": "sparse", "lv": 1, "kind": "verse"}),
    ("mem1", "mem1", {"drums": "ride", "lv": [1] * 6 + [2] * 8, "kind": "bridge"}),
    ("read2", "read2", {"drums": "sparse", "lv": 1, "kind": "verse"}),
    ("mem2", "mem2", {"drums": "half", "lv": 2, "kind": "bridge"}),
    ("read3", "read3", {"drums": "none", "lv": 0, "kind": "verse"}),
    ("mem3", "mem3", {"drums": "lib", "lv": [2] * 8 + [3] * 8, "kind": "pre"}),
    ("chorus", "chorus", {"drums": "lib", "lv": 3, "kind": "chorus", "from": "break1bar"}),
    ("ps", "ps", {"drums": "none", "lv": 0, "kind": "outro"}),
]
FADE["10"] = (0, 10)

# 11 深海の時計（86・6拍子）: 沈んでいく（テンポが 86→80→72→66→60→56 と下がる）。琴1人で始まり、深い所では時計の針（ライド）だけが刻み、琴だけが残って消える
DESC["11"] = "展開: 沈降（海面・100m・300m・700m・1000m。深くなるほど 86→48 へ遅く、低く、音数が少なく、小さくなる）。海面の明るい揺れで始まり、圧壊の一撃と琴の最後の一音で終わる。"
PLANS["11"] = [   # 2026-10-24 素材から作り直し: 沈降（深くなるほど遅く・低く・まばらに）。最後に圧壊
    ("surface", "surface", {"drums": "lib", "lv": 2, "kind": "intro"}),
    ("d100", "d100", {"drums": "half", "lv": 2, "kind": "chorus"}),
    ("d300", "d300", {"drums": "sparse", "lv": 1, "kind": "verse", "bpm": 72}),
    ("d700", "d700", {"drums": "heart", "lv": [1] * 5 + [0] * 5, "kind": "bridge", "bpm": 60}),
    ("d1000", "d1000", {"drums": "none", "lv": 0, "kind": "outro", "bpm": 48}),
    ("crush", "crush", {"drums": "own", "lv": 3, "kind": "break"}),
]
FADE["11"] = (0, 10)

# 12 塹壕の朝（124）: 三部構成（突撃→休戦→再突撃）。スネアの行進だけで始まり、真ん中で金管だけの休戦（テンポ96）、スネアのロールで再突撃、最後は朝の金管でフェードアウト
DESC["12"] = "展開: 前半が戦い（ラッパ・総攻撃・砲撃）、停戦の合図のあと、後ろの3分の1以上は誰も撃たない静かな朝（76・クリーンの歌）。遠い砲声で始まり、金管の静かな聖歌でフェードアウト。"
FADE["12"] = (0, 12)
PLANS["12"] = [   # 2026-10-24 素材から作り直し: 前半が戦い、後ろ3分の1以上が静かな朝
    ("night", "night", {"drums": "own", "lv": 0, "kind": "intro"}),
    ("bugle", "bugle", {"drums": "none", "lv": 1, "kind": "interlude"}),
    ("assault", ("assault", 0, 16), {"drums": "double", "lv": 3, "kind": "chorus", "from": "break1bar"}),
    ("trench", ("assault", 16, 20), {"drums": "sparse", "lv": 2, "kind": "break"}),
    ("assault2", ("assault", 20, 32), {"drums": "double", "lv": 3, "kind": "chorus"}),
    ("barrage", "barrage", {"drums": "half", "lv": 3, "kind": "break", "stop": True}),
    ("signal", "signal", {"drums": "none", "lv": 1, "kind": "interlude"}),
    ("morning", "morning", {"drums": "sparse", "lv": [0] * 8 + [1] * 24, "kind": "verse", "bpm": 76, "calm": True}),
    ("light", "light", {"drums": "none", "lv": 0, "kind": "outro"}),
]

# 13 闇市の値札（108）: 値切りのかけ合い。サックスとベースで始まり、ギターとサックスが2小節→1小節と交互に言い合って、決めの一撃で「商談成立」
DESC["13"] = "展開: かけ合い（値切り）。始まりはサックスとベースだけ、2番のAメロとソロでギターとバリトンサックスが2小節ずつ、最後は1小節ずつ言い合い、決めの一撃で商談成立。終わりはサックスがフェードアウト。"
PLANS["13"] = ([
    ("intro", "intro", {"keep": ["extra", "bass", "drums"], "drums": "ride"}),
    ("intro", "intro", {"drums": "own"}),
    ("verse", "verse", {"give": ("lead", "バリトンサックス"), "drums": "sparse"}),
    ("verse", "verse", {}),
    ("pre", "pre", {}),
    ("chorus", "chorus", {}),
    ("inter", "inter", {"drums": "half"}),
] + alt("verse2", "verse2", 8, 2, {}, {"give": ("lead", "バリトンサックス")}, "haggle", "haggle") + [
    ("pre", "pre2", {"drums": "build"}),
    ("chorus", "chorus2", {}),
    ("bridge", "bridge", {"drums": "shuffle"}),
] + alt("solo", "solo", 4, 2, {}, {"give": ("lead", "バリトンサックス")}, "trade", "trade")
  + alt("solo", "solo", 4, 1, {"drums": "double"}, {"give": ("lead", "バリトンサックス"), "drums": "double"}, "trade", "trade", start=4) + [
    ("deal", "break", {"kime": [0, 0.5, 1.5, 3]}),
    ("chorus", "chorus3", {"from": "stopBeat"}),
    ("chorus", "chorus2", {"semi": 1, "drums": "double"}),
    ("outro", "outro", {"drums": "own"}),
    ("outro", ("intro", 0, 4), {"keep": ["extra"], "kind": "outro"}),
])
FADE["13"] = (0, 6)

# 14 裏通りのサイレン（140）: クラブのドロップ型。サイレンのタッピングだけで始まり、4つ打ちのループ→スネアの助走→全員が抜けた1小節→ドロップ、を3回。終わりはループのフェードアウト
DESC["14"] = "展開: クラブのドロップ型（4つ打ちのループ→スネアがだんだん細かくなる助走→1小節の空白→ドロップ、を3回）。始まりは遠くの空気だけで、低い音・心拍・リフの助走と空間が広がって盛大に始まる（タッピングなし）。終わりは4つ打ちのループがフェードアウト。"
PLANS["14"] = [
    # 2026-10-23 人間（14）「前奏が違う。だんだん小さい音が空間を広げて大きくなって盛大にスタートする感じ。ピロピロはいらない」:
    #   タッピングのサイレンをやめ、遠くの空気（シンセの層）だけ → 低い音と心拍のキックが加わる → リフとドラムの助走で一気にふくらみ → 走るリフで盛大に始まる
    ("intro", "intro", {"keep": ["extra", "fx"], "kind": "intro"}),
    ("intro", "intro", {"keep": ["extra", "fx", "bass", "drums"], "drums": "heart", "kind": "intro"}),
    ("intro", ("inter", 0, 4), {"keep": ["extra", "fx", "bass", "drums", "riff"], "drums": "build", "kind": "pre"}),
    ("loop", "inter", {"drums": "kick4", "from": "break1bar"}),
    ("loop", "inter2", {"drums": "kick4", "keep": ["drums", "bass", "riff"]}),
    ("verse", "verse", {"drums": "kick4"}),
    ("build", "run", {"drums": "build", "kind": "pre"}),
    ("drop", "chorus", {"from": "break1bar", "kind": "chorus"}),
    ("loop", "inter2", {"drums": "half"}),
    ("verse", "verse2", {"drums": "kick4"}),
    ("build", "run", {"drums": "build", "kind": "pre"}),
    ("drop", "chorus2", {"from": "stopBeat", "drums": "double", "kind": "chorus"}),
    ("bridge", "bridge", {"drums": "sparse"}),
    ("siren", "siren", {"drums": "own"}),
    ("loop", "inter", {"drums": "toms", "keep": ["drums", "bass", "riff", "extra"]}),
    ("solo", "solo", {}),
    ("build", ("run", 4, 8), {"drums": "build", "kind": "pre"}),
    ("drop", "chorus3", {"from": "break1bar", "kind": "chorus"}),
    ("outro", "inter", {"keep": ["riff", "drums", "bass"], "drums": "kick4", "kind": "outro"}),
]
FADE["14"] = (0, 10)

# 15 月の裏で眠る（82）: アーチ形式（鏡のように折り返す）。鉄琴で始まり、夢→落下→夜→真ん中の山場→夜→落下→夢と同じ道を戻って、始まりの鉄琴でフェードアウト
DESC["15"] = "展開: アーチ形式（真ん中のサビを山にして、来た道を鏡のように戻る：鉄琴→夢→落下→リフ→夜→山場→夜→リフ→目覚め→夢→鉄琴）。終わりは始まりと同じ鉄琴がゆっくりフェードアウト。"
PLANS["15"] = [
    ("intro", "intro", {"drums": "own"}),
    ("dream", "dream", {"drums": "own"}),
    ("dream", "dream2", {"drums": "ride"}),
    ("fall", "fall", {"drums": "own"}),
    ("riff", "riff", {"drums": "half"}),
    ("night", "night", {}),
    ("chorus", "chorus", {"from": "stopBeat"}),
    ("night", "night2", {"drums": "double"}),
    ("riff", "riff", {"drums": "own"}),
    ("wake", "wake", {"drums": "own"}),
    ("dream", "dream3", {"drums": "sparse"}),
    ("outro", "intro", {"bpm": (70, 2), "drums": "own", "kind": "outro"}),
    ("outro", "outro", {"drums": "own"}),
]
FADE["15"] = (0, 10)

# 16 仁義の雨（116・7拍子）: 回想形式。葬列（テンポ80）で始まり、昔の抗争（116）を思い出し、また葬列に戻ってアコーディオンが消える
DESC["16"] = "展開: 回想形式（葬列の場面＝テンポ80のハーフタイムで始まり、昔の抗争＝116の速い本編を思い出し、最後にまた葬列へ戻る）。終わりはアコーディオンとベースだけがフェードアウト。"
PLANS["16"] = [
    ("funeral", "funeral", {"bpm": 80, "drums": "half", "kind": "intro"}),
    ("funeral", "inter", {"drums": "half", "kind": "intro"}),
    ("intro", "intro", {"bpm": 116, "drums": "own"}),
    ("verse", "verse", {}),
    ("pre", "pre", {}),
    ("chorus", "chorus", {"calm": True}),
    ("inter", "inter", {"drums": "double"}),
    ("verse", "verse2", {"drums": "own"}),
    ("pre", "pre2", {}),
    ("chorus", "chorus2", {"calm": True}),
    ("bridge", "bridge", {"drums": "tribal"}),
    ("kime", ("chorus3", 0, 2), {"kime": [0, 1.5, 3, 4.5, 6]}),
    ("chorus", "chorus3", {"calm": True}),
    ("funeral", "funeral", {"bpm": (76, 2), "drums": "half", "kind": "outro"}),
    ("outro", "outro", {"bpm": 72, "keep": ["extra", "bass"]}),
]
FADE["16"] = (0, 8)

# 17 堕天の証明（136）: 縮まるかけ合い（ストレッタ）。悪魔と天使が8小節→4小節→2小節→1小節と交代を速め、最後に一つに溶ける。終わりは決めで止める
DESC["17"] = "展開: 縮まるかけ合い（悪魔＝重いハーフタイムと、天使＝合唱が、8小節→4小節→2小節→1小節と交代を速めていき、最後に一つに溶け合う）。終わりはピタッと止める。"
PLANS["17"] = ([
    ("intro", ("angel", 0, 4), {"keep": ["extra", "fx"], "kind": "intro"}),        # 人間「17の前奏、ピロピロやめて空間がだんだん広がるように」: 天使の合唱だけで始まり
    ("intro", ("angel", 4, 8), {"keep": ["extra", "fx", "bass", "drums"], "drums": "sparse", "kind": "intro"}),   # 低い音と薄いドラムが加わって
    ("intro", "intro", {"drop": ["gtr"], "drums": "own"}),                          # リフが入って空間がいっぱいに（速弾きは外す）
    ("demon", "demon", {"drums": "half"}),
    ("angel", "angel", {"drums": "ride"}),
    ("demon", "dchorus", {}),
    ("angel", "achorus", {}),
] + alt("demon2", "angel2", 8, 4, {"drums": "half"}, {"drums": "ride"}, "demon", "angel")
  + [("battle", ("battle", 0, 8), {})]
  + alt("dchorus", "achorus", 8, 2, {"drums": "half"}, {}, "demon", "angel")
  + alt("dchorus", "achorus", 8, 1, {"drums": "double"}, {"drums": "double"}, "demon", "angel")
  + [("battle", ("battle", 8, 24), {"drums": "own"}),
     ("fall", "fall", {"bpm": (110, 2), "drums": "sparse"}),
     ("angel", "angel", {"keep": ["extra", "lead", "bass"], "soft": ["lead"], "kind": "bridge"}),
     ("demon", "demon", {"bpm": 136, "drums": "half"}),
     ("merge", "merge", {"bpm": 136, "from": "stopBeat"}),
     ("merge", ("merge", 8, 16), {"semi": 1, "drums": "double"}),
     ("outro", "outro", {"semi": 1, "stop": True, "drums": "own"})])

# 18 祈りの音量（90・3拍子）: ボレロ型（一つのテーマを何度もくり返し、そのたびに楽器と音量が増える）。最初はギターとベースだけでささやき、バグパイプが受け継ぎ、最後は全音上がって全員で
DESC["18"] = "展開: ボレロ型（サビのテーマを6回くり返し、そのたびに楽器と音量が増えていく。1回目はギターとベースだけのささやき、3回目はバグパイプが歌い、最後の2回は全音上がって全員で）。"
PLANS["18"] = [
    ("intro", "intro", {"drums": "own"}),
    ("theme", "chorus", {"keep": ["lead", "bass"], "soft": ["lead"], "kind": "verse"}),
    ("theme", "chorus2", {"keep": ["lead", "bass", "drums", "extra"], "drums": "sparse", "kind": "verse"}),
    ("lament", "lament", {"drums": "own"}),
    ("theme", "chorus", {"give": ("lead", "バグパイプ"), "drop": ["riff"], "drums": "ride", "kind": "pre"}),
    ("prayer", "prayer", {"drums": "own"}),
    ("pre", "pre", {"drums": "build"}),
    ("theme", "chorus2", {"kind": "chorus"}),
    ("theme", "chorus3", {"semi": 2, "kind": "chorus"}),
    ("theme", "chorus3", {"semi": 2, "drums": "double", "kind": "chorus"}),
    ("outro", "outro", {"semi": 2, "stop": True, "drums": "own"}),
]

# 19 最後の呼吸（104）: 人生を巻き戻す（山場→大人→若い頃→子ども→戻る→山場）。若い頃は速く（116）、子どもの頃はドラムなしで、最後は息が止まるように遅くなって終わる
DESC["19"] = "展開: 人生を巻き戻す（死の間際の山場から始まり、大人→若い頃＝テンポ116→子ども＝ドラムなし→記憶の中でテーマを弦がささやく→今へ戻る→山場）。終わりは息が細くなるように遅くなって止まる。"
PLANS["19"] = [
    ("climax", "climax", {"drums": "own"}),
    ("breath", "breath", {"keep": ["extra"]}),
    ("adult", "adult", {"drums": "half"}),
    ("adult", "adult2", {}),
    ("youth", "youth", {"bpm": 116, "drums": "double"}),
    ("youth", ("youth", 0, 8), {"drums": "toms", "semi": 2}),
    ("child", "child", {"bpm": 96, "keep": ["extra", "bass", "gtr"]}),
    ("memory", ("climax", 0, 8), {"keep": ["extra", "bass"], "soft": ["extra"], "kind": "bridge"}),
    ("return", "return", {"bpm": 104}),
    ("climax", "climax2", {"from": "stopBeat"}),
    ("climax", ("climax2", 8, 16), {"semi": 1, "drums": "double"}),
    ("breath", "breath", {"keep": ["extra"], "semi": 1}),
    ("last", "last", {"bpm": (72, 3), "semi": 1, "drums": "sparse"}),
]

# 20 赦しの値段（120・5拍子）: サーカスの演目のメドレー。幕が上がって始まり、綱渡り（ライド）→猛獣使い（タムの太鼓）→空中ぶらんこ（4つ打ち）→ピエロの悲しい芸（テンポ96）→フィナーレ。最後は笑い声でぷつりと切れる
DESC["20"] = "展開: サーカスの演目のメドレー（幕開け→綱渡り＝ライド→猛獣使い＝タムの太鼓→空中ぶらんこ＝4つ打ち→ピエロの悲しい芸＝テンポ96のハーフタイム→フィナーレは半音上）。終わりは木琴の笑い声でぷつりと切れる。"
PLANS["20"] = [
    ("curtain", "curtain", {"kind": "intro", "drums": "own"}),
    ("intro", "intro", {"drums": "own"}),
    ("act1", "verse", {"drums": "ride", "kind": "verse"}),
    ("act1", "chorus", {"kind": "chorus"}),
    ("laugh", "laugh", {"drums": "own"}),
    ("act2", "inter", {"drums": "tribal", "kind": "interlude"}),
    ("act2", "verse2", {"drums": "toms", "kind": "verse"}),
    ("pre", "pre", {"drums": "build"}),
    ("act3", "chorus2", {"drums": "kick4", "kind": "chorus"}),
    ("circus", "circus", {"drums": "own"}),
    ("act4", "circus", {"semi": 1, "drums": "half", "bpm": 96, "drop": ["riff"], "kind": "bridge"}),
    ("chorus", "chorus3", {"bpm": 120, "semi": 1, "from": "stopBeat"}),
    ("laugh", "laugh", {"semi": 1, "stop": True, "drums": "own"}),
]

# 21 群青の滑走路（140）: 離陸・巡航・着陸（テンポの山）。ベースだけのエンジン音（110）から加速して離陸、雲の上はドラムなし、着陸でテンポが下がり、ベースとバイオリンが残ってフェードアウト
DESC["21"] = "展開: 離陸・巡航・着陸（ベースだけのエンジン音＝テンポ110から 140 まで加速して離陸、雲の中はドラムなし、雲の上は全音上がる、着陸で 100→90 へ減速）。終わりはベースとバイオリンがフェードアウト。"
PLANS["21"] = [
    ("taxi", ("intro", 0, 4), {"keep": ["bass"], "bpm": 110, "kind": "intro"}),
    ("taxi", ("intro", 4, 8), {"keep": ["bass", "drums", "extra"], "drums": "sparse", "bpm": (140, 4), "kind": "intro"}),
    ("takeoff", "pre", {"drums": "build", "kind": "pre"}),
    ("chorus", "chorus", {"from": "stopBeat"}),
    ("verse", "verse", {"drums": "ride"}),
    ("pre", "pre2", {}),
    ("chorus", "chorus2", {}),
    ("cloud", "cloud", {"keep": ["riff", "gtr", "bass", "extra", "fx"]}),
    ("above", "above", {"drums": "ride"}),
    ("above", "above", {"semi": 2, "drums": "toms"}),
    ("solo", "solo", {"semi": 2, "drums": "double"}),
    ("verse", "verse2", {"drums": "half"}),
    ("chorus", "chorus3", {"from": "stopBeat"}),
    ("chorus", ("chorus2", 8, 16), {"semi": 2}),
    ("landing", "outro", {"bpm": (100, 8), "drums": "half", "semi": 2}),
    ("landing", "intro", {"keep": ["bass", "extra"], "bpm": 90, "semi": 2, "kind": "outro"}),
]
FADE["21"] = (0, 10)

# 22 難破船の歌（96・6拍子）: 船歌のメドレー→嵐→難破→生き残りの歌。フィドル1人で始まり、ジグはテンポ120、嵐は全音上がって荒れ、難破で1小節の無音、生き残りはドラムなしでフィドルがサビを歌う
DESC["22"] = "展開: 物語の場面転換（フィドル1人→船歌→陽気なジグ＝テンポ120→嵐＝104・112でだんだん荒れる→難破＝1小節の無音→生き残り＝ドラムなし・テンポ80でフィドルがサビを歌う→最後のサビ）。終わりはフィドルとベースがフェードアウト。"
PLANS["22"] = [
    ("intro", "intro", {"keep": ["extra"]}),
    ("verse", "verse", {}),
    ("chorus", "chorus", {}),
    ("jig", "jig", {"bpm": 120, "drums": "own"}),
    ("jig", "jig", {"drums": "double"}),
    ("jig", "jig", {"semi": 2, "drums": "own"}),
    ("verse", "verse2", {"bpm": 96, "drums": "ride"}),
    ("chorus", "chorus2", {}),
    ("storm", "storm", {"bpm": 104, "drums": "own"}),
    ("storm", "storm", {"bpm": 112, "drums": "double", "semi": 1}),
    ("wreck", "wreck", {"bpm": 96, "stop": True, "drums": "own"}),
    ("silence", ("wreck", 0, 1), {"keep": [], "kind": "break"}),
    ("survivor", "survivor", {"bpm": 80, "keep": ["gtr", "extra", "bass"]}),
    ("survivor", "chorus", {"keep": ["extra", "gtr", "lead"], "soft": ["lead"], "give": ("lead", "フィドル"), "kind": "bridge"}),
    ("chorus", "chorus3", {"bpm": 96, "from": "stopBeat"}),
    ("outro", "outro", {"keep": ["extra", "bass"]}),
]
FADE["22"] = (0, 8)

# 23 焼け野原の国歌（80）: 壊れていく変奏。ピアノの国歌（そのまま）で始まり、行進→重い本編→半音下がる→国歌が決めの破片になる→国歌の全力→ピアノの国歌が途中で途切れて終わる
DESC["23"] = "展開: 壊れていく変奏（はじめはピアノだけの国歌、行進・本編と進むうちに半音・全音と調が下がって崩れ、国歌が決めの一撃の破片になる）。終わりはピアノの国歌が途中で途切れる。"
PLANS["23"] = [
    ("anthem", "intro", {"keep": ["extra"], "kind": "intro"}),
    ("march", "march", {"drums": "build"}),
    ("verse", "verse", {}),
    ("chorus", "chorus", {}),
    ("inter", "inter", {"drums": "toms"}),
    ("verse", "verse2", {"drums": "half"}),
    ("chorus", "chorus2", {"drums": "half", "semi": -1}),
    ("roll", "roll", {"drums": "own", "semi": -1}),
    ("solo", "solo", {"semi": -1, "drums": "double"}),
    ("broken", ("anthem", 0, 4), {"kime": [0, 1.5, 3], "semi": -1}),
    ("anthem", "anthem", {"semi": -1, "from": "stopBeat"}),
    ("anthem", "anthem", {"semi": -2, "drums": "half", "bpm": 72}),
    ("outro", ("intro", 0, 5), {"keep": ["extra"], "bpm": 68, "semi": -2, "kind": "outro"}),
]

# 24 錆びた天秤（126）: 溜めて最後に一度だけ解放。鐘だけで始まり、判決の場面は2回とも決めの一撃だけ（サビを鳴らさない）、裁きの天秤とソロをはさんで、最後の判決で初めて全員のサビ
DESC["24"] = "展開: 溜めて最後に解放（鐘だけで始まり、罪→言い訳→判決が2回くるが、判決は決めの一撃だけでサビを鳴らさない。天秤とソロで溜めて、最後の判決で初めて全員のサビが3回続く）。終わりは鐘だけが残る。"
PLANS["24"] = [
    ("bell", "bell", {"drums": "own"}),
    ("intro", "intro", {"drums": "own"}),
    ("sin", "sin", {}),
    ("excuse", "excuse", {"drums": "half"}),
    ("verdict", ("verdict", 0, 4), {"kime": [0, 1.5, 3], "kind": "break"}),
    ("sin", "sin2", {"drums": "ride"}),
    ("excuse", "excuse2", {}),
    ("verdict", ("verdict2", 0, 4), {"kime": [0, 0.75, 1.5, 3], "kind": "break"}),
    ("weigh", "weigh", {"drums": "toms"}),
    ("sin", "sin", {"drums": "half", "keep": ["riff", "drums", "bass"]}),
    ("solo", "solo", {"drums": "double"}),
    ("bell", "bell", {"stop": True, "drums": "own"}),
    ("verdict", "verdict3", {"from": "stopBeat", "kind": "chorus"}),
    ("verdict", "verdict2", {"semi": 1, "kind": "chorus"}),
    ("weigh", "weigh", {"semi": 1, "drums": "double"}),
    ("verdict", "verdict3", {"semi": 1, "kind": "chorus"}),
    ("end", "end", {"semi": 1, "drums": "own"}),
    ("bell", "bell", {"keep": ["extra"], "semi": 1, "kind": "outro"}),
]

# 25 夜明けの闇市（112）: 時刻の組曲（0時＝ハーフタイム／2時＝ライドとシャッフル／3時＝ドラムが薄い／4時＝タムの太鼓／夜明け＝テンポ120で全員）。最後は朝のバイオリンとクリーンでフェードアウト
DESC["25"] = "展開: 時刻の組曲（0時＝重いハーフタイム、2時＝ライドとシャッフルの酒場、3時＝人の消えた市場、4時＝タムの太鼓と取引、夜明け＝テンポ120で全員）。終わりは朝のバイオリンとクリーンギターでフェードアウト。"
PLANS["25"] = [
    ("0時", "intro", {"drums": "half", "kind": "intro"}),
    ("0時", "riff", {"drums": "half", "kind": "intro"}),
    ("verse", "verse", {"drums": "half"}),
    ("pre", "pre", {}),
    ("chorus", "chorus", {"drums": "half"}),
    ("1時", "riff", {"drums": "toms", "kind": "interlude"}),
    ("2時", "market", {"drums": "shuffle", "kind": "interlude"}),
    ("verse", "verse2", {"drums": "ride"}),
    ("pre", "pre2", {"drums": "build"}),
    ("chorus", "chorus2", {}),
    ("3時", "market", {"keep": ["extra", "bass", "drums", "gtr"], "drums": "sparse", "kind": "bridge"}),
    ("4時", "tap", {"drums": "tribal", "kind": "solo"}),
    ("4時", "trade", {"drums": "double", "kind": "solo"}),
    ("4時", "tap", {"drums": "own", "semi": 2, "kind": "solo"}),
    ("still", "still", {"stop": True, "drums": "own"}),
    ("dawn", "dawn", {"bpm": 120, "drums": "own"}),
    ("chorus", "chorusM", {"from": "stopBeat"}),
    ("chorus", "chorusM", {"drums": "double"}),
    ("outro", "outro", {"drums": "own"}),
    ("朝", "intro", {"keep": ["extra", "gtr"], "kind": "outro"}),
]
FADE["25"] = (0, 8)

# 26 鬼灯の撥（128）: 祖母と孫のかけ合い。祖母の三味線と尺八だけで始まり、Aメロを祖母が歌い、2番は孫とギターが2小節ずつ交代、櫓の太鼓、最後は二人の撥が重なり、送り火（はじめの音）がフェードアウト
DESC["26"] = "展開: 祖母と孫のかけ合い（始まりは祖母の三味線と尺八だけ、1番のAメロは祖母の三味線が歌い、2番は孫の三味線とギターが2小節ずつ交代、ブリッジは櫓の太鼓、最後は二人の撥が重なって半音上へ）。終わりは送り火＝はじめの音がフェードアウト。"
PLANS["26"] = ([
    ("intro", "intro", {"drums": "own"}),
    ("riff", "riff", {"drums": "own"}),
    ("verse", "verse", {"give": ("lead", "三味線（祖母"), "drums": "ride"}),
    ("pre", "pre", {}),
    ("chorus", "chorus", {}),
    ("inter", "inter", {"drums": "toms"}),
] + alt("verse2", "verse2", 8, 2, {}, {"give": ("lead", "三味線（孫")}, "verse", "verse") + [
    ("pre", "pre2", {"drums": "build"}),
    ("chorus", "chorus2", {}),
    ("bridge", "bridge", {"drums": "tribal"}),
    ("bridge", "bridge", {"drums": "solo", "keep": ["drums", "extra"], "kind": "break"}),
    ("solo", "solo", {}),
    ("verse", "verse", {"give": ("lead", "三味線（孫"), "drums": "half", "phr": False}),
    ("pre", "pre", {"drums": "build"}),
    ("chorus", "chorus", {"drums": "own"}),
    ("solo", "solo", {"semi": 1, "drums": "double"}),
    ("kime", ("chorus3", 0, 2), {"kime": [0, 0.75, 1.5, 3], "semi": 1}),
    ("chorus", "chorus3", {"semi": 1, "from": "stopBeat"}),
    ("outro", "outro", {"semi": 1, "drums": "own"}),
    ("送り火", "intro", {"keep": ["extra"], "semi": 1, "kind": "outro"}),
])
FADE["26"] = (0, 10)
FADE["17"] = (6, 0)    # 前奏は6秒かけて、遠くから近づくように


KEYS = {"01": ("C#", "dorian"), "02": ("F#", "aeolian"), "03": ("D", "aeolian"), "04": ("A", "aeolian"), "05": ("E", "phrygian"),
        "06": ("B", "aeolian"), "07": ("E", "ionian"), "08": ("G", "aeolian"), "09": ("C", "aeolian"), "10": ("A", "mixolydian"),
        "11": ("F", "aeolian"), "12": ("D", "phrygian"), "13": ("Bb", "dorian"), "14": ("E", "aeolian"), "15": ("C#", "aeolian"),
        "16": ("G#", "aeolian"), "17": ("F#", "aeolian"), "18": ("E", "aeolian"), "19": ("B", "aeolian"), "20": ("A", "aeolian"),
        "21": None, "22": ("E", "aeolian"), "23": ("C", "aeolian"), "24": ("B", "aeolian"), "25": None, "26": ("E", "phrygian")}


# ギター・ベースの弾き方をどれだけ変えるか（曲の物語で決める。決まりにしない）
PHR_POLICY = {
    # 看板のリフを守り通す: 螺旋は同じリフのまま上っていく／クラブのループは同じループが命／ボレロは伴奏を変えないのが型／アーチは鏡なので同じ物が戻る
    "02": "keep", "14": "keep", "18": "keep", "15": "keep", "04": "keep",
    # 場面ごとにどんどん変える: サーカスの演目／時刻の組曲／船の場面転換／天使と悪魔の戦い／壊れていく国歌／人生の各時代
    "20": "often", "25": "often", "22": "often", "23": "often", "19": "often",
}


# 曲名（2026-10-23 人間「曲名もなんかゲームの曲名だよね。そのイメージも取っ払って」）。
# 「〇〇の〇〇」の形をやめ、今のラウドの曲名のように: 英語の短い言い切り・長い一文・漢字の熟語・日本語の命令や言い切り。
# 中身（物語）は変えない。乱数の種はもとの曲名（song.title）のまま（書き出しの結果がずれないように）
TITLES = {
    "01": "灰皿にネオン", "02": "PALE ORBIT", "03": "EYEWALL", "04": "口を縫え", "05": "Seven Horns, No Halo",
    "06": "偶像崩落", "07": "Terminal Velocity of a Feather", "08": "心拍、加速、停止", "09": "Down Is the Only Way",
    "10": "Airmail to Nowhere", "11": "Crush Depth", "12": "Ceasefire at 5AM", "13": "No Receipts", "14": "SIREN//LOOP",
    "15": "Sleep Where the Moon Can't See", "16": "喪服と雨", "17": "Q.E.D. (Fallen)", "18": "Pray Louder",
    "19": "Rewind My Last Breath", "20": "Clowns Don't Apologize", "21": "V1, Rotate", "22": "Survivors Sing Off-Key",
    "23": "Anthem for Ashes", "24": "Guilty Until Proven", "25": "Last Deal Before Sunrise", "26": "BACHI",
}


# 曲ごとの音量の好み（割合）。16: 人間「16ドラムの音3落とそう」（×0.97）・「サビでドラムのガチャガチャした感じを抑えよう」（サビは calm）
GAINS = {"16": {"drums": 0.97}, "01": {"lead": 0.85, "_guitar_delay": 0.07}}   # 01: 人間「ギターにほんの少しディレイ入れよう」「リフ」（看板リフだけ）   # 01: 人間「リードの音少し下げる」
HAT_DELICATE = {"16"}
# 「きーーーん」を入れない曲（静けさが主役・眠り・深海）。人間「良い場面だけ使えるといい」
NO_SCREAM = {"04", "11", "15"}   # 人間「16のハイハットのシャッフルは少し繊細な音に変えよう。強弱をつけよう」


def apply_plan(song, no):
    if no not in PLANS: return
    song.plan = PLANS[no]
    song.key_mode = KEYS.get(no) or (None, None)
    song.phr_policy = PHR_POLICY.get(no, "rare")
    song.gains = GAINS.get(no, {})
    song.hat_delicate = no in HAT_DELICATE
    if not hasattr(song, "auto_scream"): song.auto_scream = no not in NO_SCREAM   # 曲のファイルで決めていれば、そちらを使う
    song.display_title = TITLES.get(no)
    if song.display_title: song.desc = f"もとの仮題「{song.title}」。" + song.desc
    song.desc += " " + DESC[no]
    fi, fo = FADE.get(no, (0, 0))
    song.fade_in, song.fade_out = fi, fo
