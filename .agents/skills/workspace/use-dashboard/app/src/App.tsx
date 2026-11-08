import { type ReactNode, useMemo, useState } from 'react';

import { NoticeBanner, RichText, SectionCards, SiteHeader } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { DashboardSection } from '@/components/sections';
import { useReloadOnNewRevision } from '@/hooks/page-refresh';
import { References, ReferencesContext } from '@/lib/references';
import { withKeys } from '@/lib/utils';
import { type Dashboard, PageLayout } from '@/spec';

// A reload, whether the page's own or a viewer's frame loading a new copy, keeps window.name.
const OPEN_PAGE_PREFIX: string = 'dashboard-page:';

export function App({ dashboard }: { dashboard: Dashboard }): ReactNode {
  const [current, setCurrent] = useState(() =>
    Math.max(
      0,
      dashboard.pages.findIndex((candidate) => `${OPEN_PAGE_PREFIX}${candidate.title}` === window.name),
    ),
  );
  const references = useMemo(() => new References(dashboard.references ?? []), [dashboard.references]);
  const page = dashboard.pages[current];
  const metrics = dashboard.metrics ?? [];
  const progress = page.progress ?? (current === 0 ? dashboard.progress : undefined);
  const pageMetrics = current === 0 ? metrics : [];
  const showSummary = Boolean(progress) || pageMetrics.length > 0;

  useReloadOnNewRevision();

  function handleSelectPage(position: number) {
    setCurrent(position);

    window.name = `${OPEN_PAGE_PREFIX}${dashboard.pages[position].title}`;

    window.scrollTo({ top: 0 });
  }

  return (
    <ReferencesContext.Provider value={references}>
      <SiteHeader
        title={dashboard.title}
        icon={dashboard.icon}
        status={dashboard.status}
        updatedAt={dashboard.updated_at}
        pages={dashboard.pages}
        current={current}
        onSelectPage={handleSelectPage}
      />
      <Stack as="main" gap="xl" frame="page" block="page">
        <Stack gap="xs" inset="page">
          <Text as="h1" size="title" weight="bold">
            {page.title}
          </Text>
          {(page.subtitle ?? dashboard.subtitle) && (
            <Text as="p" tone="muted" measure>
              <RichText text={page.subtitle ?? dashboard.subtitle ?? ''} />
            </Text>
          )}
        </Stack>
        {dashboard.notice && (
          <Stack inset="page">
            <NoticeBanner notice={dashboard.notice} />
          </Stack>
        )}
        {showSummary && <SectionCards progress={progress} metrics={pageMetrics} />}
        <Grid key={current} inset="page" gap="lg" columns={page.layout === PageLayout.ROWS ? 'single' : 'wide'}>
          {withKeys(page.sections, (section) => section.title).map(({ key, item: section }) => (
            <DashboardSection key={key} section={section} />
          ))}
        </Grid>
      </Stack>
    </ReferencesContext.Provider>
  );
}
