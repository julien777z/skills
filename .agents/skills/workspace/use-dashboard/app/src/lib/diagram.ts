import { CHANGES, ChangeName, TONES, type ToneName } from '@/lib/tone';
import type { DiagramNode, DiagramSection } from '@/spec';

interface Mermaid {
  initialize: (config: object) => void;
  render: (id: string, source: string, container: Element) => Promise<{ svg: string }>;
}

declare global {
  interface Window {
    mermaid?: Mermaid;
  }
}

const DIRECTIONS = ['LR', 'TB'] as const;

type Direction = (typeof DIRECTIONS)[number];

const BASE_COLORS = ['background', 'card', 'foreground', 'muted-foreground', 'border'] as const;

type Colors = Record<(typeof BASE_COLORS)[number] | (typeof TONES)[ToneName]['color'], string>;

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

const SVG_NAMESPACE: string = 'http://www.w3.org/2000/svg';

const XHTML_NAMESPACE: string = 'http://www.w3.org/1999/xhtml';

const INLINED_TEXT_STYLES: readonly string[] = [
  'color',
  'font-family',
  'font-size',
  'font-weight',
  'line-height',
  'text-decoration-line',
  'max-width',
  'white-space',
];

const PNG_SCALE: number = 2;

const MAX_CANVAS_SIDE: number = 16384;

const MAX_CANVAS_AREA: number = 16_000_000;

const DOWNLOAD_URL_LIFETIME_MS: number = 60_000;

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
  ) as Colors;
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

  return `stroke:${colors[TONES[style.tone].color]},stroke-width:${style.strokeWidth}${style.dashed ? ',stroke-dasharray:5 4' : ''}`;
}

function flowchartSource(section: DiagramSection, direction: Direction, colors: Colors): string {
  const ids = new Map(section.nodes.map((node, index) => [node.id, `n${index}`]));
  const lines = [RANK_SPACING[direction], `flowchart ${direction}`];

  function nodeLine(node: DiagramNode): string {
    const detail = node.detail ? `<br/><small>${mermaidString(node.detail)}</small>` : '';

    return `${ids.get(node.id)}["<b>${mermaidString(node.label)}</b>${detail}"]:::${node.change ?? ChangeName.UNCHANGED}`;
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

  section.nodes.forEach((node) => {
    if (node.tone) {
      lines.push(`style ${ids.get(node.id)} stroke:${colors[TONES[node.tone].color]},stroke-width:3px`);
    }
  });

  section.edges.forEach((edge, index) => {
    if (edge.tone) {
      lines.push(`linkStyle ${index} stroke:${colors[TONES[edge.tone].color]},stroke-width:3px`);
    } else if (edge.change) {
      lines.push(`linkStyle ${index} ${strokeStyle(edge.change, colors)}`);
    }
  });

  for (const change of Object.values(ChangeName)) {
    const text = CHANGES[change].mutedText ? colors['muted-foreground'] : colors.foreground;

    lines.push(`classDef ${change} fill:${colors.card},color:${text},${strokeStyle(change, colors)}`);
  }

  return lines.join('\n');
}

export async function drawDiagram(section: DiagramSection, container: HTMLElement): Promise<Drawing> {
  const available = container.clientWidth;
  const id = `diagram-${diagramCount++}`;
  const { mermaid, colors } = await loadMermaid();
  const sandbox = document.createElement('div');

  sandbox.style.cssText = `position:absolute;visibility:hidden;pointer-events:none;width:${available}px`;
  container.append(sandbox);

  const results = await Promise.all(
    DIRECTIONS.map((direction) =>
      mermaid.render(`${id}-${direction}`, flowchartSource(section, direction, colors), sandbox),
    ),
  ).finally(() => sandbox.remove());

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

function opaqueBackground(element: Element): string {
  for (let current: Element | null = element; current; current = current.parentElement) {
    const color = getComputedStyle(current).backgroundColor;

    if (color && color !== 'transparent' && !color.endsWith(', 0)')) {
      return color;
    }
  }

  return getComputedStyle(document.body).backgroundColor;
}

function fontFaces(): string {
  const rules: string[] = [];

  for (const sheet of Array.from(document.styleSheets)) {
    try {
      for (const rule of Array.from(sheet.cssRules)) {
        if (rule instanceof CSSFontFaceRule) {
          rules.push(rule.cssText);
        }
      }
    } catch (error) {
      // A cross-origin stylesheet hides its rules; the page's own fonts are bundled inline.
      if (!(error instanceof DOMException && error.name === 'SecurityError')) {
        throw error;
      }
    }
  }

  return rules.join('\n');
}

export function diagramFileName(...titles: string[]): string {
  const slug = (text: string): string =>
    text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');

  return `${titles.map(slug).filter(Boolean).join('-') || 'diagram'}.png`;
}

function standaloneSvg(svg: SVGSVGElement): { markup: string; width: number; height: number } {
  const copy = svg.cloneNode(true) as SVGSVGElement;
  const originals = svg.querySelectorAll('*');
  const copies = copy.querySelectorAll('*');

  originals.forEach((original, index) => {
    if (original.namespaceURI !== XHTML_NAMESPACE) {
      return;
    }

    const computed = getComputedStyle(original);
    const target = copies[index] as HTMLElement;

    for (const property of INLINED_TEXT_STYLES) {
      target.style.setProperty(property, computed.getPropertyValue(property));
    }
  });

  copy.querySelectorAll('foreignObject').forEach((foreign) => {
    foreign.setAttribute('overflow', 'visible');
  });

  const { x, y, width, height } = svg.viewBox.baseVal;
  const background = document.createElementNS(SVG_NAMESPACE, 'rect');

  background.setAttribute('x', String(x));
  background.setAttribute('y', String(y));
  background.setAttribute('width', String(width));
  background.setAttribute('height', String(height));
  background.setAttribute('fill', opaqueBackground(svg));
  copy.insertBefore(background, copy.firstChild);

  const fonts = document.createElementNS(SVG_NAMESPACE, 'style');

  fonts.textContent = fontFaces();
  copy.insertBefore(fonts, copy.firstChild);
  copy.setAttribute('xmlns', SVG_NAMESPACE);
  copy.setAttribute('width', String(Math.round(width)));
  copy.setAttribute('height', String(Math.round(height)));
  copy.style.removeProperty('max-width');
  copy.style.removeProperty('width');

  return { markup: new XMLSerializer().serializeToString(copy), width, height };
}

function loadImage(source: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();

    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('The diagram could not be drawn as an image'));
    image.src = source;
  });
}

export async function downloadDiagram(svg: SVGSVGElement, fileName: string): Promise<void> {
  const { markup, width, height } = standaloneSvg(svg);
  const bytes = new TextEncoder().encode(markup);
  let binary = '';

  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }

  const image = await loadImage(`data:image/svg+xml;base64,${btoa(binary)}`);
  const scale = Math.min(
    PNG_SCALE,
    MAX_CANVAS_SIDE / width,
    MAX_CANVAS_SIDE / height,
    Math.sqrt(MAX_CANVAS_AREA / (width * height)),
  );
  const canvas = document.createElement('canvas');

  canvas.width = Math.round(width * scale);
  canvas.height = Math.round(height * scale);

  const context = canvas.getContext('2d');

  if (!context) {
    throw new Error('Canvas 2D is unavailable to save the diagram');
  }

  context.drawImage(image, 0, 0, canvas.width, canvas.height);

  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, 'image/png'));

  if (!blob) {
    throw new Error('The diagram could not be encoded as PNG');
  }

  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');

  link.href = url;
  link.download = fileName;
  link.hidden = true;
  document.body.append(link);
  link.click();
  link.remove();
  // Safari reads the file after this task ends, so the address stays valid until it has.
  setTimeout(() => URL.revokeObjectURL(url), DOWNLOAD_URL_LIFETIME_MS);
}
