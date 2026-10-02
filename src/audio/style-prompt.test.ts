import { describe, expect, it } from "vitest";
import { parseBpm, parseKey, parseStylePrompt } from "./style-prompt";

describe("スタイル指定の読み取り", () => {
  it("マスタープロンプトの10ジャンルを、それぞれ正しい曲調・味つけにする", () => {
    const cases: [string, string, string[]][] = [
      ["melodic metal, twin guitars, galloping riffs", "metal", []],
      ["progressive metal, odd meter 7/8", "progmetal", []],
      ["old school hardcore punk with gang vocals and breakdown", "hardcore", []],
      ["technical death metal, blast beats, guttural growl", "deathmetal", []],
      ["loud metal, heavy low end, screamed and clean vocals", "metal", ["loud"]],
      ["ラウドロック、シャウトと歌の切り替え", "rock", ["loud"]],
      ["dance rock, four on the floor, synth bass", "dancerock", []],
      ["drift phonk, cowbell, distorted 808", "phonk", []],
      ["rock x orchestra, strings brass timpani", "rock", ["orchestra"]],
      ["ロック×和楽器、尺八と三味線", "rock", ["wagakki"]],
    ];
    for (const [text, style, flavors] of cases) {
      const c = parseStylePrompt(text);
      expect(c.style, text).toBe(style);
      expect(c.flavors, text).toEqual(flavors);
    }
  });

  it("デスメタルは「メタル」より先に判定する（デスメタルがメタルにならない）", () => {
    expect(parseStylePrompt("デスメタル").style).toBe("deathmetal");
    expect(parseStylePrompt("ラウドメタル").style).toBe("metal");
    expect(parseStylePrompt("ラウドメタル").flavors).toEqual(["loud"]);
  });

  it("飾りの言葉で、ほかの曲調に取られない", () => {
    expect(parseStylePrompt("soulful rock ballad with electronic drums").style).toBe("rock");
    expect(parseStylePrompt("metal with progressive build-up and electronic intro").style).toBe("metal");
    expect(parseStylePrompt("EDM festival banger, big drop").style).toBe("electro");
    expect(parseStylePrompt("deep soul and funk groove").style).toBe("rnb");
  });

  it("オーケストラだけのときは劇伴、味つけだけでジャンルがないときはロックを土台にする", () => {
    expect(parseStylePrompt("full orchestra, cinematic").style).toBe("epic");
    expect(parseStylePrompt("和楽器").style).toBe("rock");
    expect(parseStylePrompt("和楽器").flavors).toEqual(["wagakki"]);
  });

  it("テンポと調を文章から読む。なければ曲調の標準値を使う", () => {
    expect(parseBpm("fast 172 BPM")).toBe(172);
    expect(parseBpm("BPM: 95")).toBe(95);
    expect(parseBpm("テンポ140で")).toBe(140);
    expect(parseBpm("no tempo here")).toBeNull();
    expect(parseKey("in F# minor")).toEqual({ tonic: "F#", minor: true });
    expect(parseKey("Bb major")).toEqual({ tonic: "Bb", minor: false });
    expect(parseKey("Em")).toEqual({ tonic: "E", minor: true });
    expect(parseKey("ホ短調")).toBeNull();
    const c = parseStylePrompt("melodic metal 150 BPM E minor");
    expect([c.bpm, c.tonic, c.minor]).toEqual([150, "E", true]);
    const d = parseStylePrompt("phonk");
    expect([d.bpm, d.tonic, d.minor]).toEqual([140, "F", true]);
  });

  it("設計図（songs.json）のテンポ・調・拍子は文章より優先する", () => {
    const c = parseStylePrompt("metal 150 BPM E minor", { bpm: 175, keyScale: "A minor", timeSignature: "4" });
    expect([c.bpm, c.tonic, c.minor, c.beats]).toEqual([175, "A", true, 4]);
  });

  it("プログレは7拍子。ラウド以外の味つけは4拍子だけなので注意を出す", () => {
    const c = parseStylePrompt("progressive metal with orchestra");
    expect(c.beats).toBe(7);
    expect(c.warnings.length).toBe(1);
    expect(parseStylePrompt("progressive loud metal").warnings).toEqual([]);
  });
});
