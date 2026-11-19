import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { Stack } from '@/components/primitives';
import { Badge } from '@/components/ui/badge';
import { linkAttributes } from '@/lib/references';
import { PULL_REQUESTS } from '@/lib/tone';
import { cn, withKeys } from '@/lib/utils';
import { type PullRequestState, SourceKind, type SourceLink } from '@/spec';

const KIND_LABELS: Record<Exclude<SourceKind, typeof SourceKind.PULL_REQUEST>, string> = {
  [SourceKind.DOC]: 'Doc',
  [SourceKind.CODE]: 'Code',
  [SourceKind.DIFF]: 'Diff',
  [SourceKind.SPEC]: 'Spec',
  [SourceKind.CONFIG]: 'Config',
  [SourceKind.TEST]: 'Test',
  [SourceKind.PAGE]: 'Page',
  [SourceKind.DATA]: 'Data',
};

export function PullRequestIcon({ state, className }: { state: PullRequestState; className?: string }): ReactNode {
  const style = PULL_REQUESTS[state];

  return (
    <svg viewBox="0 0 16 16" role="img" className={cn('fill-current', className)}>
      <title>{style.label}</title>
      <path d={style.path} />
    </svg>
  );
}

function PullRequestPill({ label, url, state }: { label: string; url: string; state: PullRequestState }): ReactNode {
  const attributes = linkAttributes(url);
  const content = (
    <>
      <PullRequestIcon state={state} />
      {label}
    </>
  );

  return attributes ? (
    <Badge variant="pullRequest" className={PULL_REQUESTS[state].pill} asChild>
      <a {...attributes}>{content}</a>
    </Badge>
  ) : (
    <Badge variant="pullRequest" className={PULL_REQUESTS[state].pill}>
      {content}
    </Badge>
  );
}

function PillContent({
  kind,
  label,
  linked,
}: {
  kind: keyof typeof KIND_LABELS;
  label: string;
  linked: boolean;
}): ReactNode {
  return (
    <>
      <span className="bg-muted px-1.5 py-0.5 font-medium text-foreground">{KIND_LABELS[kind]}</span>
      <span className="flex items-center gap-1 px-1.5 py-0.5">
        {label}
        {linked && <ArrowUpRight className="size-3" />}
      </span>
    </>
  );
}

export function SourceLinks({ links }: { links: SourceLink[] }): ReactNode {
  return (
    <Stack direction="row" gap="xs" wrap>
      {withKeys(links, (link) => link.url).map(({ key, item: link }) => {
        if (link.kind === SourceKind.PULL_REQUEST) {
          return link.state && <PullRequestPill key={key} label={link.label} url={link.url} state={link.state} />;
        }

        const attributes = linkAttributes(link.url);

        return attributes ? (
          <Badge key={key} variant="source" asChild>
            <a {...attributes}>
              <PillContent kind={link.kind} label={link.label} linked />
            </a>
          </Badge>
        ) : (
          <Badge key={key} variant="source">
            <PillContent kind={link.kind} label={link.label} linked={false} />
          </Badge>
        );
      })}
    </Stack>
  );
}
