import { Board, Callout, DataTable, Notes, Outline } from '@/components/sections/blocks';
import { Diagram } from '@/components/sections/diagram';
import { ChangeRow, LinkRow, PagedList, QuestionRow } from '@/components/sections/lists';
import { Badge } from '@/components/ui/badge';
import { Card, CardAction, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import type { Section } from '@/spec';

const WIDE_SECTIONS = new Set<Section['type']>(['board', 'table', 'diagram', 'outline', 'callout']);

const FLUSH_SECTIONS = new Set<Section['type']>(['questions', 'links', 'changes']);

function sectionCount(section: Section): string | undefined {
  switch (section.type) {
    case 'questions': {
      const open = section.items.filter((question) => question.status !== 'answered').length;

      return open ? `${open} waiting on you` : 'All answered';
    }
    case 'links':
    case 'changes':
    case 'notes':
      return String(section.items.length);
    case 'table':
      return String(section.rows.length);
    default:
      return undefined;
  }
}

function SectionBody({ section }: { section: Section }) {
  switch (section.type) {
    case 'board':
      return <Board section={section} />;
    case 'table':
      return <DataTable section={section} />;
    case 'notes':
      return <Notes section={section} />;
    case 'outline':
      return <Outline section={section} />;
    case 'diagram':
      return <Diagram section={section} />;
    case 'callout':
      return <Callout section={section} />;
    case 'questions':
      return (
        <PagedList
          title={section.title}
          items={section.items}
          pageSize={section.page_size}
          render={(question) => <QuestionRow question={question} />}
        />
      );
    case 'links':
      return (
        <PagedList
          title={section.title}
          items={section.items}
          pageSize={section.page_size}
          render={(item) => <LinkRow item={item} />}
        />
      );
    case 'changes':
      return (
        <PagedList
          title={section.title}
          items={section.items}
          pageSize={section.page_size}
          render={(item) => <ChangeRow item={item} />}
        />
      );
  }
}

export function DashboardSection({ section }: { section: Section }) {
  const wide = WIDE_SECTIONS.has(section.type);
  const count = sectionCount(section);

  if (section.type === 'callout') {
    return (
      <div className="col-span-full">
        <SectionBody section={section} />
      </div>
    );
  }

  return (
    <Card
      className={cn(
        '@container/card min-w-0',
        wide && 'col-span-full',
        FLUSH_SECTIONS.has(section.type) && 'gap-4 pb-2',
      )}
    >
      <CardHeader>
        <CardTitle>
          <h2>{section.title}</h2>
        </CardTitle>
        {count && (
          <CardAction>
            <Badge variant="outline" className="text-muted-foreground tabular-nums">
              {count}
            </Badge>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className={cn(FLUSH_SECTIONS.has(section.type) && 'px-0')}>
        <SectionBody section={section} />
      </CardContent>
    </Card>
  );
}
