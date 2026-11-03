import { type ReactNode, useContext, useEffect, useRef, useState } from 'react';

import { ExternalLink, RichText } from '@/components';
import { Grid, Stack, Text } from '@/components/primitives';
import { drawDiagram } from '@/lib/diagram';
import { linkAttributes, type References, ReferencesContext } from '@/lib/references';
import { CHANGES, ChangeName, TONES } from '@/lib/tone';
import { cn, scrollToSection, withKeys } from '@/lib/utils';
import type { DiagramEdge, DiagramSection as DiagramSectionSpec, Section } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';
import { TextList } from './text-list';

const DrawStatus = { DRAWING: 'drawing', DRAWN: 'drawn', FAILED: 'failed' } as const;

type DrawStatus = (typeof DrawStatus)[keyof typeof DrawStatus];

const SPLIT_RATIO: number = 0.6;

const HTML_NAMESPACE: string = 'http://www.w3.org/1999/xhtml';

function linkFigureText(root: HTMLElement, references: References): void {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes: Text[] = [];

  while (walker.nextNode()) {
    const node = walker.currentNode as Text;

    if (
      node.parentElement?.namespaceURI === HTML_NAMESPACE &&
      !node.parentElement.closest('a') &&
      !node.parentElement.closest('[data-jump]')
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

        const attributes = linkAttributes(part.href);

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
  const paths = root.querySelectorAll<SVGElement>('.edgePaths path');
  const edgeLabels = root.querySelectorAll<SVGElement>('.edgeLabels > .edgeLabel');

  section.edges.forEach((edge, index) => {
    const label = edgeLabels[index];

    if (!edge.details) {
      return;
    }

    const details = edge.details;

    for (const target of [paths[index], label]) {
      if (target) {
        makeOpener(target, `Open ${edgeName(edge, labels)}`, () => open(details, target));
      }
    }
  });

  section.nodes.forEach((node, index) => {
    const target = root.querySelector<SVGElement>(`g.node[id*="-n${index}-"]`);
    const details = node.details;
    const jump = node.target;

    if (details && target) {
      makeOpener(target, `Open ${node.label}`, () => open(details, target));
    } else if (jump && target) {
      target.dataset.jump = jump;
      makeOpener(target, `Go to ${jump}`, () => scrollToSection(jump));
    }
  });
}

export function DiagramSection({ section }: { section: DiagramSectionSpec }): ReactNode {
  const figure = useRef<HTMLDivElement>(null);
  const references = useContext(ReferencesContext);
  const [status, setStatus] = useState<DrawStatus>(DrawStatus.DRAWING);
  const [split, setSplit] = useState(false);
  const [opened, setOpened] = useState<Section | null>(null);
  const opener = useRef<SVGElement | null>(null);
  const labels = new Map(section.nodes.map((node) => [node.id, node.label]));
  const used = new Set([...section.nodes, ...section.edges].map((part) => part.change).filter(Boolean));
  const legend = Object.values(ChangeName).filter((change) => change === ChangeName.UNCHANGED || used.has(change));

  useEffect(() => {
    const target = figure.current;

    if (!target) {
      return;
    }

    let cancelled = false;

    drawDiagram(section, target)
      .then((drawing) => {
        if (cancelled) {
          return;
        }

        drawing.svg.style.maxWidth = 'none';
        drawing.svg.style.width = `${Math.round(drawing.width)}px`;

        target.replaceChildren(drawing.svg);
        target.scrollLeft = (target.scrollWidth - target.clientWidth) / 2;

        openEdgesOnClick(target, section, (details, element) => {
          opener.current = element;
          setOpened(details);
        });
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
        <SectionDialog section={opened} open onOpenChange={(open) => !open && setOpened(null)} opener={opener} />
      )}
    </SectionCard>
  );
}
