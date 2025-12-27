import type {
  InputHTMLAttributes,
  ReactNode,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from 'react';

type FieldElement = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
type FieldAttributes = InputHTMLAttributes<HTMLInputElement> &
  SelectHTMLAttributes<HTMLSelectElement> &
  TextareaHTMLAttributes<HTMLTextAreaElement>;

interface FormFieldProps extends FieldAttributes {
  label: string;
  helper?: ReactNode;
  as?: 'input' | 'select' | 'textarea';
  error?: string;
  datalistId?: string;
  datalistOptions?: string[];
}

export function FormField({
  label,
  helper,
  error,
  as = 'input',
  children,
  datalistId,
  datalistOptions,
  ...rest
}: FormFieldProps) {
  const sharedProps: FieldAttributes & { 'aria-invalid': boolean } = {
    ...rest,
    'aria-invalid': Boolean(error),
    'aria-describedby': error ? `${rest.name}-error` : undefined,
  };

  let control: ReactNode;
  if (as === 'select') {
    control = <select {...sharedProps as SelectHTMLAttributes<HTMLSelectElement>}>{children}</select>;
  } else if (as === 'textarea') {
    control = <textarea {...sharedProps as TextareaHTMLAttributes<HTMLTextAreaElement>} />;
  } else {
    control = (
      <input
        {...sharedProps as InputHTMLAttributes<HTMLInputElement>}
        list={datalistId}
      />
    );
  }

  return (
    <label className={`form-field${error ? ' form-field--error' : ''}`}>
      <span className="form-field__label">{label}</span>
      {control}
      {datalistId && datalistOptions && as === 'input' ? (
        <datalist id={datalistId}>
          {datalistOptions.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>
      ) : null}
      {error ? (
        <span className="form-field__error" id={`${rest.name}-error`}>{error}</span>
      ) : helper ? (
        <span className="form-field__helper">{helper}</span>
      ) : null}
    </label>
  );
}
