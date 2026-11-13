import { type ReactNode, type RefObject, useCallback } from 'react';

import { Dialog, DialogContent } from '@/components/ui/dialog';
import type { Section } from '@/spec';
import { DashboardSection } from './dashboard-section';
import { InDialogContext, InTabPanelContext } from './section-card';

const DIALOG_MARGIN_PX: number = 16;

interface SectionDialogProps {
  section: Section;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  opener: RefObject<HTMLOrSVGElement | null>;
}

/**
 * Place the dialog just below its opener, kept inside the viewport.
 *
 * A host that sizes its frame to the page makes the viewport as tall as the whole page, so a dialog
 * centered in the viewport can open far from the entry that was clicked and out of the reader's sight.
 */
function placeBelowOpener(dialog: HTMLElement, opener: Element): void {
  const below = opener.getBoundingClientRect().bottom + DIALOG_MARGIN_PX;
  const lowestTop = window.innerHeight - dialog.offsetHeight - DIALOG_MARGIN_PX;

  dialog.style.top = `${Math.max(DIALOG_MARGIN_PX, Math.min(below, lowestTop))}px`;
}

export function SectionDialog({ section, open, onOpenChange, opener }: SectionDialogProps): ReactNode {
  const keepBelowOpener = useCallback(
    (dialog: HTMLDivElement | null) => {
      const anchor = opener.current;

      if (!dialog || !(anchor instanceof Element)) {
        return;
      }

      const place = (): void => placeBelowOpener(dialog, anchor);
      const resizes = new ResizeObserver(place);

      place();
      resizes.observe(dialog);

      return () => resizes.disconnect();
    },
    [opener],
  );

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        ref={keepBelowOpener}
        className="max-h-[640px] translate-y-0 overflow-y-auto sm:max-w-3xl"
        onCloseAutoFocus={(event) => {
          event.preventDefault();
          opener.current?.focus();
        }}
      >
        <InTabPanelContext.Provider value={false}>
          <InDialogContext.Provider value>
            <DashboardSection section={section} />
          </InDialogContext.Provider>
        </InTabPanelContext.Provider>
      </DialogContent>
    </Dialog>
  );
}
