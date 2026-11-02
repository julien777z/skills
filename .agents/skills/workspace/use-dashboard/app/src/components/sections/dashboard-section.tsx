import type { ReactNode } from 'react';

import { type Section, SectionType } from '@/spec';
import { BoardSection } from './board-section';
import { CalloutSection } from './callout-section';
import { ChangesSection } from './changes-section';
import { DiagramSection } from './diagram-section';
import { LinksSection } from './links-section';
import { NotesSection } from './notes-section';
import { OutlineSection } from './outline-section';
import { QuestionsSection } from './questions-section';
import { TableSection } from './table-section';

export function DashboardSection({ section }: { section: Section }): ReactNode {
  switch (section.type) {
    case SectionType.BOARD:
      return <BoardSection section={section} />;
    case SectionType.QUESTIONS:
      return <QuestionsSection section={section} />;
    case SectionType.LINKS:
      return <LinksSection section={section} />;
    case SectionType.CHANGES:
      return <ChangesSection section={section} />;
    case SectionType.TABLE:
      return <TableSection section={section} />;
    case SectionType.NOTES:
      return <NotesSection section={section} />;
    case SectionType.OUTLINE:
      return <OutlineSection section={section} />;
    case SectionType.CALLOUT:
      return <CalloutSection section={section} />;
    case SectionType.DIAGRAM:
      return <DiagramSection section={section} />;
  }
}
