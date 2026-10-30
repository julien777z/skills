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
import type * as React from 'react';

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
import type { Page, PageIcon } from '@/spec';

const PAGE_ICONS: Record<PageIcon, LucideIcon> = {
  overview: LayoutDashboard,
  list: List,
  chart: ChartColumn,
  diagram: Workflow,
  document: FileText,
  shield: Shield,
  people: Users,
  data: Database,
  settings: Settings,
  alert: TriangleAlert,
  check: CircleCheck,
  calendar: Calendar,
};

interface AppSidebarProps {
  variant?: React.ComponentProps<typeof Sidebar>['variant'];
  title: string;
  updated: string;
  pages: Page[];
  current: number;
  onSelectPage: (position: number) => void;
}

export function AppSidebar({ variant, title, updated, pages, current, onSelectPage }: AppSidebarProps) {
  const { isMobile, setOpenMobile } = useSidebar();

  function select(position: number) {
    onSelectPage(position);

    if (isMobile) {
      setOpenMobile(false);
    }
  }

  return (
    <Sidebar collapsible="offcanvas" variant={variant}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" className="cursor-default hover:bg-transparent active:bg-transparent">
              <span className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <LayoutDashboard className="size-4" />
              </span>
              <span className="grid min-w-0 flex-1 text-left leading-tight">
                <span className="truncate font-semibold">{title}</span>
                <span className="truncate text-xs text-muted-foreground">{updated}</span>
              </span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Pages</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {pages.map((page, position) => {
                const Icon = PAGE_ICONS[page.icon ?? (position === 0 ? 'overview' : 'document')];

                return (
                  <SidebarMenuItem key={page.title}>
                    <SidebarMenuButton
                      tooltip={page.title}
                      isActive={position === current}
                      aria-current={position === current ? 'page' : undefined}
                      onClick={() => select(position)}
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
