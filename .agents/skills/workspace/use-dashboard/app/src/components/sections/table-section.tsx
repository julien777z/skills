import { type ReactNode, useRef, useState } from 'react';

import { RichText } from '@/components';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { cn, withKeys } from '@/lib/utils';
import type { TableSection as TableSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

const PROSE_CELL_LENGTH: number = 40;

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
  const [open, setOpen] = useState(false);
  const [openedRow, setOpenedRow] = useState('');
  const opener = useRef<HTMLButtonElement | null>(null);
  const details = section.details;
  const rows = withKeys(section.rows, (cells) => cells.join('\u0000'));
  const openedDetails = details?.[rows.findIndex(({ key }) => key === openedRow)];
  const proseColumns = section.columns.map((_, column) =>
    section.rows.some((cells) => cells[column].length > PROSE_CELL_LENGTH),
  );

  if (openedRow && !openedDetails) {
    setOpenedRow('');
    setOpen(false);
  }

  function handleOpenRow(rowKey: string, button: HTMLButtonElement) {
    opener.current = button;

    setOpenedRow(rowKey);
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
              {withKeys(section.columns, (column) => column).map(({ key, item: column }, index) => (
                <TableHead key={key} className={cn('px-4', proseColumns[index] && 'min-w-64')}>
                  <RichText text={column} />
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map(({ key: rowKey, item: cells }) => (
              <TableRow
                key={rowKey}
                className={
                  details &&
                  'relative focus-within:bg-muted/50 [&_a]:relative [&_a]:z-10 [&_[data-reference]]:relative [&_[data-reference]]:z-10'
                }
              >
                {withKeys(cells, (cell) => cell).map(({ key, item: cell }, column) => (
                  <TableCell
                    key={key}
                    className={cn('px-4 align-top whitespace-normal tabular-nums', proseColumns[column] && 'min-w-64')}
                  >
                    {details && column === 0 ? (
                      <button
                        type="button"
                        onClick={(event) => handleOpenRow(rowKey, event.currentTarget)}
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
      {openedDetails && <SectionDialog section={openedDetails} open={open} onOpenChange={setOpen} opener={opener} />}
    </SectionCard>
  );
}
