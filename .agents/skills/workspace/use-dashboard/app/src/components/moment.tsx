import type { ReactNode } from 'react';

import { formatMoment } from '@/lib/time';

export function Moment({ at }: { at: string }): ReactNode {
  return <time dateTime={at}>{formatMoment(at, Date.now())}</time>;
}
