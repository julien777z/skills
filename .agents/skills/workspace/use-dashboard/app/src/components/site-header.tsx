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
import { type ReactNode, useState } from 'react';
import { Stack, Text } from '@/components/primitives';
import { Button } from '@/components/ui/button';
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from '@/components/ui/navigation-menu';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
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
  pages: Page[];
  current: number;
  onSelectPage: (position: number) => void;
}

type PageLinksProps = Pick<SiteHeaderProps, 'pages' | 'current' | 'onSelectPage'>;

function PageLabel({ page, icon = false }: { page: Page; icon?: boolean }): ReactNode {
  const Icon = page.locked ? Lock : ICONS[page.icon];

  return (
    <>
      {(icon || page.locked) && <Icon />}
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
      <NavigationMenu viewport={false} aria-label="Dashboard pages" className="max-w-none justify-start">
        <NavigationMenuList className="-ml-3 justify-start gap-0">
          {pages.map((page, position) => (
            <NavigationMenuItem key={page.icon}>
              <NavigationMenuLink
                asChild
                active={position === current}
                className="relative h-14 flex-row items-center gap-1.5 rounded-none px-3 py-0 text-muted-foreground after:absolute after:inset-x-3 after:bottom-0 after:h-0.5 hover:bg-transparent hover:text-foreground focus:bg-transparent focus-visible:ring-inset disabled:opacity-50 data-active:bg-transparent data-active:text-foreground data-active:after:bg-foreground data-active:hover:bg-transparent data-active:focus:bg-transparent"
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

function PageMenu({ title, icon, pages, current, onSelectPage }: SiteHeaderProps): ReactNode {
  const [open, setOpen] = useState(false);
  const BrandIcon = ICONS[icon];

  function handleSelect(position: number) {
    setOpen(false);
    onSelectPage(position);
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="-ml-2" aria-label="Open pages">
          <Menu />
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>
            <Stack direction="row" align="center" gap="sm">
              <BrandIcon className="size-4" />
              {title}
            </Stack>
          </SheetTitle>
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
                  <PageLabel page={page} icon />
                </Button>
              </li>
            ))}
          </Stack>
        </Stack>
      </SheetContent>
    </Sheet>
  );
}

export function SiteHeader(props: SiteHeaderProps): ReactNode {
  const { status, pages, current } = props;

  return (
    <header className="sticky top-[env(safe-area-inset-top,0px)] z-40 w-full border-b bg-background">
      <Stack direction="row" align="center" gap="sm" inset="page" frame="page" height="bar">
        <Stack direction="row" align="center" gap="sm" show="belowLg">
          <PageMenu {...props} />
          <Text size="sm" weight="medium">
            {pages[current].title}
          </Text>
        </Stack>
        <Stack direction="row" align="center" grow show="fromLg">
          <PageNavigation {...props} />
        </Stack>
        {status && (
          <Stack push>
            <StatusBadge label={status.label} tone={status.tone} />
          </Stack>
        )}
      </Stack>
    </header>
  );
}
