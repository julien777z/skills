import { cn } from 'cn';
import { type Context, createContext, type ReactNode, useContext } from 'react';
import { RichText } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { Badge } from '@/components/ui/badge';
import { Card, CardAction, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { sectionAnchor } from '@/lib/utils';

export const InDialogContext: Context<boolean> = createContext(false);

export const InTabPanelContext: Context<boolean> = createContext(false);

interface SectionCardProps {
  title: string;
  description?: string;
  summary?: number | string;
  wide?: boolean;
  flush?: boolean;
  children: ReactNode;
}

function Count({ summary }: { summary?: number | string }): ReactNode {
  return typeof summary === 'number' ? (
    <Badge variant="secondary" className="px-1.5 font-normal text-muted-foreground tabular-nums">
      {summary}
    </Badge>
  ) : null;
}

function Summary({ summary }: { summary?: number | string }): ReactNode {
  return typeof summary === 'string' ? (
    <Text size="sm" tone="muted" numeric>
      {summary}
    </Text>
  ) : null;
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
  const inTabPanel = useContext(InTabPanelContext);

  if (inTabPanel) {
    return (
      <div {...sectionAnchor(title)} className={cn('min-w-0 scroll-mt-20', wide && 'col-span-full')}>
        <Stack gap="lg">
          <Stack direction="row" align="start" justify="between" gap="md">
            <Stack gap="xs">
              <Stack direction="row" align="center" gap="sm">
                <Text as="h3" size="sm" weight="semibold">
                  <RichText text={title} />
                </Text>
                <Count summary={summary} />
              </Stack>
              {description && (
                <Text size="sm" tone="muted">
                  <RichText text={description} />
                </Text>
              )}
            </Stack>
            <Summary summary={summary} />
          </Stack>
          {children}
        </Stack>
      </div>
    );
  }

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
      {...sectionAnchor(title)}
      className={cn('@container/card min-w-0 scroll-mt-20 shadow-none', wide && 'col-span-full', flush && 'gap-4 pb-2')}
    >
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <h2>
            <RichText text={title} />
          </h2>
          <Count summary={summary} />
        </CardTitle>
        {description && (
          <CardDescription>
            <RichText text={description} />
          </CardDescription>
        )}
        {typeof summary === 'string' && (
          <CardAction>
            <Summary summary={summary} />
          </CardAction>
        )}
      </CardHeader>
      <CardContent className={cn(flush && 'px-0')}>{children}</CardContent>
    </Card>
  );
}
