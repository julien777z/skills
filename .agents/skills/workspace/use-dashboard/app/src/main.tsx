import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from '@/App';
import type { Dashboard } from '@/spec';

import '@/index.css';

const root = document.getElementById('root');
const data = document.getElementById('dashboard-data');

if (root) {
  try {
    const dashboard = JSON.parse(data?.textContent ?? '') as Dashboard;

    createRoot(root).render(
      <StrictMode>
        <App dashboard={dashboard} />
      </StrictMode>,
    );
  } catch (error) {
    root.textContent = `This dashboard's data could not be read: ${error instanceof Error ? error.message : String(error)}`;
  }
}
