import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from '@/App';
import type { Dashboard } from '@/spec';

import '@/index.css';

const dashboard: Dashboard = JSON.parse(document.getElementById('dashboard-data')?.textContent ?? '');

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <App dashboard={dashboard} />
  </StrictMode>,
);
