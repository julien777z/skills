import type { ReactNode } from 'react';

import { RichText } from '@/components';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { withKeys } from '@/lib/utils';
import type { TableSection as TableSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
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
            {withKeys(section.rows, (cells) => cells.join('\u0000')).map(({ key: rowKey, item: cells }) => (
              <TableRow key={rowKey}>
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
    </SectionCard>
  );
}
