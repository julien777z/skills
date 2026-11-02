import { type ReactNode, useRef, useState } from 'react';

import { RichText } from '@/components';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { withKeys } from '@/lib/utils';
import type { TableSection as TableSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
  const [open, setOpen] = useState(false);
  const [opened, setOpened] = useState(0);
  const opener = useRef<HTMLButtonElement | null>(null);
  const details = section.details;

  function handleOpenRow(position: number, button: HTMLButtonElement) {
    opener.current = button;

    setOpened(position);
    setOpen(true);
  }

  return (
    <SectionCard
      title={section.title}
      description={section.description}
      summary={section.counted ? section.rows.length : undefined}
      wide
    >
      <div className="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader className="bg-muted">
            <TableRow>
              {withKeys(section.columns, (column) => column).map(({ key, item: column }) => (
                <TableHead key={key} className="px-4">
                  <RichText text={column} />
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {withKeys(section.rows, (cells) => cells.join('\u0000')).map(({ key: rowKey, item: cells }, position) => (
              <TableRow
                key={rowKey}
                className={details && 'relative focus-within:bg-muted/50 [&_a]:relative [&_a]:z-10'}
              >
                {withKeys(cells, (cell) => cell).map(({ key, item: cell }, column) => (
                  <TableCell key={key} className="px-4 align-top whitespace-normal tabular-nums">
                    {details && column === 0 ? (
                      <button
                        type="button"
                        onClick={(event) => handleOpenRow(position, event.currentTarget)}
                        className="text-left after:absolute after:inset-0 focus-visible:outline-none"
                      >
                        {cell}
                      </button>
                    ) : (
                      <RichText text={cell} />
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {details && <SectionDialog section={details[opened]} open={open} onOpenChange={setOpen} opener={opener} />}
    </SectionCard>
  );
}
