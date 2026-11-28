import type { ReactNode } from 'react';

import { Badge } from '@/components/ui/badge';
import { TONES, ToneName } from '@/lib/tone';
import { cn } from '@/lib/utils';
import { ToneDot } from './tone-dot';

export function StatusBadge({
  label,
  tone = ToneName.NEUTRAL,
  dot = true,
}: {
  label: string;
  tone?: ToneName;
  dot?: boolean;
}): ReactNode {
  return (
    <Badge variant="outline" className={cn('gap-1.5 tabular-nums', TONES[tone].badge)}>
      {dot && <ToneDot tone={tone} />}
      {label}
    </Badge>
  );
}
