import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { Badge } from '@/components/ui/badge';
import { linkAttributes } from '@/lib/references';
import { PULL_REQUESTS } from '@/lib/tone';
import { withKeys } from '@/lib/utils';
import { type PullRequestState, SourceKind, type SourceLink } from '@/spec';
import { PullRequestIcon } from './pull-request-icon';

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

function PullRequestPill({ label, url, state }: { label: string; url: string; state: PullRequestState }): ReactNode {
  const attributes = linkAttributes(url);
  const content = (
    <>
      <PullRequestIcon state={state} />
      {label}
    </>
  );

  return attributes ? (
    <Badge className={PULL_REQUESTS[state].pill} asChild>
      <a {...attributes}>{content}</a>
    </Badge>
  ) : (
    <Badge className={PULL_REQUESTS[state].pill}>{content}</Badge>
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
      <Text weight="medium">{KIND_LABELS[kind]}</Text>
      <Text tone="muted">{label}</Text>
      {linked && <ArrowUpRight />}
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
          <Badge key={key} variant="outline" asChild>
            <a {...attributes}>
              <PillContent kind={link.kind} label={link.label} linked />
            </a>
          </Badge>
        ) : (
          <Badge key={key} variant="outline">
            <PillContent kind={link.kind} label={link.label} linked={false} />
          </Badge>
        );
      })}
    </Stack>
  );
}
