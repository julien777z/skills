import { type ReactNode, useContext, useMemo, useRef, useState } from 'react';

import { SectionDialog } from '@/components/sections';
import { ReferencesContext } from '@/lib/references';
import { withKeys } from '@/lib/utils';
import type { Section } from '@/spec';
import { ExternalLink } from './external-link';

function DetailsReference({ text, details }: { text: string; details: Section }): ReactNode {
  const references = useContext(ReferencesContext);
  const [open, setOpen] = useState(false);
  const opener = useRef<HTMLButtonElement>(null);
  const otherReferences = useMemo(() => references.without(text), [references, text]);

  return (
    <>
      <button ref={opener} type="button" data-reference onClick={() => setOpen(true)}>
        {text}
      </button>
      {open && (
        <ReferencesContext.Provider value={otherReferences}>
          <SectionDialog section={details} open onOpenChange={setOpen} opener={opener} />
        </ReferencesContext.Provider>
      )}
    </>
  );
}

export function RichText({ text }: { text: string }): ReactNode {
  const references = useContext(ReferencesContext);

  return withKeys(references.split(text), (part) => (typeof part === 'string' ? part : part.text)).map(
    ({ key, item: part }) => {
      if (typeof part === 'string') {
        return part;
      }

      if (part.details) {
        return <DetailsReference key={key} text={part.text} details={part.details} />;
      }

      return (
        <ExternalLink key={key} href={part.href ?? ''}>
          {part.text}
        </ExternalLink>
      );
    },
  );
}
