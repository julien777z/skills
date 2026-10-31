import type { ComponentProps, ReactNode } from 'react';

import { Grid, Text } from '@/components/primitives';
import { Card, CardAction, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TONES } from '@/lib/tone';
import { cn, withKeys } from '@/lib/utils';
import type { Metric, ProgressSummary } from '@/spec';
import { RichText } from './rich-text';
import { StatusBadge } from './status-badge';

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
    <Card
      className={cn(
        '@container/card bg-gradient-to-t from-primary/5 to-card shadow-xs dark:bg-card',
        wide && '@xl/page:col-span-2',
      )}
    >
      <CardHeader>
        <CardDescription>
          <RichText text={label} />
        </CardDescription>
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
          {withKeys(progress.segments, (segment) => segment.label).map(({ key, item: segment }) => (
            <span
              key={key}
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

const STAT_COLUMNS: Record<number, NonNullable<ComponentProps<typeof Grid>['columns']>> = {
  1: 'stats2',
  2: 'stats2',
  3: 'stats3',
  4: 'stats4',
  5: 'stats5',
  6: 'stats6',
};

export function SectionCards({ progress, metrics }: { progress?: ProgressSummary; metrics: Metric[] }): ReactNode {
  const columns = (progress ? 2 : 0) + metrics.length;
  const percent = progress ? Math.round(progress.value * 100) : 0;

  return (
    <Grid columns={STAT_COLUMNS[columns]} inset="page" align="stretch">
      {progress && (
        <StatCard label={progress.label} figure={`${percent}%`} badge={progress.detail} wide>
          <ProgressBar progress={progress} percent={percent} />
        </StatCard>
      )}
      {withKeys(metrics, (metric) => metric.label).map(({ key, item: metric }) => (
        <StatCard key={key} label={metric.label} figure={metric.value}>
          {metric.detail && (
            <Text size="sm" tone="muted">
              <RichText text={metric.detail} />
            </Text>
          )}
        </StatCard>
      ))}
    </Grid>
  );
}
