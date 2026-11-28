import { cn } from 'cn';
import { Fragment, type ReactNode, useContext } from 'react';

import { Stack } from '@/components/primitives/stack';
import { Text } from '@/components/primitives/text';
import { RichText } from '@/components/rich-text';
import { StatusBadge } from '@/components/status-badge';
import { ToneDot } from '@/components/tone-dot';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { CLOCK, DATE_AND_CLOCK, formatDuration, formatSpan, MINUTE_MS } from '@/lib/time';
import { TONES, ToneName } from '@/lib/tone';
import { withKeys } from '@/lib/utils';
import type { TimelineBar, TimelineGap, TimelineLane, TimelineSection as TimelineSectionSpec } from '@/spec';
import { DetailsLabel } from './details-label';
import { InDialogContext, SectionCard } from './section-card';

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

const DATE_TICK: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' };

const TickAnchor = { START: 'start', CENTER: 'center', END: 'end' } as const;

type TickAnchor = (typeof TickAnchor)[keyof typeof TickAnchor];

const TICK_ANCHOR_CLASSES: Record<TickAnchor, string> = {
  [TickAnchor.START]: 'translate-x-0',
  [TickAnchor.CENTER]: '-translate-x-1/2',
  [TickAnchor.END]: '-translate-x-full',
};

const GAP_PERCENT: number = 5;

const EDGE_PERCENT: number = 6;

const BREAK_CLEARANCE_PERCENT: number = 4;

const PERCENT_PER_LABEL_CHARACTER: number = 1.4;

interface Segment {
  start: number;
  end: number;
  left: number;
  width: number;
  collapsed: boolean;
}

interface Scale {
  segments: Segment[];
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
  const end = Math.max(start + MINUTE_MS, Math.max(...moments));
  const breaks = gaps
    .map((gap) => ({ start: Math.max(start, Date.parse(gap.start)), end: Math.min(end, Date.parse(gap.end)) }))
    .filter((gap) => gap.end > gap.start)
    .sort((first, second) => first.start - second.start);
  const pieces: Omit<Segment, 'left' | 'width'>[] = [];
  let cursor = start;

  for (const gap of breaks) {
    if (gap.start > cursor) {
      pieces.push({ start: cursor, end: gap.start, collapsed: false });
    }

    pieces.push({ start: Math.max(cursor, gap.start), end: gap.end, collapsed: true });
    cursor = Math.max(cursor, gap.end);
  }

  if (end > cursor) {
    pieces.push({ start: cursor, end, collapsed: false });
  }

  const collapsedShare = pieces.filter((piece) => piece.collapsed).length * GAP_PERCENT;
  const active = pieces.filter((piece) => !piece.collapsed).reduce((sum, piece) => sum + piece.end - piece.start, 0);
  let left = 0;

  return {
    segments: pieces.map((piece) => {
      const width = piece.collapsed
        ? GAP_PERCENT
        : ((piece.end - piece.start) / Math.max(MINUTE_MS, active)) * (100 - collapsedShare);
      const segment = { ...piece, left, width };

      left += width;

      return segment;
    }),
  };
}

function offset(scale: Scale, at: number): number {
  const segment = scale.segments.find((candidate) => at <= candidate.end) ?? scale.segments[scale.segments.length - 1];
  const fraction = (at - segment.start) / Math.max(1, segment.end - segment.start);

  return segment.left + Math.min(1, Math.max(0, fraction)) * segment.width;
}

function tickAnchor(left: number): TickAnchor {
  if (left < EDGE_PERCENT) {
    return TickAnchor.START;
  }

  return left > 100 - EDGE_PERCENT ? TickAnchor.END : TickAnchor.CENTER;
}

function labelReach(label: string, position: number): number {
  return ((label.length + 2) * PERCENT_PER_LABEL_CHARACTER) / (tickAnchor(position) === TickAnchor.CENTER ? 2 : 1);
}

function firstTickAt(start: number, interval: number): number {
  const midnight = new Date(start);

  midnight.setHours(0, 0, 0, 0);

  return midnight.getTime() + Math.ceil((start - midnight.getTime()) / interval) * interval;
}

function spaced(scale: Scale, ticks: Tick[]): Tick[] {
  const breakEdges = scale.segments
    .filter((segment) => segment.collapsed)
    .flatMap((segment) => [segment.left, segment.left + segment.width]);
  const kept: Tick[] = [];

  for (const tick of ticks) {
    const at = offset(scale, tick.at);
    const previous = kept[kept.length - 1];
    const nearBreak = breakEdges.some((edge) => Math.abs(edge - at) < BREAK_CLEARANCE_PERCENT);
    const nearPrevious =
      previous !== undefined &&
      at - offset(scale, previous.at) <
        labelReach(previous.label, offset(scale, previous.at)) + labelReach(tick.label, at);

    if (!nearBreak && !nearPrevious) {
      kept.push(tick);
    }
  }

  return kept;
}

function ticksOf(scale: Scale): Tick[] {
  const active = scale.segments.filter((segment) => !segment.collapsed);
  const first = scale.segments[0].start;
  const last = scale.segments[scale.segments.length - 1].end;
  const crossesDays = new Date(first).toDateString() !== new Date(last).toDateString();
  const ticks: Tick[] = [];
  let previousDay = '';

  for (const segment of active) {
    const span = segment.end - segment.start;
    const allowed = Math.max(1, Math.round((MAX_TICKS * segment.width) / 100));
    const interval =
      TICK_INTERVALS_MS.find((candidate) => span / candidate <= allowed) ??
      TICK_INTERVALS_MS[TICK_INTERVALS_MS.length - 1];

    for (let at = firstTickAt(segment.start, interval); at <= segment.end; at += interval) {
      const moment = new Date(at);
      const day = moment.toDateString();
      const dated = crossesDays && day !== previousDay;
      const format = interval >= DAY_MS ? DATE_TICK : dated ? DATE_AND_CLOCK : CLOCK;

      ticks.push({ at, label: moment.toLocaleString(undefined, format) });
      previousDay = day;
    }
  }

  return spaced(scale, ticks);
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
  return (
    <div className="flex min-h-8 min-w-0 items-start gap-2 py-1.5">
      <ToneDot tone={lane.tone} offset />
      <span className="min-w-0 text-sm break-words">
        <DetailsLabel label={lane.label} details={lane.details} className="cursor-pointer" />
        {lane.tag && (
          <>
            {' '}
            <StatusBadge label={lane.tag} dot={false} />
          </>
        )}
      </span>
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

function TrackBackdrop({ ticks, gaps, scale }: { ticks: Tick[]; gaps: TimelineGap[]; scale: Scale }): ReactNode {
  return (
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
  );
}

export function TimelineSection({ section }: { section: TimelineSectionSpec }): ReactNode {
  const gaps = section.gaps ?? [];
  const scale = scaleOf(section.lanes, gaps);
  const ticks = ticksOf(scale);
  const lanes = withKeys(section.lanes, (lane) => lane.label);
  const inDialog = useContext(InDialogContext);
  const labelCell = cn('pr-4 sm:sticky sm:left-0 sm:z-10', inDialog ? 'bg-background' : 'bg-card');

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <TooltipProvider>
        <ScrollArea type="auto" className="w-full">
          <div className="grid min-w-[48rem] grid-cols-[minmax(10rem,18rem)_minmax(0,1fr)] pb-3">
            <div className={labelCell} />
            <div aria-hidden="true" className="relative h-6 text-xs text-muted-foreground tabular-nums">
              {withKeys(ticks, (tick) => String(tick.at)).map(({ key, item: tick }) => (
                <span
                  key={key}
                  style={{ left: `${offset(scale, tick.at)}%` }}
                  className={cn(
                    'absolute top-0 whitespace-nowrap',
                    TICK_ANCHOR_CLASSES[tickAnchor(offset(scale, tick.at))],
                  )}
                >
                  {tick.label}
                </span>
              ))}
            </div>
            {gaps.length > 0 && (
              <>
                <div className={labelCell} />
                <div className="relative h-5">
                  <TrackBackdrop ticks={ticks} gaps={gaps} scale={scale} />
                  {withKeys(gaps, (gap) => gap.start).map(({ key, item: gap }) => (
                    <GapLabel key={key} gap={gap} scale={scale} />
                  ))}
                </div>
              </>
            )}
            {lanes.map(({ key, item: lane }) => (
              <Fragment key={key}>
                <div className={cn(labelCell, 'border-b border-border/50')}>
                  <LaneLabel lane={lane} />
                </div>
                <div className="relative min-h-8 border-b border-border/50">
                  <TrackBackdrop ticks={ticks} gaps={gaps} scale={scale} />
                  {withKeys(lane.bars, (bar) => bar.start).map(({ key: barKey, item: bar }) => (
                    <BarMark key={barKey} lane={lane} bar={bar} scale={scale} />
                  ))}
                </div>
              </Fragment>
            ))}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </TooltipProvider>
    </SectionCard>
  );
}
