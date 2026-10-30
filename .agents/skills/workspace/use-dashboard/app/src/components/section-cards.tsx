import { Badge } from '@/components/ui/badge';
import { Card, CardAction, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TONE_DOT } from '@/lib/tone';
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

function ProgressCard({ progress }: { progress: ProgressSummary }) {
  const percent = Math.round(progress.value * 100);

  return (
    <Card className="@container/card @xl/main:col-span-2">
      <CardHeader>
        <CardDescription>{progress.label}</CardDescription>
        <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">{percent}%</CardTitle>
        {progress.detail && (
          <CardAction>
            <Badge variant="outline">{progress.detail}</Badge>
          </CardAction>
        )}
      </CardHeader>
      <CardFooter className="flex-col items-stretch gap-2">
        {progress.segments ? (
          <div aria-hidden="true" className="flex h-2 gap-0.5">
            {progress.segments.map((segment, index) => (
              <span
                key={`${segment.label}-${index}`}
                title={segment.label}
                style={{ flexGrow: segment.weight ?? 1 }}
                className={cn('basis-0 rounded-[2px]', segment.tone ? TONE_DOT[segment.tone] : 'bg-foreground/15')}
              />
            ))}
          </div>
        ) : (
          <Progress value={percent} aria-hidden="true" />
        )}
        <meter className="sr-only" min={0} max={100} value={percent} aria-label={progress.label} />
      </CardFooter>
    </Card>
  );
}

export function SectionCards({ progress, metrics }: { progress?: ProgressSummary; metrics: Metric[] }) {
  const columns = (progress ? 2 : 0) + metrics.length;

  return (
    <div
      className={cn(
        'grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 dark:*:data-[slot=card]:bg-card',
        WIDE_COLUMNS[columns],
      )}
    >
      {progress && <ProgressCard progress={progress} />}
      {metrics.map((metric) => (
        <Card key={metric.label} className="@container/card">
          <CardHeader>
            <CardDescription>{metric.label}</CardDescription>
            <CardTitle className="text-2xl font-semibold tabular-nums [overflow-wrap:anywhere] @[250px]/card:text-3xl">
              {metric.value}
            </CardTitle>
          </CardHeader>
          {metric.detail && <CardFooter className="text-sm text-muted-foreground">{metric.detail}</CardFooter>}
        </Card>
      ))}
    </div>
  );
}
