import { CircleAlert, CircleCheck, Info, TriangleAlert } from 'lucide-react';

import { Pager, usePage } from '@/components/pager';
import { ToneDot } from '@/components/status';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { ExternalLink, RichText } from '@/lib/links';
import { NEUTRAL_BADGE, TONE_ALERT, TONE_BADGE } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type {
  BoardColumn,
  BoardSection,
  CalloutSection,
  NotesSection,
  OutlineSection,
  TableSection,
  Tone,
} from '@/spec';

const OUTLINE_OPEN_LIMIT = 2;

const CALLOUT_ICONS: Record<Tone | 'neutral', typeof Info> = {
  good: CircleCheck,
  warning: TriangleAlert,
  critical: CircleAlert,
  accent: Info,
  done: CircleCheck,
  neutral: Info,
};

function BoardColumnPanel({ column }: { column: BoardColumn }) {
  const state = usePage(column.items, column.page_size);

  return (
    <div className="grid content-start gap-3 rounded-lg border bg-muted/30 p-3">
      <div className="flex items-center gap-2 px-1">
        <ToneDot tone={column.tone} />
        <span className="text-sm font-medium">{column.title}</span>
        <Badge variant="secondary" className="ml-auto tabular-nums">
          {column.items.length}
        </Badge>
      </div>
      {!column.items.length && <p className="px-1 text-sm text-muted-foreground">Nothing here.</p>}
      {state.visible.map((card, index) => (
        <div key={state.start + index} className="grid gap-1.5 rounded-md border bg-card px-3 py-2.5 shadow-xs">
          <span className="text-sm font-medium [overflow-wrap:anywhere]">
            {card.url ? <ExternalLink href={card.url}>{card.title}</ExternalLink> : <RichText text={card.title} />}
          </span>
          {card.detail && (
            <span className="text-xs text-muted-foreground [overflow-wrap:anywhere]">
              <RichText text={card.detail} />
            </span>
          )}
          {(card.tag || card.meta) && (
            <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1">
              {card.tag ? (
                <Badge variant="outline" className="text-muted-foreground">
                  {card.tag}
                </Badge>
              ) : (
                <span />
              )}
              {card.meta && <span className="text-xs text-muted-foreground tabular-nums">{card.meta}</span>}
            </div>
          )}
        </div>
      ))}
      <Pager label={column.title} total={column.items.length} state={state} />
    </div>
  );
}

export function Board({ section }: { section: BoardSection }) {
  return (
    <div className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,220px),1fr))] items-start gap-4">
      {section.columns.map((column) => (
        <BoardColumnPanel key={column.title} column={column} />
      ))}
    </div>
  );
}

export function DataTable({ section }: { section: TableSection }) {
  return (
    <div className="overflow-hidden rounded-lg border">
      <Table>
        <TableHeader className="bg-muted">
          <TableRow>
            {section.columns.map((column) => (
              <TableHead key={column} className="px-4">
                {column}
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
  );
}

export function Notes({ section }: { section: NotesSection }) {
  return (
    <ul className="grid list-disc gap-1.5 pl-5 text-sm text-muted-foreground marker:text-muted-foreground/60">
      {section.items.map((note, index) => (
        <li key={index}>
          <RichText text={note} />
        </li>
      ))}
    </ul>
  );
}

export function Outline({ section }: { section: OutlineSection }) {
  return (
    <div className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,340px),1fr))] items-start gap-x-8 gap-y-6">
      {section.groups.map((group) => {
        const open = group.items.length <= OUTLINE_OPEN_LIMIT ? group.items.map((_, index) => String(index)) : [];

        return (
          <div key={group.title} className="grid content-start">
            <h3 className="pb-1 text-xs font-medium tracking-wide text-muted-foreground uppercase">{group.title}</h3>
            <Accordion type="multiple" defaultValue={open}>
              {group.items.map((item, index) => (
                <AccordionItem key={index} value={String(index)}>
                  <AccordionTrigger className="gap-3 py-3 hover:no-underline">
                    <span className="flex min-w-0 flex-1 items-start gap-2.5">
                      <ToneDot tone={item.tone} className="mt-1.5" />
                      <span className="grid min-w-0 gap-1.5">
                        <span className="[overflow-wrap:anywhere]">
                          <RichText text={item.title} />
                        </span>
                        {(item.tag || item.meta) && (
                          <span className="flex flex-wrap items-center gap-2 text-xs font-normal text-muted-foreground">
                            {item.tag && (
                              <Badge variant="outline" className={item.tone ? TONE_BADGE[item.tone] : NEUTRAL_BADGE}>
                                {item.tag}
                              </Badge>
                            )}
                            {item.meta && <span>{item.meta}</span>}
                          </span>
                        )}
                      </span>
                    </span>
                  </AccordionTrigger>
                  <AccordionContent className="pl-[18px] text-muted-foreground">
                    <RichText text={item.detail} />
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        );
      })}
    </div>
  );
}

export function Callout({ section }: { section: CalloutSection }) {
  const Icon = CALLOUT_ICONS[section.tone ?? 'neutral'];

  return (
    <Alert className={cn(section.tone && TONE_ALERT[section.tone])}>
      <Icon />
      <AlertTitle className="line-clamp-none">
        <RichText text={section.title} />
      </AlertTitle>
      <AlertDescription className="text-foreground/80">
        <p>
          <RichText text={section.body} />
        </p>
      </AlertDescription>
    </Alert>
  );
}
