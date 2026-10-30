import { createContext, type ReactNode, useContext } from 'react';

import type { Reference } from '@/spec';

const REFERENCE_BOUNDARY = 'A-Za-z0-9_/-';

export interface ReferenceLinks {
  urls: Record<string, string>;
  pattern: RegExp;
}

export function safeUrl(value: string): string | null {
  try {
    const url = new URL(value);

    return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null;
  } catch {
    return null;
  }
}

function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export function compileReferences(entries: Reference[]): ReferenceLinks | null {
  const urls: Record<string, string> = {};

  for (const entry of entries) {
    const href = safeUrl(entry.url);

    if (href) {
      urls[entry.text] = href;
    }
  }

  const texts = Object.keys(urls).sort((first, second) => second.length - first.length);

  if (!texts.length) {
    return null;
  }

  const alternatives = texts.map(escapeRegExp).join('|');

  return {
    urls,
    pattern: new RegExp(`(?<![${REFERENCE_BOUNDARY}])(?:${alternatives})(?![${REFERENCE_BOUNDARY}])`, 'g'),
  };
}

export const ReferencesContext = createContext<ReferenceLinks | null>(null);

export function ExternalLink({ href, children, className }: { href: string; children: ReactNode; className?: string }) {
  const url = safeUrl(href);

  if (!url) {
    return <span className={className}>{children}</span>;
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className={className ?? 'font-medium text-info underline-offset-4 hover:underline'}
    >
      {children}
    </a>
  );
}

function splitReferences(text: string, references: ReferenceLinks | null): ReactNode[] {
  if (!references) {
    return [text];
  }

  const parts: ReactNode[] = [];
  let start = 0;

  for (const match of text.matchAll(references.pattern)) {
    const index = match.index ?? 0;

    parts.push(text.slice(start, index));
    parts.push(
      <ExternalLink key={index} href={references.urls[match[0]]}>
        {match[0]}
      </ExternalLink>,
    );
    start = index + match[0].length;
  }

  parts.push(text.slice(start));

  return parts;
}

export function RichText({ text }: { text: string }) {
  const references = useContext(ReferencesContext);

  return <>{splitReferences(text, references)}</>;
}
