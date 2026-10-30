import { type ReactNode, useContext, useEffect, useRef, useState } from 'react';

import { ExternalLink } from '@/components/external-link';
import { Stack, Text } from '@/components/primitives';
import { RichText } from '@/components/rich-text';
import { drawDiagram } from '@/lib/diagram';
import { type References, ReferencesContext } from '@/lib/references';
import { CHANGES, type ChangeName, TONES } from '@/lib/tone';
import { cn } from '@/lib/utils';
import type { DiagramSection as DiagramSectionSpec } from '@/spec';
import { SectionCard } from './section-card';

const DrawStatus = { DRAWING: 'drawing', DRAWN: 'drawn', FAILED: 'failed' } as const;

type DrawStatus = (typeof DrawStatus)[keyof typeof DrawStatus];

const SPLIT_RATIO: number = 0.6;

const HTML_NAMESPACE: string = 'http://www.w3.org/1999/xhtml';

function linkFigureText(root: HTMLElement, references: References): void {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes: Text[] = [];

  while (walker.nextNode()) {
    const node = walker.currentNode as Text;

    if (node.parentElement?.namespaceURI === HTML_NAMESPACE && !node.parentElement.closest('a')) {
      textNodes.push(node);
    }
  }

  for (const node of textNodes) {
    const parts = references.split(node.nodeValue ?? '');

    if (parts.length < 2) {
      continue;
    }

    node.replaceWith(
      ...parts.map((part) => {
        if (typeof part === 'string') {
          return document.createTextNode(part);
        }

        const anchor = document.createElement('a');

        anchor.href = part.href;
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        anchor.textContent = part.text;

        return anchor;
      }),
    );
  }
}

export function DiagramSection({ section }: { section: DiagramSectionSpec }): ReactNode {
  const figure = useRef<HTMLDivElement>(null);
  const references = useContext(ReferencesContext);
  const [status, setStatus] = useState<DrawStatus>(DrawStatus.DRAWING);
  const [split, setSplit] = useState(false);
  const labels = new Map(section.nodes.map((node) => [node.id, node.label]));
  const used = new Set([...section.nodes, ...section.edges].map((part) => part.change).filter(Boolean));
  const legend = (Object.keys(CHANGES) as ChangeName[]).filter((change) => change === 'unchanged' || used.has(change));

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

        drawing.svg.style.maxWidth = 'none';
        drawing.svg.style.width = `${Math.round(drawing.width)}px`;

        target.replaceChildren(drawing.svg);
        target.scrollLeft = (target.scrollWidth - target.clientWidth) / 2;
        linkFigureText(target, references);

        setSplit(Boolean(section.steps) && drawing.width < target.clientWidth * SPLIT_RATIO);
        setStatus(DrawStatus.DRAWN);
      })
      .catch((error: unknown) => {
        console.error(error);

        setStatus(DrawStatus.FAILED);
      });

    return () => {
      cancelled = true;
    };
  }, [section, references]);

  return (
    <SectionCard title={section.title} wide>
      <div className={cn('grid gap-5', split && 'lg:grid-cols-[auto_minmax(300px,1fr)] lg:items-start')}>
        <Stack gap="md">
          {status === DrawStatus.FAILED && (
            <Text size="sm" tone="muted">
              The diagram could not be drawn, so its connections are listed instead.
            </Text>
          )}
          {status !== DrawStatus.DRAWN && (
            <ul className="list-disc pl-5 text-sm text-muted-foreground">
              {section.edges.map((edge, index) => (
                <li key={index}>
                  {labels.get(edge.from)} → {labels.get(edge.to)}
                  {edge.label ? `: ${edge.label}` : ''}
                </li>
              ))}
            </ul>
          )}
          <div ref={figure} className="grid justify-items-center overflow-x-auto [&_svg]:h-auto" />
          {used.size > 0 && (
            <Stack direction="row" gap="lg" wrap>
              {legend.map((change) => (
                <Stack key={change} direction="row" align="center" gap="xs">
                  <span
                    className={cn(
                      'size-3 rounded-[3px] border-[1.5px]',
                      TONES[CHANGES[change].tone].border,
                      CHANGES[change].dashed && 'border-dashed',
                    )}
                  />
                  <Text size="xs" tone="muted">
                    {CHANGES[change].label}
                  </Text>
                </Stack>
              ))}
            </Stack>
          )}
          {section.prs && (
            <Stack direction="row" gap="lg" wrap>
              {section.prs.map((entry, index) => (
                <Text key={index} size="xs">
                  <ExternalLink href={entry.url}>{entry.ref}</ExternalLink>
                </Text>
              ))}
            </Stack>
          )}
        </Stack>
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
    </SectionCard>
  );
}
