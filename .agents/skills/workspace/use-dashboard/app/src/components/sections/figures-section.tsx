import type { ReactNode } from 'react';

import { RichText } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { withKeys } from '@/lib/utils';
import type { FiguresSection as FiguresSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function FiguresSection({ section }: { section: FiguresSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns={section.stacked || section.items.length === 1 ? 'single' : 'pair'} gap="lg">
        {withKeys(section.items, (figure) => figure.alt).map(({ key, item: figure }) => (
          <Stack key={key} as="figure" gap="sm" frame={section.stacked ? 'readable' : 'none'}>
            <img src={figure.image} alt={figure.alt} className="block h-auto w-full rounded-lg border" />
            {figure.caption && (
              <Text as="figcaption" size="sm" tone="muted">
                <RichText text={figure.caption} />
              </Text>
            )}
          </Stack>
        ))}
      </Grid>
    </SectionCard>
  );
}
