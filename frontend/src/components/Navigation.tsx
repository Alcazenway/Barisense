import type { ReactNode } from 'react';

interface NavigationItem {
  id: string;
  title: string;
  description: string;
  eyebrow?: string;
  badge?: ReactNode;
}

interface NavigationProps {
  items: NavigationItem[];
}

export function Navigation({ items }: NavigationProps) {
  return (
    <nav className="app-nav" aria-label="Navigation rapide">
      {items.map((item) => (
        <a key={item.id} className="app-nav__item" href={`#${item.id}`}>
          <div>
            <p className="eyebrow">{item.eyebrow ?? 'Section'}</p>
            <h3>{item.title}</h3>
            <p className="app-nav__description">{item.description}</p>
          </div>
          {item.badge ? (
            <span className="app-nav__badge">{item.badge}</span>
          ) : (
            <span aria-hidden="true">↗</span>
          )}
        </a>
      ))}
    </nav>
  );
}
