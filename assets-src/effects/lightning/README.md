# 雷の術のエフェクト（ボス用）

作り方と決まりは `docs/design/battle-effects.md`。

- `aura.json` 発動（ボスのまわり。予言の歪みの両手を振り上げた姿の形から作った）
- `charge.json` ため ／ `bolt.json` 落雷（1人） ／ `storm.json` 雷の嵐（全体）
- `editor/` ドット絵エディタで1コマずつフレームに入れて書き出したもの（`*.project.json` はエディタの「作品を開く」で開ける、`*.gif`、`*.sheet.png`、`*.editor.png` はエディタの画面）
- 作りなおし: `python3 tools/pixel-art/fx/lightning.py assets-src/effects/lightning --boss assets-src/monsters/kiri-yugami/anim.json`
- まだゲームには入れていない（仮）。呪文の名前も未定。
