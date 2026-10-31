import type { ReactNode } from 'react';

import { linkAttributes } from '@/lib/references';

export function ExternalLink({ href, children }: { href: string; children: ReactNode }): ReactNode {
  const attributes = linkAttributes(href);

  if (!attributes) {
    return children;
  }

  return <a {...attributes}>{children}</a>;
}
