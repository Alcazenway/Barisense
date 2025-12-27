import type { InputHTMLAttributes, ReactNode } from 'react';

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement | HTMLSelectElement> {
  label: string;
  helper?: ReactNode;
  as?: 'input' | 'select';
}

export function FormField({ label, helper, as = 'input', children, ...rest }: FormFieldProps) {
  return (
    <label className="form-field">
      <span className="form-field__label">{label}</span>
      {as === 'select' ? (
        <select {...rest}>{children}</select>
      ) : (
        <input {...rest} />
      )}
      {helper ? <span className="form-field__helper">{helper}</span> : null}
    </label>
  );
}
