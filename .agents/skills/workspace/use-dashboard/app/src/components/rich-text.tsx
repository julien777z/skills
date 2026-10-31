import { type ReactNode, useContext } from 'react';

import { ReferencesContext } from '@/lib/references';
import { ExternalLink } from './external-link';

export function RichText({ text }: { text: string }): ReactNode {
  const references = useContext(ReferencesContext);

  return references.split(text).map((part, index) =>
    typeof part === 'string' ? (
      part
    ) : (
      <ExternalLink key={index} href={part.href}>
        {part.text}
      </ExternalLink>
    ),
  );
}
