import type { ReactNode } from 'react';

import { RichText } from '@/components/rich-text';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import type { TableSection as TableSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

export function TableSection({ section }: { section: TableSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} count={String(section.rows.length)} wide>
      <div className="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader className="bg-muted">
            <TableRow>
              {section.columns.map((column, index) => (
                <TableHead key={index} className="px-4">
                  <RichText text={column} />
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {section.rows.map((cells, row) => (
              <TableRow key={row}>
                {cells.map((cell, column) => (
                  <TableCell key={column} className="px-4 align-top whitespace-normal tabular-nums">
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
