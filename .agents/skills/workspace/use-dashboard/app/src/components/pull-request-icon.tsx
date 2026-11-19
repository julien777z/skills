import type { ReactNode } from 'react';

import { PULL_REQUESTS } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { PullRequestState } from '@/spec';

export function PullRequestIcon({ state, className }: { state: PullRequestState; className?: string }): ReactNode {
  const style = PULL_REQUESTS[state];

  return (
    <svg viewBox="0 0 16 16" role="img" className={cn('fill-current', className)}>
      <title>{style.label}</title>
      <path d={style.path} />
    </svg>
  );
}
