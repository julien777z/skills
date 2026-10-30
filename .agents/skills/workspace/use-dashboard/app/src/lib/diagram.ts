import type { Change, DiagramSection } from '@/spec';

interface Mermaid {
  initialize: (config: object) => void;
  render: (id: string, source: string) => Promise<{ svg: string }>;
}

declare global {
  interface Window {
    mermaid?: Mermaid;
  }
}

type Direction = 'LR' | 'TB';

type ColorToken = 'background' | 'card' | 'foreground' | 'muted-foreground' | 'border' | 'good' | 'info' | 'critical';

type Colors = Record<ColorToken, string>;

interface StrokeStyle {
  token: ColorToken;
  text: ColorToken;
  width: string;
  dashed?: boolean;
}

export interface Drawing {
  svg: SVGSVGElement;
  width: number;
  scale: number;
}

const COLOR_TOKENS: ColorToken[] = [
  'background',
  'card',
  'foreground',
  'muted-foreground',
  'border',
  'good',
  'info',
  'critical',
];

const MERMAID_SCRIPT = {
  src: 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js',
  integrity: 'sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I',
};

export const MIN_DIAGRAM_SCALE = 0.65;

export const SPLIT_RATIO = 0.6;

const RANK_SPACING: Record<Direction, string> = {
  LR: '%%{init: {"flowchart": {"rankSpacing": 36}}}%%',
  TB: '%%{init: {"flowchart": {"rankSpacing": 60}}}%%',
};

const CHANGE_STROKES: Record<Change | 'same', StrokeStyle> = {
  added: { token: 'good', text: 'foreground', width: '2px' },
  changed: { token: 'info', text: 'foreground', width: '2px' },
  removed: { token: 'critical', text: 'muted-foreground', width: '1.5px', dashed: true },
  same: { token: 'muted-foreground', text: 'foreground', width: '1px' },
};

let mermaidReady: Promise<{ mermaid: Mermaid; colors: Colors }> | null = null;

let diagramCount = 0;

function resolveColors(): Colors {
  const styles = getComputedStyle(document.documentElement);
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d', { willReadFrequently: true });
  const backdrop = styles.getPropertyValue('--background').trim();
  const colors = {} as Colors;

  canvas.width = 1;
  canvas.height = 1;

  for (const token of COLOR_TOKENS) {
    const value = styles.getPropertyValue(`--${token}`).trim();

    if (!context) {
      colors[token] = value;
      continue;
    }

    context.fillStyle = backdrop;
    context.fillRect(0, 0, 1, 1);
    context.fillStyle = value;
    context.fillRect(0, 0, 1, 1);

    const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;

    colors[token] = `#${[red, green, blue].map((channel) => channel.toString(16).padStart(2, '0')).join('')}`;
  }

  return colors;
}

function loadMermaid() {
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

function strokeStyle(style: StrokeStyle, colors: Colors): string {
  return `stroke:${colors[style.token]},stroke-width:${style.width}${style.dashed ? ',stroke-dasharray:5 4' : ''}`;
}

function flowchartSource(section: DiagramSection, direction: Direction, colors: Colors): string {
  const ids: Record<string, string> = {};
  const lines = [RANK_SPACING[direction], `flowchart ${direction}`];

  section.nodes.forEach((node, index) => {
    ids[node.id] = `n${index}`;
  });

  function nodeLine(node: DiagramSection['nodes'][number]): string {
    let text = `<b>${mermaidString(node.label)}</b>`;

    if (node.detail) {
      text += `<br/><small>${mermaidString(node.detail)}</small>`;
    }

    return `${ids[node.id]}["${text}"]:::${node.change ?? 'same'}`;
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

    lines.push(`${ids[edge.from]} --> ${label ? `|"${mermaidString(label)}"| ` : ''}${ids[edge.to]}`);
  }

  section.edges.forEach((edge, index) => {
    if (edge.change) {
      lines.push(`linkStyle ${index} ${strokeStyle(CHANGE_STROKES[edge.change], colors)}`);
    }
  });

  for (const [change, style] of Object.entries(CHANGE_STROKES)) {
    lines.push(`classDef ${change} fill:${colors.card},color:${colors[style.text]},${strokeStyle(style, colors)}`);
  }

  return lines.join('\n');
}

function parseDrawing(svgSource: string, available: number): Drawing {
  const holder = document.createElement('div');

  holder.innerHTML = svgSource;

  const svg = holder.querySelector('svg') as SVGSVGElement;
  const width = svg.viewBox.baseVal.width;

  return { svg, width, scale: Math.min(1, available / width) };
}

export async function drawDiagram(section: DiagramSection, available: number): Promise<Drawing> {
  const id = `diagram-${diagramCount++}`;
  const { mermaid, colors } = await loadMermaid();
  const directions: Direction[] = ['LR', 'TB'];
  const results = await Promise.all(
    directions.map((direction) => mermaid.render(`${id}-${direction}`, flowchartSource(section, direction, colors))),
  );
  const [preferred, fallback] = results.map((result) => parseDrawing(result.svg, available));
  const readable = preferred.scale >= MIN_DIAGRAM_SCALE || preferred.scale >= fallback.scale;

  return readable ? preferred : fallback;
}
