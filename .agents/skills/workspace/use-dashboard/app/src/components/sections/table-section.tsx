import { type ReactNode, useState } from 'react';

import { RichText } from '@/components';
import { Dialog, DialogContent } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { withKeys } from '@/lib/utils';
import type { TableSection as TableSectionSpec } from '@/spec';
import { DashboardSection } from './dashboard-section';
import { InDialogContext, SectionCard } from './section-card';

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
  const [opened, setOpened] = useState<number | undefined>();
  const details = section.details;

  return (
    <SectionCard title={section.title} description={section.description} summary={section.rows.length} wide>
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
              <TableRow key={rowKey} className={details && 'relative cursor-pointer focus-within:bg-muted/50'}>
                {withKeys(cells, (cell) => cell).map(({ key, item: cell }, column) => (
                  <TableCell key={key} className="px-4 align-top whitespace-normal tabular-nums">
                    {details && column === 0 ? (
                      <button
                        type="button"
                        onClick={() => setOpened(position)}
                        className="text-left after:absolute after:inset-0 focus-visible:outline-none"
                      >
                        <RichText text={cell} />
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
      {details && (
        <Dialog open={opened !== undefined} onOpenChange={(open) => !open && setOpened(undefined)}>
          <DialogContent className="max-h-[85vh] overflow-y-auto sm:max-w-3xl">
            {opened !== undefined && (
              <InDialogContext.Provider value>
                <DashboardSection section={details[opened]} />
              </InDialogContext.Provider>
            )}
          </DialogContent>
        </Dialog>
      )}
    </SectionCard>
  );
}
