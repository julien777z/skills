import type { ReactNode } from 'react';

import { RichText } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { withKeys } from '@/lib/utils';

export function TextList({ items, numbered = false }: { items: string[]; numbered?: boolean }): ReactNode {
  return (
    <Stack as={numbered ? 'ol' : 'ul'} gap="xs" marker={numbered ? 'number' : 'bullet'}>
      {withKeys(items, (item) => item).map(({ key, item }) => (
        <Text key={key} as="li" size="sm" tone="muted">
          <RichText text={item} />
        </Text>
      ))}
    </Stack>
  );
}
