import { CHANGES, type ChangeName, TONES } from '@/lib/tone';
import type { DiagramNode, DiagramSection } from '@/spec';

interface Mermaid {
  initialize: (config: object) => void;
  render: (id: string, source: string) => Promise<{ svg: string }>;
}

declare global {
  interface Window {
    mermaid?: Mermaid;
  }
}

const DIRECTIONS = ['LR', 'TB'] as const;

type Direction = (typeof DIRECTIONS)[number];

const BASE_COLORS = ['background', 'card', 'foreground', 'muted-foreground', 'border'] as const;

type Colors = Record<string, string>;

export interface Drawing {
  svg: SVGSVGElement;
  width: number;
}

const MERMAID_SCRIPT: Readonly<{ src: string; integrity: string }> = {
  src: 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js',
  integrity: 'sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I',
};

const MIN_DIAGRAM_SCALE: number = 0.65;

const RANK_SPACING: Record<Direction, string> = {
  LR: '%%{init: {"flowchart": {"rankSpacing": 36}}}%%',
  TB: '%%{init: {"flowchart": {"rankSpacing": 60}}}%%',
};

let mermaidReady: Promise<{ mermaid: Mermaid; colors: Colors }> | null = null;

let diagramCount: number = 0;

function resolveColors(): Colors {
  const styles = getComputedStyle(document.documentElement);
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d', { willReadFrequently: true });
  const tokens = [...BASE_COLORS, ...Object.values(TONES).map((tone) => tone.color)];

  if (!context) {
    throw new Error('Canvas 2D is unavailable to convert theme colors for Mermaid');
  }

  canvas.width = 1;
  canvas.height = 1;

  return Object.fromEntries(
    tokens.map((token) => {
      context.fillStyle = styles.getPropertyValue('--background').trim();
      context.fillRect(0, 0, 1, 1);
      context.fillStyle = styles.getPropertyValue(`--${token}`).trim();
      context.fillRect(0, 0, 1, 1);

      const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;

      return [token, `#${[red, green, blue].map((channel) => channel.toString(16).padStart(2, '0')).join('')}`];
    }),
  );
}

function loadMermaid(): Promise<{ mermaid: Mermaid; colors: Colors }> {
  if (!mermaidReady) {
    mermaidReady = new Promise<Mermaid>((resolve, reject) => {
      const script = document.createElement('script');

      script.src = MERMAID_SCRIPT.src;
      script.integrity = MERMAID_SCRIPT.integrity;
      script.crossOrigin = 'anonymous';
      script.onload = () => (window.mermaid ? resolve(window.mermaid) : reject(new Error('Mermaid did not load')));
      script.onerror = () => reject(new Error('Mermaid did not load'));

      document.head.append(script);
    }).then((mermaid) => {
      const colors = resolveColors();

      mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: 'base',
        fontFamily: getComputedStyle(document.body).fontFamily,
        flowchart: { curve: 'basis', padding: 10, nodeSpacing: 28, wrappingWidth: 400 },
        themeVariables: {
          fontSize: '14px',
          primaryColor: colors.card,
          primaryTextColor: colors.foreground,
          primaryBorderColor: colors.border,
          lineColor: colors['muted-foreground'],
          clusterBkg: colors.background,
          clusterBorder: colors.border,
          titleColor: colors['muted-foreground'],
          edgeLabelBackground: colors.card,
        },
      });

      return { mermaid, colors };
    });
  }

  return mermaidReady;
}

function mermaidString(value: string): string {
  return value.replace(/`/g, '').replace(/[&<>"#%]/g, (character) => `#${character.charCodeAt(0)};`);
}

function strokeStyle(change: ChangeName, colors: Colors): string {
  const style = CHANGES[change];
  const width = change === 'unchanged' ? '1px' : style.dashed ? '1.5px' : '2px';

  return `stroke:${colors[TONES[style.tone].color]},stroke-width:${width}${style.dashed ? ',stroke-dasharray:5 4' : ''}`;
}

function flowchartSource(section: DiagramSection, direction: Direction, colors: Colors): string {
  const ids = new Map(section.nodes.map((node, index) => [node.id, `n${index}`]));
  const lines = [RANK_SPACING[direction], `flowchart ${direction}`];

  function nodeLine(node: DiagramNode): string {
    const detail = node.detail ? `<br/><small>${mermaidString(node.detail)}</small>` : '';

    return `${ids.get(node.id)}["<b>${mermaidString(node.label)}</b>${detail}"]:::${node.change ?? 'unchanged'}`;
  }

  for (const node of section.nodes.filter((entry) => !entry.pr)) {
    lines.push(nodeLine(node));
  }

  (section.prs ?? []).forEach((entry, index) => {
    lines.push(`subgraph pr${index}["${mermaidString(entry.ref)}"]`);

    for (const node of section.nodes.filter((part) => part.pr === entry.ref)) {
      lines.push(`  ${nodeLine(node)}`);
    }

    lines.push('end');
  });

  for (const edge of section.edges) {
    const label = [edge.step, edge.label].filter(Boolean).join(' · ');

    lines.push(`${ids.get(edge.from)} --> ${label ? `|"${mermaidString(label)}"| ` : ''}${ids.get(edge.to)}`);
  }

  section.edges.forEach((edge, index) => {
    if (edge.change) {
      lines.push(`linkStyle ${index} ${strokeStyle(edge.change, colors)}`);
    }
  });

  for (const change of Object.keys(CHANGES) as ChangeName[]) {
    const text = change === 'removed' || change === 'unchanged' ? colors['muted-foreground'] : colors.foreground;

    lines.push(`classDef ${change} fill:${colors.card},color:${text},${strokeStyle(change, colors)}`);
  }

  return lines.join('\n');
}

export async function drawDiagram(section: DiagramSection, available: number): Promise<Drawing> {
  const id = `diagram-${diagramCount++}`;
  const { mermaid, colors } = await loadMermaid();
  const results = await Promise.all(
    DIRECTIONS.map((direction) => mermaid.render(`${id}-${direction}`, flowchartSource(section, direction, colors))),
  );

  const drawings = results.map((result) => {
    const holder = document.createElement('div');

    holder.innerHTML = result.svg;

    const svg = holder.querySelector('svg') as SVGSVGElement;
    const width = svg.viewBox.baseVal.width;

    return { svg, width, scale: Math.min(1, available / width) };
  });

  const [preferred, fallback] = drawings;
  const chosen = preferred.scale >= MIN_DIAGRAM_SCALE || preferred.scale >= fallback.scale ? preferred : fallback;

  return { svg: chosen.svg, width: chosen.width * Math.max(chosen.scale, MIN_DIAGRAM_SCALE) };
}
