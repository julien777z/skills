import { type ReactNode, useId, useState } from 'react';

import { RichText, SourceLinks, StatusBadge, ToneDot } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { withKeys } from '@/lib/utils';
import type { OutlineGroup, OutlineSection as OutlineSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { TextList } from './text-list';

const OPEN_GROUP_LIMIT: number = 2;
const DETAIL_LINE_LENGTH: number = 80;

function opensAll(group: OutlineGroup, expanded: boolean): boolean {
  return expanded || group.items.length <= OPEN_GROUP_LIMIT;
}

function groupWeight(group: OutlineGroup, expanded: boolean): number {
  const open = opensAll(group, expanded);

  return group.items.reduce(
    (sum, item) =>
      sum +
      2 +
      (item.links ? 1 : 0) +
      (open ? Math.ceil(item.detail.length / DETAIL_LINE_LENGTH) + (item.points?.length ?? 0) : 0),
    1,
  );
}

function splitColumns(groups: OutlineGroup[], expanded: boolean): OutlineGroup[][] {
  const weights = groups.map((group) => groupWeight(group, expanded));
  const total = weights.reduce((sum, weight) => sum + weight, 0);

  let split = 1;
  let left = 0;
  let bestGap = Number.POSITIVE_INFINITY;

  for (let index = 0; index < groups.length - 1; index++) {
    left += weights[index];

    const gap = Math.abs(total - 2 * left);

    if (gap < bestGap) {
      bestGap = gap;
      split = index + 1;
    }
  }

  return [groups.slice(0, split), groups.slice(split)];
}

function PlainGroup({ group, first }: { group: OutlineGroup; first: boolean }): ReactNode {
  return (
    <Grid gap="sm" divider={first ? 'none' : 'top'}>
      <Text as="h3" size="sm" weight="medium" tone="muted">
        <RichText text={group.title} />
      </Text>
      <dl className="grid grid-cols-1 gap-x-6 gap-y-1 sm:grid-cols-[minmax(0,11rem)_minmax(0,1fr)] sm:gap-y-2">
        {withKeys(group.items, (item) => item.title).map(({ key, item }) => (
          <div key={key} className="contents">
            <dt className="pt-1 sm:pt-0">
              <Stack direction="row" align="start" gap="sm">
                {item.tone && <ToneDot tone={item.tone} offset />}
                <Text size="sm" tone="muted" breakAnywhere>
                  <RichText text={item.title} />
                </Text>
              </Stack>
            </dt>
            <dd>
              <Stack gap="xs">
                <Stack direction="row" align="start" gap="sm" wrap>
                  {item.tag && <StatusBadge label={item.tag} tone={item.tone} dot={false} />}
                  <Text size="sm" breakAnywhere>
                    <RichText text={item.detail} />
                    {item.meta && (
                      <Text as="span" size="sm" tone="muted">
                        {' · '}
                        <RichText text={item.meta} />
                      </Text>
                    )}
                  </Text>
                </Stack>
                {item.points && <TextList items={item.points} />}
                {item.links && <SourceLinks links={item.links} />}
              </Stack>
            </dd>
          </div>
        ))}
      </dl>
    </Grid>
  );
}

function Group({ group, expanded }: { group: OutlineGroup; expanded: boolean }): ReactNode {
  const [open, setOpen] = useState<string[]>(() =>
    opensAll(group, expanded) ? group.items.map((_, index) => String(index)) : [],
  );

  const triggerId = useId();
  const entries = withKeys(group.items, (item) => item.title).map((entry, position) => ({
    ...entry,
    value: String(position),
  }));

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
      <Text as="h3" size="sm" weight="medium" tone="muted">
        <RichText text={group.title} />
      </Text>
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
                <Stack gap="sm">
                  <RichText text={item.detail} />
                  {item.points && <TextList items={item.points} />}
                </Stack>
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
  const columns =
    section.stacked || section.groups.length === 1 ? [section.groups] : splitColumns(section.groups, expanded);

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns={columns.length > 1 ? 'pair' : 'single'} gap="loose">
        {columns.map((column) => (
          <Stack key={column.map((group) => group.title).join('|')} gap={section.collapsible === false ? 'lg' : 'xl'}>
            {column.map((group, position) =>
              section.collapsible === false ? (
                <PlainGroup key={group.title} group={group} first={position === 0} />
              ) : (
                <Group key={group.title} group={group} expanded={expanded} />
              ),
            )}
          </Stack>
        ))}
      </Grid>
    </SectionCard>
  );
}
