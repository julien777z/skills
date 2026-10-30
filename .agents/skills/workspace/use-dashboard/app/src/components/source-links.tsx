import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { Stack } from '@/components/primitives';
import { Badge } from '@/components/ui/badge';
import { safeUrl } from '@/lib/references';
import { SourceKind, type SourceLink } from '@/spec';

const KIND_LABELS: Record<SourceKind, string> = {
  [SourceKind.DOC]: 'Doc',
  [SourceKind.CODE]: 'Code',
  [SourceKind.DIFF]: 'Diff',
  [SourceKind.SPEC]: 'Spec',
  [SourceKind.PULL_REQUEST]: 'PR',
  [SourceKind.CONFIG]: 'Config',
  [SourceKind.TEST]: 'Test',
  [SourceKind.PAGE]: 'Page',
  [SourceKind.DATA]: 'Data',
};

function PillContent({ link, linked }: { link: SourceLink; linked: boolean }): ReactNode {
  return (
    <>
      <span className="bg-muted px-1.5 py-0.5 font-medium text-foreground">{KIND_LABELS[link.kind]}</span>
      <span className="flex items-center gap-1 px-1.5 py-0.5">
        {link.label}
        {linked && <ArrowUpRight className="size-3" />}
      </span>
    </>
  );
}

export function SourceLinks({ links }: { links: SourceLink[] }): ReactNode {
  return (
    <Stack direction="row" gap="xs" wrap>
      {links.map((link, index) => {
        const href = safeUrl(link.url);

        return href ? (
          <Badge key={index} variant="source" asChild>
            <a href={href} target="_blank" rel="noopener noreferrer">
              <PillContent link={link} linked />
            </a>
          </Badge>
        ) : (
          <Badge key={index} variant="source">
            <PillContent link={link} linked={false} />
          </Badge>
        );
      })}
    </Stack>
  );
}
