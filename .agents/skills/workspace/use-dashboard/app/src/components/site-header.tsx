import { StatusBadge } from '@/components/status';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import type { Label } from '@/spec';

export function SiteHeader({ title, status }: { title: string; status?: Label }) {
  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b">
      <div className="flex w-full min-w-0 items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
        <h1 className="truncate text-base font-medium">{title}</h1>
        {status && (
          <div className="ml-auto flex shrink-0 items-center gap-2">
            <StatusBadge label={status.label} tone={status.tone} />
          </div>
        )}
      </div>
    </header>
  );
}
