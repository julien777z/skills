import { type ReactNode, useId, useState } from 'react';

import { RichText, SourceLinks, StatusBadge, ToneDot } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { withKeys } from '@/lib/utils';
import type { OutlineGroup, OutlineSection as OutlineSectionSpec } from '@/spec';
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

function splitColumns(groups: OutlineGroup[], expanded: boolean): GroupPart[][] {
  const entries = groups.flatMap((group, groupIndex) => {
    const open = opensAll(group, expanded);

    return group.items.map((item, index) => ({
      groupIndex,
      index,
      weight:
        2 +
        (item.links ? 1 : 0) +
        (open ? Math.ceil(item.detail.length / DETAIL_LINE_LENGTH) : 0) +
        (index === 0 ? 1 : 0),
    }));
  });

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

  const triggerId = useId();
  const entries = withKeys(group.items, (item) => item.title)
    .map((entry, position) => ({ ...entry, value: String(position) }))
    .slice(start, end);

  function handleOpenChange(next: string[]) {
    const changed = [
      ...next.filter((value) => !open.includes(value)),
      ...open.filter((value) => !next.includes(value)),
    ];
    const trigger = document.getElementById(`${triggerId}-${changed[0]}`);
    const label = trigger && document.querySelector(`label[for="${CSS.escape(trigger.id)}"]`);
    const selection = window.getSelection();

    if (
      selection &&
      !selection.isCollapsed &&
      label?.contains(selection.anchorNode) &&
      document.activeElement !== trigger
    ) {
      return;
    }

    setOpen(next);
  }

  return (
    <Stack>
      {start === 0 && (
        <Text as="h3" size="xs" weight="medium" tone="muted" caps>
          <RichText text={group.title} />
        </Text>
      )}
      <Accordion type="multiple" value={open} onValueChange={handleOpenChange}>
        {entries.map(({ key, item, value }) => {
          const id = `${triggerId}-${value}`;

          return (
            <AccordionItem key={key} value={value}>
              <Stack direction="row" align="start" gap="md" block="row">
                <Stack direction="row" align="start" gap="sm" grow>
                  <ToneDot tone={item.tone} offset />
                  {item.tag && <StatusBadge label={item.tag} tone={item.tone} dot={false} />}
                  <Stack gap="xs" grow>
                    <Text labelFor={id} weight="medium" size="sm" breakAnywhere>
                      <RichText text={item.title} />
                    </Text>
                    {item.meta && (
                      <Text size="xs" tone="muted" breakAnywhere>
                        <RichText text={item.meta} />
                      </Text>
                    )}
                  </Stack>
                </Stack>
                <AccordionTrigger id={id} className="flex-none py-0" aria-label={item.title} />
              </Stack>
              {item.links && (
                <Stack inset="item">
                  <SourceLinks links={item.links} />
                </Stack>
              )}
              <AccordionContent
                aria-labelledby={id}
                className="pl-[18px] text-muted-foreground [overflow-wrap:anywhere]"
              >
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
        {splitColumns(section.groups, expanded).map((column) => (
          <Stack key={column.map((part) => `${part.group.title}:${part.start}`).join('|')} gap="xl">
            {column.map((part) => (
              <Group
                key={`${part.group.title}:${part.start}`}
                group={part.group}
                expanded={expanded}
                start={part.start}
                end={part.end}
              />
            ))}
          </Stack>
        ))}
      </Grid>
    </SectionCard>
  );
}
