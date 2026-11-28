import type { ReactNode } from 'react';

import { Badge } from '@/components/ui/badge';
import { ToneName } from '@/lib/tone';
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
    <Badge variant="outline" className="px-1.5 text-muted-foreground tabular-nums">
      {dot && <ToneDot tone={tone} />}
      {label}
    </Badge>
  );
}
