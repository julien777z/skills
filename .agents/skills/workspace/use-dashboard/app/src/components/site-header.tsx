import {
  Activity,
  BookOpen,
  Calendar,
  ChartColumn,
  CircleCheck,
  Database,
  FileText,
  Gauge,
  GitPullRequest,
  LayoutDashboard,
  List,
  ListChecks,
  type LucideIcon,
  Menu,
  Package,
  Rocket,
  Scale,
  Settings,
  Shield,
  SquareKanban,
  TriangleAlert,
  Users,
  Workflow,
} from 'lucide-react';
import { type ReactNode, useEffect, useState } from 'react';

import { Stack, Text } from '@/components/primitives';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { relativeTime } from '@/lib/time';
import { cn } from '@/lib/utils';
import { IconName, type Label, type Page } from '@/spec';

const ICONS: Record<IconName, LucideIcon> = {
  [IconName.OVERVIEW]: LayoutDashboard,
  [IconName.PROGRESS]: Gauge,
  [IconName.BOARD]: SquareKanban,
  [IconName.CHECKLIST]: ListChecks,
  [IconName.LIST]: List,
  [IconName.CHART]: ChartColumn,
  [IconName.ACTIVITY]: Activity,
  [IconName.DIAGRAM]: Workflow,
  [IconName.DOCUMENT]: FileText,
  [IconName.GUIDE]: BookOpen,
  [IconName.LEGAL]: Scale,
  [IconName.SHIELD]: Shield,
  [IconName.PEOPLE]: Users,
  [IconName.DATA]: Database,
  [IconName.PACKAGE]: Package,
  [IconName.RELEASE]: Rocket,
  [IconName.PULL_REQUEST]: GitPullRequest,
  [IconName.SETTINGS]: Settings,
  [IconName.ALERT]: TriangleAlert,
  [IconName.CHECK]: CircleCheck,
  [IconName.CALENDAR]: Calendar,
};

interface SiteHeaderProps {
  title: string;
  icon: IconName;
  status?: Label;
  updatedAt: string;
  pages: Page[];
  current: number;
  onSelectPage: (position: number) => void;
}

function PageLinks({
  pages,
  current,
  vertical,
  onSelectPage,
}: Pick<SiteHeaderProps, 'pages' | 'current' | 'onSelectPage'> & { vertical: boolean }): ReactNode {
  return (
    <Stack as="ul" direction={vertical ? 'column' : 'row'} gap="xs">
      {pages.map((page, position) => {
        const Icon = ICONS[page.icon];
        const active = position === current;

        return (
          <li key={position}>
            <Button
              variant="ghost"
              size="sm"
              aria-current={active ? 'page' : undefined}
              onClick={() => onSelectPage(position)}
              className={cn(
                'text-muted-foreground hover:text-foreground',
                vertical && 'w-full justify-start',
                active && 'bg-accent text-foreground',
              )}
            >
              <Icon />
              {page.title}
            </Button>
          </li>
        );
      })}
    </Stack>
  );
}

export function SiteHeader({
  title,
  icon,
  status,
  updatedAt,
  pages,
  current,
  onSelectPage,
}: SiteHeaderProps): ReactNode {
  const [now, setNow] = useState(() => Date.now());
  const [menuOpen, setMenuOpen] = useState(false);
  const hasPages = pages.length > 1;
  const BrandIcon = ICONS[icon];

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 60_000);

    return () => window.clearInterval(timer);
  }, []);

  function handleSelectFromMenu(position: number) {
    setMenuOpen(false);
    onSelectPage(position);
  }

  return (
    <header className="sticky top-[env(safe-area-inset-top,0px)] z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <Stack direction="row" align="center" gap="lg" inset="page" frame="page" height="bar">
        {hasPages && (
          <Stack show="belowLg">
            <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="-ml-2" aria-label="Open pages">
                  <Menu />
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-72">
                <SheetHeader>
                  <SheetTitle>{title}</SheetTitle>
                </SheetHeader>
                <Stack as="nav" label="Dashboard pages" inset="page">
                  <PageLinks pages={pages} current={current} vertical onSelectPage={handleSelectFromMenu} />
                </Stack>
              </SheetContent>
            </Sheet>
          </Stack>
        )}
        <Stack direction="row" align="center" gap="sm">
          <span className="flex size-7 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <BrandIcon className="size-4" />
          </span>
          <Text weight="semibold" truncate>
            {title}
          </Text>
        </Stack>
        {hasPages && (
          <Stack as="nav" label="Dashboard pages" show="fromLg" scroll>
            <PageLinks pages={pages} current={current} vertical={false} onSelectPage={onSelectPage} />
          </Stack>
        )}
        <Stack direction="row" align="center" gap="md" push>
          <Stack show="fromSm">
            <Text size="xs" tone="muted">
              {relativeTime(updatedAt, now)}
            </Text>
          </Stack>
          {status && <StatusBadge label={status.label} tone={status.tone} />}
        </Stack>
      </Stack>
    </header>
  );
}
