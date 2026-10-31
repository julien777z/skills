import type { ReactNode } from 'react';

import { RichText, SourceLinks, StatusBadge } from '@/components';
import { CHANGES } from '@/lib/tone';
import type { ChangesSection as ChangesSectionSpec } from '@/spec';
import { ListSection } from './list-section';

export function ChangesSection({ section }: { section: ChangesSectionSpec }): ReactNode {
  return (
    <ListSection
      title={section.title}
      description={section.description}
      summary={section.items.length}
      items={section.items}
      pageSize={section.page_size}
      row={(item) => ({
        title: <RichText text={item.name} />,
        detail: item.detail && <RichText text={item.detail} />,
        aside: <StatusBadge label={CHANGES[item.change].label} tone={CHANGES[item.change].tone} />,
        body: item.links && <SourceLinks links={item.links} />,
      })}
    />
  );
}
