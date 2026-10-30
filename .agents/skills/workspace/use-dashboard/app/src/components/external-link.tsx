import type { ReactNode } from 'react';

import { safeUrl } from '@/lib/references';

export function ExternalLink({ href, children }: { href: string; children: ReactNode }): ReactNode {
  const url = safeUrl(href);

  if (!url) {
    return children;
  }

  return (
    <a href={url} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  );
}
