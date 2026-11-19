import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { ExternalLink, PullRequestIcon, RichText, StatusBadge } from '@/components';
import { PULL_REQUESTS } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { LinkItem, LinksSection as LinksSectionSpec } from '@/spec';
import { ListSection } from './list-section';

function LinkIcon({ item }: { item: LinkItem }): ReactNode {
  if (!item.state) {
    return <ArrowUpRight className="size-4 text-muted-foreground" aria-hidden="true" />;
  }

  return <PullRequestIcon state={item.state} className={cn('size-4', PULL_REQUESTS[item.state].text)} />;
}

export function LinksSection({ section }: { section: LinksSectionSpec }): ReactNode {
  return (
    <ListSection
      title={section.title}
      description={section.description}
      summary={(items) => (section.counted ? items.length : undefined)}
      items={section.items}
      pageSize={section.page_size}
      groupLabel={section.group_label}
      row={(item) => ({
        icon: <LinkIcon item={item} />,
        title: <ExternalLink href={item.url}>{item.label}</ExternalLink>,
        detail: item.detail && <RichText text={item.detail} />,
        aside: item.status && <StatusBadge label={item.status} tone={item.tone} />,
      })}
    />
  );
}
