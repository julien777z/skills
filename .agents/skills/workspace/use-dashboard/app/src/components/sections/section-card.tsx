import type { ReactNode } from 'react';
import { Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { Card, CardAction, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface SectionCardProps {
  title: string;
  description?: string;
  count?: string;
  wide?: boolean;
  flush?: boolean;
  children: ReactNode;
}

export function SectionCard({
  title,
  description,
  count,
  wide = false,
  flush = false,
  children,
}: SectionCardProps): ReactNode {
  return (
    <Card className={cn('@container/card min-w-0', wide && 'col-span-full', flush && 'gap-4 pb-2')}>
      <CardHeader>
        <CardTitle>
          <h2>
            <RichText text={title} />
          </h2>
        </CardTitle>
        {description && (
          <CardDescription>
            <RichText text={description} />
          </CardDescription>
        )}
        {count && (
          <CardAction>
            <Text size="sm" tone="muted" numeric>
              {count}
            </Text>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className={cn(flush && 'px-0')}>{children}</CardContent>
    </Card>
  );
}
