import type { ReactNode } from 'react';
import { Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';

interface ListRowProps {
  icon?: ReactNode;
  title: ReactNode;
  detail?: string;
  aside?: ReactNode;
  children?: ReactNode;
}

export function ListRow({ icon, title, detail, aside, children }: ListRowProps): ReactNode {
  return (
    <Stack as="li" direction="row" align="start" gap="md" inset="list">
      {icon && <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center">{icon}</span>}
      <Stack grow gap="xs">
        <Text weight="medium" breakAnywhere>
          {title}
        </Text>
        {detail && (
          <Text size="sm" tone="muted" breakAnywhere>
            <RichText text={detail} />
          </Text>
        )}
        {children}
      </Stack>
      {aside}
    </Stack>
  );
}
