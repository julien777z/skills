import { type MouseEvent, type ReactNode, useState } from 'react';

import { Grid, Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { SourceLinks } from '@/components/source-links';
import { StatusBadge } from '@/components/status-badge';
import { ToneDot } from '@/components/tone-dot';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import type { OutlineGroup, OutlineSection as OutlineSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

const OPEN_GROUP_LIMIT: number = 2;

function Group({ group }: { group: OutlineGroup }): ReactNode {
  const [open, setOpen] = useState<string[]>(() =>
    group.items.length <= OPEN_GROUP_LIMIT ? group.items.map((_, index) => String(index)) : [],
  );

  function handleRowClick(event: MouseEvent<HTMLDivElement>, value: string) {
    if (window.getSelection()?.toString() || (event.target as HTMLElement).closest('a, button')) {
      return;
    }

    setOpen((current) => (current.includes(value) ? current.filter((entry) => entry !== value) : [...current, value]));
  }

  return (
    <Stack>
      <Text as="h3" size="xs" weight="medium" tone="muted" caps>
        <RichText text={group.title} />
      </Text>
      <Accordion type="multiple" value={open} onValueChange={setOpen}>
        {group.items.map((item, index) => (
          <AccordionItem key={index} value={String(index)}>
            <div
              className="flex cursor-pointer items-start gap-3 py-3"
              onClick={(event) => handleRowClick(event, String(index))}
            >
              <Stack direction="row" align="start" gap="sm" grow>
                <ToneDot tone={item.tone} offset />
                <Stack gap="xs" grow>
                  <Text weight="medium" size="sm" breakAnywhere>
                    <RichText text={item.title} />
                  </Text>
                  {(item.tag || item.meta) && (
                    <Stack direction="row" align="center" gap="sm" wrap>
                      {item.tag && <StatusBadge label={item.tag} tone={item.tone} dot={false} />}
                      {item.meta && (
                        <Text size="xs" tone="muted" breakAnywhere>
                          <RichText text={item.meta} />
                        </Text>
                      )}
                    </Stack>
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
        ))}
      </Accordion>
    </Stack>
  );
}

export function OutlineSection({ section }: { section: OutlineSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns="flow" gap="loose">
        {section.groups.map((group, index) => (
          <Group key={index} group={group} />
        ))}
      </Grid>
    </SectionCard>
  );
}
