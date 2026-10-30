import {
  Calendar,
  ChartColumn,
  CircleCheck,
  Database,
  FileText,
  LayoutDashboard,
  List,
  type LucideIcon,
  Settings,
  Shield,
  TriangleAlert,
  Users,
  Workflow,
} from 'lucide-react';
import { type ReactNode, useEffect, useState } from 'react';

import { Stack, Text } from '@/components/primitives';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';
import { type Page, PageIcon } from '@/spec';

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

interface AppSidebarProps {
  title: string;
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

export function AppSidebar({ title, updatedAt, pages, current, onSelectPage }: AppSidebarProps): ReactNode {
  const { isMobile, setOpenMobile } = useSidebar();
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), MINUTE_MS);

    return () => window.clearInterval(timer);
  }, []);

  function handleSelectPage(position: number) {
    onSelectPage(position);

    if (isMobile) {
      setOpenMobile(false);
    }
  }

  return (
    <Sidebar collapsible="offcanvas" variant="inset">
      <SidebarHeader>
        <Stack direction="row" align="center" gap="sm">
          <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
            <LayoutDashboard className="size-4" />
          </span>
          <Stack grow>
            <Text weight="semibold" size="sm" truncate>
              {title}
            </Text>
            <Text size="xs" tone="muted" truncate>
              {relativeTime(updatedAt, now)}
            </Text>
          </Stack>
        </Stack>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Pages</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {pages.map((page, position) => {
                const Icon = PAGE_ICONS[page.icon ?? (position === 0 ? PageIcon.OVERVIEW : PageIcon.DOCUMENT)];

                return (
                  <SidebarMenuItem key={position}>
                    <SidebarMenuButton
                      tooltip={page.title}
                      isActive={position === current}
                      aria-current={position === current ? 'page' : undefined}
                      onClick={() => handleSelectPage(position)}
                    >
                      <Icon />
                      <span>{page.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
