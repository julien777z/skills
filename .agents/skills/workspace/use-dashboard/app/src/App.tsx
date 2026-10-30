import { type CSSProperties, type ReactNode, useMemo, useState } from 'react';

import { AppSidebar } from '@/components/app-sidebar';
import { Grid, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { SectionCards } from '@/components/section-cards';
import { DashboardSection } from '@/components/sections';
import { SiteHeader } from '@/components/site-header';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { References, ReferencesContext } from '@/lib/references';
import { type Dashboard, PageLayout } from '@/spec';

type LayoutSizes = CSSProperties & Record<'--sidebar-width' | '--header-height', string>;

const LAYOUT_SIZES: LayoutSizes = {
  '--sidebar-width': 'calc(var(--spacing) * 64)',
  '--header-height': 'calc(var(--spacing) * 12)',
};

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
      <SidebarProvider style={LAYOUT_SIZES}>
        <AppSidebar
          title={dashboard.title}
          updatedAt={dashboard.updated_at}
          pages={dashboard.pages}
          current={current}
          onSelectPage={handleSelectPage}
        />
        <SidebarInset>
          <SiteHeader title={page.title} status={dashboard.status} />
          <div className="@container/main flex flex-1 flex-col gap-4 py-4 md:gap-6 md:py-6">
            {dashboard.subtitle && (
              <Grid inset="page">
                <Text as="p" size="sm" tone="muted" measure>
                  <RichText text={dashboard.subtitle} />
                </Text>
              </Grid>
            )}
            {showSummary && <SectionCards progress={dashboard.progress} metrics={metrics} />}
            <Grid key={current} inset="page" gap="lg" columns={page.layout === PageLayout.ROWS ? 'single' : 'wide'}>
              {page.sections.map((section, index) => (
                <DashboardSection key={index} section={section} />
              ))}
            </Grid>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </ReferencesContext.Provider>
  );
}
