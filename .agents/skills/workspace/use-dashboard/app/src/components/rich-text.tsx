import { type ReactNode, useContext } from 'react';

import { ReferencesContext } from '@/lib/references';
import { withKeys } from '@/lib/utils';
import { ExternalLink } from './external-link';

export function RichText({ text }: { text: string }): ReactNode {
  const references = useContext(ReferencesContext);

  return withKeys(references.split(text), (part) => (typeof part === 'string' ? part : part.text)).map(
    ({ key, item: part }) =>
      typeof part === 'string' ? (
        part
      ) : (
        <ExternalLink key={key} href={part.href}>
          {part.text}
        </ExternalLink>
      ),
  );
}
