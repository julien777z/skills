import { cn } from 'cn';
import type { ReactNode } from 'react';
import { TONES, ToneName } from '@/lib/tone';

export function ToneDot({ tone = ToneName.NEUTRAL, offset = false }: { tone?: ToneName; offset?: boolean }): ReactNode {
  return (
    <span aria-hidden="true" className={cn('size-2 shrink-0 rounded-full', offset && 'mt-1.5', TONES[tone].dot)} />
  );
}
