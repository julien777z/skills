import type { ReactNode } from 'react';

import { Text } from '@/components/primitives';
import { formatMoment } from '@/lib/time';
import { RichText } from './rich-text';

export function ItemMeta({ tag, meta, at }: { tag?: string; meta?: string; at?: string }): ReactNode {
  if (!tag && !meta && !at) {
    return null;
  }

  const parts: ReactNode[] = [
    tag && <RichText key="tag" text={tag} />,
    meta && <RichText key="meta" text={meta} />,
    at && (
      <time key="at" dateTime={at}>
        {formatMoment(at, Date.now())}
      </time>
    ),
  ].filter(Boolean);

  return (
    <Text size="xs" tone="muted" numeric>
      {parts.flatMap((part, position) => (position === 0 ? [part] : [' · ', part]))}
    </Text>
  );
}
