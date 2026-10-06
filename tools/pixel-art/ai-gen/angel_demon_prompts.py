"""天使20体・悪魔20体のドット絵（128×128・24色）の指示文（2026-10-06、人間の指示「天使と悪魔で20体ずつドット絵を作ってください 128×128」）。

決まり（CLAUDE.md 1-1・make-art）:
- 既存作品（ゲーム・漫画など）の天使・悪魔の名前や姿に寄せない。固有の名前（神話・宗教の個人名）も使わない。
- 名簿の kind は "extra"（ゲームにはまだ組み込まない絵。書き出しの対象外）。
- 下絵に無い目は足さない（2026-10-05、人間の指示）。白い・光る天使は暗い背景で描く（bg: dark）。
使い方: python3 angel_demon_prompts.py   → monster-roster.json に40体を足す（すでにあれば指示文だけ更新）
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROSTER = os.path.join(HERE, "monster-roster.json")

# (id, 名前, 形, 体のおおまかな色, 暗い背景で描くか, 指示文)
ANGELS = [
    ("angel-01", "光輪の見張り", "winged", [220, 200, 140], True, "a tall angel in white and gold robes with four large feathered wings and a halo of light, holding a long spear, serene face"),
    ("angel-02", "祈りの天使", "tall", [200, 210, 230], True, "a kneeling angel with folded white wings and hands held together in prayer, pale blue robes, soft glowing halo"),
    ("angel-03", "盾の天使", "tall", [190, 195, 205], False, "an angel knight in polished silver armor with white wings, holding a large round shield with a sun emblem"),
    ("angel-04", "弓の天使", "winged", [170, 200, 150], True, "an angel archer in green and gold clothes drawing a bow made of light, white wings spread wide"),
    ("angel-05", "炎の天使", "winged", [220, 120, 60], False, "an angel with wings made of flames, red and gold armor, holding a burning sword"),
    ("angel-06", "氷の天使", "winged", [150, 190, 230], True, "an angel with wings of clear ice crystals, pale blue robes, a crown of icicles, cold mist around"),
    ("angel-07", "天秤の天使", "tall", [210, 190, 130], True, "a blindfolded angel in white robes holding golden balance scales, folded wings, calm and stern"),
    ("angel-08", "書の天使", "tall", [200, 180, 150], True, "an angel reading a large floating glowing book, holding a feather quill, cream robes and brown-tipped wings"),
    ("angel-09", "星の天使", "winged", [60, 70, 140], True, "an angel in dark blue robes with wings dotted with tiny stars like a night sky, a small star above its head"),
    ("angel-10", "竪琴の天使", "tall", [220, 200, 170], True, "an angel playing a golden harp, long flowing robes, wings curved around the body, glowing music notes of light"),
    ("angel-11", "車輪の天使", "float", [210, 180, 90], True, "a celestial being made of interlocking golden rings covered in eyes, with small white wings, glowing core, no human body"),
    ("angel-12", "翼の集まり", "float", [230, 230, 240], True, "a celestial creature made only of many white wings folded around a glowing golden core with one calm eye, no human body"),
    ("angel-13", "鎖の天使", "tall", [180, 170, 160], False, "an angel bound by heavy golden chains, torn grey wings, cracked halo, head lowered"),
    ("angel-14", "灯火の天使", "tall", [200, 160, 100], True, "an angel holding up a glowing lantern, brown traveling cloak over white robes, small wings, warm light"),
    ("angel-15", "花の天使", "winged", [230, 170, 190], True, "an angel with wings made of pink and white flower petals, a crown of flowers, green leafy robes"),
    ("angel-16", "審判の天使", "tall", [200, 170, 90], False, "a stern angel warrior in heavy gold armor and a closed helmet, holding a huge two-handed sword, great white wings"),
    ("angel-17", "風の天使", "winged", [180, 220, 210], True, "an angel with swirling pale green robes and wings made of streaks of wind, floating, hair blowing"),
    ("angel-18", "薄明の天使", "winged", [190, 130, 170], True, "an angel in dusk colors, purple and orange wings, holding a tall staff with a setting sun ornament"),
    ("angel-19", "癒しの天使", "tall", [200, 230, 210], True, "a gentle angel in pale green robes holding a glowing water jar, small white wings, soft light around its hands"),
    ("angel-20", "門番の天使", "tall", [170, 175, 190], False, "a huge angel gatekeeper in stone grey armor holding a giant key and a halberd, six folded wings"),
]
DEMONS = [
    ("demon-01", "角の悪魔", "winged", [150, 50, 45], False, "a red-skinned demon with curled black horns, leathery bat wings, clawed hands, holding a forked spear, armored"),
    ("demon-02", "小悪魔", "ground", [110, 130, 90], False, "a small grey-green imp with long pointed ears, a wide grin, tiny bat wings and a thin tail, crouching"),
    ("demon-03", "炎の悪魔", "big", [80, 50, 45], False, "a hulking demon made of black stone with glowing molten cracks, fire burning from its shoulders and horns"),
    ("demon-04", "影の悪魔", "tall", [50, 45, 60], False, "a tall thin shadow demon with very long claws, a smoky body and glowing red eyes, hunched"),
    ("demon-05", "骨の悪魔", "winged", [200, 190, 170], False, "a skeletal demon with ribcage wings, a horned skull head and glowing violet eye sockets, tattered cloth"),
    ("demon-06", "鎖の悪魔", "tall", [100, 85, 80], False, "a demon wrapped in rusty chains wearing an iron mask, heavy hooks hanging from the chains, dark robes"),
    ("demon-07", "蛇の悪魔", "long", [70, 110, 80], False, "a demon with a long scaly green serpent lower body, four arms holding curved blades, horned head"),
    ("demon-08", "雄羊角の悪魔", "big", [110, 80, 60], False, "a hulking demon with big curled ram horns, furry legs and hooves, holding a heavy axe, leather armor"),
    ("demon-09", "蝙蝠の悪魔", "winged", [70, 55, 70], False, "a demon with a bat-like head, huge ears, membrane wings and long arms, crouching on a rock"),
    ("demon-10", "蜘蛛の悪魔", "big", [60, 50, 60], False, "a demon with a horned upper body and eight long spider legs coming from its back, purple markings"),
    ("demon-11", "契約の悪魔", "tall", [70, 60, 80], False, "an elegant thin demon in a dark tailcoat holding a glowing scroll contract, small curved horns, sly smile"),
    ("demon-12", "悪夢の悪魔", "winged", [110, 80, 140], True, "a nightmare demon with dusty purple moth wings, a long thin body, a horned mask face, sleepy mist around"),
    ("demon-13", "沼の悪魔", "big", [80, 95, 60], False, "a fat toad-like swamp demon covered in moss and mud, small horns, a wide mouth, sitting in murky water"),
    ("demon-14", "氷の悪魔", "tall", [90, 130, 170], False, "a frost demon with pale blue skin, icicle horns and claws, ragged dark fur cloak, cold breath"),
    ("demon-15", "大口の悪魔", "big", [130, 70, 70], False, "a demon whose body is mostly a giant toothy mouth on short legs, small arms, horns on top"),
    ("demon-16", "宝石の悪魔", "tall", [120, 80, 130], False, "a greedy demon encrusted with glittering gems, holding a sack of gold coins, jeweled horns, purple robe"),
    ("demon-17", "仮面の悪魔", "tall", [90, 70, 90], False, "a demon wearing many different masks on its head and body, a long dark cloak, thin clawed hands"),
    ("demon-18", "炉の悪魔", "big", [90, 70, 60], False, "a demon with a glowing iron furnace built into its chest, soot-black skin, pipes on its back, heavy fists"),
    ("demon-19", "堕ちた天使", "winged", [60, 55, 70], False, "a fallen angel with tattered black feathered wings, a broken dark halo, torn grey armor, sorrowful"),
    ("demon-20", "角冠の悪魔", "tall", [90, 40, 50], False, "a demon lord with a crown of black horns, a long red cape, dark armor and a glowing scepter, seated pose"),
]

NEG_EXTRA = "nude, naked, bare chest, cleavage, gore, blood"


def main():
    r = json.load(open(ROSTER))
    by = {e["id"]: e for e in r}
    added = 0
    for kind, rows in (("天使", ANGELS), ("悪魔", DEMONS)):
        for i, name, shape, tone, dark, prompt in rows:
            e = by.get(i)
            if e is None:
                e = {"id": i, "status": "todo", "kind": "extra"}
                r.append(e); added += 1
            e.update({"name": name, "group": kind, "shape": shape, "tone": tone, "prompt": prompt,
                      "size": 128, "ncol": 24, "neg_extra": NEG_EXTRA, "neg_drop": ["human, human face", "statue"]})
            if dark:
                e["bg"] = "dark"
    json.dump(r, open(ROSTER, "w"), ensure_ascii=False, indent=1)
    print("足した:", added, "／ 天使", len(ANGELS), "悪魔", len(DEMONS))


if __name__ == "__main__":
    main()
