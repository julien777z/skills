import type { ReactNode } from 'react';

import { Text } from '@/components/primitives';
import { StatusBadge } from '@/components/status-badge';
import { Card, CardAction, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TONES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { Metric, ProgressSummary } from '@/spec';

const WIDE_COLUMNS: Record<number, string> = {
  1: '@5xl/main:grid-cols-1',
  2: '@5xl/main:grid-cols-2',
  3: '@5xl/main:grid-cols-3',
  4: '@5xl/main:grid-cols-4',
  5: '@5xl/main:grid-cols-5',
  6: '@5xl/main:grid-cols-6',
};

function StatCard({
  label,
  figure,
  badge,
  wide = false,
  children,
}: {
  label: string;
  figure: string;
  badge?: string;
  wide?: boolean;
  children?: ReactNode;
}): ReactNode {
  return (
    <Card className={cn('@container/card', wide && '@xl/main:col-span-2')}>
      <CardHeader>
        <CardDescription>{label}</CardDescription>
        <CardTitle>
          <Text size="figure" weight="semibold" numeric breakAnywhere>
            {figure}
          </Text>
        </CardTitle>
        {badge && (
          <CardAction>
            <StatusBadge label={badge} dot={false} />
          </CardAction>
        )}
      </CardHeader>
      {children && <CardFooter className="flex-col items-stretch gap-2">{children}</CardFooter>}
    </Card>
  );
}

function ProgressBar({ progress, percent }: { progress: ProgressSummary; percent: number }): ReactNode {
  return (
    <>
      {progress.segments ? (
        <div aria-hidden="true" className="flex h-2 gap-0.5">
          {progress.segments.map((segment, index) => (
            <span
              key={index}
              title={segment.label}
              style={{ flexGrow: segment.weight ?? 1 }}
              className={cn('basis-0 rounded-[2px]', segment.tone ? TONES[segment.tone].dot : 'bg-foreground/15')}
            />
          ))}
        </div>
      ) : (
        <Progress value={percent} aria-hidden="true" />
      )}
      <meter className="sr-only" min={0} max={100} value={percent} aria-label={progress.label} />
    </>
  );
}

export function SectionCards({ progress, metrics }: { progress?: ProgressSummary; metrics: Metric[] }): ReactNode {
  const columns = (progress ? 2 : 0) + metrics.length;
  const percent = progress ? Math.round(progress.value * 100) : 0;

  return (
    <div
      className={cn(
        'grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 dark:*:data-[slot=card]:bg-card',
        WIDE_COLUMNS[columns],
      )}
    >
      {progress && (
        <StatCard label={progress.label} figure={`${percent}%`} badge={progress.detail} wide>
          <ProgressBar progress={progress} percent={percent} />
        </StatCard>
      )}
      {metrics.map((metric, index) => (
        <StatCard key={index} label={metric.label} figure={metric.value}>
          {metric.detail && (
            <Text size="sm" tone="muted">
              {metric.detail}
            </Text>
          )}
        </StatCard>
      ))}
    </div>
  );
}
