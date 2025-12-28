import { fireEvent, render, screen, within } from '@testing-library/react';

import App from './App';
import { coffees, justifiedVerdicts, leaderboardSlices, shots } from './data/sampleData';

describe('App', () => {
  it('affiche les métriques clés et la navigation segmentée', () => {
    render(<App />);

    expect(screen.getByText('Collecte, dégustation et verdicts')).toBeInTheDocument();
    expect(screen.getByText(`${coffees.length} cafés suivis`)).toBeInTheDocument();
    expect(screen.getByText(`${shots.length} extractions notées`)).toBeInTheDocument();
    expect(screen.getByText(`${justifiedVerdicts.length} verdicts`)).toBeInTheDocument();

    expect(screen.getByText('Collecte segmentée')).toBeInTheDocument();
    expect(screen.getByText('Analyses & décisions')).toBeInTheDocument();
    expect(screen.getByText('Synthèse & classements')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: /Synthèse/i }));
    leaderboardSlices[0].entries.forEach((entry) => {
      expect(screen.getAllByText(entry.coffee).length).toBeGreaterThan(0);
    });
  });

  it('met à jour les statuts des brouillons lors de la soumission des formulaires', () => {
    render(<App />);

    fireEvent.click(screen.getByRole('tab', { name: /Collecte/i }));

    const coffeeForm = screen.getByLabelText('Torréfacteur').closest('form');
    const shotForm = screen.getByPlaceholderText('6.0').closest('form');
    const tastingForm = screen.getByLabelText('Arômes dominants').closest('form');

    // Renseigner les champs requis pour déclencher une soumission valide
    if (coffeeForm) {
      fireEvent.change(within(coffeeForm).getByLabelText('Torréfacteur'), { target: { value: 'Test Roaster' } });
      fireEvent.change(within(coffeeForm).getByLabelText('Référence'), { target: { value: 'Blend X' } });
      fireEvent.change(within(coffeeForm).getByLabelText('Type'), { target: { value: 'Grain' } });
      fireEvent.submit(coffeeForm);
    }

    if (shotForm) {
      fireEvent.change(within(shotForm).getByLabelText('Café utilisé'), { target: { value: coffees[0].name } });
      fireEvent.change(within(shotForm).getByLabelText('Boisson'), { target: { value: 'Expresso' } });
      fireEvent.submit(shotForm);
    }

    if (tastingForm) {
      fireEvent.change(within(tastingForm).getByLabelText('Café dégusté'), { target: { value: coffees[0].name } });
      fireEvent.change(within(tastingForm).getByLabelText('Arômes dominants'), { target: { value: 'fruits jaunes' } });
      fireEvent.change(within(tastingForm).getByLabelText('Texture'), { target: { value: 'rond' } });
      fireEvent.change(within(tastingForm).getByLabelText('Finale'), { target: { value: 'longueur' } });
      fireEvent.change(within(tastingForm).getByLabelText('Verdict'), { target: { value: 'Racheter' } });
      fireEvent.submit(tastingForm);
    }

    expect(screen.getAllByText(/Brouillon prêt/)).toHaveLength(3);
  });
});
