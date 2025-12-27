import { render, screen } from '@testing-library/react';

import { FormField } from './FormField';

describe('FormField', () => {
  it('affiche le label, le champ et le helper', () => {
    render(<FormField label="Poids" name="weight" helper="En grammes" placeholder="250" />);

    expect(screen.getByLabelText('Poids')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('250')).toBeInTheDocument();
    expect(screen.getByText('En grammes')).toBeInTheDocument();
  });

  it('rend un select lorsque le type select est demandé', () => {
    render(
      <FormField label="Eau" name="water" as="select" defaultValue="">
        <option value="" disabled>
          Choisir
        </option>
        <option value="volvic">Volvic</option>
      </FormField>,
    );

    expect(screen.getByRole('combobox', { name: 'Eau' })).toBeInTheDocument();
    expect(screen.getByText('Volvic')).toBeInTheDocument();
  });
});
