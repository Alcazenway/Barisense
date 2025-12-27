import { useMemo, useState } from 'react';
import { FormField } from './components/FormField';
import { Pill } from './components/Pill';
import { SectionCard } from './components/SectionCard';
import { coffees, leaderboard, shots, tastingVerdicts } from './data/sampleData';
import type { CoffeeType } from './types';
import './App.css';

interface DraftState {
  coffeeStatus?: string;
  shotStatus?: string;
  tastingStatus?: string;
}

const beverageOptions = ['Ristretto', 'Expresso', 'Café long'];
const waterOptions = ['Volvic', 'Cristalline', 'Robinet filtrée'];
const coffeeTypes: CoffeeType[] = ['Grain', 'Moulu'];

function formatCurrency(value: number) {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 2,
  }).format(value);
}

export default function App() {
  const [draftState, setDraftState] = useState<DraftState>({});

  const waterDiversity = useMemo(
    () => new Set(coffees.map((coffee) => coffee.water)).size,
    [],
  );

  const latestShot = shots[shots.length - 1];

  const handleSubmit = (key: keyof DraftState) => (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const timestamp = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    setDraftState((previous) => ({
      ...previous,
      [key]: `Brouillon prêt • ${timestamp}`,
    }));
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Barisense • Pilote barista</p>
          <h1>Collecte, dégustation et verdicts</h1>
          <p className="lede">
            Un hub unique pour tracer les cafés, suivre les réglages, comparer les eaux et rendre les verdicts
            sans jamais afficher de chiffres.
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

      <main className="grid">
        <SectionCard
          title="Référentiel Café"
          subtitle="Achat et coûts"
          action={draftState.coffeeStatus ? <Pill tone="success">{draftState.coffeeStatus}</Pill> : null}
        >
          <p className="section-description">
            Renseigne le lot utilisé pour calculer les coûts par shot et suivre les verdicts associés.
          </p>
          <form className="form-grid" onSubmit={handleSubmit('coffeeStatus')}>
            <FormField label="Torréfacteur" name="roaster" placeholder="Ex: Five Elephant" required />
            <FormField label="Référence" name="name" placeholder="Nom du café" required />
            <FormField label="Type" name="type" as="select" defaultValue="">
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
            />
            <FormField
              label="Prix payé (€)"
              name="price"
              type="number"
              min={0}
              step={0.1}
              placeholder="14.5"
            />
            <FormField label="Date d’achat" name="purchaseDate" type="date" />
            <FormField label="Eau par défaut" name="water" as="select" defaultValue="">
              <option value="" disabled>Choisir l&apos;eau</option>
              {waterOptions.map((water) => (
                <option key={water} value={water}>{water}</option>
              ))}
            </FormField>
            <div className="form-actions">
              <button type="submit">Enregistrer le lot</button>
              <span className="hint">Sauvegardé localement avant envoi API</span>
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
          title="Journal d&apos;extraction"
          subtitle="Shot factuel"
          action={draftState.shotStatus ? <Pill tone="success">{draftState.shotStatus}</Pill> : null}
        >
          <p className="section-description">
            Note uniquement les faits techniques : paramètres machine, ratio, eau. Aucun jugement sensoriel ici.
          </p>
          <form className="form-grid" onSubmit={handleSubmit('shotStatus')}>
            <FormField label="Café utilisé" name="coffee" as="select" defaultValue="">
              <option value="" disabled>Choisir un café</option>
              {coffees.map((coffee) => (
                <option key={coffee.id} value={coffee.name}>{coffee.name}</option>
              ))}
            </FormField>
            <FormField label="Boisson" name="beverage" as="select" defaultValue="">
              <option value="" disabled>Type d&apos;extraction</option>
              {beverageOptions.map((beverage) => (
                <option key={beverage} value={beverage}>{beverage}</option>
              ))}
            </FormField>
            <FormField label="Mouture" name="grind" type="number" min={0} step={0.1} placeholder="6.0" />
            <FormField label="Dose (g)" name="dose" type="number" min={0} step={0.1} placeholder="18.0" />
            <FormField label="Poids en tasse (g)" name="yield" type="number" min={0} step={0.1} placeholder="36" />
            <FormField label="Temps (s)" name="time" type="number" min={0} step={0.5} placeholder="28" />
            <FormField label="Eau" name="water" as="select" defaultValue="">
              <option value="" disabled>Sélectionner l&apos;eau</option>
              {waterOptions.map((water) => (
                <option key={water} value={water}>{water}</option>
              ))}
            </FormField>
            <div className="form-actions">
              <button type="submit">Enregistrer le shot</button>
              <span className="hint">Diagnostics ratio et suggestions seront proposés après envoi</span>
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
          title="Dégustation & verdict"
          subtitle="Sensoriel"
          action={draftState.tastingStatus ? <Pill tone="success">{draftState.tastingStatus}</Pill> : null}
        >
          <p className="section-description">
            Jugements exprimés avec des mots uniquement. Les valeurs numériques sont converties et stockées en back-end.
          </p>
          <form className="form-grid" onSubmit={handleSubmit('tastingStatus')}>
            <FormField label="Café dégusté" name="tastingCoffee" as="select" defaultValue="">
              <option value="" disabled>Choisir un café</option>
              {coffees.map((coffee) => (
                <option key={coffee.id} value={coffee.name}>{coffee.name}</option>
              ))}
            </FormField>
            <FormField label="Arômes dominants" name="aromas" placeholder="Fruits jaunes, miel" />
            <FormField label="Acidité" name="acidity" placeholder="Douce / vive / croquante" />
            <FormField label="Amertume" name="bitterness" placeholder="Absente / présente / nette" />
            <FormField label="Corps" name="body" placeholder="Fluide / rond / sirupeux" />
            <FormField label="Équilibre" name="balance" placeholder="Harmonieux, légèrement sec" />
            <FormField label="Appréciation" name="overall" placeholder="Verdict en mots" />
            <div className="form-actions">
              <button type="submit">Enregistrer la dégustation</button>
              <span className="hint">La décision sera générée dans la section Verdicts</span>
            </div>
          </form>

          <div className="verdict-grid">
            {tastingVerdicts.map((verdict) => (
              <article key={verdict.coffee} className="mini-card verdict">
                <div className="mini-card__top">
                  <div>
                    <p className="eyebrow">Verdict</p>
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
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Classements" subtitle="Synthèse sensorielle">
          <p className="section-description">
            Visualise rapidement les cafés qui sortent du lot selon la boisson et les critères sensoriels collectés.
          </p>
          <div className="leaderboard">
            {leaderboard.map((entry) => (
              <article key={entry.coffee} className="leaderboard__item">
                <div className="leaderboard__pos">#{entry.position}</div>
                <div className="leaderboard__meta">
                  <p className="eyebrow">{entry.beverage}</p>
                  <h3>{entry.coffee}</h3>
                  <p className="muted">{entry.tag}</p>
                </div>
                <Pill tone={entry.position === 1 ? 'success' : 'info'}>
                  {entry.position === 1 ? 'Favori' : 'Solide'}
                </Pill>
              </article>
            ))}
          </div>
        </SectionCard>
      </main>
    </div>
  );
}
