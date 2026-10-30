import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { ExternalLink } from '@/components/external-link';
import { Stack } from '@/components/primitives';
import { StatusBadge } from '@/components/status-badge';
import { PULL_REQUESTS, TONES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { LinkItem, LinksSection as LinksSectionSpec } from '@/spec';
import { ListRow } from './list-row';
import { Paged } from './paged';
import { SectionCard } from './section-card';

function LinkIcon({ item }: { item: LinkItem }): ReactNode {
  if (!item.state) {
    return <ArrowUpRight className="size-4 text-muted-foreground" aria-hidden="true" />;
  }

  const style = PULL_REQUESTS[item.state];

  return (
    <svg viewBox="0 0 16 16" role="img" className={cn('size-4 fill-current', TONES[style.tone].text)}>
      <title>{style.label}</title>
      <path d={style.path} />
    </svg>
  );
}

export function LinksSection({ section }: { section: LinksSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} count={String(section.items.length)} flush>
      <Paged items={section.items} pageSize={section.page_size} label={section.title} flush>
        {(visible) => (
          <Stack as="ul" divided>
            {visible.map((item, index) => (
              <ListRow
                key={index}
                icon={<LinkIcon item={item} />}
                title={<ExternalLink href={item.url}>{item.label}</ExternalLink>}
                detail={item.detail}
                aside={item.status && <StatusBadge label={item.status} tone={item.tone} />}
              />
            ))}
          </Stack>
        )}
      </Paged>
    </SectionCard>
  );
}
