import { type KeyboardEvent, type ReactNode, useId, useRef, useState } from 'react';

import { DialogOpener } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { TONES } from '@/lib/tone';
import { cn, withKeys } from '@/lib/utils';
import { type ChartItem, ChartKind, type ChartSection as ChartSectionSpec, type Tone } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

/** The hue of each `--series-<n>` color, in order, so a chart can skip those close to a tone it uses. */
const SERIES_HUES: readonly number[] = [235, 50, 170, 345, 205, 95, 15, 130];

const TONE_HUES: Record<Tone, number> = { good: 152, warning: 75, critical: 22, accent: 250, done: 300 };

const NEAR_TONE_DEGREES = 30;

const RING_RADIUS = 15.9155;

const RING_WIDTH = 5;

const DIMMED = 'opacity-35';

interface Slice {
  key: string;
  item: ChartItem;
  color: string;
  share: number;
}

function hueDistance(first: number, second: number): number {
  const distance = Math.abs(first - second) % 360;

  return Math.min(distance, 360 - distance);
}

/** Series colors whose hue stays clear of every tone the chart uses, so a toned item stands out. */
function seriesColorsFor(items: ChartItem[]): string[] {
  const toneHues = items.flatMap((item) => (item.tone ? [TONE_HUES[item.tone]] : []));
  const clear = SERIES_HUES.flatMap((hue, index) =>
    toneHues.every((toneHue) => hueDistance(hue, toneHue) > NEAR_TONE_DEGREES) ? [`var(--series-${index + 1})`] : [],
  );

  return clear.length > 0 ? clear : ['var(--series-1)'];
}

function slicesOf(items: ChartItem[], kind: ChartKind): Slice[] {
  const total = items.reduce((sum, item) => sum + item.value, 0);
  const series = seriesColorsFor(items);
  let next = 0;

  return withKeys(items, (item) => item.label).map(({ key, item }) => {
    let color = series[0];

    if (item.tone) {
      color = `var(--${TONES[item.tone].color})`;
    } else if (kind === ChartKind.PIE) {
      color = series[next++ % series.length];
    }

    return { key, item, color, share: total > 0 ? item.value / total : 0 };
  });
}

function percentOf(share: number): string {
  const percent = share * 100;

  return percent > 0 && percent < 1 ? '<1%' : `${Math.round(percent)}%`;
}

function Swatch({ color }: { color: string }): ReactNode {
  return <span aria-hidden className="mt-1 size-2.5 shrink-0 rounded-sm" style={{ backgroundColor: color }} />;
}

interface Selection {
  active: string | null;
  setActive: (key: string | null) => void;
  open: (slice: Slice, opener: HTMLOrSVGElement) => void;
}

function hoverProps(key: string, { setActive }: Selection) {
  return {
    onPointerEnter: () => setActive(key),
    onPointerLeave: () => setActive(null),
    onFocus: () => setActive(key),
    onBlur: () => setActive(null),
  };
}

function ItemLabel({ slice, selection }: { slice: Slice; selection: Selection }): ReactNode {
  const label = (
    <Text size="sm" weight="medium">
      {slice.item.label}
    </Text>
  );

  if (!slice.item.details) {
    return label;
  }

  return (
    <DialogOpener onOpen={(button) => selection.open(slice, button)} className="text-left hover:underline">
      {label}
    </DialogOpener>
  );
}

/** A slice's popup, so a reader reads an item off the ring without matching colors to the legend. */
function SliceTip({ slice }: { slice: Slice }): ReactNode {
  return (
    <TooltipContent>
      <Stack gap="xs">
        <Text size="sm" weight="medium">
          {slice.item.label}
        </Text>
        <Text size="xs" numeric>
          {slice.item.figure} · {percentOf(slice.share)}
        </Text>
      </Stack>
    </TooltipContent>
  );
}

function Legend({ slices, selection }: { slices: Slice[]; selection: Selection }): ReactNode {
  return (
    <ul className="grid min-w-0 flex-1 gap-2">
      {slices.map((slice) => (
        <li
          key={slice.key}
          {...hoverProps(slice.key, selection)}
          className={cn(
            'flex min-w-0 items-start gap-2 transition-opacity',
            selection.active && selection.active !== slice.key && DIMMED,
          )}
        >
          <Swatch color={slice.color} />
          <Stack gap="none">
            <span className="flex flex-wrap items-baseline gap-x-2">
              <ItemLabel slice={slice} selection={selection} />
              <Text size="xs" tone="muted" numeric>
                {slice.item.figure} · {percentOf(slice.share)}
              </Text>
            </span>
            {slice.item.detail && (
              <Text size="xs" tone="muted">
                {slice.item.detail}
              </Text>
            )}
          </Stack>
        </li>
      ))}
    </ul>
  );
}

function Pie({ slices, total, selection }: { slices: Slice[]; total?: string; selection: Selection }): ReactNode {
  const hovered = slices.find(({ key }) => key === selection.active);
  const ringId = useId();
  const sliceAt = (target: EventTarget): Slice | undefined =>
    target instanceof Element ? slices.find(({ key }) => key === target.getAttribute('data-slice')) : undefined;

  /** Arrow keys walk the ring's slices, as the pointer does, and Enter opens the one selected. */
  function handleKey(event: KeyboardEvent<HTMLDivElement>): void {
    const index = slices.findIndex(({ key }) => key === selection.active);
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];

    if (step) {
      event.preventDefault();
      selection.setActive(slices[(index + step + slices.length) % slices.length].key);
    } else if ((event.key === 'Enter' || event.key === ' ') && hovered?.item.details) {
      event.preventDefault();
      selection.open(hovered, event.currentTarget);
    }
  }

  let offset = 25;

  return (
    <div className="flex flex-col items-center gap-5 @md/card:flex-row @md/card:items-start">
      <div
        className="relative size-40 shrink-0 rounded-full outline-none focus-visible:ring-2 focus-visible:ring-ring"
        role="listbox"
        aria-label="Chart items"
        aria-activedescendant={hovered ? `${ringId}-${slices.indexOf(hovered)}` : undefined}
        tabIndex={0}
        onKeyDown={handleKey}
        onBlur={() => selection.setActive(null)}
        onPointerOver={(event) => selection.setActive(sliceAt(event.target)?.key ?? null)}
        onPointerLeave={() => selection.setActive(null)}
        onClick={(event) => {
          const slice = sliceAt(event.target);

          if (slice?.item.details) {
            selection.open(slice, event.currentTarget);
          }
        }}
      >
        <div className="sr-only">
          {slices.map((slice, index) => (
            <div
              key={slice.key}
              id={`${ringId}-${index}`}
              role="option"
              tabIndex={-1}
              aria-selected={hovered?.key === slice.key}
            >
              {`${slice.item.label}: ${slice.item.figure}, ${percentOf(slice.share)}`}
            </div>
          ))}
        </div>
        <svg viewBox="0 0 42 42" className="size-full" aria-hidden>
          <circle cx="21" cy="21" r={RING_RADIUS} fill="none" stroke="var(--muted)" strokeWidth={RING_WIDTH} />
          {slices.map((slice) => {
            const length = slice.share * 100;
            const dashOffset = offset;

            offset = (offset - length + 100) % 100;

            return (
              <Tooltip key={slice.key}>
                <TooltipTrigger asChild>
                  <circle
                    data-slice={slice.key}
                    cx="21"
                    cy="21"
                    r={RING_RADIUS}
                    fill="none"
                    stroke={slice.color}
                    strokeWidth={hovered?.key === slice.key ? RING_WIDTH + 1.5 : RING_WIDTH}
                    strokeDasharray={`${length} ${100 - length}`}
                    strokeDashoffset={dashOffset}
                    className={cn(
                      'transition-[opacity,stroke-width]',
                      slice.item.details && 'cursor-pointer',
                      hovered && hovered.key !== slice.key && DIMMED,
                    )}
                  />
                </TooltipTrigger>
                <SliceTip slice={slice} />
              </Tooltip>
            );
          })}
        </svg>
        <span className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
          {hovered ? (
            <>
              <Text size="xs" tone="muted">
                {hovered.item.label}
              </Text>
              <Text size="sm" weight="semibold" numeric>
                {percentOf(hovered.share)}
              </Text>
            </>
          ) : (
            total && (
              <Text size="sm" weight="semibold" numeric>
                {total}
              </Text>
            )
          )}
        </span>
      </div>
      <Legend slices={slices} selection={selection} />
    </div>
  );
}

function BarFill({ slice, largest }: { slice: Slice; largest: number }): ReactNode {
  return (
    <span
      className="block h-full rounded-full"
      style={{ width: `${largest > 0 ? (slice.item.value / largest) * 100 : 0}%`, backgroundColor: slice.color }}
    />
  );
}

function Bars({ slices, selection }: { slices: Slice[]; selection: Selection }): ReactNode {
  const largest = Math.max(...slices.map(({ item }) => item.value));

  return (
    <ul className="grid gap-3">
      {slices.map((slice) => (
        <li
          key={slice.key}
          {...hoverProps(slice.key, selection)}
          className={cn('grid gap-1 transition-opacity', selection.active && selection.active !== slice.key && DIMMED)}
        >
          <span className="flex min-w-0 items-baseline justify-between gap-3">
            <ItemLabel slice={slice} selection={selection} />
            <Text size="xs" tone="muted" numeric>
              {slice.item.figure}
            </Text>
          </span>
          <span aria-hidden className="block h-2 w-full overflow-hidden rounded-full bg-muted">
            <BarFill slice={slice} largest={largest} />
          </span>
          {slice.item.detail && (
            <Text size="xs" tone="muted">
              {slice.item.detail}
            </Text>
          )}
        </li>
      ))}
    </ul>
  );
}

export function ChartSection({ section }: { section: ChartSectionSpec }): ReactNode {
  const slices = slicesOf(section.items, section.kind);
  const [active, setActive] = useState<string | null>(null);
  const [opened, setOpened] = useState<Slice | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const opener = useRef<HTMLOrSVGElement | null>(null);
  const selection: Selection = {
    active,
    setActive,
    open: (slice, element) => {
      opener.current = element;

      setOpened(slice);
      setDialogOpen(true);
    },
  };

  return (
    <SectionCard title={section.title} description={section.description}>
      {section.kind === ChartKind.PIE ? (
        <TooltipProvider>
          <Pie slices={slices} total={section.total} selection={selection} />
        </TooltipProvider>
      ) : (
        <Bars slices={slices} selection={selection} />
      )}
      {opened?.item.details && (
        <SectionDialog section={opened.item.details} open={dialogOpen} onOpenChange={setDialogOpen} opener={opener} />
      )}
    </SectionCard>
  );
}
