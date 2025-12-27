import { fireEvent, render, screen, within } from '@testing-library/react';

import App from './App';
import { coffees, leaderboard, shots, tastingVerdicts } from './data/sampleData';

describe('App', () => {
  it('affiche les métriques clés et la navigation', () => {
    render(<App />);

    expect(screen.getByText('Collecte, dégustation et verdicts')).toBeInTheDocument();
    expect(screen.getByText(`${coffees.length} cafés suivis`)).toBeInTheDocument();
    expect(screen.getByText(`${shots.length} extractions notées`)).toBeInTheDocument();
    expect(screen.getByText(`${tastingVerdicts.length} verdicts`)).toBeInTheDocument();

    leaderboard.forEach((entry) => {
      expect(screen.getByText(entry.coffee)).toBeInTheDocument();
    });
  });

  it('met à jour les statuts des brouillons lors de la soumission des formulaires', () => {
    render(<App />);

    const coffeeForm = screen.getByLabelText('Torréfacteur').closest('form');
    const shotForm = screen.getByLabelText('Mouture').closest('form');
    const tastingForm = screen.getByLabelText('Arômes dominants').closest('form');

    // Renseigner les champs requis pour déclencher une soumission valide
    if (coffeeForm) {
      fireEvent.change(within(coffeeForm).getByLabelText('Torréfacteur'), { target: { value: 'Test Roaster' } });
      fireEvent.change(within(coffeeForm).getByLabelText('Référence'), { target: { value: 'Blend X' } });
      fireEvent.submit(coffeeForm);
    }

    if (shotForm) {
      fireEvent.change(within(shotForm).getByLabelText('Café utilisé'), { target: { value: coffees[0].name } });
      fireEvent.change(within(shotForm).getByLabelText('Boisson'), { target: { value: 'Expresso' } });
      fireEvent.submit(shotForm);
    }

    if (tastingForm) {
      fireEvent.change(within(tastingForm).getByLabelText('Café dégusté'), { target: { value: coffees[0].name } });
      fireEvent.submit(tastingForm);
    }

    expect(screen.getAllByText(/Brouillon prêt/)).toHaveLength(3);
  });
});
