import { cn } from 'cn';
import { type ReactNode, useContext, useRef, useState } from 'react';

import { DialogOpener, RichText, StatusBadge, ToneDot } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { formatDuration, formatSpan } from '@/lib/time';
import { TONES, ToneName } from '@/lib/tone';
import { withKeys } from '@/lib/utils';
import type { TimelineBar, TimelineGap, TimelineLane, TimelineSection as TimelineSectionSpec } from '@/spec';
import { InDialogContext, SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

const MINUTE_MS: number = 60_000;

const HOUR_MS: number = 60 * MINUTE_MS;

const DAY_MS: number = 24 * HOUR_MS;

const TICK_INTERVALS_MS: readonly number[] = [
  MINUTE_MS,
  2 * MINUTE_MS,
  5 * MINUTE_MS,
  10 * MINUTE_MS,
  15 * MINUTE_MS,
  30 * MINUTE_MS,
  HOUR_MS,
  2 * HOUR_MS,
  3 * HOUR_MS,
  6 * HOUR_MS,
  12 * HOUR_MS,
  DAY_MS,
  2 * DAY_MS,
  7 * DAY_MS,
];

const MAX_TICKS: number = 6;

const CLOCK_TICK: Intl.DateTimeFormatOptions = { hour: 'numeric', minute: '2-digit', hour12: true };

const DATED_TICK: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric', ...CLOCK_TICK };

const DATE_TICK: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' };

interface Scale {
  start: number;
  span: number;
}

interface Tick {
  at: number;
  label: string;
}

function scaleOf(lanes: TimelineLane[], gaps: TimelineGap[]): Scale {
  const moments = [...lanes.flatMap((lane) => lane.bars), ...gaps].flatMap((span) => [
    Date.parse(span.start),
    Date.parse(span.end),
  ]);
  const start = Math.min(...moments);

  return { start, span: Math.max(MINUTE_MS, Math.max(...moments) - start) };
}

const EDGE_PERCENT: number = 6;

function offset(scale: Scale, at: number): number {
  return ((at - scale.start) / scale.span) * 100;
}

function tickAnchor(left: number): string {
  if (left < EDGE_PERCENT) {
    return 'translate-x-0';
  }

  return left > 100 - EDGE_PERCENT ? '-translate-x-full' : '-translate-x-1/2';
}

function firstTickAt(start: number, interval: number): number {
  const midnight = new Date(start);

  midnight.setHours(0, 0, 0, 0);

  return midnight.getTime() + Math.ceil((start - midnight.getTime()) / interval) * interval;
}

function ticksOf(scale: Scale): Tick[] {
  const end = scale.start + scale.span;
  const interval =
    TICK_INTERVALS_MS.find((candidate) => scale.span / candidate <= MAX_TICKS) ??
    TICK_INTERVALS_MS[TICK_INTERVALS_MS.length - 1];
  const crossesDays = new Date(scale.start).toDateString() !== new Date(end).toDateString();
  const ticks: Tick[] = [];
  let previousDay = '';

  for (let at = firstTickAt(scale.start, interval); at <= end; at += interval) {
    const moment = new Date(at);
    const day = moment.toDateString();
    const dated = crossesDays && day !== previousDay;
    const format = interval >= DAY_MS ? DATE_TICK : dated ? DATED_TICK : CLOCK_TICK;

    ticks.push({ at, label: moment.toLocaleString(undefined, format) });
    previousDay = day;
  }

  return ticks;
}

function placement(scale: Scale, span: { start: string; end: string }): { left: string; width: string } {
  const left = offset(scale, Date.parse(span.start));

  return { left: `${left}%`, width: `${offset(scale, Date.parse(span.end)) - left}%` };
}

function BarMark({ lane, bar, scale }: { lane: TimelineLane; bar: TimelineBar; scale: Scale }): ReactNode {
  const range = formatSpan(bar.start, bar.end, Date.now());
  const duration = formatDuration(Date.parse(bar.end) - Date.parse(bar.start));

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          type="button"
          aria-label={[lane.label, bar.label, range, duration].filter(Boolean).join(', ')}
          style={placement(scale, bar)}
          className={cn(
            'absolute top-1/2 h-3 min-w-[3px] -translate-y-1/2 cursor-default rounded-[3px] outline-none transition-opacity hover:opacity-80 focus-visible:ring-[3px] focus-visible:ring-ring/50',
            TONES[bar.tone ?? ToneName.NEUTRAL].dot,
          )}
        />
      </TooltipTrigger>
      <TooltipContent>
        <Stack gap="xs">
          <Text size="sm" weight="medium">
            {lane.label}
          </Text>
          {bar.label && <Text size="xs">{bar.label}</Text>}
          <Text size="xs" numeric>
            {`${range} · ${duration}`}
          </Text>
        </Stack>
      </TooltipContent>
    </Tooltip>
  );
}

function LaneLabel({ lane }: { lane: TimelineLane }): ReactNode {
  const [showDetails, setShowDetails] = useState(false);
  const opener = useRef<HTMLButtonElement | null>(null);

  return (
    <div className="flex h-8 min-w-0 items-center gap-2">
      <ToneDot tone={lane.tone} />
      <span className="min-w-0 truncate text-sm">
        {lane.details ? (
          <DialogOpener
            opener={opener}
            onOpen={() => setShowDetails(true)}
            className="cursor-pointer text-left focus-visible:underline focus-visible:outline-none"
          >
            {lane.label}
          </DialogOpener>
        ) : (
          <Text as="span" size="sm" weight="medium">
            <RichText text={lane.label} />
          </Text>
        )}
      </span>
      {lane.tag && <StatusBadge label={lane.tag} dot={false} />}
      {lane.details && (
        <SectionDialog section={lane.details} open={showDetails} onOpenChange={setShowDetails} opener={opener} />
      )}
    </div>
  );
}

function GapBand({ gap, scale }: { gap: TimelineGap; scale: Scale }): ReactNode {
  return (
    <div
      aria-hidden="true"
      style={placement(scale, gap)}
      className="absolute inset-y-0 border-x border-dashed border-muted-foreground/40 bg-[repeating-linear-gradient(135deg,color-mix(in_oklab,var(--color-muted-foreground)_30%,transparent)_0_1px,transparent_1px_7px)]"
    />
  );
}

function GapLabel({ gap, scale }: { gap: TimelineGap; scale: Scale }): ReactNode {
  const { left, width } = placement(scale, gap);

  return (
    <span
      style={{ left: `calc(${left} + ${width} / 2)` }}
      className="absolute top-0 -translate-x-1/2 whitespace-nowrap text-xs text-muted-foreground"
    >
      <RichText text={gap.label} />
    </span>
  );
}

export function TimelineSection({ section }: { section: TimelineSectionSpec }): ReactNode {
  const gaps = section.gaps ?? [];
  const scale = scaleOf(section.lanes, gaps);
  const ticks = ticksOf(scale);
  const lanes = withKeys(section.lanes, (lane) => lane.label);
  const inDialog = useContext(InDialogContext);

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <TooltipProvider>
        <ScrollArea type="auto" className="w-full">
          <div className="grid min-w-[48rem] grid-cols-[minmax(8rem,14rem)_minmax(0,1fr)] pb-3">
            <div className={cn('pr-4 sm:sticky sm:left-0 sm:z-10', inDialog ? 'bg-background' : 'bg-card')}>
              <div className="h-6" />
              {gaps.length > 0 && <div className="h-5" />}
              {lanes.map(({ key, item: lane }) => (
                <LaneLabel key={key} lane={lane} />
              ))}
            </div>
            <div className="relative">
              <div aria-hidden="true" className="relative h-6 text-xs text-muted-foreground tabular-nums">
                {withKeys(ticks, (tick) => String(tick.at)).map(({ key, item: tick }) => (
                  <span
                    key={key}
                    style={{ left: `${offset(scale, tick.at)}%` }}
                    className={cn('absolute top-0 whitespace-nowrap', tickAnchor(offset(scale, tick.at)))}
                  >
                    {tick.label}
                  </span>
                ))}
              </div>
              <div className="relative">
                <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
                  {withKeys(ticks, (tick) => String(tick.at)).map(({ key, item: tick }) => (
                    <div
                      key={key}
                      style={{ left: `${offset(scale, tick.at)}%` }}
                      className="absolute inset-y-0 border-l border-border"
                    />
                  ))}
                  {withKeys(gaps, (gap) => gap.start).map(({ key, item: gap }) => (
                    <GapBand key={key} gap={gap} scale={scale} />
                  ))}
                </div>
                {gaps.length > 0 && (
                  <div className="relative h-5">
                    {withKeys(gaps, (gap) => gap.start).map(({ key, item: gap }) => (
                      <GapLabel key={key} gap={gap} scale={scale} />
                    ))}
                  </div>
                )}
                {lanes.map(({ key, item: lane }) => (
                  <div key={key} className="relative h-8 border-b border-border/50 last:border-b-0">
                    {withKeys(lane.bars, (bar) => bar.start).map(({ key: barKey, item: bar }) => (
                      <BarMark key={barKey} lane={lane} bar={bar} scale={scale} />
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </TooltipProvider>
    </SectionCard>
  );
}
