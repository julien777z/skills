import { type Context, createContext, type ReactNode, useContext } from 'react';

import { RichText } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { Card, CardAction, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { cn } from '@/lib/utils';

export const InDialogContext: Context<boolean> = createContext(false);

interface SectionCardProps {
  title: string;
  description?: string;
  summary?: ReactNode;
  wide?: boolean;
  flush?: boolean;
  children: ReactNode;
}

export function SectionCard({
  title,
  description,
  summary,
  wide = false,
  flush = false,
  children,
}: SectionCardProps): ReactNode {
  const inDialog = useContext(InDialogContext);

  if (inDialog) {
    return (
      <Stack gap="lg">
        <DialogHeader>
          <DialogTitle>
            <RichText text={title} />
          </DialogTitle>
          {description && (
            <DialogDescription>
              <RichText text={description} />
            </DialogDescription>
          )}
        </DialogHeader>
        {children}
      </Stack>
    );
  }

  return (
    <Card
      data-section-title={title}
      className={cn('@container/card min-w-0 scroll-mt-20', wide && 'col-span-full', flush && 'gap-4 pb-2')}
    >
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
        {summary === undefined ? null : (
          <CardAction>
            <Text size="sm" tone="muted" numeric>
              {summary}
            </Text>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className={cn(flush && 'px-0')}>{children}</CardContent>
    </Card>
  );
}
