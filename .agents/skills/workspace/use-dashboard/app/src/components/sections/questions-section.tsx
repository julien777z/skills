import { Check, CircleHelp } from 'lucide-react';
import type { ReactNode } from 'react';

import { Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { QuestionStatus, type QuestionsSection as QuestionsSectionSpec } from '@/spec';
import { ListRow } from './list-row';
import { Paged } from './paged';
import { SectionCard } from './section-card';

export function QuestionsSection({ section }: { section: QuestionsSectionSpec }): ReactNode {
  const open = section.items.filter((question) => question.status === QuestionStatus.OPEN).length;

  return (
    <SectionCard
      title={section.title}
      description={section.description}
      count={open ? `${open} waiting on you` : 'All answered'}
      flush
    >
      <Paged items={section.items} pageSize={section.page_size} label={section.title} flush>
        {(visible) => (
          <Stack as="ul" divided>
            {visible.map((question, index) => {
              const answered = question.status === QuestionStatus.ANSWERED;

              return (
                <ListRow
                  key={index}
                  icon={
                    answered ? (
                      <span className="flex size-5 items-center justify-center rounded-full bg-good text-background">
                        <Check className="size-3" aria-label="Answered" />
                      </span>
                    ) : (
                      <CircleHelp className="size-5 text-warning" aria-label="Waiting on you" />
                    )
                  }
                  title={<RichText text={question.question} />}
                  detail={question.context}
                  aside={
                    question.meta && (
                      <Text size="xs" tone="muted" numeric>
                        <RichText text={question.meta} />
                      </Text>
                    )
                  }
                >
                  {question.options && !answered && (
                    <Stack as="ol" gap="xs" marker="number">
                      {question.options.map((option, position) => (
                        <Text key={position} as="li" size="sm" tone="muted">
                          <RichText text={option} />
                        </Text>
                      ))}
                    </Stack>
                  )}
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
                </ListRow>
              );
            })}
          </Stack>
        )}
      </Paged>
    </SectionCard>
  );
}
