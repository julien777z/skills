import { Check, CircleHelp } from 'lucide-react';
import type { ReactNode } from 'react';

import { Moment, RichText } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { QuestionStatus, type QuestionsSection as QuestionsSectionSpec } from '@/spec';
import { ListSection } from './list-section';
import { TextList } from './text-list';

export function QuestionsSection({ section }: { section: QuestionsSectionSpec }): ReactNode {
  const open = section.items.filter((question) => question.status === QuestionStatus.OPEN).length;

  return (
    <ListSection
      title={section.title}
      description={section.description}
      summary={open ? `${open} waiting on you` : 'All answered'}
      items={section.items}
      pageSize={section.page_size}
      row={(question) => {
        const answered = question.status === QuestionStatus.ANSWERED;

        return {
          icon: answered ? (
            <Stack align="center" justify="center" badge="goodFilled">
              <Check className="size-3" aria-label="Answered" />
            </Stack>
          ) : (
            <CircleHelp className="size-5 text-warning" aria-label="Waiting on you" />
          ),
          title: <RichText text={question.question} />,
          detail: question.context && <RichText text={question.context} />,
          aside: <Moment meta={question.meta} at={question.at} />,
          body: (
            <>
              {question.options && !answered && <TextList items={question.options} numbered />}
              {question.recommendation && !answered && (
                <Text as="p" size="sm" tone="muted">
                  <Text as="b" weight="semibold" tone="default">
                    Recommended:{' '}
                  </Text>
                  <RichText text={question.recommendation} />
                </Text>
              )}
              {question.answer && (
                <Text as="p" size="sm" tone="muted">
                  <Text as="b" weight="semibold" tone="default">
                    Your answer:{' '}
                  </Text>
                  <RichText text={question.answer} />
                </Text>
              )}
            </>
          ),
        };
      }}
    />
  );
}
