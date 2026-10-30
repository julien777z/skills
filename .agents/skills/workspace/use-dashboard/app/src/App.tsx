import { type ReactNode, useMemo, useState } from 'react';

import { Grid, Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { SectionCards } from '@/components/section-cards';
import { DashboardSection } from '@/components/sections';
import { SiteHeader } from '@/components/site-header';
import { References, ReferencesContext } from '@/lib/references';
import { type Dashboard, PageLayout } from '@/spec';

export function App({ dashboard }: { dashboard: Dashboard }): ReactNode {
  const [current, setCurrent] = useState(0);
  const references = useMemo(() => new References(dashboard.references ?? []), [dashboard.references]);
  const page = dashboard.pages[current];
  const metrics = dashboard.metrics ?? [];
  const showSummary = current === 0 && (dashboard.progress || metrics.length > 0);

  function handleSelectPage(position: number) {
    setCurrent(position);
    window.scrollTo({ top: 0 });
  }

  return (
    <ReferencesContext.Provider value={references}>
      <SiteHeader
        title={dashboard.title}
        status={dashboard.status}
        updatedAt={dashboard.updated_at}
        pages={dashboard.pages}
        current={current}
        onSelectPage={handleSelectPage}
      />
      <main className="@container/main mx-auto flex w-full max-w-screen-2xl flex-col gap-6 py-8">
        <Stack gap="xs" inset="page">
          <Text as="h1" size="title" weight="bold">
            {page.title}
          </Text>
          {dashboard.subtitle && (
            <Text as="p" tone="muted" measure>
              <RichText text={dashboard.subtitle} />
            </Text>
          )}
        </Stack>
        {showSummary && <SectionCards progress={dashboard.progress} metrics={metrics} />}
        <Grid key={current} inset="page" gap="lg" columns={page.layout === PageLayout.ROWS ? 'single' : 'wide'}>
          {page.sections.map((section, index) => (
            <DashboardSection key={index} section={section} />
          ))}
        </Grid>
      </main>
    </ReferencesContext.Provider>
  );
}
