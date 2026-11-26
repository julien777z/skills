import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { TONES } from '@/lib/tone';
import { withKeys } from '@/lib/utils';
import { type ChartItem, ChartKind, type ChartSection as ChartSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

const SERIES_COUNT = 8;
const MUTED_COUNT = 4;
const RING_RADIUS = 15.9155;
const RING_WIDTH = 5;

interface Slice {
  key: string;
  item: ChartItem;
  color: string;
  share: number;
}

function slicesOf(items: ChartItem[], kind: ChartKind): Slice[] {
  const total = items.reduce((sum, item) => sum + item.value, 0);
  const toned = items.some((item) => item.tone);
  let series = 0;

  return withKeys(items, (item) => item.label).map(({ key, item }) => {
    const index = (series++ % SERIES_COUNT) + 1;
    let color = `var(--series-${index})`;

    if (item.tone) {
      color = `var(--${TONES[item.tone].color})`;
    } else if (kind === ChartKind.BAR) {
      color = 'var(--series-1)';
    } else if (toned) {
      color = `var(--series-muted-${((index - 1) % MUTED_COUNT) + 1})`;
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

function Legend({ slices }: { slices: Slice[] }): ReactNode {
  return (
    <ul className="grid min-w-0 flex-1 gap-2">
      {slices.map(({ key, item, color, share }) => (
        <li key={key} className="flex min-w-0 items-start gap-2">
          <Swatch color={color} />
          <Stack gap="none">
            <span className="flex flex-wrap items-baseline gap-x-2">
              <Text size="sm" weight="medium">
                {item.label}
              </Text>
              <Text size="xs" tone="muted" numeric>
                {item.figure} · {percentOf(share)}
              </Text>
            </span>
            {item.detail && (
              <Text size="xs" tone="muted">
                {item.detail}
              </Text>
            )}
          </Stack>
        </li>
      ))}
    </ul>
  );
}

function Pie({ slices, total }: { slices: Slice[]; total?: string }): ReactNode {
  let offset = 25;

  return (
    <div className="flex flex-col items-center gap-5 @md/card:flex-row @md/card:items-start">
      <div className="relative size-40 shrink-0">
        <svg
          viewBox="0 0 42 42"
          className="size-full"
          role="img"
          aria-label={slices.map(({ item }) => `${item.label} ${item.figure}`).join(', ')}
        >
          <circle cx="21" cy="21" r={RING_RADIUS} fill="none" stroke="var(--muted)" strokeWidth={RING_WIDTH} />
          {slices.map(({ key, item, color, share }) => {
            const length = share * 100;
            const dash = `${length} ${100 - length}`;
            const dashOffset = offset;

            offset = (offset - length + 100) % 100;

            return (
              <circle
                key={key}
                cx="21"
                cy="21"
                r={RING_RADIUS}
                fill="none"
                stroke={color}
                strokeWidth={RING_WIDTH}
                strokeDasharray={dash}
                strokeDashoffset={dashOffset}
              >
                <title>{`${item.label}: ${item.figure} (${percentOf(share)})`}</title>
              </circle>
            );
          })}
        </svg>
        {total && (
          <span className="absolute inset-0 flex items-center justify-center px-8 text-center">
            <Text size="sm" weight="semibold" numeric>
              {total}
            </Text>
          </span>
        )}
      </div>
      <Legend slices={slices} />
    </div>
  );
}

function Bars({ slices }: { slices: Slice[] }): ReactNode {
  const largest = Math.max(...slices.map(({ item }) => item.value));

  return (
    <ul className="grid gap-3">
      {slices.map(({ key, item, color }) => (
        <li key={key} className="grid gap-1">
          <span className="flex min-w-0 items-baseline justify-between gap-3">
            <Text size="sm" weight="medium">
              {item.label}
            </Text>
            <Text size="xs" tone="muted" numeric>
              {item.figure}
            </Text>
          </span>
          <span className="block h-2 w-full overflow-hidden rounded-full bg-muted">
            <span
              className="block h-full rounded-full"
              style={{ width: `${largest > 0 ? (item.value / largest) * 100 : 0}%`, backgroundColor: color }}
            />
          </span>
          {item.detail && (
            <Text size="xs" tone="muted">
              {item.detail}
            </Text>
          )}
        </li>
      ))}
    </ul>
  );
}

export function ChartSection({ section }: { section: ChartSectionSpec }): ReactNode {
  const slices = slicesOf(section.items, section.kind);

  return (
    <SectionCard title={section.title} description={section.description}>
      {section.kind === ChartKind.PIE ? <Pie slices={slices} total={section.total} /> : <Bars slices={slices} />}
    </SectionCard>
  );
}
