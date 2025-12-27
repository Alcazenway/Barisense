export type CoffeeType = 'Grain' | 'Moulu';

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
  beverage: 'Ristretto' | 'Expresso' | 'Café long';
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
