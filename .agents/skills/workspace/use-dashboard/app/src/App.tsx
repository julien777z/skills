import type * as React from 'react';
import { useEffect, useMemo, useState } from 'react';

import { AppSidebar } from '@/components/app-sidebar';
import { SectionCards } from '@/components/section-cards';
import { DashboardSection } from '@/components/sections/section';
import { SiteHeader } from '@/components/site-header';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { compileReferences, ReferencesContext, RichText } from '@/lib/links';
import { relativeTime } from '@/lib/time';
import { cn } from '@/lib/utils';
import type { Dashboard } from '@/spec';

const MINUTE = 60_000;

const LAYOUT_SIZES = {
  '--sidebar-width': 'calc(var(--spacing) * 64)',
  '--header-height': 'calc(var(--spacing) * 12)',
} as React.CSSProperties;

export function App({ dashboard }: { dashboard: Dashboard }) {
  const [current, setCurrent] = useState(0);
  const [now, setNow] = useState(() => Date.now());
  const references = useMemo(() => compileReferences(dashboard.references ?? []), [dashboard.references]);
  const page = dashboard.pages[current];
  const metrics = dashboard.metrics ?? [];
  const showSummary = current === 0 && (dashboard.progress || metrics.length > 0);

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), MINUTE);

    return () => window.clearInterval(timer);
  }, []);

  function select(position: number) {
    setCurrent(position);
    window.scrollTo({ top: 0 });
  }

  return (
    <ReferencesContext.Provider value={references}>
      <SidebarProvider style={LAYOUT_SIZES}>
        <AppSidebar
          variant="inset"
          title={dashboard.title}
          updated={relativeTime(dashboard.updated_at, now)}
          pages={dashboard.pages}
          current={current}
          onSelectPage={select}
        />
        <SidebarInset>
          <SiteHeader title={page.title} status={dashboard.status} />
          <div className="@container/main flex flex-1 flex-col gap-4 py-4 md:gap-6 md:py-6">
            {dashboard.subtitle && (
              <p className="max-w-[75ch] px-4 text-sm text-muted-foreground lg:px-6">
                <RichText text={dashboard.subtitle} />
              </p>
            )}
            {showSummary && <SectionCards progress={dashboard.progress} metrics={metrics} />}
            <div
              key={current}
              className={cn(
                'grid items-start gap-4 px-4 md:gap-6 lg:px-6',
                page.layout === 'rows' ? 'grid-cols-1' : 'grid-cols-[repeat(auto-fit,minmax(min(100%,380px),1fr))]',
              )}
            >
              {page.sections.map((section, index) => (
                <DashboardSection key={`${section.type}-${index}`} section={section} />
              ))}
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </ReferencesContext.Provider>
  );
}
