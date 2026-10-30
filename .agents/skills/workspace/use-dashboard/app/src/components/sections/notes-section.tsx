import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import type { NotesSection as NotesSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function NotesSection({ section }: { section: NotesSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} count={String(section.items.length)}>
      <Stack as="ul" gap="xs" marker="bullet">
        {section.items.map((note, index) => (
          <Text key={index} as="li" size="sm" tone="muted">
            <RichText text={note} />
          </Text>
        ))}
      </Stack>
    </SectionCard>
  );
}
