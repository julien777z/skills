import type { ReactNode } from 'react';

import type { NotesSection as NotesSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { TextList } from './text-list';

export function NotesSection({ section }: { section: NotesSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} summary={section.items.length}>
      <TextList items={section.items} />
    </SectionCard>
  );
}
