import { fireEvent, render, screen, within } from '@testing-library/react';

import App from './App';

beforeEach(() => {
  localStorage.clear();
});

describe('App', () => {
  it('affiche la navigation principale et la vue Hub', () => {
    render(<App />);

    expect(screen.getByText(/MonExpresso/i)).toBeInTheDocument();
    const nav = screen.getByRole('navigation', { name: /Navigation principale/i });
    expect(within(nav).getByRole('button', { name: /Hub/i })).toBeInTheDocument();
    expect(within(nav).getByRole('button', { name: /Cave/i })).toBeInTheDocument();
    expect(within(nav).getByRole('button', { name: /Shot/i })).toBeInTheDocument();
    expect(within(nav).getByRole('button', { name: /Elite/i })).toBeInTheDocument();
    expect(within(nav).getByRole('button', { name: /Journal/i })).toBeInTheDocument();

    expect(screen.getByText(/Barista en service/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Shots/i)).toBeInTheDocument();
  });

  it('permet d’ajouter un café et de l’ouvrir', () => {
    render(<App />);

    fireEvent.click(screen.getByRole('button', { name: /Cave/i }));
    fireEvent.click(screen.getByRole('button', { name: /\+ Ajouter/i }));

    const form = screen.getByPlaceholderText('Nom du café (ex: Honduras)').closest('form');
    expect(form).not.toBeNull();

    if (form) {
      fireEvent.change(within(form).getByPlaceholderText('Nom du café (ex: Honduras)'), {
        target: { value: 'Test Café' },
      });
      fireEvent.change(within(form).getByPlaceholderText('Torréfacteur (ex: Lomi)'), {
        target: { value: 'Test Roaster' },
      });
      fireEvent.change(within(form).getByPlaceholderText('Origine'), { target: { value: 'Kenya' } });
      fireEvent.change(within(form).getByLabelText('Intensité (1-10)'), { target: { value: '7' } });
      fireEvent.submit(form);
    }

    const cafeCard = screen.getByText('Test Café').closest('[role=\"button\"]');
    expect(cafeCard).not.toBeNull();
    if (cafeCard) {
      const openButton = within(cafeCard).getByRole('button', { name: /Ouvrir/i });
      fireEvent.click(openButton);
    }

    expect(screen.getByText('Test Café')).toBeInTheDocument();
    expect(screen.getByText(/Barista en service/i)).toBeInTheDocument();
  });
});
