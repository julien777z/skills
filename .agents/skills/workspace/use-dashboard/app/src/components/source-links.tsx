import { ArrowUpRight } from 'lucide-react';
import type { ReactNode } from 'react';

import { Stack } from '@/components/primitives';
import { Badge } from '@/components/ui/badge';
import { safeUrl } from '@/lib/references';
import type { SourceLink } from '@/spec';

export function SourceLinks({ links }: { links: SourceLink[] }): ReactNode {
  return (
    <Stack direction="row" gap="xs" wrap>
      {links.map((link, index) => {
        const href = safeUrl(link.url);

        return href ? (
          <Badge key={index} variant="outline" asChild>
            <a href={href} target="_blank" rel="noopener noreferrer">
              {link.label}
              <ArrowUpRight />
            </a>
          </Badge>
        ) : (
          <Badge key={index} variant="outline">
            {link.label}
          </Badge>
        );
      })}
    </Stack>
  );
}
