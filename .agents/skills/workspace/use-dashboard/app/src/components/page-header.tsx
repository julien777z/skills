import { type ReactNode, useEffect, useState } from 'react';
import { Stack, Text } from '@/components/primitives';
import { relativeTime } from '@/lib/time';
import { RichText } from './rich-text';

export function PageHeader({
  title,
  subtitle,
  updatedAt,
}: {
  title: string;
  subtitle?: string;
  updatedAt: string;
}): ReactNode {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 60_000);

    return () => window.clearInterval(timer);
  }, []);

  return (
    <Stack gap="xs" inset="page">
      <Text as="h1" size="title" weight="bold">
        {title}
      </Text>
      {subtitle && (
        <Text as="p" tone="muted" measure>
          <RichText text={subtitle} />
        </Text>
      )}
      <Text as="p" size="xs" tone="muted">
        {relativeTime(updatedAt, now)}
      </Text>
    </Stack>
  );
}
