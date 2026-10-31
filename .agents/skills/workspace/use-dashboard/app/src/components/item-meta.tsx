import type { ReactNode } from 'react';

import { Text } from '@/components/primitives';
import { formatMoment } from '@/lib/time';
import { RichText } from './rich-text';

export function ItemMeta({ meta, at }: { meta?: string; at?: string }): ReactNode {
  if (!meta && !at) {
    return null;
  }

  return (
    <Text size="xs" tone="muted" numeric>
      {meta && <RichText text={meta} />}
      {meta && at && ' · '}
      {at && <time dateTime={at}>{formatMoment(at, Date.now())}</time>}
    </Text>
  );
}
