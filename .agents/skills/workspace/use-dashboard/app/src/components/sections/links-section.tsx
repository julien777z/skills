import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { ExternalLink, RichText, StatusBadge } from '@/components';
import { PULL_REQUESTS, TONES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { LinkItem, LinksSection as LinksSectionSpec } from '@/spec';
import { ListSection } from './list-section';

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
    <ListSection
      title={section.title}
      description={section.description}
      summary={section.items.length}
      items={section.items}
      pageSize={section.page_size}
      row={(item) => ({
        icon: <LinkIcon item={item} />,
        title: <ExternalLink href={item.url}>{item.label}</ExternalLink>,
        detail: item.detail && <RichText text={item.detail} />,
        aside: item.status && <StatusBadge label={item.status} tone={item.tone} />,
      })}
    />
  );
}
