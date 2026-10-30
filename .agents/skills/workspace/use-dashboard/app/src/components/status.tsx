import { Badge } from '@/components/ui/badge';
import { NEUTRAL_BADGE, NEUTRAL_DOT, TONE_BADGE, TONE_DOT } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { Tone } from '@/spec';

export function ToneDot({ tone, className }: { tone?: Tone; className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cn('size-2 shrink-0 rounded-full', tone ? TONE_DOT[tone] : NEUTRAL_DOT, className)}
    />
  );
}

export function StatusBadge({ label, tone, className }: { label: string; tone?: Tone; className?: string }) {
  return (
    <Badge variant="outline" className={cn('gap-1.5', tone ? TONE_BADGE[tone] : NEUTRAL_BADGE, className)}>
      <ToneDot tone={tone} />
      {label}
    </Badge>
  );
}
