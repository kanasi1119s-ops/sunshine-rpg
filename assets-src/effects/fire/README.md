# 炎の術のエフェクト（ボス用）

作り方と決まりは `docs/design/battle-effects.md` の「炎系」。

- `aura.json` 発動（ボスのまわり。予言の歪みの両手を振り上げた姿の形から作った） ／ `charge.json` ため
- `fireball.json` 火球（1人。コマごとに画面の置き場所 `at`） ／ `pillars.json` 火柱（全体）
- `editor/` ドット絵エディタで1コマずつフレームに入れて書き出したもの（食い違い0マス）
- 作りなおし: `python3 tools/pixel-art/fx/fire.py assets-src/effects/fire --boss assets-src/monsters/kiri-yugami/anim.json`
- まだゲームには入れていない（仮）。呪文の名前も未定。
