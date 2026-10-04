"""雑魚の敵200種の、下絵の指示文（英語）・形（shape）・体のおおまかな色（tone）（2026-10-05、人間の指示
「雑魚敵も200種類全部違うのでお願いします。時間はいくらかかってもいいです」）。

決まり（CLAUDE.md 1-1・make-art）:
- 既存作品のモンスターの名前・姿に寄せない（ゼリー状の笑う玉、有名なドラゴン・ゴーレムの形、などを避ける）。
- 名前が同じ敵（例: 砂ぬけ・野ねずみの影）も、地方ごとに材質・色・形を変えて、200種すべて別の姿にする。
- 形: ground（四つ足・低い）/ float（浮く）/ tall（立つ）/ long（細長い）/ winged（羽）/ big（大きな塊）。
使い方: python3 mob_prompts.py   → monster-roster.json の prompt・shape・tone を埋める（すでに書いてある敵は変えない）
"""
import json
import os

P = {
    # 灯里の郊外（草原・紫の歪みが入りはじめた土地）
    "enc-touri-outskirts-4": ("a small lost bat with tattered purple wings, a lantern-like glowing belly and big round ears", "winged", [90, 70, 110]),
    "enc-touri-outskirts-5": ("a small walking pebble creature made of grey cobblestones with stubby legs and a violet crack for a mouth", "ground", [125, 120, 115]),
    # 麦香野・水源（干上がった田と井戸）
    "enc-mugikano-water-source-0": ("a hovering water spirit shaped like a long teardrop with a glassy surface, a single dark eye and trailing water ribbons", "float", [90, 140, 190]),
    "enc-mugikano-water-source-1": ("a creature made of cracked dry rice-paddy earth and withered rice stalks, with hollow glowing purple eyes, on four legs", "ground", [150, 125, 85]),
    "enc-mugikano-water-source-2": ("a cave bat with a miner's broken lamp hanging from its neck, stone-grey fur, wide leathery wings", "winged", [100, 95, 90]),
    "enc-mugikano-water-source-3": ("a long water-channel insect like a water strider with very long thin legs and a shiny blue-green shell", "long", [70, 120, 110]),
    "enc-mugikano-water-source-4": ("a lumpy creature of wet brown mud with pebbles stuck in it, two stalk eyes and dripping arms", "big", [110, 85, 60]),
    "enc-mugikano-water-source-5": ("an old stone well ring come alive, mossy bricks, a dark water mouth with a rope and bucket like a tongue", "big", [120, 125, 110]),
    # 硝子湖・密輸倉庫
    "enc-garasuko-warehouse-0": ("a fat cargo rat with a burlap sack on its back, scarred ears, glowing amber eyes", "ground", [115, 95, 75]),
    "enc-garasuko-warehouse-1": ("a damp shapeless shadow seeping from wet wooden planks, mold spots, many small dim eyes", "float", [70, 85, 80]),
    "enc-garasuko-warehouse-2": ("a living shadow shaped like a small wooden crate with spider-like legs of dark smoke, iron corner brackets", "ground", [95, 80, 65]),
    "enc-garasuko-warehouse-3": ("a beaver-like gnawing creature with huge front teeth, coils of chewed hemp rope wrapped around its body", "ground", [140, 110, 70]),
    "enc-garasuko-warehouse-4": ("a walking wine barrel creature with iron hoops, stone-heavy legs and a cork for a nose, wood grain body", "big", [130, 90, 55]),
    "enc-garasuko-warehouse-5": ("a dusty warehouse moth with grey-brown patterned wings, feathery antennae and a lamp-glow spot on each wing", "winged", [150, 135, 110]),
    # 鉄鏈鉱山・坑内
    "enc-tetsukusari-mine-1": ("a tall thin shadow wearing a broken miner's helmet, long arms dragging a pickaxe, coal-black body", "tall", [55, 50, 55]),
    "enc-tetsukusari-mine-2": ("a glowing ore beetle with a crystal on its back that shines like a lamp, orange-gold shell", "ground", [190, 140, 60]),
    "enc-tetsukusari-mine-3": ("a rusty mine cart machine walking on four mechanical legs, a furnace mouth with burning coal, rivets", "ground", [120, 80, 60]),
    "enc-tetsukusari-mine-4": ("a creature formed from a pile of fallen rocks and timber supports, one glowing red eye between the stones", "big", [110, 100, 95]),
    "enc-tetsukusari-mine-5": ("a pale translucent echo of a miner with a lantern, faded overalls, empty glowing eyes, floating", "tall", [160, 170, 175]),
    # 砂音・隊商の野営地
    "enc-sanone-camp-0": ("a sand-burrowing creature like a mole with a flat shovel-shaped head and sandy plated back, peeking out of a sand mound", "ground", [190, 160, 110]),
    "enc-sanone-camp-1": ("a swirling wind spirit made of sand streaks and a torn caravan cloth, two bright eyes in the swirl", "float", [200, 175, 130]),
    "enc-sanone-camp-2": ("a shadowy desert scorpion with a translucent dark body, a pale glowing stinger and sand-colored pincers", "ground", [110, 90, 70]),
    "enc-sanone-camp-3": ("a heat-shimmering droplet spirit of sunlight with a dry cracked crust and a burning core, floating", "float", [230, 180, 90]),
    "enc-sanone-camp-4": ("a creature made of bleached animal bones fused with sandstone, horned skull head, walking on four bone legs", "ground", [210, 200, 175]),
    "enc-sanone-camp-5": ("a sandstorm bird with ragged tan feathers that shed sand, a long hooked beak and goggle-like eye rings", "winged", [180, 145, 95]),
    # 霧断崖・記録の間
    "enc-kiri-archive-0": ("a silverfish shadow creature with a long segmented body made of torn paper scraps, many legs, ink spots", "long", [170, 175, 165]),
    "enc-kiri-archive-1": ("a whispering mist spirit with a long trailing body, a faint mouth and floating letters of light around it", "float", [180, 205, 200]),
    "enc-kiri-archive-2": ("a bookworm insect with a hard leather book-cover shell, gold page edges and a curling bookmark tail", "ground", [120, 85, 60]),
    "enc-kiri-archive-3": ("a floating black ink drop creature with brush-stroke tendrils, a single white eye and splatter trail", "float", [35, 35, 50]),
    "enc-kiri-archive-4": ("a bookshelf guardian made of a tall wooden shelf with books, carved wooden arms holding a quill spear", "tall", [110, 80, 55]),
    "enc-kiri-archive-5": ("a fog-winged owl-like spirit with misty feathers fading at the edges and pale teal glowing eyes", "winged", [170, 190, 190]),
    # 霜原・戦跡の施設
    "enc-shimohara-facility-0": ("a frost-covered distortion shaped like a crouching beast of ice shards and dark violet cracks", "ground", [170, 200, 225]),
    "enc-shimohara-facility-1": ("a shadow of an ice soldier wearing a cracked frozen helmet and long coat, holding an icicle rifle", "tall", [120, 140, 165]),
    "enc-shimohara-facility-2": ("a frozen old machine on two legs with frost on its pipes, a round glass eye and steam vents", "tall", [140, 155, 170]),
    "enc-shimohara-facility-3": ("a creature made of tall frost column crystals growing from frozen soil, with a cold blue core", "big", [190, 220, 240]),
    "enc-shimohara-facility-4": ("a long centipede-like insect crawling along cold metal pipes, frosty grey segments and blue joint lights", "long", [130, 150, 160]),
    "enc-shimohara-facility-5": ("a pale shadow of a bird with white frost feathers and smoky dark edges, piercing pale eyes", "winged", [205, 215, 225]),
    # 浮嶼・基地
    "enc-fushima-base-0": ("a cloud shadow creature, a dark storm cloud body with small lightning eyes and wispy arms", "float", [120, 125, 150]),
    "enc-fushima-base-1": ("a tangle of old electrical wires and cables forming a twisted creature with sparking ends", "big", [90, 90, 100]),
    "enc-fushima-base-2": ("a floating surveillance eye machine, a brass ring frame with a large glass lens and small propellers", "float", [170, 140, 80]),
    "enc-fushima-base-3": ("a floating stone with a small tree growing on top and hanging roots, two glowing slits in the rock", "float", [120, 115, 105]),
    "enc-fushima-base-4": ("a small fluffy cloud insect with translucent wings and a cotton-like body, tiny antenna lights", "winged", [215, 220, 235]),
    "enc-fushima-base-5": ("a sentry soldier in pale blue armor with a long spyglass helmet visor and a halberd", "tall", [110, 125, 160]),
    # 深部1層（大乱期の戦場）
    "enc-deep-1-0": ("a ghostly echo of an ancient war, a tattered banner wrapped around a faint armored figure, faceless", "tall", [150, 160, 180]),
    "enc-deep-1-1": ("the memory of an ice soldier, a translucent icy figure with a broken lance, cracks of blue light", "tall", [160, 195, 220]),
    "enc-deep-1-2": ("a shadow creature formed around a broken sword stuck in its back, dark smoke body, rusty blade edges", "ground", [70, 70, 80]),
    "enc-deep-1-3": ("a fragment of a rusty round shield that floats and spins, with a rust-red eye in the boss and chipped edges", "float", [140, 90, 60]),
    "enc-deep-1-4": ("an old battlefield beetle with a helmet-like shell and arrowheads stuck in its back, dark bronze color", "ground", [110, 95, 70]),
    "enc-deep-1-5": ("a floating frozen tear drop of ice with a sad face reflection inside and a frosty halo", "float", [185, 215, 235]),
    # 深部2層（静まりの議場）
    "enc-deep-2-0": ("an echo of silence, a hollow hooded figure with a covered mouth, grey robes fading into dust", "tall", [140, 135, 130]),
    "enc-deep-2-1": ("a shadow of an assembly hall, a creature made of stacked carved chairs and a podium with a dark face", "big", [100, 75, 55]),
    "enc-deep-2-2": ("a floating blank nameplate with smeared golden letters, ribbons and a blurred face, ghostly", "float", [200, 180, 120]),
    "enc-deep-2-3": ("a heavy stone seal creature, a carved square seal stamp walking on short legs, red ink on its base", "ground", [150, 140, 125]),
    "enc-deep-2-4": ("a scribe insect with quill-like antennae, a parchment-colored body and ink-dipped legs", "ground", [190, 170, 130]),
    "enc-deep-2-5": ("a floating golden liquid droplet creature with a metallic sheen, coins orbiting it", "float", [220, 180, 70]),
    # 深部3層（歪みのたまり場）
    "enc-deep-3-0": ("a fragment of distortion, jagged floating shards of purple glass orbiting a dark core with an eye", "float", [140, 80, 170]),
    "enc-deep-3-1": ("a lingering scent of dried water, a thin wispy ghost of steam above a cracked bowl", "float", [180, 175, 160]),
    "enc-deep-3-2": ("a fragment of a stone guardian, a broken stone arm and half a helmet held together by violet light", "big", [130, 125, 130]),
    "enc-deep-3-3": ("a cluster of violet crystals that walks on crystal legs, light refracting inside", "ground", [160, 100, 190]),
    "enc-deep-3-4": ("a thirsty dark droplet creature with a cracked dry shell and a wide gaping mouth", "float", [100, 60, 80]),
    "enc-deep-3-5": ("a twisted wing creature, a single huge bent wing with eyes on its feathers, purple and black", "winged", [110, 70, 130]),
    # 深部4層（初源）
    "enc-deep-4-0": ("a primordial droplet, a luminous pearl-like drop with swirling starlight inside and a soft halo", "float", [200, 195, 230]),
    "enc-deep-4-1": ("a nameless shadow, a tall featureless silhouette with blank white gaps where a face should be", "tall", [50, 45, 70]),
    "enc-deep-4-2": ("an echo of sorrow, a floating veiled figure with tear-like light streaks and drooping sleeves", "float", [150, 150, 190]),
    "enc-deep-4-3": ("an ancient origin stone, a smooth egg-shaped monolith with glowing spiral carvings and small floating pebbles", "big", [120, 115, 140]),
    "enc-deep-4-4": ("a dawn-colored feathered creature with pale gold and rose wings, a small glowing crest", "winged", [230, 190, 160]),
    "enc-deep-4-5": ("an insect of forgetting, a moth with grey wings that fade into transparency and a blank white face", "winged", [175, 175, 180]),
    # 芯環塔1層（光と根）
    "enc-tower-1-0": ("a floating light crystal with prism facets and a beam-like eye in the center", "float", [190, 225, 245]),
    "enc-tower-1-1": ("a living stone creature with moss joints, a rounded rock body and leafy sprouts on its head", "big", [125, 130, 115]),
    "enc-tower-1-2": ("the master of a blue ore vein, a beast whose back is covered in blue crystal ore spikes, heavy jaw", "ground", [80, 120, 170]),
    "enc-tower-1-3": ("a tower gear machine, a walking clockwork body of brass gears with a lantern head", "tall", [170, 140, 80]),
    "enc-tower-1-4": ("a tiny insect of light with glowing transparent wings and a bright tail like a firefly", "winged", [230, 230, 170]),
    "enc-tower-1-5": ("a root guardian, a humanoid made of thick tree roots holding a wooden shield, glowing green eyes", "tall", [110, 90, 60]),
    # 芯環塔2層（雲の道）
    "enc-tower-2-0": ("a cloud-road crystal, a pale blue crystal with clouds trapped inside, floating with small wings of mist", "float", [175, 200, 230]),
    "enc-tower-2-1": ("misty footprints come alive, a low creature of fog with heavy foot shapes and a lantern eye", "ground", [185, 195, 205]),
    "enc-tower-2-2": ("a stone wrapped in swirling wind ribbons, a round boulder with carved wind symbols and one eye", "float", [140, 150, 160]),
    "enc-tower-2-3": ("a cloud gear machine, white porcelain gears and cloud puffs coming from its vents, on spindly legs", "tall", [210, 215, 220]),
    "enc-tower-2-4": ("a fog soldier with a hazy body, a misty spear and a visor of condensed water", "tall", [160, 175, 190]),
    "enc-tower-2-5": ("a crackling thunder droplet, a floating drop of yellow electricity with sparking spikes", "float", [230, 220, 100]),
    # 芯環塔3層（金と紋様）
    "enc-tower-3-0": ("a fragment of a golden ring floating with engraved runes and a light seam", "float", [210, 180, 90]),
    "enc-tower-3-1": ("a shadow made of intricate engraved patterns, a dark lace-like figure with glowing gold lines", "tall", [70, 60, 50]),
    "enc-tower-3-2": ("a guardian of light in white and gold armor with a halo-shaped helmet crest and a radiant sword", "tall", [225, 215, 180]),
    "enc-tower-3-3": ("a golden gear machine, a round gold clockwork creature with many gear legs and a ruby eye", "ground", [210, 170, 70]),
    "enc-tower-3-4": ("a heraldic crest stone, a shield-shaped stone slab with a carved emblem that walks on stone feet", "big", [170, 160, 140]),
    "enc-tower-3-5": ("a feather of light, a large glowing white-gold feather with a living eye at its base", "winged", [240, 225, 180]),
    # 環奥1層（境目）
    "enc-kanou-1-0": ("a wavering boundary creature, a rippling silhouette that looks half transparent and half solid, blue-violet", "float", [130, 120, 180]),
    "enc-kanou-1-1": ("a wandering light, a small orb of pale light with a long flickering tail and two dot eyes", "float", [210, 210, 240]),
    "enc-kanou-1-2": ("a drifting shadow like a jellyfish of darkness with long flowing tendrils", "float", [70, 65, 100]),
    "enc-kanou-1-3": ("a boundary insect with a body split down the middle in two different colors, violet and grey", "ground", [120, 105, 140]),
    "enc-kanou-1-4": ("a lost wing creature, a pair of wings without a body that flap with a dim eye between them", "winged", [150, 140, 190]),
    "enc-kanou-1-5": ("a boundary marker stone, a tall carved milestone with faded signs and an eye-shaped hole", "tall", [125, 120, 135]),
    # 環奥2層（静かな森）
    "enc-kanou-2-0": ("a quiet shadow, a soft round dark figure sitting with folded hands, faint green eyes", "big", [60, 75, 70]),
    "enc-kanou-2-1": ("the presence of someone waiting, a faint figure holding an umbrella of leaves, mostly transparent", "tall", [150, 175, 160]),
    "enc-kanou-2-2": ("a green light spirit, a glowing green flame-like wisp with leaf-shaped flickers", "float", [120, 210, 140]),
    "enc-kanou-2-3": ("a moss stone, a round stone completely covered in thick moss and small mushrooms, with a sleepy eye", "big", [95, 130, 85]),
    "enc-kanou-2-4": ("a forest dew droplet creature with a leaf hat and a stem tail, translucent green", "float", [140, 200, 150]),
    "enc-kanou-2-5": ("a leaf-winged insect with wings exactly like green leaves with veins, a twig body", "winged", [110, 160, 90]),
    # 環奥3層（裂け目）
    "enc-kanou-3-0": ("a flower growing from a rift, a large pink flower with a dark crack-shaped center full of teeth, on a vine body", "tall", [220, 130, 180]),
    "enc-kanou-3-1": ("overlapping scenery creature, a body made of mismatched picture fragments of landscapes stitched together", "big", [150, 140, 160]),
    "enc-kanou-3-2": ("a thin boundary, a paper-thin flat creature like a sheet of glass with a reflected face", "tall", [190, 190, 210]),
    "enc-kanou-3-3": ("a rift insect with a cracked shell leaking pink light and long antennae", "ground", [150, 90, 130]),
    "enc-kanou-3-4": ("a mirror crystal creature, sharp mirror shards forming a spiky body reflecting colors", "float", [200, 205, 220]),
    "enc-kanou-3-5": ("a flower droplet creature, a floating drop of nectar with petals around it and a tiny pollen crown", "float", [240, 170, 200]),
    # 環奥4層（全環）
    "enc-kanou-4-0": ("a fragment of the great ring, a curved white stone arc piece floating with gold inlay and an eye", "float", [225, 220, 210]),
    "enc-kanou-4-1": ("a white wavering figure like a heat haze of white light with a faint human outline", "float", [235, 235, 240]),
    "enc-kanou-4-2": ("an echo of the ring, concentric floating white rings around a hollow center that hums", "float", [210, 210, 225]),
    "enc-kanou-4-3": ("a creature of white feathers, a bird made only of layered white wings with no visible face", "winged", [240, 240, 245]),
    "enc-kanou-4-4": ("a ring crystal, a white crystal grown in the shape of a ring with prism light inside", "float", [220, 225, 240]),
    "enc-kanou-4-5": ("the last droplet, a dark droplet with a white ring around it, looking calm and heavy", "float", [90, 85, 110]),
    # 浮島1（月の庭）
    "enc-islet-1-1-0": ("an echo of moonlight, a pale silver ghost of a dancer with flowing sleeves", "tall", [190, 195, 220]),
    "enc-islet-1-1-1": ("the shadow of a garden stone statue, a weathered stone lion-dog figure with dark glowing cracks", "ground", [130, 130, 125]),
    "enc-islet-1-1-2": ("a moss-covered broken fragment of a garden lantern, stone pieces held by vines, a dim candle inside", "big", [110, 125, 100]),
    "enc-islet-1-1-3": ("a moon droplet, a floating silvery drop with a crescent moon reflected inside and star sparkles", "float", [200, 205, 235]),
    "enc-islet-1-1-4": ("a night moth with deep blue wings dotted with star-like spots and furry antennae", "winged", [60, 70, 130]),
    "enc-islet-1-1-5": ("a garden guardian, a figure made of trimmed hedge and garden stones holding a rake like a spear", "tall", [80, 120, 80]),
    # 浮島2（熱）
    "enc-islet-2-1-0": ("a heat shadow, a wavering dark shape with orange glowing edges like a mirage", "float", [120, 60, 40]),
    "enc-islet-2-1-1": ("a melting stone creature, a half-molten rock dripping orange lava with a cooling black crust", "big", [150, 80, 50]),
    "enc-islet-2-1-2": ("a spark insect, a small beetle with a glowing ember abdomen and sparks trailing from it", "ground", [200, 110, 50]),
    "enc-islet-2-1-3": ("a flame-feathered bird with burning orange feathers and a smoky tail", "winged", [230, 120, 50]),
    "enc-islet-2-1-4": ("an iron furnace machine walking on thick legs, a chimney on its back and glowing grill teeth", "big", [100, 90, 85]),
    "enc-islet-2-1-5": ("a droplet of heat, a floating red-hot drop of molten metal with a shimmering aura", "float", [220, 90, 40]),
    # 浮島3（潮と灯台）
    "enc-islet-3-1-0": ("a sea breeze shadow, a salty wind spirit with seaweed streamers and a gull-shaped head", "float", [140, 170, 170]),
    "enc-islet-3-1-1": ("a fragment of a lighthouse, a broken white and red striped stone piece with a lit lens eye", "big", [200, 120, 100]),
    "enc-islet-3-1-2": ("an insect between the waves, a sea skater bug with oar-like legs and a shell of shells", "ground", [90, 140, 150]),
    "enc-islet-3-1-3": ("a tide droplet creature, a floating drop of seawater with a tiny crab living inside and foam", "float", [100, 170, 190]),
    "enc-islet-3-1-4": ("a lighthouse guardian, a tall keeper figure in a salt-stained coat with a lamp for a head", "tall", [170, 150, 110]),
    "enc-islet-3-1-5": ("a seabird with white and grey feathers, a long orange beak and fish-scale patterns on its wings", "winged", [210, 210, 205]),
    # 浮島4（砦）
    "enc-islet-4-1-0": ("a shadow of a war banner, a tattered purple flag on a pole that moves by itself with a face in the cloth", "tall", [120, 80, 140]),
    "enc-islet-4-1-1": ("a shadow of a fortress soldier with a tall pointed helmet, round shield and a dark smoky body", "tall", [80, 75, 95]),
    "enc-islet-4-1-2": ("a fragment of cloud with a cracked stone core, floating and dripping light rain", "float", [200, 200, 215]),
    "enc-islet-4-1-3": ("a fortress siege machine, a small wooden catapult creature with a stone mouth and wheels", "big", [130, 100, 70]),
    "enc-islet-4-1-4": ("an echo of an archer, a faded translucent bowman with a glowing bowstring and empty quiver", "tall", [160, 150, 190]),
    "enc-islet-4-1-5": ("a castle wall stone creature, a chunk of battlement with arrow slits as eyes, walking on brick legs", "big", [140, 130, 120]),
    # 浮島5（海の底）
    "enc-islet-5-1-0": ("a sunken shadow, a dark sea creature like a manta made of shadow with glowing blue spots", "float", [40, 60, 90]),
    "enc-islet-5-1-1": ("a coral stone creature, a rock covered in pink and orange coral branches with small fish hiding", "big", [210, 130, 120]),
    "enc-islet-5-1-2": ("a sea firefly bug, a small crustacean that glows bright blue, with feathery legs", "ground", [60, 140, 200]),
    "enc-islet-5-1-3": ("a deep sea droplet, a dark drop with a hanging lure light like an anglerfish and tiny teeth", "float", [30, 50, 80]),
    "enc-islet-5-1-4": ("a shell crystal creature, a spiral seashell made of mother-of-pearl crystal with an eye in the opening", "ground", [220, 210, 220]),
    "enc-islet-5-1-5": ("a bubble wing creature, a fish-like body with wings made of clustered bubbles", "winged", [150, 200, 220]),
    # 浮島6（溶岩）
    "enc-islet-6-1-0": ("a lava shadow, a crawling dark creature with cracks of flowing lava along its back", "ground", [80, 40, 30]),
    "enc-islet-6-1-1": ("a scorched stone creature, a charred black rock with smoking holes and ember eyes", "big", [60, 50, 45]),
    "enc-islet-6-1-2": ("an ember bat with wings of glowing coals and a smoking trail", "winged", [180, 80, 40]),
    "enc-islet-6-1-3": ("a volcanic smoke bird with dark grey smoke feathers and glowing ash specks", "winged", [90, 85, 85]),
    "enc-islet-6-1-4": ("a lava droplet creature, a floating drop of molten rock with a crust shell cracking open", "float", [210, 80, 30]),
    "enc-islet-6-1-5": ("an obsidian soldier, a tall warrior made of black volcanic glass with sharp shard armor", "tall", [40, 35, 45]),
    # 世界1（草原）
    "enc-world-1-0": ("a field grasshopper-like insect with leaf-green armor plates and long jumping legs", "ground", [110, 160, 80]),
    "enc-world-1-1": ("a roadside shadow, a hunched dark figure wearing a travel hat and holding a broken signpost", "tall", [80, 75, 70]),
    "enc-world-1-2": ("a field mouse shadow, a small dark mouse with a long tail of smoke and wheat stuck in its fur", "ground", [120, 100, 80]),
    "enc-world-1-3": ("a meadow dew droplet, a floating clear drop holding a tiny clover and a rainbow gleam", "float", [150, 200, 160]),
    "enc-world-1-4": ("a roadside stone creature, a milestone rock with a moss beard and wooden stick arms", "big", [140, 135, 120]),
    "enc-world-1-5": ("a little songbird with brown and cream feathers, a puffed chest and a sharp beak", "winged", [170, 130, 90]),
    # 世界2（峠と湖）
    "enc-world-2-0": ("a mountain pass shadow, a tall thin shadow with a walking staff and a cloak flapping in the wind", "tall", [90, 95, 110]),
    "enc-world-2-1": ("a lakeside bat with blue-grey fur, webbed wings and a fishing line tangled on it", "winged", [100, 120, 140]),
    "enc-world-2-2": ("a stone distortion, a rock that twists into a spiral shape with a violet glow inside", "big", [120, 110, 125]),
    "enc-world-2-3": ("a lake droplet, a floating drop of blue lake water with a small fish swimming inside", "float", [110, 160, 200]),
    "enc-world-2-4": ("a mountain pass insect, a sturdy beetle with a rocky shell and short strong legs", "ground", [120, 115, 100]),
    "enc-world-2-5": ("a rocky mountain soldier made of stacked grey stones wearing a rusty helmet, carrying a stone club", "tall", [130, 125, 115]),
    # 世界3（砂漠）
    "enc-world-3-0": ("a dune-slipping creature like a sand eel with a smooth sandy body leaping out of the dunes", "long", [210, 180, 120]),
    "enc-world-3-1": ("a hot wind shadow, a whirling dust devil with an orange glowing face inside", "float", [200, 140, 90]),
    "enc-world-3-2": ("a desert scorpion shadow with glassy sand-colored plates and a long curved tail made of glass", "ground", [190, 160, 110]),
    "enc-world-3-3": ("a sand dune stone creature, a sandstone rock eroded into a face, half buried in sand", "big", [200, 165, 115]),
    "enc-world-3-4": ("a mirage droplet, a floating shimmering drop that shows a fake oasis inside, wavering edges", "float", [170, 210, 220]),
    "enc-world-3-5": ("a desert vulture-like bird with sand-colored feathers, a bald head and long wings", "winged", [160, 125, 90]),
    # 世界4（雪原）
    "enc-world-4-0": ("a snowfield ice soldier shadow, a figure of packed snow and ice with a fur hat and an ice axe", "tall", [190, 205, 220]),
    "enc-world-4-1": ("a frost distortion on four legs, a wolf-like shape of frozen mist with violet ice teeth", "ground", [175, 195, 215]),
    "enc-world-4-2": ("a white shadow, a pale snow-covered blob-free figure like a tall snowdrift with dark eyes", "tall", [225, 230, 235]),
    "enc-world-4-3": ("a snowfield insect, a white furry caterpillar with icy blue spots and frost on its hairs", "long", [215, 225, 235]),
    "enc-world-4-4": ("an ice crystal creature, a large hexagonal snowflake crystal with a frozen face in the center", "float", [180, 215, 240]),
    "enc-world-4-5": ("a blizzard bird with feathers like flying snow, a pale blue body and an icy crest", "winged", [200, 220, 235]),
    # 世界5（火山）
    "enc-world-5-0": ("an ember shadow, a dark figure with glowing ember speckles all over and burning eyes", "tall", [90, 50, 40]),
    "enc-world-5-1": ("a lava distortion, a twisted lava rock creature with violet cracks mixed with orange magma", "big", [140, 60, 70]),
    "enc-world-5-2": ("an ash-covered shadow, a hunched creature buried in grey volcanic ash with red eyes peeking out", "big", [110, 105, 105]),
    "enc-world-5-3": ("an ash insect, a grey beetle with a soot-covered shell and glowing orange joints", "ground", [100, 95, 90]),
    "enc-world-5-4": ("a volcano stone creature, a dark basalt column rock with a magma mouth, on stubby legs", "big", [70, 60, 60]),
    "enc-world-5-5": ("a magma droplet, a heavy floating drop of glowing magma with a black cooled skin", "float", [200, 70, 30]),
    # 世界6（荒野）
    "enc-world-6-0": ("a wasteland shadow, a lean dog-like creature of dust and shadow with a cracked bone collar", "ground", [130, 110, 90]),
    "enc-world-6-1": ("a distortion whose light went out, an old broken street lamp creature with a dark empty glass head", "tall", [80, 85, 90]),
    "enc-world-6-2": ("an old machine insect, a rusty mechanical beetle with exposed gears and a dented lamp eye", "ground", [130, 100, 70]),
    "enc-world-6-3": ("a wasteland stone creature, a cracked red rock with dry thorny brush growing on it, one eye", "big", [160, 110, 80]),
    "enc-world-6-4": ("a rusted machine, a boxy rusty robot on tank treads with a broken antenna and a loose jaw", "big", [140, 90, 60]),
    "enc-world-6-5": ("a withered field bird, a scarecrow-like bird made of dry straw and torn cloth wings", "winged", [170, 150, 100]),
    # 海
    "enc-world-sea-0": ("a shadow between the waves, a dark eel-like creature with foam crests and glowing teal eyes", "long", [40, 80, 100]),
    "enc-world-sea-1": ("a tide stone creature, a barnacle-covered rock with a crab-claw arm and seaweed hair", "big", [100, 110, 100]),
    "enc-world-sea-2": ("a sea firefly bug swarm queen, a larger glowing insect with transparent shell and blue light trails", "winged", [70, 160, 210]),
    "enc-world-sea-3": ("a whirlpool droplet, a floating drop of seawater spinning into a spiral with a dark eye at its center", "float", [60, 120, 160]),
    "enc-world-sea-4": ("a sea feather creature, a flying fish with huge feather-like fins and silver scales", "winged", [170, 200, 210]),
    "enc-world-sea-5": ("an echo of a boat, a ghostly small wooden rowboat with a faint rower and a lantern", "big", [140, 150, 160]),
    "enc-world-sea-6": ("a sunken ship guardian, a figure made of ship planks and an anchor with a ship wheel shield", "tall", [100, 85, 70]),
    # 空
    "enc-world-air-0": ("a shadow with wind wings, a dark streamlined bird-like shadow with feathers made of wind lines", "winged", [90, 100, 130]),
    "enc-world-air-1": ("a fragment of cloud, a fluffy white cloud chunk with a grumpy face and small hailstones", "float", [225, 230, 240]),
    "enc-world-air-2": ("a thundercloud shadow, a dark heavy cloud creature with a lightning bolt tail and yellow eyes", "float", [80, 85, 110]),
    "enc-world-air-3": ("a sky droplet, a floating drop of pale sky blue with a cloud inside and a tiny sun reflection", "float", [160, 200, 240]),
    "enc-world-air-4": ("a lightning crystal, a jagged yellow crystal crackling with electricity, floating", "float", [230, 210, 90]),
    "enc-world-air-5": ("a cloud insect, a dragonfly with wings of mist and a long pale body", "long", [200, 210, 225]),
    "enc-world-air-6": ("a storm feather creature, a large bird with dark storm-grey feathers and lightning patterns", "winged", [100, 105, 125]),
}


def main():
    path = os.path.join(os.path.dirname(__file__), "monster-roster.json")
    r = json.load(open(path))
    n = 0
    for e in r:
        if e["id"] in P and not e.get("prompt"):
            p, shape, tone = P[e["id"]]
            e["prompt"], e["shape"], e["tone"] = p, shape, tone
            n += 1
    json.dump(r, open(path, "w"), ensure_ascii=False, indent=1)
    left = [e["id"] for e in r if e.get("kind") != "boss" and not e.get("prompt")]
    print("書いた:", n, "／ まだ空:", left)


if __name__ == "__main__":
    main()
