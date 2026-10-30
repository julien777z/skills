import type { Change, Tone } from '@/spec';

export const TONE_DOT: Record<Tone, string> = {
  good: 'bg-good',
  warning: 'bg-warning',
  critical: 'bg-critical',
  accent: 'bg-info',
  done: 'bg-done',
};

export const TONE_BADGE: Record<Tone, string> = {
  good: 'border-good/30 bg-good/15 text-good',
  warning: 'border-warning/30 bg-warning/15 text-warning',
  critical: 'border-critical/30 bg-critical/15 text-critical',
  accent: 'border-info/30 bg-info/15 text-info',
  done: 'border-done/30 bg-done/15 text-done',
};

export const TONE_ALERT: Record<Tone, string> = {
  good: 'border-good/40 bg-good/10 [&>svg]:text-good',
  warning: 'border-warning/40 bg-warning/10 [&>svg]:text-warning',
  critical: 'border-critical/40 bg-critical/10 [&>svg]:text-critical',
  accent: 'border-info/40 bg-info/10 [&>svg]:text-info',
  done: 'border-done/40 bg-done/10 [&>svg]:text-done',
};

export const NEUTRAL_DOT = 'bg-muted-foreground';

export const NEUTRAL_BADGE = 'border-border bg-muted text-muted-foreground';

export interface ChangeStyle {
  label: string;
  tone?: Tone;
}

export const CHANGE_STYLES: Record<Change | 'same', ChangeStyle> = {
  added: { label: 'Added', tone: 'good' },
  changed: { label: 'Changed', tone: 'accent' },
  removed: { label: 'Removed', tone: 'critical' },
  same: { label: 'Unchanged' },
};
