import type { ReactNode } from 'react';

interface PillProps {
  tone?: 'success' | 'warning' | 'info' | 'danger';
  children: ReactNode;
}

export function Pill({ tone = 'info', children }: PillProps) {
  return <span className={`pill pill--${tone}`}>{children}</span>;
}
