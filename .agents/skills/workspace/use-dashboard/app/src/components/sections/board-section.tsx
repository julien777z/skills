import type { ReactNode } from 'react';

import { ExternalLink, ItemMeta, RichText, SourceLinks, StatusBadge, ToneDot } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { withKeys } from '@/lib/utils';
import type { BoardColumn, BoardSection as BoardSectionSpec } from '@/spec';
import { Paged } from './paged';
import { SectionCard } from './section-card';

function Column({ column }: { column: BoardColumn }): ReactNode {
  return (
    <Stack gap="md" surface="panel">
      <Stack direction="row" align="center" gap="sm">
        <ToneDot tone={column.tone} />
        <Text size="sm" weight="medium">
          <RichText text={column.title} />
        </Text>
        <Stack direction="row" justify="end" grow>
          <Text size="sm" tone="muted" numeric>
            {column.items.length}
          </Text>
        </Stack>
      </Stack>
      {!column.items.length && (
        <Text size="sm" tone="muted">
          Nothing here.
        </Text>
      )}
      <Paged items={column.items} pageSize={column.page_size} label={column.title}>
        {(visible) =>
          withKeys(visible, (card) => card.title).map(({ key, item: card }) => (
            <Stack key={key} gap="xs" surface="card">
              <Text size="sm" weight="medium" breakAnywhere>
                {card.url ? <ExternalLink href={card.url}>{card.title}</ExternalLink> : <RichText text={card.title} />}
              </Text>
              {card.detail && (
                <Text size="xs" tone="muted" breakAnywhere>
                  <RichText text={card.detail} />
                </Text>
              )}
              {(card.tag || card.meta || card.at) && (
                <Stack direction="row" align="center" justify="between" gap="sm" wrap>
                  {card.tag && <StatusBadge label={card.tag} dot={false} />}
                  {(card.meta || card.at) && (
                    <Stack direction="row" justify="end" grow>
                      <ItemMeta meta={card.meta} at={card.at} />
                    </Stack>
                  )}
                </Stack>
              )}
              {card.links && <SourceLinks links={card.links} />}
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
        {withKeys(section.columns, (column) => column.title).map(({ key, item: column }) => (
          <Column key={key} column={column} />
        ))}
      </Grid>
    </SectionCard>
  );
}
