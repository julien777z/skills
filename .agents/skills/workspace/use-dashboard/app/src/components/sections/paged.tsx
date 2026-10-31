import { type ReactNode, useState } from 'react';

import { Stack, Text } from '@/components/primitives';
import { Button } from '@/components/ui/button';

interface PagedProps<Item> {
  items: Item[];
  pageSize?: number;
  label: string;
  flush?: boolean;
  children: (visible: Item[]) => ReactNode;
}

export function Paged<Item>({ items, pageSize, label, flush = false, children }: PagedProps<Item>): ReactNode {
  const [page, setPage] = useState(0);
  const size = pageSize && items.length > pageSize ? pageSize : items.length;
  const pages = Math.max(1, Math.ceil(items.length / Math.max(size, 1)));
  const start = page * size;
  const last = Math.min(items.length, start + size);

  return (
    <>
      {children(items.slice(start, last))}
      {pages > 1 && (
        <Stack
          as="nav"
          label={`${label} pages`}
          direction="row"
          align="center"
          justify="between"
          gap="sm"
          inset={flush ? 'page' : 'none'}
        >
          <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage(page - 1)}>
            Previous
          </Button>
          <Text size="xs" tone="muted" numeric>
            {start + 1}–{last} of {items.length}
          </Text>
          <Button variant="outline" size="sm" disabled={page === pages - 1} onClick={() => setPage(page + 1)}>
            Next
          </Button>
        </Stack>
      )}
    </>
  );
}
