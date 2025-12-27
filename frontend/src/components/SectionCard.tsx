import type { ReactNode } from 'react';

interface SectionCardProps {
  title: string;
  subtitle?: string;
  action?: ReactNode;
  children: ReactNode;
}

export function SectionCard({ title, subtitle, action, children }: SectionCardProps) {
  return (
    <section className="section-card">
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
