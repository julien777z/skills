import { ArrowUpRight, Check, CircleHelp } from 'lucide-react';
import { Fragment, type ReactNode } from 'react';

import { Pager, usePage } from '@/components/pager';
import { StatusBadge } from '@/components/status';
import { ExternalLink, RichText } from '@/lib/links';
import { CHANGE_STYLES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { ChangeItem, LinkItem, PullRequestState, Question } from '@/spec';

const PULL_REQUEST_ICONS: Record<PullRequestState, string> = {
  open: 'M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z',
  draft:
    'M3.25 1A2.25 2.25 0 0 1 4 5.372v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.251 2.251 0 0 1 3.25 1Zm9.5 14a2.25 2.25 0 1 1 0-4.5 2.25 2.25 0 0 1 0 4.5ZM2.5 3.25a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0ZM3.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm9.5 0a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM14 7.5a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0Zm0-4.25a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0Z',
  merged:
    'M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z',
  closed:
    'M3.25 1A2.25 2.25 0 0 1 4 5.372v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.251 2.251 0 0 1 3.25 1Zm9.5 5.5a.75.75 0 0 1 .75.75v3.378a2.251 2.251 0 1 1-1.5 0V7.25a.75.75 0 0 1 .75-.75Zm-2.03-5.273a.75.75 0 0 1 1.06 0l.97.97.97-.97a.748.748 0 0 1 1.265.332.75.75 0 0 1-.205.729l-.97.97.97.97a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018l-.97-.97-.97.97a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734l.97-.97-.97-.97a.75.75 0 0 1 0-1.06ZM2.5 3.25a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0ZM3.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm9.5 0a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z',
};

const PULL_REQUEST_COLORS: Record<PullRequestState, string> = {
  open: 'text-good',
  draft: 'text-muted-foreground',
  merged: 'text-done',
  closed: 'text-critical',
};

const PULL_REQUEST_LABELS: Record<PullRequestState, string> = {
  open: 'Open pull request',
  draft: 'Draft pull request',
  merged: 'Merged pull request',
  closed: 'Closed pull request',
};

function Row({ icon, children, aside }: { icon?: ReactNode; children: ReactNode; aside?: ReactNode }) {
  return (
    <li className="flex gap-3 px-6 py-3">
      {icon && <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center">{icon}</span>}
      <div className="grid min-w-0 flex-1 gap-0.5">{children}</div>
      {aside && <div className="shrink-0 self-start">{aside}</div>}
    </li>
  );
}

function Detail({ text }: { text: string }) {
  return (
    <span className="text-sm text-muted-foreground [overflow-wrap:anywhere]">
      <RichText text={text} />
    </span>
  );
}

export function PagedList<T>({
  title,
  items,
  pageSize,
  render,
}: {
  title: string;
  items: T[];
  pageSize?: number;
  render: (item: T) => ReactNode;
}) {
  const state = usePage(items, pageSize);

  return (
    <>
      <ul className="divide-y border-t">
        {state.visible.map((item, index) => (
          <Fragment key={state.start + index}>{render(item)}</Fragment>
        ))}
      </ul>
      <div className="px-6">
        <Pager label={title} total={items.length} state={state} />
      </div>
    </>
  );
}

export function QuestionRow({ question }: { question: Question }) {
  const answered = question.status === 'answered';

  return (
    <Row
      icon={
        answered ? (
          <span className="flex size-5 items-center justify-center rounded-full bg-good text-background">
            <Check className="size-3" aria-label="Answered" />
          </span>
        ) : (
          <CircleHelp className="size-5 text-warning" aria-label="Waiting on you" />
        )
      }
      aside={question.meta && <span className="text-xs text-muted-foreground tabular-nums">{question.meta}</span>}
    >
      <span className="font-medium [overflow-wrap:anywhere]">
        <RichText text={question.question} />
      </span>
      {question.context && <Detail text={question.context} />}
      {question.options && !answered && (
        <ol className="mt-1 list-decimal space-y-0.5 pl-5 text-sm text-muted-foreground">
          {question.options.map((option) => (
            <li key={option}>
              <RichText text={option} />
            </li>
          ))}
        </ol>
      )}
      {question.recommendation && !answered && (
        <p className="text-sm text-muted-foreground">
          <b className="font-semibold text-foreground">Recommended: </b>
          <RichText text={question.recommendation} />
        </p>
      )}
      {question.answer && (
        <p className="mt-1 border-l-2 pl-3 text-sm text-muted-foreground">
          <b className="font-semibold text-foreground">Your answer: </b>
          <RichText text={question.answer} />
        </p>
      )}
    </Row>
  );
}

export function LinkRow({ item }: { item: LinkItem }) {
  const icon = item.state ? (
    <svg viewBox="0 0 16 16" className={cn('size-4 fill-current', PULL_REQUEST_COLORS[item.state])} role="img">
      <title>{PULL_REQUEST_LABELS[item.state]}</title>
      <path d={PULL_REQUEST_ICONS[item.state]} />
    </svg>
  ) : (
    <ArrowUpRight className="size-4 text-muted-foreground" aria-hidden="true" />
  );

  return (
    <Row icon={icon} aside={item.status && <StatusBadge label={item.status} tone={item.tone} />}>
      <span className="font-medium [overflow-wrap:anywhere]">
        <ExternalLink href={item.url} className="hover:underline underline-offset-4">
          {item.label}
        </ExternalLink>
      </span>
      {item.detail && <Detail text={item.detail} />}
    </Row>
  );
}

export function ChangeRow({ item }: { item: ChangeItem }) {
  const style = CHANGE_STYLES[item.change];

  return (
    <Row aside={<StatusBadge label={style.label} tone={style.tone} />}>
      <span className="font-mono text-sm font-medium [overflow-wrap:anywhere]">
        <RichText text={item.name} />
      </span>
      {item.detail && <Detail text={item.detail} />}
    </Row>
  );
}
