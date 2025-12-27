export type CoffeeType = 'Grain' | 'Moulu';
export type BeverageType = 'Ristretto' | 'Expresso' | 'Café long';

export interface CoffeeLot {
  id: string;
  roaster: string;
  name: string;
  type: CoffeeType;
  pricePerKg: number;
  costPerShot: number;
  water: string;
  status: 'Approuvé' | 'À affiner' | 'À éviter' | 'En observation';
}

export interface ShotNote {
  id: string;
  coffee: string;
  beverage: BeverageType;
  dose: number;
  yield: number;
  time: number;
  water: string;
  date: string;
}

export interface TastingVerdict {
  coffee: string;
  verdict: 'Racheter' | 'À affiner' | 'À éviter' | 'En observation';
  highlights: string[];
}

export interface LeaderboardItem {
  coffee: string;
  position: number;
  beverage: 'Ristretto' | 'Expresso' | 'Global';
  tag: string;
}

export interface LeaderboardSlice {
  id: string;
  label: string;
  description: string;
  entries: LeaderboardItem[];
}

export interface JustifiedVerdict extends TastingVerdict {
  beverage: BeverageType;
  justification: string;
  trace: string;
  sensoryWords: string[];
  water: string;
}

export interface AnalysisSignal {
  endpoint: string;
  label: string;
  words: string[];
  verdictWord: string;
  trace: string;
  focus: string;
}

export interface SensoryVocabulary {
  aromas: string[];
  mouthfeels: string[];
  finishes: string[];
  verdicts: TastingVerdict['verdict'][];
}
