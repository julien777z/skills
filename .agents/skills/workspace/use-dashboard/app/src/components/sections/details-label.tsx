import { cn } from 'cn';
import { type ReactNode, useRef, useState } from 'react';

import { Text } from '@/components/primitives/text';
import { DialogOpener, RichText } from '@/components/rich-text';
import type { Section } from '@/spec';
import { SectionDialog } from './section-dialog';

export function DetailsLabel({
  label,
  details,
  className,
}: {
  label: string;
  details?: Section;
  className?: string;
}): ReactNode {
  const [showDetails, setShowDetails] = useState(false);
  const opener = useRef<HTMLButtonElement | null>(null);

  if (!details) {
    return (
      <Text as="span" size="sm" weight="medium">
        <RichText text={label} />
      </Text>
    );
  }

  return (
    <>
      <DialogOpener
        opener={opener}
        onOpen={() => setShowDetails(true)}
        className={cn('text-left focus-visible:underline focus-visible:outline-none', className)}
      >
        {label}
      </DialogOpener>
      <SectionDialog section={details} open={showDetails} onOpenChange={setShowDetails} opener={opener} />
    </>
  );
}
