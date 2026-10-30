import type { ReactNode } from 'react';

import { RichText } from '@/components/rich-text';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { TONES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { CalloutSection as CalloutSectionSpec } from '@/spec';

export function CalloutSection({ section }: { section: CalloutSectionSpec }): ReactNode {
  const style = TONES[section.tone ?? 'neutral'];
  const Icon = style.icon;

  return (
    <Alert className={cn('col-span-full', style.alert)}>
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
