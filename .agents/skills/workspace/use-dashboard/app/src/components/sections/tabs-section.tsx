import { type ReactNode, useState } from 'react';

import { Stack } from '@/components/primitives';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { withKeys } from '@/lib/utils';
import type { Tab, TabsSection as TabsSectionSpec } from '@/spec';
import { DashboardSection } from './dashboard-section';
import { InTabPanelContext, SectionCard } from './section-card';

function TabSections({ tab }: { tab: Tab }): ReactNode {
  return (
    <InTabPanelContext.Provider value>
      <Stack gap="xl">
        {withKeys(tab.sections, (section) => section.title).map(({ key, item: section }) => (
          <DashboardSection key={key} section={section} />
        ))}
      </Stack>
    </InTabPanelContext.Provider>
  );
}

export function TabsSection({ section }: { section: TabsSectionSpec }): ReactNode {
  const tabs = withKeys(
    section.tabs.filter((tab) => tab.sections.length > 0),
    (tab) => tab.label,
  );
  const [chosen, setChosen] = useState('');
  const selected = tabs.some(({ key }) => key === chosen) ? chosen : tabs[0].key;

  if (tabs.length === 1) {
    return (
      <SectionCard title={section.title} description={section.description} wide>
        <TabSections tab={tabs[0].item} />
      </SectionCard>
    );
  }

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Tabs value={selected} onValueChange={setChosen} className="gap-4">
        <TabsList variant="line" aria-label={section.title} className="max-w-full justify-start overflow-x-auto">
          {tabs.map(({ key, item: tab }) => (
            <TabsTrigger key={key} value={key} className="flex-none">
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>
        {tabs.map(({ key, item: tab }) => (
          <TabsContent key={key} value={key}>
            <TabSections tab={tab} />
          </TabsContent>
        ))}
      </Tabs>
    </SectionCard>
  );
}
