import type { ReactNode } from 'react';

import { Stack } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { SourceLinks } from '@/components/source-links';
import { StatusBadge } from '@/components/status-badge';
import { CHANGES } from '@/lib/tone';
import type { ChangesSection as ChangesSectionSpec } from '@/spec';
import { ListRow } from './list-row';
import { Paged } from './paged';
import { SectionCard } from './section-card';

export function ChangesSection({ section }: { section: ChangesSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} count={String(section.items.length)} flush>
      <Paged items={section.items} pageSize={section.page_size} label={section.title} flush>
        {(visible) => (
          <Stack as="ul" divided>
            {visible.map((item, index) => (
              <ListRow
                key={index}
                title={<RichText text={item.name} />}
                detail={item.detail}
                aside={<StatusBadge label={CHANGES[item.change].label} tone={CHANGES[item.change].tone} />}
              >
                {item.links && <SourceLinks links={item.links} />}
              </ListRow>
            ))}
          </Stack>
        )}
      </Paged>
    </SectionCard>
  );
}
