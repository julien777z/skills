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

interface ComparedSides {
  current?: string;
  proposed?: string;
}

/** What a part does on the current side and on the proposed side, each on its own labeled line. */
export function ComparedLines({ current, proposed }: ComparedSides): ReactNode {
  const lines = [
    { label: 'Current', text: current },
    { label: 'Proposed', text: proposed },
  ].flatMap(({ label, text }) => (text ? [{ label, text }] : []));

  if (lines.length === 0) {
    return null;
  }

  return (
    <Stack gap="xs">
      {lines.map(({ label, text }) => (
        <Text key={label} as="p" size="sm" tone="muted" breakAnywhere>
          <Text as="b" weight="semibold" tone="strong">
            {label}
          </Text>{' '}
          <RichText text={text} />
        </Text>
      ))}
    </Stack>
  );
}
