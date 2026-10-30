import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { StatusBadge } from '@/components/status-badge';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import type { Label } from '@/spec';

export function SiteHeader({ title, status }: { title: string; status?: Label }): ReactNode {
  return (
    <header className="flex h-(--header-height) shrink-0 items-center border-b">
      <Stack direction="row" align="center" gap="sm" grow inset="page">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mx-1 data-[orientation=vertical]:h-4" />
        <Text as="h1" size="base" weight="medium" truncate>
          {title}
        </Text>
        {status && (
          <Stack direction="row" justify="end" grow>
            <StatusBadge label={status.label} tone={status.tone} />
          </Stack>
        )}
      </Stack>
    </header>
  );
}
