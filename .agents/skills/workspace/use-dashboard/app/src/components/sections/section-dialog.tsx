import type { ReactNode, RefObject } from 'react';

import { Dialog, DialogContent } from '@/components/ui/dialog';
import type { Section } from '@/spec';
import { DashboardSection } from './dashboard-section';
import { InDialogContext } from './section-card';

interface SectionDialogProps {
  section: Section;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  opener: RefObject<HTMLButtonElement | null>;
}

export function SectionDialog({ section, open, onOpenChange, opener }: SectionDialogProps): ReactNode {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className="max-h-[85vh] overflow-y-auto sm:max-w-3xl"
        onCloseAutoFocus={(event) => {
          event.preventDefault();
          opener.current?.focus();
        }}
      >
        <InDialogContext.Provider value>
          <DashboardSection section={section} />
        </InDialogContext.Provider>
      </DialogContent>
    </Dialog>
  );
}
