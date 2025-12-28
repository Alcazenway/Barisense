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
  activeId?: string;
  onSelect?: (id: string) => void;
}

export function Navigation({ items, activeId, onSelect }: NavigationProps) {
  return (
    <nav className="app-nav" aria-label="Navigation rapide">
      {items.map((item) => (
        <a
          key={item.id}
          className={`app-nav__item${activeId === item.id ? ' app-nav__item--active' : ''}`}
          href={`#${item.id}`}
          onClick={(event) => {
            if (!onSelect) return;
            event.preventDefault();
            onSelect(item.id);
            requestAnimationFrame(() => {
              const target = document.getElementById(item.id);
              if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            });
          }}
        >
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
