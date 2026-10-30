import type { ReactNode } from 'react';

import { ToneDot } from '@/components/tone-dot';
import { Badge } from '@/components/ui/badge';
import { TONES, type ToneName } from '@/lib/tone';
import { cn } from '@/lib/utils';

export function StatusBadge({
  label,
  tone = 'neutral',
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
