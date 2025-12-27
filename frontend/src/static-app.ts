const coffees = [
  { name: 'Ethiopia Dimtu', roaster: 'Five Elephant', type: 'Grain', water: 'Volvic' },
  { name: 'Serra do Cabral', roaster: 'Terroir', type: 'Grain', water: 'Cristalline' },
  { name: 'La Esperanza', roaster: 'Structure Coffee', type: 'Moulu', water: 'Robinet filtrée' },
];

const shots = [
  { coffee: 'Ethiopia Dimtu', beverage: 'Ristretto', ratio: '18g → 36g', water: 'Volvic' },
  { coffee: 'Serra do Cabral', beverage: 'Expresso', ratio: '18.5g → 40g', water: 'Cristalline' },
  { coffee: 'La Esperanza', beverage: 'Expresso', ratio: '19g → 42g', water: 'Robinet filtrée' },
];

const verdicts = [
  {
    coffee: 'Ethiopia Dimtu',
    verdict: 'Racheter',
    details: ['Pêche blanche', 'Jasmin', 'Texture soyeuse'],
  },
  {
    coffee: 'Serra do Cabral',
    verdict: 'À affiner',
    details: ['Privilégier eau minérale', 'Mouture plus fine'],
  },
  {
    coffee: 'La Esperanza',
    verdict: 'En observation',
    details: ['Acidité vive', 'Longueur à lisser'],
  },
];

function createList(title: string, items: string[]): HTMLElement {
  const article = document.createElement('article');
  article.className = 'card';

  const heading = document.createElement('h3');
  heading.textContent = title;
  article.appendChild(heading);

  const list = document.createElement('ul');
  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    list.appendChild(li);
  });
  article.appendChild(list);

  return article;
}

function renderStaticPage() {
  const root = document.getElementById('root');
  if (!root) return;

  const page = document.createElement('div');
  page.className = 'page';

  const header = document.createElement('header');
  const title = document.createElement('h1');
  title.textContent = 'Barisense (version HTML statique)';
  const lead = document.createElement('p');
  lead.textContent = 'Vue simplifiée en HTML pur, sans React ni dépendances.';
  header.appendChild(title);
  header.appendChild(lead);
  page.appendChild(header);

  const intro = document.createElement('section');
  const introTitle = document.createElement('h2');
  introTitle.textContent = 'Résumé';
  const introText = document.createElement('p');
  introText.textContent = 'Formulaires et tableaux convertis en contenu statique pour un rendu immédiat.';
  intro.appendChild(introTitle);
  intro.appendChild(introText);
  page.appendChild(intro);

  const coffeeSection = document.createElement('section');
  coffeeSection.id = 'coffees';
  const coffeeTitle = document.createElement('h2');
  coffeeTitle.textContent = 'Référentiel café';
  const coffeeText = document.createElement('p');
  coffeeText.textContent = 'Lots suivis (roaster, référence, eau par défaut).';
  const coffeeGrid = document.createElement('div');
  coffeeGrid.className = 'card-grid';

  coffees.forEach((coffee) => {
    const card = document.createElement('article');
    card.className = 'card';
    const h3 = document.createElement('h3');
    h3.textContent = coffee.name;
    const meta = document.createElement('p');
    meta.className = 'muted';
    meta.textContent = `${coffee.roaster} • ${coffee.type} • Eau : ${coffee.water}`;
    card.appendChild(h3);
    card.appendChild(meta);
    coffeeGrid.appendChild(card);
  });

  coffeeSection.appendChild(coffeeTitle);
  coffeeSection.appendChild(coffeeText);
  coffeeSection.appendChild(coffeeGrid);
  page.appendChild(coffeeSection);

  const shotSection = document.createElement('section');
  shotSection.id = 'shots';
  const shotTitle = document.createElement('h2');
  shotTitle.textContent = 'Journal d\'extraction';
  const shotText = document.createElement('p');
  shotText.textContent = 'Derniers shots enregistrés, ratio et eau utilisée.';

  const shotGrid = document.createElement('div');
  shotGrid.className = 'card-grid';

  shots.forEach((shot) => {
    const card = document.createElement('article');
    card.className = 'card';
    const h3 = document.createElement('h3');
    h3.textContent = shot.coffee;
    const meta = document.createElement('p');
    meta.className = 'muted';
    meta.textContent = `${shot.beverage} • ${shot.ratio} • Eau : ${shot.water}`;
    card.appendChild(h3);
    card.appendChild(meta);
    shotGrid.appendChild(card);
  });

  shotSection.appendChild(shotTitle);
  shotSection.appendChild(shotText);
  shotSection.appendChild(shotGrid);
  page.appendChild(shotSection);

  const verdictSection = document.createElement('section');
  verdictSection.id = 'verdicts';
  const verdictTitle = document.createElement('h2');
  verdictTitle.textContent = 'Dégustation & verdicts';
  const verdictText = document.createElement('p');
  verdictText.textContent = 'Décisions résumées en mots, sans chiffres.';

  const verdictGrid = document.createElement('div');
  verdictGrid.className = 'card-grid';

  verdicts.forEach((verdict) => {
    verdictGrid.appendChild(createList(verdict.coffee, [verdict.verdict, ...verdict.details]));
  });

  verdictSection.appendChild(verdictTitle);
  verdictSection.appendChild(verdictText);
  verdictSection.appendChild(verdictGrid);
  page.appendChild(verdictSection);

  root.innerHTML = '';
  root.appendChild(page);
}

renderStaticPage();
