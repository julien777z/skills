import { cn } from 'cn';
import {
  Activity,
  BookOpen,
  Calendar,
  ChartColumn,
  CircleCheck,
  Database,
  FilePenLine,
  FileText,
  Gauge,
  GitCompareArrows,
  GitPullRequest,
  LayoutDashboard,
  List,
  ListChecks,
  Lock,
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
import { Button } from '@/components/ui/button';
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { relativeTime } from '@/lib/time';
import { IconName, type Label, type Page } from '@/spec';
import { StatusBadge } from './status-badge';
import { ToneDot } from './tone-dot';

const ICONS: Record<IconName, LucideIcon> = {
  [IconName.OVERVIEW]: LayoutDashboard,
  [IconName.PROPOSALS]: FilePenLine,
  [IconName.PROGRESS]: Gauge,
  [IconName.BOARD]: SquareKanban,
  [IconName.CHECKLIST]: ListChecks,
  [IconName.LIST]: List,
  [IconName.CHART]: ChartColumn,
  [IconName.ACTIVITY]: Activity,
  [IconName.COMPARE]: GitCompareArrows,
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

type PageLinksProps = Pick<SiteHeaderProps, 'pages' | 'current' | 'onSelectPage'>;

function PageLabel({ page }: { page: Page }): ReactNode {
  const Icon = page.locked ? Lock : ICONS[page.icon];

  return (
    <>
      <Icon />
      {page.title}
      {page.status && (
        <>
          <ToneDot tone={page.status.tone} />
          <Text srOnly>{`, ${page.status.label}`}</Text>
        </>
      )}
    </>
  );
}

function PageNavigation({ pages, current, onSelectPage }: PageLinksProps): ReactNode {
  return (
    <ScrollArea type="auto" className="min-w-0 flex-1 whitespace-nowrap">
      <NavigationMenu viewport={false} aria-label="Dashboard pages" className="max-w-none justify-start py-1">
        <NavigationMenuList className="justify-start">
          {pages.map((page, position) => (
            <NavigationMenuItem key={page.icon}>
              <NavigationMenuLink
                asChild
                active={position === current}
                className={cn(
                  navigationMenuTriggerStyle(),
                  'flex-row gap-2 bg-transparent text-muted-foreground data-active:bg-accent/50 data-active:text-foreground',
                )}
              >
                <button type="button" disabled={page.locked} onClick={() => onSelectPage(position)}>
                  <PageLabel page={page} />
                </button>
              </NavigationMenuLink>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  );
}

function PageMenu({ title, pages, current, onSelectPage }: PageLinksProps & { title: string }): ReactNode {
  const [open, setOpen] = useState(false);

  function handleSelect(position: number) {
    setOpen(false);
    onSelectPage(position);
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="-ml-2 lg:hidden" aria-label="Open pages">
          <Menu />
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>{title}</SheetTitle>
        </SheetHeader>
        <Stack as="nav" label="Dashboard pages" inset="page">
          <Stack as="ul" gap="xs">
            {pages.map((page, position) => (
              <li key={page.icon}>
                <Button
                  variant="ghost"
                  aria-current={position === current ? 'page' : undefined}
                  disabled={page.locked}
                  onClick={() => handleSelect(position)}
                  className="w-full justify-start text-muted-foreground aria-[current=page]:bg-accent aria-[current=page]:text-foreground"
                >
                  <PageLabel page={page} />
                </Button>
              </li>
            ))}
          </Stack>
        </Stack>
      </SheetContent>
    </Sheet>
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
  const hasPages = pages.length > 1;
  const BrandIcon = ICONS[icon];

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 60_000);

    return () => window.clearInterval(timer);
  }, []);

  return (
    <header className="sticky top-[env(safe-area-inset-top,0px)] z-40 w-full border-b bg-background">
      <Stack direction="row" align="center" gap="sm" inset="page" frame="page" height="bar">
        {hasPages && <PageMenu title={title} pages={pages} current={current} onSelectPage={onSelectPage} />}
        <Stack direction="row" align="center" gap="sm" shrink="belowLg">
          <Stack align="center" justify="center" badge="brand">
            <BrandIcon className="size-4" />
          </Stack>
          <Text weight="semibold">{title}</Text>
        </Stack>
        {hasPages && (
          <Stack direction="row" align="center" grow show="fromLg">
            <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
            <PageNavigation pages={pages} current={current} onSelectPage={onSelectPage} />
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
