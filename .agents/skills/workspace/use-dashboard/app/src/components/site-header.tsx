import {
  Calendar,
  ChartColumn,
  CircleCheck,
  Database,
  FileText,
  LayoutDashboard,
  List,
  type LucideIcon,
  Menu,
  Settings,
  Shield,
  TriangleAlert,
  Users,
  Workflow,
} from 'lucide-react';
import { type ReactNode, useEffect, useState } from 'react';

import { Stack, Text } from '@/components/primitives';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { cn } from '@/lib/utils';
import { type Label, type Page, PageIcon } from '@/spec';

const MINUTE_MS: number = 60_000;

const MINUTES_PER_DAY: number = 1_440;

const PAGE_ICONS: Record<PageIcon, LucideIcon> = {
  [PageIcon.OVERVIEW]: LayoutDashboard,
  [PageIcon.LIST]: List,
  [PageIcon.CHART]: ChartColumn,
  [PageIcon.DIAGRAM]: Workflow,
  [PageIcon.DOCUMENT]: FileText,
  [PageIcon.SHIELD]: Shield,
  [PageIcon.PEOPLE]: Users,
  [PageIcon.DATA]: Database,
  [PageIcon.SETTINGS]: Settings,
  [PageIcon.ALERT]: TriangleAlert,
  [PageIcon.CHECK]: CircleCheck,
  [PageIcon.CALENDAR]: Calendar,
};

interface SiteHeaderProps {
  title: string;
  status?: Label;
  updatedAt: string;
  pages: Page[];
  current: number;
  onSelectPage: (position: number) => void;
}

function relativeTime(iso: string, now: number): string {
  const then = new Date(iso);
  const minutes = Math.round((now - then.getTime()) / MINUTE_MS);

  if (minutes < 1) {
    return 'Updated just now';
  }

  if (minutes < 60) {
    return `Updated ${minutes} min ago`;
  }

  if (minutes < MINUTES_PER_DAY) {
    return `Updated ${Math.round(minutes / 60)} h ago`;
  }

  return `Updated ${then.toLocaleDateString()}`;
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
        const Icon = PAGE_ICONS[page.icon ?? (position === 0 ? PageIcon.OVERVIEW : PageIcon.DOCUMENT)];
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

export function SiteHeader({ title, status, updatedAt, pages, current, onSelectPage }: SiteHeaderProps): ReactNode {
  const [now, setNow] = useState(() => Date.now());
  const [menuOpen, setMenuOpen] = useState(false);
  const hasPages = pages.length > 1;

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), MINUTE_MS);

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
          <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="-ml-2 lg:hidden" aria-label="Open pages">
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
        )}
        <Stack direction="row" align="center" gap="sm">
          <span className="flex size-7 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <LayoutDashboard className="size-4" />
          </span>
          <Text weight="semibold" truncate>
            {title}
          </Text>
        </Stack>
        {hasPages && (
          <Stack as="nav" label="Dashboard pages" show="wide">
            <PageLinks pages={pages} current={current} vertical={false} onSelectPage={onSelectPage} />
          </Stack>
        )}
        <Stack direction="row" align="center" gap="md" push>
          <span className="hidden sm:inline">
            <Text size="xs" tone="muted">
              {relativeTime(updatedAt, now)}
            </Text>
          </span>
          {status && <StatusBadge label={status.label} tone={status.tone} />}
        </Stack>
      </Stack>
    </header>
  );
}
