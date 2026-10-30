import { useContext, useEffect, useRef, useState } from 'react';

import { drawDiagram, MIN_DIAGRAM_SCALE, SPLIT_RATIO } from '@/lib/diagram';
import { ExternalLink, type ReferenceLinks, ReferencesContext, RichText, safeUrl } from '@/lib/links';
import { cn } from '@/lib/utils';
import type { Change, DiagramSection } from '@/spec';

const HTML_NAMESPACE = 'http://www.w3.org/1999/xhtml';

const LEGEND: Record<Change | 'same', { label: string; swatch: string }> = {
  added: { label: 'Added', swatch: 'border-good' },
  changed: { label: 'Changed', swatch: 'border-info' },
  removed: { label: 'Removed', swatch: 'border-critical border-dashed' },
  same: { label: 'Unchanged', swatch: 'border-muted-foreground' },
};

function linkFigureReferences(root: HTMLElement, references: ReferenceLinks | null) {
  if (!references) {
    return;
  }

  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes: Text[] = [];

  while (walker.nextNode()) {
    const node = walker.currentNode as Text;
    const parent = node.parentElement;

    if (parent && parent.namespaceURI === HTML_NAMESPACE && !parent.closest('a, button')) {
      textNodes.push(node);
    }
  }

  for (const node of textNodes) {
    const text = node.nodeValue ?? '';
    const parts: Node[] = [];
    let start = 0;

    for (const match of text.matchAll(references.pattern)) {
      const index = match.index ?? 0;
      const href = safeUrl(references.urls[match[0]]);

      if (!href) {
        continue;
      }

      const anchor = document.createElement('a');

      anchor.href = href;
      anchor.target = '_blank';
      anchor.rel = 'noopener noreferrer';
      anchor.textContent = match[0];
      parts.push(document.createTextNode(text.slice(start, index)), anchor);
      start = index + match[0].length;
    }

    if (!parts.length) {
      continue;
    }

    parts.push(document.createTextNode(text.slice(start)));
    node.replaceWith(...parts);
  }
}

export function Diagram({ section }: { section: DiagramSection }) {
  const figure = useRef<HTMLDivElement>(null);
  const references = useContext(ReferencesContext);
  const [split, setSplit] = useState(false);
  const [failed, setFailed] = useState(false);
  const labels = Object.fromEntries(section.nodes.map((node) => [node.id, node.label]));
  const used = new Set([...section.nodes, ...section.edges].map((part) => part.change).filter(Boolean));
  const legend = (Object.keys(LEGEND) as (Change | 'same')[]).filter((change) => change === 'same' || used.has(change));

  useEffect(() => {
    const target = figure.current;

    if (!target) {
      return;
    }

    let cancelled = false;

    drawDiagram(section, target.clientWidth)
      .then((drawing) => {
        if (cancelled) {
          return;
        }

        const drawnWidth = drawing.width * Math.max(drawing.scale, MIN_DIAGRAM_SCALE);

        drawing.svg.style.maxWidth = 'none';
        drawing.svg.style.width = `${Math.round(drawnWidth)}px`;
        target.replaceChildren(drawing.svg);
        target.scrollLeft = (target.scrollWidth - target.clientWidth) / 2;
        linkFigureReferences(target, references);
        setSplit(Boolean(section.steps) && drawnWidth < target.clientWidth * SPLIT_RATIO);
      })
      .catch((error: unknown) => {
        console.error(error);
        setFailed(true);
      });

    return () => {
      cancelled = true;
    };
  }, [section, references]);

  return (
    <div className={cn('grid gap-5', split && 'lg:grid-cols-[auto_minmax(300px,1fr)] lg:items-start')}>
      <div className="grid min-w-0 content-start gap-3">
        {failed && (
          <p className="text-sm text-muted-foreground">
            The diagram could not be drawn, so its connections are listed instead.
          </p>
        )}
        <div ref={figure} className="grid min-h-[120px] justify-items-center overflow-x-auto [&_svg]:h-auto">
          <ul className="list-disc pl-5 text-sm text-muted-foreground">
            {section.edges.map((edge, index) => (
              <li key={index}>
                {labels[edge.from]} → {labels[edge.to]}
                {edge.label ? `: ${edge.label}` : ''}
              </li>
            ))}
          </ul>
        </div>
        {used.size > 0 && (
          <div className="flex flex-wrap gap-x-4 gap-y-1.5 text-xs text-muted-foreground">
            {legend.map((change) => (
              <span key={change} className="inline-flex items-center gap-1.5">
                <span className={cn('size-3 rounded-[3px] border-[1.5px]', LEGEND[change].swatch)} />
                {LEGEND[change].label}
              </span>
            ))}
          </div>
        )}
        {section.prs && (
          <div className="flex flex-wrap gap-x-4 gap-y-1.5 text-xs">
            {section.prs.map((entry) => (
              <ExternalLink key={entry.ref} href={entry.url}>
                {entry.ref}
              </ExternalLink>
            ))}
          </div>
        )}
      </div>
      {section.steps && (
        <ol
          className={cn(
            'grid gap-3 border-t pt-4 sm:grid-cols-[repeat(auto-fill,minmax(min(100%,300px),1fr))]',
            split && 'lg:grid-cols-1 lg:border-t-0 lg:border-l lg:pt-0 lg:pl-7',
          )}
        >
          {section.steps.map((step, index) => (
            <li key={index} className="flex gap-2.5 text-sm text-muted-foreground">
              <span className="flex size-5 shrink-0 items-center justify-center rounded-full border border-info text-[11px] font-bold text-info">
                {index + 1}
              </span>
              <span>
                <RichText text={step} />
              </span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
