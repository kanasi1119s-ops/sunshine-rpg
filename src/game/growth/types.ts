export interface GrowthProfile {
  hpGrowth: number;
  mpGrowth: number;
  attackGrowth: number;
  defenseGrowth: number;
  speedGrowth: number;
}

export interface LeveledStats {
  level: number;
  exp: number;
  maxHp: number;
  hp: number;
  maxMp: number;
  mp: number;
  attack: number;
  defense: number;
  speed: number;
}
