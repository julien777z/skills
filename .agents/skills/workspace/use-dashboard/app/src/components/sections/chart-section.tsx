import { type KeyboardEvent, type ReactNode, useId, useMemo, useRef, useState } from 'react';

import { DialogOpener } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { Progress } from '@/components/ui/progress';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { TONES } from '@/lib/tone';
import { cn, steppedIndex, withKeys } from '@/lib/utils';
import { type ChartItem, ChartKind, type ChartSection as ChartSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

const SERIES_COUNT: number = 8;

const NEAR_TONE_DEGREES: number = 30;

const RING_RADIUS_FOR_CIRCUMFERENCE_100: number = 15.9155;

const RING_WIDTH: number = 5;

const DIMMED: string = 'opacity-40';

interface Slice {
  key: string;
  item: ChartItem;
  color: string;
  share: number;
}

function themeHue(variable: string): number {
  const value = getComputedStyle(document.documentElement).getPropertyValue(`--${variable}`).trim();

  return Number(value.slice(value.lastIndexOf(' ') + 1, -1));
}

function hueDistance(first: number, second: number): number {
  const distance = Math.abs(first - second) % 360;

  return Math.min(distance, 360 - distance);
}

function seriesColorsFor(items: ChartItem[]): string[] {
  const toneHues = items.flatMap((item) => (item.tone ? [themeHue(TONES[item.tone].color)] : []));
  const series = Array.from({ length: SERIES_COUNT }, (_, index) => {
    const name = `series-${index + 1}`;
    const hue = themeHue(name);
    const clearance = Math.min(360, ...toneHues.map((toneHue) => hueDistance(hue, toneHue)));

    return { color: `var(--${name})`, clearance };
  });
  const clear = series.filter(({ clearance }) => clearance > NEAR_TONE_DEGREES);
  const near = series
    .filter(({ clearance }) => clearance <= NEAR_TONE_DEGREES)
    .sort((first, second) => second.clearance - first.clearance);

  return [...clear, ...near].map(({ color }) => color);
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

    return { key, item, color, share: item.value / total };
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
    <DialogOpener onOpen={(button) => selection.open(slice, button)} className="text-left">
      {label}
    </DialogOpener>
  );
}

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

function ItemRow({ slice, selection, children }: { slice: Slice; selection: Selection; children: ReactNode }) {
  return (
    <li
      {...hoverProps(slice.key, selection)}
      className={cn('min-w-0 transition-opacity', selection.active && selection.active !== slice.key && DIMMED)}
    >
      {children}
    </li>
  );
}

function Legend({ slices, selection }: { slices: Slice[]; selection: Selection }): ReactNode {
  return (
    <Stack as="ul" gap="sm" grow>
      {slices.map((slice) => (
        <ItemRow key={slice.key} slice={slice} selection={selection}>
          <Stack direction="row" gap="sm" align="start">
            <Swatch color={slice.color} />
            <Stack>
              <Stack direction="row" gap="sm" wrap>
                <ItemLabel slice={slice} selection={selection} />
                <Text size="xs" tone="muted" numeric>
                  {slice.item.figure} · {percentOf(slice.share)}
                </Text>
              </Stack>
              {slice.item.detail && (
                <Text size="xs" tone="muted">
                  {slice.item.detail}
                </Text>
              )}
            </Stack>
          </Stack>
        </ItemRow>
      ))}
    </Stack>
  );
}

function Pie({
  title,
  slices,
  total,
  selection,
}: {
  title: string;
  slices: Slice[];
  total?: string;
  selection: Selection;
}): ReactNode {
  const active = slices.find(({ key }) => key === selection.active);
  const ringId = useId();
  const drawn = slices.filter(({ share }) => share > 0);
  const sliceAt = (target: EventTarget): Slice | undefined =>
    target instanceof Element ? slices.find(({ key }) => key === target.getAttribute('data-slice')) : undefined;

  function handleKey(event: KeyboardEvent<HTMLDivElement>): void {
    const target = steppedIndex(event.key, active ? drawn.indexOf(active) : -1, drawn.length);

    if (target !== undefined) {
      event.preventDefault();
      selection.setActive(drawn[target].key);
    } else if ((event.key === 'Enter' || event.key === ' ') && active?.item.details) {
      event.preventDefault();
      selection.open(active, event.currentTarget);
    }
  }

  let offset = 25;

  return (
    <Stack align="center" gap="lg" rowFromMdCard>
      <div
        className="relative size-40 shrink-0 rounded-full outline-none focus-visible:ring-2 focus-visible:ring-ring"
        role="listbox"
        aria-label={title}
        aria-activedescendant={active ? `${ringId}-${slices.indexOf(active)}` : undefined}
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
              aria-selected={active?.key === slice.key}
            >
              {`${slice.item.label}: ${slice.item.figure}, ${percentOf(slice.share)}`}
            </div>
          ))}
        </div>
        <svg viewBox="0 0 42 42" className="size-full" aria-hidden>
          <circle
            cx="21"
            cy="21"
            r={RING_RADIUS_FOR_CIRCUMFERENCE_100}
            fill="none"
            stroke="var(--muted)"
            strokeWidth={RING_WIDTH}
          />
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
                    r={RING_RADIUS_FOR_CIRCUMFERENCE_100}
                    fill="none"
                    stroke={slice.color}
                    strokeWidth={active?.key === slice.key ? RING_WIDTH + 1.5 : RING_WIDTH}
                    strokeDasharray={`${length} ${100 - length}`}
                    strokeDashoffset={dashOffset}
                    className={cn(
                      'transition-[opacity,stroke-width]',
                      slice.item.details && 'cursor-pointer',
                      active && active.key !== slice.key && DIMMED,
                    )}
                  />
                </TooltipTrigger>
                <SliceTip slice={slice} />
              </Tooltip>
            );
          })}
        </svg>
        <span className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
          {active ? (
            <>
              <Text size="xs" tone="muted">
                {active.item.label}
              </Text>
              <Text size="sm" weight="semibold" numeric>
                {percentOf(active.share)}
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
    </Stack>
  );
}

function Bars({ slices, selection }: { slices: Slice[]; selection: Selection }): ReactNode {
  const largest = Math.max(...slices.map(({ item }) => item.value));

  return (
    <Stack as="ul" gap="md">
      {slices.map((slice) => (
        <ItemRow key={slice.key} slice={slice} selection={selection}>
          <Stack gap="xs">
            <Stack direction="row" gap="md" justify="between">
              <ItemLabel slice={slice} selection={selection} />
              <Text size="xs" tone="muted" numeric>
                {slice.item.figure}
              </Text>
            </Stack>
            <Progress value={(slice.item.value / largest) * 100} color={slice.color} aria-hidden="true" />
            {slice.item.detail && (
              <Text size="xs" tone="muted">
                {slice.item.detail}
              </Text>
            )}
          </Stack>
        </ItemRow>
      ))}
    </Stack>
  );
}

export function ChartSection({ section }: { section: ChartSectionSpec }): ReactNode {
  const slices = useMemo(() => slicesOf(section.items, section.kind), [section.items, section.kind]);
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
          <Pie title={section.title} slices={slices} total={section.total} selection={selection} />
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
