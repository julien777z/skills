import type { ReactNode } from 'react';

import { RichText } from '@/components/rich-text';
import type { NotesSection as NotesSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function NotesSection({ section }: { section: NotesSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} count={String(section.items.length)}>
      <ul className="grid list-disc gap-1.5 pl-5 text-sm text-muted-foreground">
        {section.items.map((note, index) => (
          <li key={index}>
            <RichText text={note} />
          </li>
        ))}
      </ul>
    </SectionCard>
  );
}
