import type { ReactNode } from 'react';

import { ExternalLink, ItemMeta, RichText, SourceLinks, StatusBadge, ToneDot } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { withKeys } from '@/lib/utils';
import type { BoardColumn, BoardSection as BoardSectionSpec } from '@/spec';
import { Paged } from './paged';
import { SectionCard } from './section-card';

function Column({ column }: { column: BoardColumn }): ReactNode {
  return (
    <Stack>
      <Stack direction="row" align="center" gap="sm" block="heading">
        <ToneDot tone={column.tone} />
        <Text size="sm" weight="medium">
          <RichText text={column.title} />
        </Text>
        <Stack direction="row" justify="end" grow>
          <Text size="xs" tone="muted" numeric>
            {column.items.length}
          </Text>
        </Stack>
      </Stack>
      {!column.items.length && (
        <Stack block="row">
          <Text size="detail" tone="muted">
            Nothing here.
          </Text>
        </Stack>
      )}
      <Paged items={column.items} pageSize={column.page_size} label={column.title}>
        {(visible) => (
          <Stack as="ul" divided="between">
            {withKeys(visible, (card) => card.title).map(({ key, item: card }) => (
              <Stack key={key} as="li" gap="xs" block="row">
                <Text size="sm" weight="medium" breakAnywhere>
                  {card.url ? (
                    <ExternalLink href={card.url}>{card.title}</ExternalLink>
                  ) : (
                    <RichText text={card.title} />
                  )}
                </Text>
                {card.detail && (
                  <Text size="detail" tone="muted" breakAnywhere>
                    <RichText text={card.detail} />
                  </Text>
                )}
                {card.status && <StatusBadge label={card.status.label} tone={card.status.tone} />}
                <ItemMeta tag={card.tag} meta={card.meta} at={card.at} />
                {card.links && <SourceLinks links={card.links} />}
              </Stack>
            ))}
          </Stack>
        )}
      </Paged>
    </Stack>
  );
}

export function BoardSection({ section }: { section: BoardSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns="narrow" gap="loose">
        {withKeys(section.columns, (column) => column.title).map(({ key, item: column }) => (
          <Column key={key} column={column} />
        ))}
      </Grid>
    </SectionCard>
  );
}
