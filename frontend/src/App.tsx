import { type ChangeEvent, type FormEvent, useEffect, useMemo, useRef, useState } from 'react';
import './App.css';

interface CafeLot {
  id: string;
  nom: string;
  marque: string;
  origine?: string;
  intensite: number;
  statut: 'stock' | 'ouvert';
  dateAchat: string;
}

interface ShotNote {
  id: string;
  cafeId: string;
  grind: string;
  in: string;
  out: string;
  time: string;
  tasted: boolean;
  flavor: string | null;
  score: number;
  date: string;
}

interface DbState {
  cafes: CafeLot[];
  shots: ShotNote[];
}

type View = 'hub' | 'cave' | 'shot' | 'ranking' | 'history' | 'admin' | 'cafe-detail';

const STORAGE_KEY = 'MONEX_V7_DB';
const FLAVOR_OPTIONS = ['Equilibré', 'Acide', 'Amer'];

const defaultCafeForm = {
  nom: '',
  marque: '',
  origine: '',
  intensite: 5,
};

const defaultShotForm = {
  grind: '',
  in: '',
  out: '',
  time: '',
};

export default function App() {
  const [db, setDb] = useState<DbState>({ cafes: [], shots: [] });
  const [view, setView] = useState<View>('hub');
  const [detailCafeId, setDetailCafeId] = useState<string | null>(null);
  const [cafeForm, setCafeForm] = useState(defaultCafeForm);
  const [shotForm, setShotForm] = useState(defaultShotForm);
  const [formVisible, setFormVisible] = useState(false);
  const [tasteShotId, setTasteShotId] = useState<string | null>(null);
  const [tasteFlavor, setTasteFlavor] = useState(FLAVOR_OPTIONS[0]);
  const [tasteScore, setTasteScore] = useState(5);
  const importInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setDb(JSON.parse(stored));
      } catch (error) {
        console.error('Impossible de charger la base locale', error);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
  }, [db]);

  const pendingShots = useMemo(() => db.shots.filter((shot) => !shot.tasted), [db.shots]);
  const openCafe = useMemo(() => db.cafes.find((cafe) => cafe.statut === 'ouvert'), [db.cafes]);

  const statsForCafe = (cafeId: string) => {
    const tastedShots = db.shots.filter((shot) => shot.cafeId === cafeId && shot.tasted);
    if (tastedShots.length === 0) {
      return { avg: 0, status: 'À TESTER', best: null as ShotNote | null, count: 0 };
    }
    const avg = tastedShots.reduce((total, shot) => total + Number(shot.score), 0) / tastedShots.length;
    const best = [...tastedShots].sort((a, b) => b.score - a.score)[0];
    const status = avg >= 7.5 ? 'RACHETER' : avg >= 5 ? 'AFFINER' : 'ÉVITER';
    return { avg: Number(avg.toFixed(1)), status, best, count: tastedShots.length };
  };

  const setViewWithDetail = (nextView: View, cafeId?: string) => {
    setView(nextView);
    setDetailCafeId(cafeId ?? null);
    window.scrollTo({ top: 0 });
  };

  const toggleForm = () => setFormVisible((previous) => !previous);

  const handleCafeChange = (
    field: keyof typeof defaultCafeForm,
  ) => (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const value = field === 'intensite' ? Number(event.target.value) : event.target.value;
    setCafeForm((previous) => ({ ...previous, [field]: value }));
  };

  const handleShotChange = (
    field: keyof typeof defaultShotForm,
  ) => (event: ChangeEvent<HTMLInputElement>) => {
    setShotForm((previous) => ({ ...previous, [field]: event.target.value }));
  };

  const saveCafe = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!cafeForm.nom.trim() || !cafeForm.marque.trim()) return;
    const newCafe: CafeLot = {
      id: `C${Date.now()}`,
      nom: cafeForm.nom.trim(),
      marque: cafeForm.marque.trim(),
      origine: cafeForm.origine.trim(),
      intensite: cafeForm.intensite,
      statut: 'stock',
      dateAchat: new Date().toLocaleDateString('fr-FR'),
    };
    setDb((previous) => ({ ...previous, cafes: [newCafe, ...previous.cafes] }));
    setCafeForm(defaultCafeForm);
    setFormVisible(false);
    setView('cave');
  };

  const markCafeOpen = (id: string) => {
    setDb((previous) => ({
      ...previous,
      cafes: previous.cafes.map((cafe) => ({
        ...cafe,
        statut: cafe.id === id ? 'ouvert' : 'stock',
      })),
    }));
    setView('hub');
  };

  const saveShot = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!openCafe) return;
    const newShot: ShotNote = {
      id: `S${Date.now()}`,
      cafeId: openCafe.id,
      grind: shotForm.grind,
      in: shotForm.in,
      out: shotForm.out,
      time: shotForm.time,
      tasted: false,
      flavor: null,
      score: 0,
      date: new Date().toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      }),
    };
    setDb((previous) => ({ ...previous, shots: [...previous.shots, newShot] }));
    setShotForm(defaultShotForm);
    setView('hub');
  };

  const openTasteModal = (shotId: string) => {
    setTasteShotId(shotId);
    setTasteFlavor(FLAVOR_OPTIONS[0]);
    setTasteScore(5);
  };

  const saveTaste = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!tasteShotId) return;
    setDb((previous) => ({
      ...previous,
      shots: previous.shots.map((shot) =>
        shot.id === tasteShotId
          ? { ...shot, flavor: tasteFlavor, score: tasteScore, tasted: true }
          : shot,
      ),
    }));
    closeModal();
    setView('history');
  };

  const closeModal = () => setTasteShotId(null);

  const exportDb = () => {
    const blob = new Blob([JSON.stringify(db, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `monexpresso_backup_${new Date().toISOString().split('T')[0]}.json`;
    anchor.click();
  };

  const importDb = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (loadEvent) => {
      try {
        const imported: DbState = JSON.parse(String(loadEvent.target?.result));
        setDb(imported);
        setView('hub');
      } catch (error) {
        console.error('Fichier illisible', error);
      }
    };
    reader.readAsText(file);
  };

  const injectDemo = () => {
    const cafes: CafeLot[] = [
      { id: 'C1', nom: 'Moka Sidamo', marque: 'Terres de Café', intensite: 6, statut: 'ouvert', dateAchat: '01/01/24' },
      { id: 'C2', nom: 'Bourbon Pointu', marque: 'Lomi', intensite: 4, statut: 'stock', dateAchat: '05/01/24' },
    ];
    const shots: ShotNote[] = Array.from({ length: 20 }, (_, index) => ({
      id: `S${index}`,
      cafeId: 'C1',
      grind: String(4 + (index % 3)),
      in: '18',
      out: String(36 + (index % 2)),
      time: String(24 + (index % 6)),
      flavor: index % 3 === 0 ? 'Equilibré' : 'Amer',
      score: 6 + (index % 4),
      tasted: index > 2,
      date: '12/01/24 08:30',
    }));
    setDb({ cafes, shots });
    setView('hub');
  };

  const resetAll = () => {
    if (window.confirm('Supprimer TOUT ?')) {
      setDb({ cafes: [], shots: [] });
      setView('hub');
    }
  };

  const renderHub = () => {
    const stats = openCafe ? statsForCafe(openCafe.id) : null;

    return (
      <div className="space-y-6">
        {pendingShots.length > 0 ? (
          <button
            type="button"
            className="bg-amber-500 p-4 rounded-2xl flex justify-between items-center shadow-lg pulse w-full"
            onClick={() => setView('history')}
          >
            <span className="text-white text-[10px] font-black uppercase tracking-widest">
              {pendingShots.length} Dégustation(s) à noter
            </span>
            <i className="fa-solid fa-chevron-right text-white/50" />
          </button>
        ) : null}

        <div className="space-y-4">
          <h2 className="text-[10px] font-black uppercase text-stone-400 tracking-widest">Barista en service</h2>
          {openCafe ? (
            <button
              type="button"
              onClick={() => setViewWithDetail('cafe-detail', openCafe.id)}
              className="card p-8 bg-stone-900 text-white cursor-pointer relative overflow-hidden text-left"
            >
              <span className="bg-amber-500 text-stone-900 text-[8px] font-black px-2 py-1 rounded uppercase mb-4 inline-block">
                Actuel
              </span>
              <h3 className="text-4xl font-black italic tracking-tighter mb-1">{openCafe.nom}</h3>
              <p className="text-xs font-bold text-stone-400 uppercase tracking-widest mb-8">{openCafe.marque}</p>
              <div className="flex justify-between items-end border-t border-stone-800 pt-6">
                <div>
                  <p className="text-[8px] text-amber-500 font-black uppercase">Verdict</p>
                  <p className="text-lg font-black">{stats?.status}</p>
                </div>
                <div className="text-right">
                  <p className="text-[8px] text-stone-500 font-black uppercase">Note Moyenne</p>
                  <p className="text-lg font-black">{stats?.avg}/10</p>
                </div>
              </div>
            </button>
          ) : (
            <div className="card p-12 text-center text-[10px] font-black uppercase text-stone-400">Aucun café ouvert.</div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="card p-6 text-center">
            <p className="text-[9px] font-black text-stone-400 uppercase mb-1">Total Shots</p>
            <p className="text-3xl font-black">{db.shots.length}</p>
          </div>
          <button
            type="button"
            onClick={() => setView('ranking')}
            className="card p-6 text-center border-amber-200 cursor-pointer"
          >
            <p className="text-[9px] font-black text-amber-600 uppercase mb-1">Elite Rank</p>
            <p className="text-3xl font-black text-amber-600">
              <i className="fa-solid fa-trophy" />
            </p>
          </button>
        </div>
      </div>
    );
  };

  const renderRanking = () => {
    const ranked = db.cafes
      .map((cafe) => ({ ...cafe, stats: statsForCafe(cafe.id) }))
      .sort((a, b) => b.stats.avg - a.stats.avg);

    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-black italic uppercase tracking-tighter mb-2">Elite Ranking</h2>
        {ranked.map((cafe, index) => (
          <button
            type="button"
            key={cafe.id}
            onClick={() => setViewWithDetail('cafe-detail', cafe.id)}
            className={`card p-5 flex items-center gap-6 cursor-pointer border-l-8 ${
              cafe.stats.status === 'RACHETER' ? 'border-green-500' : 'border-stone-100'
            }`}
          >
            <span className="text-3xl font-black text-stone-200 italic">#{index + 1}</span>
            <div className="flex-1">
              <h4 className="font-black text-sm uppercase">{cafe.nom}</h4>
              <p className="text-[9px] font-bold text-stone-400 uppercase">
                {cafe.stats.status} • {cafe.stats.count} shots
              </p>
            </div>
            <div className="text-right">
              <p className="text-xl font-black italic text-amber-600 leading-none">{cafe.stats.avg}</p>
            </div>
          </button>
        ))}
      </div>
    );
  };

  const renderHistory = () => (
    <div className="space-y-4">
      <h2 className="text-2xl font-black italic uppercase tracking-tighter mb-2">Journal & Dégustations</h2>
      {[...db.shots].reverse().map((shot) => {
        const cafe = db.cafes.find((c) => c.id === shot.cafeId);
        return (
          <div
            key={shot.id}
            className={`card p-4 flex justify-between items-center ${
              !shot.tasted ? 'border-l-4 border-amber-500 bg-amber-50/10' : ''
            }`}
          >
            <div>
              <h4 className="font-bold text-[10px] uppercase text-stone-500">{cafe?.nom}</h4>
              <p className="text-[11px] font-black mb-2">{shot.date}</p>
              <p className="text-[10px] font-mono text-stone-400">
                G:{shot.grind} | {shot.in}g &gt; {shot.out}g | {shot.time}s
              </p>
            </div>
            {!shot.tasted ? (
              <button
                type="button"
                onClick={() => openTasteModal(shot.id)}
                className="bg-amber-500 text-white px-4 py-2 rounded-lg text-[9px] font-black uppercase"
              >
                Déguster
              </button>
            ) : (
              <div className="text-right">
                <span className="text-[9px] font-black uppercase text-amber-600 block">{shot.flavor}</span>
                <span className="font-black">{shot.score}/10</span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );

  const renderCafeDetail = () => {
    if (!detailCafeId) return null;
    const cafe = db.cafes.find((c) => c.id === detailCafeId);
    if (!cafe) return null;
    const stats = statsForCafe(detailCafeId);

    return (
      <div className="space-y-4">
        <button
          type="button"
          onClick={() => setView('ranking')}
          className="text-[10px] font-black uppercase text-stone-400 mb-4 flex items-center gap-2"
        >
          <i className="fa-solid fa-arrow-left" /> Retour
        </button>
        <div className="card p-8 mb-2">
          <h2 className="text-4xl font-black italic tracking-tighter mb-2">{cafe.nom}</h2>
          <p className="text-xs font-bold text-stone-400 uppercase tracking-widest border-b pb-6 mb-6">
            {cafe.marque} • {cafe.origine || 'Sans Origine'}
          </p>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-[9px] font-black text-stone-400 uppercase">Score Moyen</p>
              <p className="text-2xl font-black text-amber-600">{stats.avg}/10</p>
            </div>
            <div>
              <p className="text-[9px] font-black text-stone-400 uppercase">Intensité</p>
              <p className="text-2xl font-black italic">{cafe.intensite}/10</p>
            </div>
          </div>
        </div>
        <div className="card p-6 bg-amber-50 border-amber-200">
          <h4 className="text-[10px] font-black uppercase text-amber-600 mb-4">Meilleur réglage SAGE (Sweet Spot)</h4>
          {stats.best ? (
            <div className="grid grid-cols-4 gap-2 text-center">
              <div className="bg-white p-2 rounded-lg">
                <p className="text-[8px] font-bold text-stone-400">Grind</p>
                <p className="font-black">{stats.best.grind}</p>
              </div>
              <div className="bg-white p-2 rounded-lg">
                <p className="text-[8px] font-bold text-stone-400">In</p>
                <p className="font-black">{stats.best.in}g</p>
              </div>
              <div className="bg-white p-2 rounded-lg">
                <p className="text-[8px] font-bold text-stone-400">Out</p>
                <p className="font-black">{stats.best.out}g</p>
              </div>
              <div className="bg-white p-2 rounded-lg">
                <p className="text-[8px] font-bold text-stone-400">Temps</p>
                <p className="font-black">{stats.best.time}s</p>
              </div>
            </div>
          ) : (
            <p className="text-xs italic text-stone-400 font-bold">Pas encore assez de données.</p>
          )}
        </div>
      </div>
    );
  };

  const renderCave = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-black italic uppercase tracking-tighter">Ma Cave</h2>
        <button type="button" onClick={toggleForm} className="btn-action px-4 py-2 text-[10px] uppercase">
          {formVisible ? 'Fermer' : '+ Ajouter'}
        </button>
      </div>

      {formVisible ? (
        <div id="form-cafe" className="card p-6 border-stone-900 border-2 shadow-xl">
          <form className="space-y-4" onSubmit={saveCafe}>
            <input
              id="nc-nom"
              placeholder="Nom du café (ex: Honduras)"
              className="input-sage"
              value={cafeForm.nom}
              onChange={handleCafeChange('nom')}
              required
            />
            <input
              id="nc-marque"
              placeholder="Torréfacteur (ex: Lomi)"
              className="input-sage"
              value={cafeForm.marque}
              onChange={handleCafeChange('marque')}
              required
            />
            <input
              id="nc-origine"
              placeholder="Origine"
              className="input-sage"
              value={cafeForm.origine}
              onChange={handleCafeChange('origine')}
            />
            <div className="bg-stone-50 p-4 rounded-xl">
              <label
                className="text-[10px] font-black uppercase text-stone-400 block mb-2"
                htmlFor="nc-intensite"
              >
                Intensité (1-10)
              </label>
              <input
                type="range"
                id="nc-intensite"
                min={1}
                max={10}
                value={cafeForm.intensite}
                onChange={handleCafeChange('intensite')}
                className="w-full accent-stone-900"
              />
            </div>
            <button type="submit" className="w-full btn-action py-4 uppercase text-xs">
              Enregistrer
            </button>
          </form>
        </div>
      ) : null}

      <div className="grid gap-4">
        {db.cafes.length === 0 ? (
          <div className="card p-12 text-center text-[10px] font-black uppercase text-stone-400">Aucun café en cave.</div>
        ) : (
          db.cafes.map((cafe) => (
            <div
              key={cafe.id}
              role="button"
              tabIndex={0}
              onClick={() => setViewWithDetail('cafe-detail', cafe.id)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') setViewWithDetail('cafe-detail', cafe.id);
              }}
              className={`card p-6 flex justify-between items-center cursor-pointer border-l-8 ${
                cafe.statut === 'ouvert' ? 'border-amber-500' : 'border-stone-200'
              }`}
            >
              <div>
                <h4 className="font-black text-lg italic">{cafe.nom}</h4>
                <p className="text-[10px] font-bold text-stone-400 uppercase">{cafe.marque}</p>
              </div>
              {cafe.statut === 'stock' ? (
                <button
                  type="button"
                  onClick={(event) => {
                    event.stopPropagation();
                    markCafeOpen(cafe.id);
                  }}
                  className="bg-stone-900 text-white text-[9px] font-black px-4 py-2 rounded-lg uppercase shadow-lg"
                >
                  Ouvrir
                </button>
              ) : (
                <i className="fa-solid fa-mug-saucer text-amber-500" />
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );

  const renderShot = () => {
    if (!openCafe) {
      return (
        <div className="card p-12 text-center text-xs font-black uppercase text-stone-400">
          Ouvrez un café dans la cave d'abord.
        </div>
      );
    }

    return (
      <div className="card p-8 max-w-sm mx-auto shadow-2xl border-t-8 border-stone-900">
        <h2 className="text-2xl font-black mb-8 italic uppercase text-center tracking-tighter">Extraction SAGE</h2>
        <form className="space-y-4" onSubmit={saveShot}>
          <div className="p-3 bg-stone-100 rounded-lg text-center font-bold text-xs uppercase mb-4">{openCafe.nom}</div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[9px] font-black text-stone-400 uppercase ml-2">Grind</label>
              <input
                type="number"
                id="s-grind"
                placeholder="4"
                className="input-sage"
                value={shotForm.grind}
                onChange={handleShotChange('grind')}
                required
              />
            </div>
            <div>
              <label className="text-[9px] font-black text-stone-400 uppercase ml-2">Dose In</label>
              <input
                type="number"
                id="s-in"
                step="0.1"
                placeholder="18.0"
                className="input-sage"
                value={shotForm.in}
                onChange={handleShotChange('in')}
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[9px] font-black text-stone-400 uppercase ml-2">Dose Out</label>
              <input
                type="number"
                id="s-out"
                step="0.1"
                placeholder="36.0"
                className="input-sage"
                value={shotForm.out}
                onChange={handleShotChange('out')}
                required
              />
            </div>
            <div>
              <label className="text-[9px] font-black text-stone-400 uppercase ml-2">Temps (s)</label>
              <input
                type="number"
                id="s-time"
                placeholder="28"
                className="input-sage"
                value={shotForm.time}
                onChange={handleShotChange('time')}
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full btn-action py-5 uppercase font-black tracking-widest shadow-xl"
          >
            Enregistrer Shot
          </button>
        </form>
      </div>
    );
  };

  const renderAdmin = () => (
    <div className="card p-8 space-y-8">
      <h2 className="text-2xl font-black italic uppercase tracking-tighter text-stone-900">Synchronisation pCloud</h2>
      <div className="space-y-4">
        <button
          type="button"
          onClick={exportDb}
          className="w-full btn-action py-4 text-xs uppercase tracking-widest shadow-lg"
        >
          <i className="fa-solid fa-download mr-2" /> Télécharger JSON (Backup)
        </button>
        <input
          ref={importInputRef}
          type="file"
          id="import-file"
          className="hidden"
          onChange={importDb}
          accept="application/json"
        />
        <button
          type="button"
          onClick={() => importInputRef.current?.click()}
          className="w-full bg-white border border-stone-200 py-4 rounded-xl text-xs font-black uppercase tracking-widest"
        >
          <i className="fa-solid fa-upload mr-2" /> Charger Fichier (Sync)
        </button>
      </div>
      <div className="pt-6 border-t space-y-3">
        <p className="text-[10px] font-black text-stone-400 uppercase tracking-widest">Zone de danger</p>
        <button
          type="button"
          onClick={injectDemo}
          className="w-full bg-blue-50 text-blue-600 py-3 rounded-xl text-[10px] font-black uppercase"
        >
          Injecter Démo (23 lignes)
        </button>
        <button
          type="button"
          onClick={resetAll}
          className="w-full bg-red-50 text-red-600 py-3 rounded-xl text-[10px] font-black uppercase"
        >
          RAZ Totale
        </button>
      </div>
    </div>
  );

  const activeView = () => {
    if (view === 'hub') return renderHub();
    if (view === 'cave') return renderCave();
    if (view === 'shot') return renderShot();
    if (view === 'ranking') return renderRanking();
    if (view === 'history') return renderHistory();
    if (view === 'admin') return renderAdmin();
    if (view === 'cafe-detail') return renderCafeDetail();
    return null;
  };

  const tasteShot = tasteShotId ? db.shots.find((shot) => shot.id === tasteShotId) : null;
  const tasteCafe = tasteShot ? db.cafes.find((cafe) => cafe.id === tasteShot.cafeId) : null;

  return (
    <div className="min-h-screen pb-24">
      <header className="glass sticky top-0 z-40 px-6 py-4 flex justify-between items-center border-bottom border-stone-100">
        <button
          type="button"
          className="flex items-center gap-2"
          onClick={() => setView('hub')}
        >
          <div className="w-8 h-8 bg-stone-900 rounded-lg flex items-center justify-center">
            <i className="fa-solid fa-mug-hot text-amber-500 text-sm" />
          </div>
          <span className="font-black text-xs uppercase tracking-tighter">
            MonExpresso <span className="text-amber-600">Elite</span>
          </span>
        </button>
        <button
          type="button"
          onClick={() => setView('admin')}
          className="text-stone-400 hover:text-stone-900 transition"
          aria-label="Ouvrir la zone admin"
        >
          <i className="fa-solid fa-cloud" />
        </button>
      </header>

      <main id="view-content" className="max-w-xl mx-auto p-4 space-y-6">
        {activeView()}
      </main>

      <nav className="tab-nav glass" role="navigation" aria-label="Navigation principale">
        <button
          type="button"
          onClick={() => setView('hub')}
          className={`nav-item ${view === 'hub' ? 'active' : ''}`}
          id="nav-hub"
        >
          <i className="fa-solid fa-house" />Hub
        </button>
        <button
          type="button"
          onClick={() => setView('cave')}
          className={`nav-item ${view === 'cave' ? 'active' : ''}`}
          id="nav-cave"
        >
          <i className="fa-solid fa-box-archive" />Cave
        </button>
        <button
          type="button"
          onClick={() => setView('shot')}
          className={`nav-item ${view === 'shot' ? 'active !text-amber-600' : '!text-amber-600'}`}
          id="nav-shot"
        >
          <i className="fa-solid fa-circle-plus" />Shot
        </button>
        <button
          type="button"
          onClick={() => setView('ranking')}
          className={`nav-item ${view === 'ranking' ? 'active' : ''}`}
          id="nav-ranking"
        >
          <i className="fa-solid fa-trophy" />Elite
        </button>
        <button
          type="button"
          onClick={() => setView('history')}
          className={`nav-item relative ${view === 'history' ? 'active' : ''}`}
          id="nav-history"
        >
          <i className="fa-solid fa-clipboard-list" />Journal
          <span id="badge-pending" className={`badge-count ${pendingShots.length === 0 ? 'hidden' : ''}`}>
            {pendingShots.length}
          </span>
        </button>
      </nav>

      {tasteShot ? (
        <div className="modal" role="dialog" aria-modal="true">
          <div className="modal__content">
            <h2 className="text-2xl font-black italic mb-1">Feedback</h2>
            <p className="text-[10px] text-stone-400 font-bold uppercase mb-6 tracking-widest">
              {tasteCafe?.nom} | {tasteShot.time}s | {tasteShot.out}g
            </p>
            <form className="space-y-5" onSubmit={saveTaste}>
              <div>
                <label className="block text-[10px] font-black uppercase text-stone-500 mb-2">
                  Profil aromatique
                </label>
                <select
                  className="input-sage"
                  value={tasteFlavor}
                  onChange={(event) => setTasteFlavor(event.target.value)}
                >
                  {FLAVOR_OPTIONS.map((flavor) => (
                    <option key={flavor} value={flavor}>
                      {flavor === 'Equilibré' ? 'Equilibré (Sweet Spot)' : flavor === 'Acide' ? 'Trop Acide (Sous-extrait)' : 'Trop Amer (Sur-extrait)'}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-black uppercase text-stone-500 mb-2">
                  Note Plaisir (1-10)
                </label>
                <input
                  type="range"
                  min={1}
                  max={10}
                  className="w-full accent-stone-900"
                  value={tasteScore}
                  onChange={(event) => setTasteScore(Number(event.target.value))}
                />
              </div>
              <button type="submit" className="w-full btn-action py-4 uppercase text-xs tracking-widest">
                Enregistrer
              </button>
              <button
                type="button"
                onClick={closeModal}
                className="w-full text-stone-400 font-bold text-[10px] uppercase"
              >
                Plus tard
              </button>
            </form>
          </div>
        </div>
      ) : null}
    </div>
  );
}
