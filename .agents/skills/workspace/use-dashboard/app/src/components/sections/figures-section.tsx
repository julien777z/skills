import type { ReactNode } from 'react';

import { RichText } from '@/components';
import { Grid, Text } from '@/components/primitives';
import { withKeys } from '@/lib/utils';
import type { FiguresSection as FiguresSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function FiguresSection({ section }: { section: FiguresSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns={section.items.length > 1 ? 'pair' : 'single'} gap="lg">
        {withKeys(section.items, (figure) => figure.alt).map(({ key, item: figure }) => (
          <figure key={key} className="m-0 min-w-0 space-y-2">
            <img src={figure.image} alt={figure.alt} className="block h-auto w-full rounded-lg border" />
            {figure.caption && (
              <figcaption>
                <Text size="sm" tone="muted">
                  <RichText text={figure.caption} />
                </Text>
              </figcaption>
            )}
          </figure>
        ))}
      </Grid>
    </SectionCard>
  );
}
