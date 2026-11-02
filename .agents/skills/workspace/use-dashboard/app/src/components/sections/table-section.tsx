import { type ReactNode, useState } from 'react';

import { RichText } from '@/components';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { withKeys } from '@/lib/utils';
import type { RowDetail, TableSection as TableSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

interface DataTableProps {
  columns: string[];
  rows: string[][];
  onOpenRow?: (position: number) => void;
}

function DataTable({ columns, rows, onOpenRow }: DataTableProps): ReactNode {
  function handleRowKey(event: React.KeyboardEvent, position: number) {
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }

    event.preventDefault();

    onOpenRow?.(position);
  }

  return (
    <div className="overflow-hidden rounded-lg border">
      <Table>
        <TableHeader className="bg-muted">
          <TableRow>
            {withKeys(columns, (column) => column).map(({ key, item: column }) => (
              <TableHead key={key} className="px-4">
                <RichText text={column} />
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {withKeys(rows, (cells) => cells.join('\u0000')).map(({ key: rowKey, item: cells }, position) => (
            <TableRow
              key={rowKey}
              tabIndex={onOpenRow ? 0 : undefined}
              role={onOpenRow ? 'button' : undefined}
              onClick={onOpenRow ? () => onOpenRow(position) : undefined}
              onKeyDown={onOpenRow ? (event) => handleRowKey(event, position) : undefined}
              className={onOpenRow ? 'cursor-pointer focus-visible:bg-muted/50 focus-visible:outline-none' : undefined}
            >
              {withKeys(cells, (cell) => cell).map(({ key, item: cell }) => (
                <TableCell key={key} className="px-4 align-top whitespace-normal tabular-nums">
                  <RichText text={cell} />
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function RowDetailDialog({ detail, onClose }: { detail: RowDetail | undefined; onClose: () => void }): ReactNode {
  return (
    <Dialog open={detail !== undefined} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl">
        {detail && (
          <>
            <DialogHeader>
              <DialogTitle>
                <RichText text={detail.title} />
              </DialogTitle>
              {detail.description && (
                <DialogDescription>
                  <RichText text={detail.description} />
                </DialogDescription>
              )}
            </DialogHeader>
            <DataTable columns={detail.columns} rows={detail.rows} />
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
  const [opened, setOpened] = useState<number | undefined>();
  const details = section.details;

  return (
    <SectionCard title={section.title} description={section.description} summary={section.rows.length} wide>
      <DataTable columns={section.columns} rows={section.rows} onOpenRow={details ? setOpened : undefined} />
      {details && (
        <RowDetailDialog
          detail={opened === undefined ? undefined : details[opened]}
          onClose={() => setOpened(undefined)}
        />
      )}
    </SectionCard>
  );
}
