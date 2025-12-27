import type { ReactNode } from 'react';

interface SectionCardProps {
  id?: string;
  title: string;
  subtitle?: string;
  action?: ReactNode;
  children: ReactNode;
}

export function SectionCard({ id, title, subtitle, action, children }: SectionCardProps) {
  return (
    <section className="section-card" id={id}>
      <header className="section-card__header">
        <div>
          <p className="eyebrow">{subtitle ?? 'Workflow'}</p>
          <h2>{title}</h2>
        </div>
        {action}
      </header>
      <div className="section-card__body">{children}</div>
    </section>
  );
}
