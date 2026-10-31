import { type MouseEvent, type ReactNode, useState } from 'react';

import { Grid, Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { SourceLinks } from '@/components/source-links';
import { StatusBadge } from '@/components/status-badge';
import { ToneDot } from '@/components/tone-dot';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import type { OutlineGroup, OutlineItem, OutlineSection as OutlineSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

const OPEN_GROUP_LIMIT: number = 2;
const DETAIL_LINE_LENGTH: number = 80;

interface GroupPart {
  group: OutlineGroup;
  start: number;
  end: number;
}

function opensAll(group: OutlineGroup, expanded: boolean): boolean {
  return expanded || group.items.length <= OPEN_GROUP_LIMIT;
}

function itemWeight(item: OutlineItem, opensAll: boolean): number {
  return 2 + (item.links ? 1 : 0) + (opensAll ? Math.ceil(item.detail.length / DETAIL_LINE_LENGTH) : 0);
}

function splitColumns(groups: OutlineGroup[], expanded: boolean): GroupPart[][] {
  const entries = groups.flatMap((group, groupIndex) =>
    group.items.map((item, index) => ({
      groupIndex,
      index,
      weight: itemWeight(item, opensAll(group, expanded)) + (index === 0 ? 1 : 0),
    })),
  );
  const total = entries.reduce((sum, entry) => sum + entry.weight, 0);

  let split = 1;
  let left = 0;
  let bestGap = Number.POSITIVE_INFINITY;

  for (let index = 0; index < entries.length - 1; index++) {
    left += entries[index].weight;

    const gap = Math.abs(total - 2 * left);

    if (gap < bestGap) {
      bestGap = gap;
      split = index + 1;
    }
  }

  const { groupIndex, index } = entries[split];
  const leftParts: GroupPart[] = groups
    .slice(0, groupIndex)
    .map((group) => ({ group, start: 0, end: group.items.length }));
  const rightParts: GroupPart[] = groups
    .slice(groupIndex + 1)
    .map((group) => ({ group, start: 0, end: group.items.length }));
  const splitGroup = groups[groupIndex];

  if (index > 0) {
    leftParts.push({ group: splitGroup, start: 0, end: index });
  }

  rightParts.unshift({ group: splitGroup, start: index, end: splitGroup.items.length });

  return [leftParts, rightParts];
}

function Group({
  group,
  expanded,
  start = 0,
  end = group.items.length,
}: {
  group: OutlineGroup;
  expanded: boolean;
  start?: number;
  end?: number;
}): ReactNode {
  const [open, setOpen] = useState<string[]>(() =>
    opensAll(group, expanded) ? group.items.map((_, index) => String(index)) : [],
  );

  function handleRowClick(event: MouseEvent<HTMLDivElement>, value: string) {
    if (window.getSelection()?.toString() || (event.target as HTMLElement).closest('a, button')) {
      return;
    }

    setOpen((current) => (current.includes(value) ? current.filter((entry) => entry !== value) : [...current, value]));
  }

  return (
    <Stack>
      {start === 0 && (
        <Text as="h3" size="xs" weight="medium" tone="muted" caps>
          <RichText text={group.title} />
        </Text>
      )}
      <Accordion type="multiple" value={open} onValueChange={setOpen}>
        {group.items.slice(start, end).map((item, offset) => {
          const index = start + offset;

          return (
            <AccordionItem key={index} value={String(index)}>
              <div
                className="flex cursor-pointer items-start gap-3 py-3"
                onClick={(event) => handleRowClick(event, String(index))}
              >
                <Stack direction="row" align="start" gap="sm" grow>
                  <ToneDot tone={item.tone} offset />
                  {item.tag && <StatusBadge label={item.tag} tone={item.tone} dot={false} />}
                  <Stack gap="xs" grow>
                    <Text weight="medium" size="sm" breakAnywhere>
                      <RichText text={item.title} />
                    </Text>
                    {item.meta && (
                      <Text size="xs" tone="muted" breakAnywhere>
                        <RichText text={item.meta} />
                      </Text>
                    )}
                  </Stack>
                </Stack>
                <AccordionTrigger className="flex-none py-0" aria-label={item.title} />
              </div>
              {item.links && (
                <Stack inset="item">
                  <SourceLinks links={item.links} />
                </Stack>
              )}
              <AccordionContent className="pl-[18px] text-muted-foreground [overflow-wrap:anywhere]">
                <RichText text={item.detail} />
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </Stack>
  );
}

export function OutlineSection({ section }: { section: OutlineSectionSpec }): ReactNode {
  const expanded = section.expanded ?? false;

  if (section.groups.length === 1) {
    return (
      <SectionCard title={section.title} description={section.description} wide>
        <Group group={section.groups[0]} expanded={expanded} />
      </SectionCard>
    );
  }

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns="pair" gap="loose">
        {splitColumns(section.groups, expanded).map((column, columnIndex) => (
          <Stack key={columnIndex} gap="xl">
            {column.map((part, index) => (
              <Group key={index} group={part.group} expanded={expanded} start={part.start} end={part.end} />
            ))}
          </Stack>
        ))}
      </Grid>
    </SectionCard>
  );
}
