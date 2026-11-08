import { useEffect } from 'react';

declare global {
  interface Window {
    dashboardRevision?: string;
  }
}

const REVISION_CHECK_INTERVAL_MS: number = 2_000;

const REVISION_SCRIPT_SUFFIX: string = '.revision.js';

interface ReloadState {
  scroll: number;
}

function isReloadState(state: unknown): state is ReloadState {
  return typeof state === 'object' && state !== null && 'scroll' in state && typeof state.scroll === 'number';
}

export function useReloadOnNewRevision(): void {
  useEffect(() => {
    const reloadState: unknown = window.history.state;

    if (isReloadState(reloadState)) {
      window.history.replaceState(null, '', window.location.href);
      window.scrollTo({ top: reloadState.scroll });
    }

    const revision = document.getElementById('dashboard-revision')?.textContent;

    if (window.location.protocol !== 'file:' || !revision) {
      return;
    }

    const scriptAddress = window.location.href.split('#')[0] + REVISION_SCRIPT_SUFFIX;

    function checkRevision() {
      const script = document.createElement('script');

      script.src = `${scriptAddress}?checked=${Date.now()}`;

      script.onload = () => {
        script.remove();

        if (window.dashboardRevision && window.dashboardRevision !== revision) {
          window.history.replaceState({ scroll: window.scrollY } satisfies ReloadState, '', window.location.href);
          window.location.reload();
        }
      };

      script.onerror = () => script.remove();

      document.head.append(script);
    }

    const timer = window.setInterval(checkRevision, REVISION_CHECK_INTERVAL_MS);

    return () => window.clearInterval(timer);
  }, []);
}
