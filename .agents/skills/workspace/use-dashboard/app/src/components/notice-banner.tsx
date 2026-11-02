import type { ReactNode } from 'react';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { TONES, ToneName } from '@/lib/tone';
import type { Notice } from '@/spec';
import { RichText } from './rich-text';

export function NoticeBanner({ notice }: { notice: Notice }): ReactNode {
  const style = TONES[notice.tone ?? ToneName.NEUTRAL];
  const Icon = style.icon;

  return (
    <Alert className={style.alert}>
      <Icon />
      <AlertTitle className="line-clamp-none">
        <RichText text={notice.title} />
      </AlertTitle>
      <AlertDescription className="text-foreground/80">
        <p>
          <RichText text={notice.body} />
        </p>
      </AlertDescription>
    </Alert>
  );
}
