import { type KeyboardEvent, type ReactNode, useId, useRef, useState } from 'react';

import { Stack } from '@/components/primitives';
import { Button } from '@/components/ui/button';
import { cn, withKeys } from '@/lib/utils';
import type { Tab, TabsSection as TabsSectionSpec } from '@/spec';
import { DashboardSection } from './dashboard-section';
import { InTabPanelContext, SectionCard } from './section-card';

const NEXT_TAB_KEYS: Record<string, number> = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };

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
  const tabs = section.tabs.filter((tab) => tab.sections.length > 0);
  const [current, setCurrent] = useState(0);
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);
  const baseId = useId();
  const selected = Math.min(current, tabs.length - 1);

  function handleKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const step = NEXT_TAB_KEYS[event.key];
    const target =
      event.key === 'Home'
        ? 0
        : event.key === 'End'
          ? tabs.length - 1
          : step === undefined
            ? undefined
            : (selected + step + tabs.length) % tabs.length;

    if (target === undefined) {
      return;
    }

    event.preventDefault();

    setCurrent(target);

    buttons.current[target]?.focus();
  }

  if (tabs.length === 1) {
    return (
      <SectionCard title={section.title} description={section.description} wide>
        <TabSections tab={tabs[0]} />
      </SectionCard>
    );
  }

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Stack gap="lg">
        <div
          role="tablist"
          aria-label={section.title}
          onKeyDown={handleKeyDown}
          className="flex gap-1 overflow-x-auto border-b"
        >
          {tabs.map((tab, position) => {
            const active = position === selected;

            return (
              <Button
                key={tab.label}
                ref={(element) => {
                  buttons.current[position] = element;
                }}
                id={`${baseId}-tab-${position}`}
                role="tab"
                variant="ghost"
                size="sm"
                aria-selected={active}
                aria-controls={active ? `${baseId}-panel-${position}` : undefined}
                tabIndex={active ? 0 : -1}
                onClick={() => setCurrent(position)}
                className={cn(
                  '-mb-px shrink-0 whitespace-nowrap rounded-b-none border-b-2 border-transparent text-muted-foreground hover:bg-transparent hover:text-foreground dark:hover:bg-transparent',
                  active && 'border-foreground font-semibold text-foreground',
                )}
              >
                {tab.label}
              </Button>
            );
          })}
        </div>
        <div
          key={selected}
          role="tabpanel"
          id={`${baseId}-panel-${selected}`}
          aria-labelledby={`${baseId}-tab-${selected}`}
        >
          <TabSections tab={tabs[selected]} />
        </div>
      </Stack>
    </SectionCard>
  );
}
