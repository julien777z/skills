import type { ReactNode } from 'react';

import { StatusBadge } from '@/components/status-badge';
import { Card, CardAction, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface SectionCardProps {
  title: string;
  count?: string;
  wide?: boolean;
  flush?: boolean;
  children: ReactNode;
}

export function SectionCard({ title, count, wide = false, flush = false, children }: SectionCardProps): ReactNode {
  return (
    <Card className={cn('@container/card min-w-0', wide && 'col-span-full', flush && 'gap-4 pb-2')}>
      <CardHeader>
        <CardTitle>
          <h2>{title}</h2>
        </CardTitle>
        {count && (
          <CardAction>
            <StatusBadge label={count} dot={false} />
          </CardAction>
        )}
      </CardHeader>
      <CardContent className={cn(flush && 'px-0')}>{children}</CardContent>
    </Card>
  );
}
