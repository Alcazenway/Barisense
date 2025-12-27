import { type CoffeeLot, type LeaderboardItem, type ShotNote, type TastingVerdict } from '../types';

export const coffees: CoffeeLot[] = [
  {
    id: 'lot-berlin',
    roaster: 'Five Elephant',
    name: 'Ethiopia Dimtu',
    type: 'Grain',
    pricePerKg: 58,
    costPerShot: 0.72,
    water: 'Volvic',
    status: 'Approuvé',
  },
  {
    id: 'lot-rio',
    roaster: 'Terroir',
    name: 'Serra do Cabral',
    type: 'Grain',
    pricePerKg: 42,
    costPerShot: 0.54,
    water: 'Cristalline',
    status: 'À affiner',
  },
  {
    id: 'lot-montreal',
    roaster: 'Structure Coffee',
    name: 'La Esperanza',
    type: 'Moulu',
    pricePerKg: 32,
    costPerShot: 0.43,
    water: 'Robinet filtrée',
    status: 'En observation',
  },
];

export const shots: ShotNote[] = [
  {
    id: 'shot-148',
    coffee: 'Ethiopia Dimtu',
    beverage: 'Ristretto',
    dose: 18,
    yield: 36,
    time: 28,
    water: 'Volvic',
    date: '2024-12-02',
  },
  {
    id: 'shot-149',
    coffee: 'Serra do Cabral',
    beverage: 'Expresso',
    dose: 18.5,
    yield: 40,
    time: 30,
    water: 'Cristalline',
    date: '2024-12-03',
  },
  {
    id: 'shot-150',
    coffee: 'La Esperanza',
    beverage: 'Expresso',
    dose: 19,
    yield: 42,
    time: 31,
    water: 'Robinet filtrée',
    date: '2024-12-04',
  },
];

export const leaderboard: LeaderboardItem[] = [
  { coffee: 'Ethiopia Dimtu', beverage: 'Global', position: 1, tag: 'Stabilité + floral' },
  { coffee: 'Serra do Cabral', beverage: 'Expresso', position: 2, tag: 'Noisette + chocolat' },
  { coffee: 'La Esperanza', beverage: 'Ristretto', position: 3, tag: 'Acidité vive' },
];

export const tastingVerdicts: TastingVerdict[] = [
  {
    coffee: 'Ethiopia Dimtu',
    verdict: 'Racheter',
    highlights: ['Pêche blanche', 'Jasmin', 'Texture soyeuse'],
  },
  {
    coffee: 'Serra do Cabral',
    verdict: 'À affiner',
    highlights: ['Privilégier eau minérale', 'Mouture légèrement plus fine'],
  },
  {
    coffee: 'La Esperanza',
    verdict: 'En observation',
    highlights: ['Stabiliser le ratio 1:2', 'Réduire le temps à 29s'],
  },
];
