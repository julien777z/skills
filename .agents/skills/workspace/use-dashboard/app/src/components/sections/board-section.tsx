import type { ReactNode } from 'react';

import { ExternalLink } from '@/components/external-link';
import { Grid, Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { StatusBadge } from '@/components/status-badge';
import { ToneDot } from '@/components/tone-dot';
import type { BoardColumn, BoardSection as BoardSectionSpec } from '@/spec';
import { Paged } from './paged';
import { SectionCard } from './section-card';

function Column({ column }: { column: BoardColumn }): ReactNode {
  return (
    <Stack gap="md" inset="panel" surface="panel">
      <Stack direction="row" align="center" gap="sm">
        <ToneDot tone={column.tone} />
        <Text size="sm" weight="medium">
          <RichText text={column.title} />
        </Text>
        <Stack direction="row" justify="end" grow>
          <StatusBadge label={String(column.items.length)} dot={false} />
        </Stack>
      </Stack>
      {!column.items.length && (
        <Text size="sm" tone="muted">
          Nothing here.
        </Text>
      )}
      <Paged items={column.items} pageSize={column.page_size} label={column.title}>
        {(visible) =>
          visible.map((card, index) => (
            <Stack key={index} gap="xs" inset="card" surface="card">
              <Text size="sm" weight="medium" breakAnywhere>
                {card.url ? <ExternalLink href={card.url}>{card.title}</ExternalLink> : <RichText text={card.title} />}
              </Text>
              {card.detail && (
                <Text size="xs" tone="muted" breakAnywhere>
                  <RichText text={card.detail} />
                </Text>
              )}
              {(card.tag || card.meta) && (
                <Stack direction="row" align="center" justify="between" gap="sm" wrap>
                  {card.tag && <StatusBadge label={card.tag} dot={false} />}
                  {card.meta && (
                    <Stack direction="row" justify="end" grow>
                      <Text size="xs" tone="muted" numeric>
                        <RichText text={card.meta} />
                      </Text>
                    </Stack>
                  )}
                </Stack>
              )}
            </Stack>
          ))
        }
      </Paged>
    </Stack>
  );
}

export function BoardSection({ section }: { section: BoardSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns="narrow">
        {section.columns.map((column, index) => (
          <Column key={index} column={column} />
        ))}
      </Grid>
    </SectionCard>
  );
}
