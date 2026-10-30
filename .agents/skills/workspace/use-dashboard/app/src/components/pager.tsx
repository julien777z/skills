import { type ReactNode, useState } from 'react';

import { Button } from '@/components/ui/button';

export function usePage<T>(items: T[], size: number | undefined) {
  const [page, setPage] = useState(0);
  const pageSize = size && items.length > size ? size : items.length;
  const pages = Math.max(1, Math.ceil(items.length / Math.max(pageSize, 1)));
  const start = page * pageSize;

  return { page, pages, start, pageSize, visible: items.slice(start, start + pageSize), setPage };
}

export function Pager({
  label,
  total,
  state,
}: {
  label: string;
  total: number;
  state: { page: number; pages: number; start: number; pageSize: number; setPage: (page: number) => void };
}): ReactNode {
  if (state.pages < 2) {
    return null;
  }

  const last = Math.min(total, state.start + state.pageSize);

  return (
    <nav aria-label={`${label} pages`} className="flex items-center justify-between gap-2 pt-2">
      <Button variant="outline" size="sm" disabled={state.page === 0} onClick={() => state.setPage(state.page - 1)}>
        Previous
      </Button>
      <span aria-live="polite" className="text-xs text-muted-foreground tabular-nums">
        {state.start + 1}–{last} of {total}
      </span>
      <Button
        variant="outline"
        size="sm"
        disabled={state.page === state.pages - 1}
        onClick={() => state.setPage(state.page + 1)}
      >
        Next
      </Button>
    </nav>
  );
}
