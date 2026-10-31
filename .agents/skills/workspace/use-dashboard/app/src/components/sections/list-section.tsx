import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { Paged } from './paged';
import { SectionCard } from './section-card';

interface ListRowContent {
  icon?: ReactNode;
  title: ReactNode;
  detail?: ReactNode;
  aside?: ReactNode;
  body?: ReactNode;
}

interface ListSectionProps<Item> {
  title: string;
  description?: string;
  summary: ReactNode;
  items: Item[];
  pageSize?: number;
  row: (item: Item) => ListRowContent;
}

function ListRow({ icon, title, detail, aside, body }: ListRowContent): ReactNode {
  return (
    <Stack as="li" direction="row" align="start" gap="md" inset="row">
      {icon && (
        <Stack align="center" justify="center" badge="slot">
          {icon}
        </Stack>
      )}
      <Stack grow gap="xs">
        <Text weight="medium" breakAnywhere>
          {title}
        </Text>
        {detail && (
          <Text size="sm" tone="muted" breakAnywhere>
            {detail}
          </Text>
        )}
        {body}
      </Stack>
      {aside}
    </Stack>
  );
}

export function ListSection<Item>({
  title,
  description,
  summary,
  items,
  pageSize,
  row,
}: ListSectionProps<Item>): ReactNode {
  return (
    <SectionCard title={title} description={description} summary={summary} flush>
      <Paged items={items} pageSize={pageSize} label={title} flush>
        {(visible) => (
          <Stack as="ul" divided>
            {visible.map((item, index) => (
              <ListRow key={index} {...row(item)} />
            ))}
          </Stack>
        )}
      </Paged>
    </SectionCard>
  );
}
