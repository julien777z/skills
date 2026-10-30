import { CircleAlert, CircleCheck, Info, type LucideIcon, TriangleAlert } from 'lucide-react';

import { Change, PullRequestState, Tone } from '@/spec';

export type ToneName = Tone | 'neutral';

export type ChangeName = Change | 'unchanged';

interface ToneStyle {
  dot: string;
  badge: string;
  alert: string;
  border: string;
  color: string;
  text: string;
  icon: LucideIcon;
}

interface ChangeStyle {
  label: string;
  tone: ToneName;
  dashed: boolean;
}

interface PullRequestStyle {
  label: string;
  tone: ToneName;
  path: string;
}

export const TONES: Record<ToneName, ToneStyle> = {
  [Tone.GOOD]: {
    dot: 'bg-good',
    badge: 'border-good/30 bg-good/15 text-good',
    alert: 'border-good/40 bg-good/10 [&>svg]:text-good',
    border: 'border-good',
    color: 'good',
    text: 'text-good',
    icon: CircleCheck,
  },
  [Tone.WARNING]: {
    dot: 'bg-warning',
    badge: 'border-warning/30 bg-warning/15 text-warning',
    alert: 'border-warning/40 bg-warning/10 [&>svg]:text-warning',
    border: 'border-warning',
    color: 'warning',
    text: 'text-warning',
    icon: TriangleAlert,
  },
  [Tone.CRITICAL]: {
    dot: 'bg-critical',
    badge: 'border-critical/30 bg-critical/15 text-critical',
    alert: 'border-critical/40 bg-critical/10 [&>svg]:text-critical',
    border: 'border-critical',
    color: 'critical',
    text: 'text-critical',
    icon: CircleAlert,
  },
  [Tone.ACCENT]: {
    dot: 'bg-info',
    badge: 'border-info/30 bg-info/15 text-info',
    alert: 'border-info/40 bg-info/10 [&>svg]:text-info',
    border: 'border-info',
    color: 'info',
    text: 'text-info',
    icon: Info,
  },
  [Tone.DONE]: {
    dot: 'bg-done',
    badge: 'border-done/30 bg-done/15 text-done',
    alert: 'border-done/40 bg-done/10 [&>svg]:text-done',
    border: 'border-done',
    color: 'done',
    text: 'text-done',
    icon: CircleCheck,
  },
  neutral: {
    dot: 'bg-muted-foreground',
    badge: 'border-border bg-muted text-muted-foreground',
    alert: '',
    border: 'border-muted-foreground',
    color: 'muted-foreground',
    text: 'text-muted-foreground',
    icon: Info,
  },
};

export const CHANGES: Record<ChangeName, ChangeStyle> = {
  [Change.ADDED]: { label: 'Added', tone: Tone.GOOD, dashed: false },
  [Change.CHANGED]: { label: 'Changed', tone: Tone.ACCENT, dashed: false },
  [Change.REMOVED]: { label: 'Removed', tone: Tone.CRITICAL, dashed: true },
  unchanged: { label: 'Unchanged', tone: 'neutral', dashed: false },
};

export const PULL_REQUESTS: Record<PullRequestState, PullRequestStyle> = {
  [PullRequestState.OPEN]: {
    label: 'Open pull request',
    tone: Tone.GOOD,
    path: 'M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z',
  },
  [PullRequestState.DRAFT]: {
    label: 'Draft pull request',
    tone: 'neutral',
    path: 'M3.25 1A2.25 2.25 0 0 1 4 5.372v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.251 2.251 0 0 1 3.25 1Zm9.5 14a2.25 2.25 0 1 1 0-4.5 2.25 2.25 0 0 1 0 4.5ZM2.5 3.25a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0ZM3.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm9.5 0a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM14 7.5a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0Zm0-4.25a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0Z',
  },
  [PullRequestState.MERGED]: {
    label: 'Merged pull request',
    tone: Tone.DONE,
    path: 'M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z',
  },
  [PullRequestState.CLOSED]: {
    label: 'Closed pull request',
    tone: Tone.CRITICAL,
    path: 'M3.25 1A2.25 2.25 0 0 1 4 5.372v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.251 2.251 0 0 1 3.25 1Zm9.5 5.5a.75.75 0 0 1 .75.75v3.378a2.251 2.251 0 1 1-1.5 0V7.25a.75.75 0 0 1 .75-.75Zm-2.03-5.273a.75.75 0 0 1 1.06 0l.97.97.97-.97a.748.748 0 0 1 1.265.332.75.75 0 0 1-.205.729l-.97.97.97.97a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018l-.97-.97-.97.97a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734l.97-.97-.97-.97a.75.75 0 0 1 0-1.06ZM2.5 3.25a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0ZM3.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm9.5 0a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z',
  },
};
