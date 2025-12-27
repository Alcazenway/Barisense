import {
  type AnalysisSignal,
  type CoffeeLot,
  type JustifiedVerdict,
  type LeaderboardItem,
  type LeaderboardSlice,
  type SensoryVocabulary,
  type ShotNote,
} from '../types';

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

export const waterOptions = ['Volvic', 'Cristalline', 'Robinet filtrée', 'Osmosée légère'];

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

export const leaderboardSlices: LeaderboardSlice[] = [
  {
    id: 'global',
    label: 'Global',
    description: 'Favoris toutes boissons',
    entries: [
      { coffee: 'Ethiopia Dimtu', beverage: 'Global', position: 1, tag: 'Floral stable' },
      { coffee: 'Serra do Cabral', beverage: 'Global', position: 2, tag: 'Noisette + régulier' },
      { coffee: 'La Esperanza', beverage: 'Global', position: 3, tag: 'Acidité vive' },
    ],
  },
  {
    id: 'ristretto',
    label: 'Ristretto',
    description: 'Concentré et sirop',
    entries: [
      { coffee: 'Ethiopia Dimtu', beverage: 'Ristretto', position: 1, tag: 'Longueur florale' },
      { coffee: 'La Esperanza', beverage: 'Ristretto', position: 2, tag: 'Épicé mais soyeux' },
      { coffee: 'Serra do Cabral', beverage: 'Ristretto', position: 3, tag: 'Praliné stable' },
    ],
  },
  {
    id: 'expresso',
    label: 'Expresso',
    description: 'Réglage droit',
    entries: [
      { coffee: 'Serra do Cabral', beverage: 'Expresso', position: 1, tag: 'Chocolat rond' },
      { coffee: 'Ethiopia Dimtu', beverage: 'Expresso', position: 2, tag: 'Pêche jasmin' },
      { coffee: 'La Esperanza', beverage: 'Expresso', position: 3, tag: 'Croquant fruité' },
    ],
  },
  {
    id: 'qp',
    label: 'Qualité / Prix',
    description: 'Impact vs coût par shot',
    entries: [
      { coffee: 'Serra do Cabral', beverage: 'Expresso', position: 1, tag: 'Rond + abordable' },
      { coffee: 'La Esperanza', beverage: 'Global', position: 2, tag: 'Acidulé efficace' },
      { coffee: 'Ethiopia Dimtu', beverage: 'Global', position: 3, tag: 'Floral premium' },
    ],
  },
  {
    id: 'stabilite',
    label: 'Stabilité',
    description: 'Régularité extraction/eau',
    entries: [
      { coffee: 'Ethiopia Dimtu', beverage: 'Global', position: 1, tag: 'Eau Volvic = constant' },
      { coffee: 'Serra do Cabral', beverage: 'Expresso', position: 2, tag: 'Cristalline OK' },
      { coffee: 'La Esperanza', beverage: 'Expresso', position: 3, tag: 'Robinet filtrée à surveiller' },
    ],
  },
  {
    id: 'retest',
    label: 'À retester',
    description: 'File d’attente sensorielle',
    entries: [
      { coffee: 'La Esperanza', beverage: 'Expresso', position: 1, tag: 'Adapter eau + grind' },
      { coffee: 'Serra do Cabral', beverage: 'Global', position: 2, tag: 'Tester eau Volvic' },
      { coffee: 'Ethiopia Dimtu', beverage: 'Ristretto', position: 3, tag: 'Confirmer longueur' },
    ],
  },
];

export const tastingVerdicts: LeaderboardItem[] = [];

export const justifiedVerdicts: JustifiedVerdict[] = [
  {
    coffee: 'Ethiopia Dimtu',
    verdict: 'Racheter',
    beverage: 'Expresso',
    highlights: ['Pêche blanche', 'Jasmin', 'Texture soyeuse'],
    justification: 'Profil floral stable confirmé par trois dégustations successives avec eau Volvic.',
    trace: 'Dégustation récente • shot Dimtu • Eau : Volvic',
    sensoryWords: ['floral', 'satiné', 'longueur'],
    water: 'Volvic',
  },
  {
    coffee: 'Serra do Cabral',
    verdict: 'À affiner',
    beverage: 'Ristretto',
    highlights: ['Privilégier eau minérale', 'Mouture légèrement plus fine'],
    justification: 'Mouture légèrement serrée avec Cristalline, noisette dominante à lisser.',
    trace: 'Dégustation début décembre • shot Cabral • Eau : Cristalline',
    sensoryWords: ['noisette', 'crémeux', 'rond'],
    water: 'Cristalline',
  },
  {
    coffee: 'La Esperanza',
    verdict: 'En observation',
    beverage: 'Café long',
    highlights: ['Stabiliser un ratio équilibré', 'Réduire légèrement le temps'],
    justification: 'Acidité vive agréable mais longueur sèche, revoir eau filtrée ou temps.',
    trace: 'Dégustation début décembre • shot Esperanza • Eau : Robinet filtrée',
    sensoryWords: ['acidulé', 'croquant', 'sec'],
    water: 'Robinet filtrée',
  },
];

export const analysisSignals: AnalysisSignal[] = [
  {
    endpoint: '/api/analyse/sensoriel',
    label: 'Analyse sensorielle',
    words: ['floral', 'velouté', 'longueur'],
    verdictWord: 'Harmonieux',
    trace: 'Synthèse croisée de trois dégustations',
    focus: 'Arômes et texture uniquement en mots',
  },
  {
    endpoint: '/api/analyse/verdict',
    label: 'Décision café',
    words: ['racheter', 'affiner', 'observer'],
    verdictWord: 'Traçable',
    trace: 'Historique shots + eau utilisée',
    focus: 'Verdict exprimé sans notation numérique',
  },
  {
    endpoint: '/api/analyse/stabilite',
    label: 'Stabilité extraction',
    words: ['régulier', 'prévisible', 'fluide'],
    verdictWord: 'Stable',
    trace: 'Comparaison des derniers shots',
    focus: 'Mise à jour continue des mots-clés',
  },
];

export const sensoryVocabulary: SensoryVocabulary = {
  aromas: ['pêche blanche', 'jasmin', 'miel', 'praliné', 'épices douces', 'noisette', 'fruit jaune'],
  mouthfeels: ['rond', 'satiné', 'velouté', 'croquant', 'juteux', 'crémeux', 'sirupeux'],
  finishes: ['longueur', 'net', 'sec', 'harmonieux', 'douceur', 'persistant'],
  verdicts: ['Racheter', 'À affiner', 'À éviter', 'En observation'],
};
