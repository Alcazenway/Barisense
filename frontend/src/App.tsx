import { useEffect, useMemo, useState } from 'react';
import { FormField } from './components/FormField';
import { Navigation } from './components/Navigation';
import { Pill } from './components/Pill';
import { SectionCard } from './components/SectionCard';
import {
  analysisSignals,
  coffees,
  justifiedVerdicts,
  leaderboardSlices,
  sensoryVocabulary,
  shots,
  waterOptions,
} from './data/sampleData';
import type { AnalysisSignal, BeverageType, CoffeeType } from './types';
import './App.css';

interface DraftState {
  coffeeStatus?: string;
  shotStatus?: string;
  tastingStatus?: string;
}

interface CoffeeFormState {
  roaster: string;
  name: string;
  type: CoffeeType | '';
  weight: string;
  price: string;
  purchaseDate: string;
  water: string;
}

interface ShotFormState {
  coffee: string;
  beverage: BeverageType | '';
  grind: string;
  dose: string;
  yield: string;
  time: string;
  water: string;
  sensoryWords: string;
}

interface TastingFormState {
  coffee: string;
  aromas: string;
  mouthfeel: string;
  finish: string;
  verdict: string;
  comment: string;
  water: string;
}

const beverageOptions: BeverageType[] = ['Ristretto', 'Expresso', 'Café long'];
const coffeeTypes: CoffeeType[] = ['Grain', 'Moulu'];

function formatCurrency(value: number) {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 2,
  }).format(value);
}

function positionToWord(position: number) {
  if (position === 1) return 'Premier';
  if (position === 2) return 'Deuxième';
  if (position === 3) return 'Troisième';
  return `Top ${position}`;
}

function uniqueWords(list: string[]) {
  return Array.from(new Set(list));
}

export default function App() {
  const [draftState, setDraftState] = useState<DraftState>({});
  const [analysisFeed, setAnalysisFeed] = useState<AnalysisSignal[]>([]);
  const [activeLeaderboard, setActiveLeaderboard] = useState(leaderboardSlices[0]?.id ?? 'global');

  const latestShot = shots[shots.length - 1];

  const [coffeeForm, setCoffeeForm] = useState<CoffeeFormState>({
    roaster: '',
    name: '',
    type: '',
    weight: '',
    price: '',
    purchaseDate: '',
    water: waterOptions[0],
  });
  const [shotForm, setShotForm] = useState<ShotFormState>({
    coffee: latestShot?.coffee ?? '',
    beverage: latestShot?.beverage ?? '',
    grind: '',
    dose: latestShot?.dose?.toString() ?? '',
    yield: latestShot?.yield?.toString() ?? '',
    time: latestShot?.time?.toString() ?? '',
    water: latestShot?.water ?? waterOptions[0],
    sensoryWords: '',
  });
  const [tastingForm, setTastingForm] = useState<TastingFormState>({
    coffee: '',
    aromas: '',
    mouthfeel: '',
    finish: '',
    verdict: '',
    comment: '',
    water: waterOptions[0],
  });

  const [coffeeErrors, setCoffeeErrors] = useState<Record<string, string>>({});
  const [shotErrors, setShotErrors] = useState<Record<string, string>>({});
  const [tastingErrors, setTastingErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnalysisFeed(analysisSignals);
    }, 220);
    return () => clearTimeout(timer);
  }, []);

  const roasterSuggestions = useMemo(
    () => uniqueWords(coffees.map((coffee) => coffee.roaster)),
    [],
  );

  const coffeeNames = useMemo(
    () => uniqueWords(coffees.map((coffee) => coffee.name)),
    [],
  );

  const sensoryWords = useMemo(
    () => uniqueWords([
      ...sensoryVocabulary.aromas,
      ...sensoryVocabulary.mouthfeels,
      ...sensoryVocabulary.finishes,
    ]),
    [],
  );

  const waterDiversity = useMemo(
    () => new Set(coffees.map((coffee) => coffee.water)).size,
    [],
  );

  const navigationItems = useMemo(
    () => [
      {
        id: 'referentiel-cafe',
        title: 'Référentiel Café',
        description: 'Lots, prix et eau par défaut',
        eyebrow: 'Collecte',
        badge: <Pill tone="info">{coffees.length} cafés</Pill>,
      },
      {
        id: 'journal-extraction',
        title: 'Journal d’extraction',
        description: 'Paramètres et ratio de vos shots',
        eyebrow: 'Production',
        badge: <Pill tone="info">{shots.length} notes</Pill>,
      },
      {
        id: 'degustation-verdict',
        title: 'Dégustation & verdict',
        description: 'Retours sensoriels et décisions',
        eyebrow: 'Sensoriel',
        badge: <Pill tone="info">{justifiedVerdicts.length} verdicts</Pill>,
      },
      {
        id: 'classements',
        title: 'Classements',
        description: 'Synthèse rapide par boisson',
        eyebrow: 'Synthèse',
        badge: <Pill tone="info">{leaderboardSlices.length} vues</Pill>,
      },
    ],
    [],
  );

  const setFormStatus = (key: keyof DraftState) => {
    const timestamp = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    setDraftState((previous) => ({
      ...previous,
      [key]: `Brouillon prêt • ${timestamp}`,
    }));
  };

  const handleCoffeeSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const errors: Record<string, string> = {};
    if (!coffeeForm.roaster.trim()) errors.roaster = 'Indique un torréfacteur';
    if (!coffeeForm.name.trim()) errors.name = 'Référence obligatoire';
    if (!coffeeForm.type) errors.type = 'Choisir un type';
    if (!coffeeForm.water) errors.water = 'Choisir une eau';
    if (coffeeForm.weight && Number(coffeeForm.weight) <= 0) errors.weight = 'Poids positif requis';
    if (coffeeForm.price && Number(coffeeForm.price) <= 0) errors.price = 'Prix positif requis';

    setCoffeeErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setFormStatus('coffeeStatus');
  };

  const handleShotSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const errors: Record<string, string> = {};
    if (!shotForm.coffee) errors.coffee = 'Sélectionner un café';
    if (!shotForm.beverage) errors.beverage = 'Choisir un format';
    if (!shotForm.water) errors.water = 'Sélectionner une eau';

    (['dose', 'yield', 'time'] as Array<keyof ShotFormState>).forEach((field) => {
      const value = Number(shotForm[field]);
      if (!shotForm[field] || Number.isNaN(value) || value <= 0) {
        errors[field] = 'Renseigne une valeur positive';
      }
    });

    setShotErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setFormStatus('shotStatus');
  };

  const handleTastingSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const errors: Record<string, string> = {};
    if (!tastingForm.coffee) errors.coffee = 'Sélectionne le café dégusté';
    if (!tastingForm.aromas.trim()) errors.aromas = 'Décris les arômes en mots';
    if (!tastingForm.mouthfeel.trim()) errors.mouthfeel = 'Décris la texture';
    if (!tastingForm.finish.trim()) errors.finish = 'Ajoute la finale';
    if (!tastingForm.verdict) errors.verdict = 'Choisis un verdict en mots';
    if (!tastingForm.water) errors.water = 'Associe l’eau utilisée';

    setTastingErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setFormStatus('tastingStatus');
  };

  const updateCoffeeField = (field: keyof CoffeeFormState) => (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setCoffeeForm((previous) => ({ ...previous, [field]: event.target.value }));
  };

  const updateShotField = (field: keyof ShotFormState) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const value = event.target.value;
    if (field === 'coffee') {
      const selectedCoffee = coffees.find((coffee) => coffee.name === value);
      setShotForm((previous) => ({
        ...previous,
        coffee: value,
        water: selectedCoffee?.water ?? previous.water,
      }));
      setTastingForm((previous) => ({ ...previous, coffee: value, water: selectedCoffee?.water ?? previous.water }));
      return;
    }

    setShotForm((previous) => ({ ...previous, [field]: value }));
  };

  const updateTastingField = (field: keyof TastingFormState) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>,
  ) => {
    const value = event.target.value;
    if (field === 'coffee') {
      const selectedCoffee = coffees.find((coffee) => coffee.name === value);
      setTastingForm((previous) => ({ ...previous, coffee: value, water: selectedCoffee?.water ?? previous.water }));
      return;
    }

    setTastingForm((previous) => ({ ...previous, [field]: value }));
  };

  const activeLeaderboardSlice = leaderboardSlices.find((slice) => slice.id === activeLeaderboard) ?? leaderboardSlices[0];

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Barisense • Pilote barista</p>
          <h1>Collecte, dégustation et verdicts</h1>
          <p className="lede">
            Un hub mobile-first pour tracer les cafés, suivre les réglages, comparer les eaux et rendre les verdicts
            uniquement en mots.
          </p>
          <div className="hero__pills">
            <Pill tone="success">{coffees.length} cafés suivis</Pill>
            <Pill tone="info">{shots.length} extractions notées</Pill>
            <Pill tone="warning">{waterDiversity} types d&apos;eau</Pill>
          </div>
        </div>
        <div className="hero__card">
          <p className="eyebrow">Prochain shot</p>
          <h3>{latestShot.coffee}</h3>
          <ul className="shot-meta">
            <li>
              <span>Boisson</span>
              <strong>{latestShot.beverage}</strong>
            </li>
            <li>
              <span>Ratio</span>
              <strong>{latestShot.dose}g → {latestShot.yield}g</strong>
            </li>
            <li>
              <span>Temps</span>
              <strong>{latestShot.time}s</strong>
            </li>
            <li>
              <span>Eau</span>
              <strong>{latestShot.water}</strong>
            </li>
          </ul>
        </div>
      </header>

      <Navigation items={navigationItems} />

      <main className="grid">
        <SectionCard
          id="referentiel-cafe"
          title="Référentiel Café"
          subtitle="Achat et coûts"
          action={draftState.coffeeStatus ? <Pill tone="success">{draftState.coffeeStatus}</Pill> : null}
        >
          <p className="section-description">
            Renseigne le lot utilisé pour calculer les coûts par shot, le choix d’eau et connecter les futures analyses.
          </p>
          <form className="form-grid" onSubmit={handleCoffeeSubmit}>
            <FormField
              label="Torréfacteur"
              name="roaster"
              placeholder="Ex: Five Elephant"
              required
              value={coffeeForm.roaster}
              onChange={updateCoffeeField('roaster')}
              datalistId="roaster-list"
              datalistOptions={roasterSuggestions}
              autoComplete="organization"
              error={coffeeErrors.roaster}
            />
            <FormField
              label="Référence"
              name="name"
              placeholder="Nom du café"
              required
              value={coffeeForm.name}
              onChange={updateCoffeeField('name')}
              datalistId="coffee-list"
              datalistOptions={coffeeNames}
              autoComplete="off"
              error={coffeeErrors.name}
            />
            <FormField
              label="Type"
              name="type"
              as="select"
              value={coffeeForm.type}
              onChange={updateCoffeeField('type')}
              error={coffeeErrors.type}
            >
              <option value="" disabled>Sélectionner</option>
              {coffeeTypes.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </FormField>
            <FormField
              label="Poids du paquet (g)"
              name="weight"
              type="number"
              min={0}
              step={10}
              placeholder="250"
              helper="Le coût/shots est calculé automatiquement"
              value={coffeeForm.weight}
              onChange={updateCoffeeField('weight')}
              error={coffeeErrors.weight}
            />
            <FormField
              label="Prix payé (€)"
              name="price"
              type="number"
              min={0}
              step={0.1}
              placeholder="14.5"
              value={coffeeForm.price}
              onChange={updateCoffeeField('price')}
              error={coffeeErrors.price}
            />
            <FormField
              label="Date d’achat"
              name="purchaseDate"
              type="date"
              value={coffeeForm.purchaseDate}
              onChange={updateCoffeeField('purchaseDate')}
            />
            <FormField
              label="Eau par défaut"
              name="water"
              as="select"
              value={coffeeForm.water}
              onChange={updateCoffeeField('water')}
              error={coffeeErrors.water}
            >
              {waterOptions.map((water) => (
                <option key={water} value={water}>{water}</option>
              ))}
            </FormField>
            <div className="form-actions">
              <button type="submit">Enregistrer le lot</button>
              <span className="hint">Validation immédiate, envoi API différé</span>
            </div>
          </form>
          <div className="card-list">
            {coffees.map((coffee) => (
              <article key={coffee.id} className="mini-card">
                <div className="mini-card__top">
                  <div>
                    <p className="eyebrow">{coffee.roaster}</p>
                    <h3>{coffee.name}</h3>
                  </div>
                  <Pill tone={coffee.status === 'Approuvé' ? 'success' : coffee.status === 'À éviter' ? 'danger' : 'warning'}>
                    {coffee.status}
                  </Pill>
                </div>
                <dl className="stats">
                  <div>
                    <dt>Type</dt>
                    <dd>{coffee.type}</dd>
                  </div>
                  <div>
                    <dt>Coût/kg</dt>
                    <dd>{formatCurrency(coffee.pricePerKg)}</dd>
                  </div>
                  <div>
                    <dt>Coût / shot</dt>
                    <dd>{formatCurrency(coffee.costPerShot)}</dd>
                  </div>
                  <div>
                    <dt>Eau</dt>
                    <dd>{coffee.water}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          id="journal-extraction"
          title="Journal d&apos;extraction"
          subtitle="Shot factuel"
          action={draftState.shotStatus ? <Pill tone="success">{draftState.shotStatus}</Pill> : null}
        >
          <p className="section-description">
            Note uniquement les faits techniques : paramètres machine, ratio, eau. Un rappel sensoriel en mots aide à sécuriser
            la cohérence sans jamais afficher de chiffres d’analyse.
          </p>
          <form className="form-grid" onSubmit={handleShotSubmit}>
            <FormField
              label="Café utilisé"
              name="coffee"
              as="select"
              value={shotForm.coffee}
              onChange={updateShotField('coffee')}
              error={shotErrors.coffee}
            >
              <option value="" disabled>Choisir un café</option>
              {coffees.map((coffee) => (
                <option key={coffee.id} value={coffee.name}>{coffee.name}</option>
              ))}
            </FormField>
            <FormField
              label="Boisson"
              name="beverage"
              as="select"
              value={shotForm.beverage}
              onChange={updateShotField('beverage')}
              error={shotErrors.beverage}
            >
              <option value="" disabled>Type d&apos;extraction</option>
              {beverageOptions.map((beverage) => (
                <option key={beverage} value={beverage}>{beverage}</option>
              ))}
            </FormField>
            <FormField
              label="Mouture"
              name="grind"
              type="number"
              min={0}
              step={0.1}
              placeholder="6.0"
              helper="Valeur machine, reste interne"
              value={shotForm.grind}
              onChange={updateShotField('grind')}
            />
            <FormField
              label="Dose (g)"
              name="dose"
              type="number"
              min={0}
              step={0.1}
              placeholder="18.0"
              value={shotForm.dose}
              onChange={updateShotField('dose')}
              error={shotErrors.dose}
            />
            <FormField
              label="Poids en tasse (g)"
              name="yield"
              type="number"
              min={0}
              step={0.1}
              placeholder="36"
              value={shotForm.yield}
              onChange={updateShotField('yield')}
              error={shotErrors.yield}
            />
            <FormField
              label="Temps (s)"
              name="time"
              type="number"
              min={0}
              step={0.5}
              placeholder="28"
              value={shotForm.time}
              onChange={updateShotField('time')}
              error={shotErrors.time}
            />
            <FormField
              label="Eau"
              name="water"
              as="select"
              value={shotForm.water}
              onChange={updateShotField('water')}
              error={shotErrors.water}
            >
              {waterOptions.map((water) => (
                <option key={water} value={water}>{water}</option>
              ))}
            </FormField>
            <FormField
              label="Repère sensoriel en mots"
              name="sensoryWords"
              placeholder="floral, velouté, doux"
              helper="Alimente l’API sans chiffres"
              value={shotForm.sensoryWords}
              onChange={updateShotField('sensoryWords')}
              datalistId="sensory-list"
              datalistOptions={sensoryWords}
            />
            <div className="chips">
              {waterOptions.map((water) => (
                <button
                  key={water}
                  type="button"
                  className={`chip${shotForm.water === water ? ' chip--active' : ''}`}
                  onClick={() => setShotForm((previous) => ({ ...previous, water }))}
                >
                  {water}
                </button>
              ))}
            </div>
            <div className="form-actions">
              <button type="submit">Enregistrer le shot</button>
              <span className="hint">Diagnostics ratio et suggestions restent textuels</span>
            </div>
          </form>

          <div className="card-list card-list--compact">
            {shots.map((shot) => (
              <article key={shot.id} className="mini-card mini-card--compact">
                <div className="mini-card__top">
                  <div>
                    <p className="eyebrow">{shot.beverage}</p>
                    <h3>{shot.coffee}</h3>
                  </div>
                  <span className="timestamp">{new Date(shot.date).toLocaleDateString('fr-FR')}</span>
                </div>
                <dl className="stats stats--wrap">
                  <div>
                    <dt>Ratio</dt>
                    <dd>{shot.dose}g → {shot.yield}g</dd>
                  </div>
                  <div>
                    <dt>Temps</dt>
                    <dd>{shot.time}s</dd>
                  </div>
                  <div>
                    <dt>Eau</dt>
                    <dd>{shot.water}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          id="degustation-verdict"
          title="Dégustation & verdict"
          subtitle="Sensoriel"
          action={draftState.tastingStatus ? <Pill tone="success">{draftState.tastingStatus}</Pill> : null}
        >
          <p className="section-description">
            Jugements exprimés avec des mots uniquement. Les réponses proviennent des endpoints d’analyse et restent traçables
            (eau, shot, arômes) sans affichage numérique.
          </p>
          <form className="form-grid" onSubmit={handleTastingSubmit}>
            <FormField
              label="Café dégusté"
              name="tastingCoffee"
              as="select"
              value={tastingForm.coffee}
              onChange={updateTastingField('coffee')}
              error={tastingErrors.coffee}
            >
              <option value="" disabled>Choisir un café</option>
              {coffees.map((coffee) => (
                <option key={coffee.id} value={coffee.name}>{coffee.name}</option>
              ))}
            </FormField>
            <FormField
              label="Arômes dominants"
              name="aromas"
              placeholder="Fruits jaunes, miel"
              value={tastingForm.aromas}
              onChange={updateTastingField('aromas')}
              datalistId="aroma-list"
              datalistOptions={sensoryVocabulary.aromas}
              error={tastingErrors.aromas}
            />
            <FormField
              label="Texture"
              name="mouthfeel"
              placeholder="Fluide / rond / sirupeux"
              value={tastingForm.mouthfeel}
              onChange={updateTastingField('mouthfeel')}
              datalistId="mouthfeel-list"
              datalistOptions={sensoryVocabulary.mouthfeels}
              error={tastingErrors.mouthfeel}
            />
            <FormField
              label="Finale"
              name="finish"
              placeholder="Longueur harmonieuse"
              value={tastingForm.finish}
              onChange={updateTastingField('finish')}
              datalistId="finish-list"
              datalistOptions={sensoryVocabulary.finishes}
              error={tastingErrors.finish}
            />
            <FormField
              label="Verdict"
              name="verdict"
              as="select"
              value={tastingForm.verdict}
              onChange={updateTastingField('verdict')}
              error={tastingErrors.verdict}
            >
              <option value="" disabled>Choisir une issue</option>
              {sensoryVocabulary.verdicts.map((verdict) => (
                <option key={verdict} value={verdict}>{verdict}</option>
              ))}
            </FormField>
            <FormField
              label="Commentaire en mots"
              name="comment"
              as="textarea"
              rows={3}
              placeholder="Décision motivée, sans chiffres"
              value={tastingForm.comment}
              onChange={updateTastingField('comment')}
            />
            <FormField
              label="Eau utilisée"
              name="tastingWater"
              as="select"
              value={tastingForm.water}
              onChange={updateTastingField('water')}
              error={tastingErrors.water}
            >
              {waterOptions.map((water) => (
                <option key={water} value={water}>{water}</option>
              ))}
            </FormField>
            <div className="form-actions">
              <button type="submit">Enregistrer la dégustation</button>
              <span className="hint">La décision reste textuelle et traçable</span>
            </div>
          </form>

          <div className="analysis-grid">
            {analysisFeed.length === 0 ? (
              <p className="muted">Connexion aux endpoints d’analyse en cours…</p>
            ) : (
              analysisFeed.map((signal) => (
                <article key={signal.endpoint} className="mini-card analysis-card">
                  <div className="mini-card__top">
                    <div>
                      <p className="eyebrow">{signal.label}</p>
                      <h3>{signal.verdictWord}</h3>
                    </div>
                    <Pill tone="info">API {signal.endpoint}</Pill>
                  </div>
                  <p className="muted">{signal.trace}</p>
                  <div className="chips">
                    {signal.words.map((word) => (
                      <span key={word} className="chip chip--ghost">{word}</span>
                    ))}
                  </div>
                  <p className="analysis-focus">{signal.focus}</p>
                </article>
              ))
            )}
          </div>

          <div className="verdict-grid">
            {justifiedVerdicts.map((verdict) => (
              <article key={verdict.coffee} className="mini-card verdict">
                <div className="mini-card__top">
                  <div>
                    <p className="eyebrow">Verdict {verdict.beverage}</p>
                    <h3>{verdict.coffee}</h3>
                  </div>
                  <Pill tone={verdict.verdict === 'Racheter' ? 'success' : verdict.verdict === 'À éviter' ? 'danger' : 'warning'}>
                    {verdict.verdict}
                  </Pill>
                </div>
                <ul className="verdict__list">
                  {verdict.highlights.map((highlight) => (
                    <li key={highlight}>{highlight}</li>
                  ))}
                </ul>
                <div className="verdict__trace">
                  <p className="muted">{verdict.justification}</p>
                  <p className="trace">{verdict.trace}</p>
                  <div className="chips">
                    <span className="chip chip--ghost">{verdict.water}</span>
                    {verdict.sensoryWords.map((word) => (
                      <span key={word} className="chip chip--ghost">{word}</span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard id="classements" title="Classements" subtitle="Synthèse sensorielle">
          <p className="section-description">
            Visualise rapidement les cafés qui sortent du lot selon la boisson et les critères sensoriels collectés en mots.
          </p>
          <div className="tabs" role="tablist" aria-label="Vues de classement">
            {leaderboardSlices.map((slice) => (
              <button
                key={slice.id}
                className={`tab${slice.id === activeLeaderboard ? ' tab--active' : ''}`}
                onClick={() => setActiveLeaderboard(slice.id)}
                type="button"
                role="tab"
                aria-selected={slice.id === activeLeaderboard}
              >
                <span>{slice.label}</span>
                <span className="tab__caption">{slice.description}</span>
              </button>
            ))}
          </div>
          <div className="leaderboard">
            {activeLeaderboardSlice.entries.map((entry) => (
              <article key={`${activeLeaderboard}-${entry.coffee}`} className="leaderboard__item">
                <div className="leaderboard__meta">
                  <p className="eyebrow">{entry.beverage}</p>
                  <h3>{entry.coffee}</h3>
                  <p className="muted">{entry.tag}</p>
                </div>
                <Pill tone={entry.position === 1 ? 'success' : 'info'}>
                  {positionToWord(entry.position)}
                </Pill>
              </article>
            ))}
          </div>
        </SectionCard>
      </main>
    </div>
  );
}
