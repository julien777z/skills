import { type ReactNode, useContext, useEffect, useRef, useState } from 'react';

import { ExternalLink, RichText } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { drawDiagram } from '@/lib/diagram';
import { linkAttributes, type References, ReferencesContext } from '@/lib/references';
import { CHANGES, TONES } from '@/lib/tone';
import { cn, scrollToSection, withKeys } from '@/lib/utils';
import { Change, type DiagramEdge, type DiagramSection as DiagramSectionSpec, type Section } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';
import { TextList } from './text-list';

const DrawStatus = { DRAWING: 'drawing', DRAWN: 'drawn', FAILED: 'failed' } as const;

type DrawStatus = (typeof DrawStatus)[keyof typeof DrawStatus];

const SPLIT_RATIO: number = 0.6;

interface OpenedDetails {
  details: Section;
  references: References;
}

const HTML_NAMESPACE: string = 'http://www.w3.org/1999/xhtml';

function linkFigureText(
  root: HTMLElement,
  references: References,
  open: (details: Section, opener: HTMLElement, reference: string) => void,
): void {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes: Text[] = [];

  while (walker.nextNode()) {
    const node = walker.currentNode as Text;

    if (
      node.parentElement?.namespaceURI === HTML_NAMESPACE &&
      !node.parentElement.closest('a') &&
      !node.parentElement.closest('[role="button"]')
    ) {
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

        const details = part.details;

        if (details) {
          const button = document.createElement('button');

          button.type = 'button';
          button.dataset.reference = '';
          button.textContent = part.text;
          button.addEventListener('click', (event) => {
            event.stopPropagation();
            open(details, button, part.text);
          });

          return button;
        }

        const attributes = part.href ? linkAttributes(part.href) : null;

        if (!attributes) {
          return document.createTextNode(part.text);
        }

        const anchor = document.createElement('a');

        Object.assign(anchor, attributes);
        anchor.textContent = part.text;

        return anchor;
      }),
    );
  }
}

function edgeName(edge: DiagramEdge, labels: Map<string, string>): string {
  return `${labels.get(edge.from)} to ${labels.get(edge.to)}${edge.label ? `: ${edge.label}` : ''}`;
}

function makeOpener(target: SVGElement, name: string, open: () => void): void {
  target.setAttribute('role', 'button');
  target.setAttribute('tabindex', '0');
  target.setAttribute('aria-label', name);
  target.style.cursor = 'pointer';
  target.style.pointerEvents = 'all';
  target.addEventListener('click', open);
  target.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      open();
    }
  });
}

function openEdgesOnClick(
  root: HTMLElement,
  section: DiagramSectionSpec,
  open: (details: Section, opener: SVGElement) => void,
): void {
  const labels = new Map(section.nodes.map((node) => [node.id, node.label]));

  // Mermaid draws a subgraph's edges in a nested group, so document order need not follow the
  // source; each path's id ends with its source index, and its label sits at the same position in
  // the sibling labels group.
  for (const group of root.querySelectorAll<SVGElement>('.edgePaths')) {
    const paths = group.querySelectorAll<SVGElement>(':scope > path');
    const groupLabels = group.parentElement?.querySelectorAll<SVGElement>(':scope > .edgeLabels > .edgeLabel') ?? [];

    paths.forEach((path, position) => {
      const edge = section.edges[Number(path.id.match(/_(\d+)$/)?.[1])];
      const details = edge?.details;

      if (!edge || !details) {
        return;
      }

      for (const target of [path, groupLabels[position]]) {
        if (target) {
          makeOpener(target, `Open ${edgeName(edge, labels)}`, () => open(details, target));
        }
      }
    });
  }

  section.nodes.forEach((node, index) => {
    const target = root.querySelector<SVGElement>(`g.node[id*="-n${index}-"]`);
    const details = node.details;
    const jump = node.target;

    if (details && target) {
      makeOpener(target, `Open ${node.label}`, () => open(details, target));
    } else if (jump && target) {
      makeOpener(target, `Go to ${jump}`, () => scrollToSection(jump));
    }
  });
}

export function DiagramSection({ section }: { section: DiagramSectionSpec }): ReactNode {
  const figure = useRef<HTMLDivElement>(null);
  const references = useContext(ReferencesContext);
  const [status, setStatus] = useState<DrawStatus>(DrawStatus.DRAWING);
  const [split, setSplit] = useState(false);
  const [opened, setOpened] = useState<OpenedDetails | null>(null);
  const opener = useRef<HTMLOrSVGElement | null>(null);
  const labels = new Map(section.nodes.map((node) => [node.id, node.label]));
  const used = new Set([...section.nodes, ...section.edges].map((part) => part.change).filter(Boolean));
  const legend = Object.values(Change).filter((change) => used.has(change));

  useEffect(() => {
    const target = figure.current;

    if (!target) {
      return;
    }

    let canceled = false;

    drawDiagram(section, target)
      .then((drawing) => {
        if (canceled) {
          return;
        }

        drawing.svg.style.maxWidth = 'none';
        drawing.svg.style.width = `${Math.round(drawing.width)}px`;

        target.replaceChildren(drawing.svg);
        target.scrollLeft = (target.scrollWidth - target.clientWidth) / 2;

        function openDetails(details: Section, element: HTMLOrSVGElement, reference?: string) {
          opener.current = element;
          setOpened({ details, references: reference ? references.without(reference) : references });
        }

        openEdgesOnClick(target, section, openDetails);
        linkFigureText(target, references, openDetails);

        setSplit(Boolean(section.steps) && drawing.width < target.clientWidth * SPLIT_RATIO);
        setStatus(DrawStatus.DRAWN);
      })
      .catch((error: unknown) => {
        console.error(error);

        setStatus(DrawStatus.FAILED);
      });

    return () => {
      canceled = true;
    };
  }, [section, references]);

  return (
    <SectionCard title={section.title} description={section.description} wide>
      <Grid columns={split ? 'figureBesideSteps' : 'single'} gap="lg">
        <Stack gap="md">
          {status === DrawStatus.FAILED && (
            <Text size="sm" tone="muted">
              The diagram could not be drawn, so its connections are listed instead.
            </Text>
          )}
          {status !== DrawStatus.DRAWN && (
            <TextList
              items={section.edges.map(
                (edge) => `${labels.get(edge.from)} → ${labels.get(edge.to)}${edge.label ? `: ${edge.label}` : ''}`,
              )}
            />
          )}
          <div
            ref={figure}
            className="grid justify-items-center overflow-x-auto [&_.cluster-label_div]:!max-w-none [&_.cluster-label_div]:!whitespace-nowrap [&_.cluster-label_foreignObject]:overflow-visible [&_svg]:h-auto"
          />
          {section.legend && (
            <Stack direction="row" gap="lg" wrap>
              {section.legend.map((entry) => (
                <Stack key={entry.label} direction="row" align="center" gap="xs">
                  <span className={cn('h-0.5 w-4 rounded-full', TONES[entry.tone].dot)} />
                  <Text size="xs" tone="muted">
                    {entry.label}
                  </Text>
                </Stack>
              ))}
            </Stack>
          )}
          {legend.length > 0 && (
            <Stack direction="row" gap="lg" wrap>
              {legend.map((change) => (
                <Stack key={change} direction="row" align="center" gap="xs">
                  <span className={cn('h-0.5 w-4 rounded-full', TONES[CHANGES[change].tone].dot)} />
                  <Text size="xs" tone="muted">
                    {CHANGES[change].label}
                  </Text>
                </Stack>
              ))}
            </Stack>
          )}
          {section.prs && (
            <Stack direction="row" gap="lg" wrap>
              {section.prs.map((entry) => (
                <Text key={entry.ref} size="xs">
                  <ExternalLink href={entry.url}>{entry.ref}</ExternalLink>
                </Text>
              ))}
            </Stack>
          )}
        </Stack>
        {section.steps && (
          <Grid as="ol" columns={split ? 'single' : 'steps'} gap="sm" divider={split ? 'side' : 'top'}>
            {withKeys(section.steps, (step) => step).map(({ key, item: step }, index) => (
              <Stack key={key} as="li" direction="row" align="start" gap="sm">
                <Stack align="center" justify="center" badge="accentRing">
                  <Text size="xxs" weight="bold">
                    {index + 1}
                  </Text>
                </Stack>
                <Text size="sm" tone="muted">
                  <RichText text={step} />
                </Text>
              </Stack>
            ))}
          </Grid>
        )}
      </Grid>
      {opened && (
        <ReferencesContext.Provider value={opened.references}>
          <SectionDialog
            section={opened.details}
            open
            onOpenChange={(open) => !open && setOpened(null)}
            opener={opener}
          />
        </ReferencesContext.Provider>
      )}
    </SectionCard>
  );
}
