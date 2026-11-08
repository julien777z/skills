import { useEffect, useState } from 'react';

import type { Dashboard } from '@/spec';

declare global {
  interface Window {
    dashboardUpdate?: DashboardUpdate;
  }
}

interface DashboardUpdate {
  app: string;
  dashboard: Dashboard;
}

const UPDATE_CHECK_INTERVAL_MS: number = 2_000;

const UPDATE_SCRIPT_SUFFIX: string = '.update.js';

interface ReloadState {
  scroll: number;
}

function isReloadState(state: unknown): state is ReloadState {
  return typeof state === 'object' && state !== null && 'scroll' in state && typeof state.scroll === 'number';
}

export function useDashboardUpdates(initial: Dashboard): Dashboard {
  const [dashboard, setDashboard] = useState(initial);

  useEffect(() => {
    const reloadState: unknown = window.history.state;

    if (isReloadState(reloadState)) {
      window.history.replaceState(null, '', window.location.href);
      window.scrollTo({ top: reloadState.scroll });
    }

    const appRevision = document.getElementById('dashboard-app-revision')?.textContent;

    if (window.location.protocol !== 'file:' || !appRevision) {
      return;
    }

    const scriptAddress = window.location.href.split(/[?#]/)[0] + UPDATE_SCRIPT_SUFFIX;
    let shown = JSON.stringify(initial);

    function checkForUpdate() {
      const script = document.createElement('script');

      script.src = `${scriptAddress}?checked=${Date.now()}`;

      script.onload = () => {
        script.remove();

        const update = window.dashboardUpdate;

        if (!update) {
          return;
        }

        if (update.app !== appRevision) {
          window.history.replaceState({ scroll: window.scrollY } satisfies ReloadState, '', window.location.href);
          window.location.reload();

          return;
        }

        const serialized = JSON.stringify(update.dashboard);

        if (serialized !== shown) {
          shown = serialized;
          document.title = `${update.dashboard.title} - ${update.dashboard.topic}`;

          setDashboard(update.dashboard);
        }
      };

      script.onerror = () => script.remove();

      document.head.append(script);
    }

    const timer = window.setInterval(checkForUpdate, UPDATE_CHECK_INTERVAL_MS);

    return () => window.clearInterval(timer);
  }, [initial]);

  return dashboard;
}
