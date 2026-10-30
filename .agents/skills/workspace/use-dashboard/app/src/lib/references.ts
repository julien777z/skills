import { createContext } from 'react';

import type { Reference } from '@/spec';

const REFERENCE_BOUNDARY: string = 'A-Za-z0-9_/-';

export interface ReferenceLink {
  text: string;
  href: string;
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

export class References {
  private readonly urls: Map<string, string>;
  private readonly pattern: RegExp | null;

  constructor(entries: Reference[]) {
    this.urls = new Map();

    for (const entry of entries) {
      const href = safeUrl(entry.url);

      if (href) {
        this.urls.set(entry.text, href);
      }
    }

    const texts = [...this.urls.keys()].sort((first, second) => second.length - first.length);
    const alternatives = texts.map(escapeRegExp).join('|');

    this.pattern = texts.length
      ? new RegExp(`(?<![${REFERENCE_BOUNDARY}])(?:${alternatives})(?![${REFERENCE_BOUNDARY}])`, 'g')
      : null;
  }

  split(text: string): (string | ReferenceLink)[] {
    if (!this.pattern) {
      return [text];
    }

    const parts: (string | ReferenceLink)[] = [];
    let start = 0;

    for (const match of text.matchAll(this.pattern)) {
      const index = match.index ?? 0;

      parts.push(text.slice(start, index), { text: match[0], href: this.urls.get(match[0]) ?? '' });
      start = index + match[0].length;
    }

    parts.push(text.slice(start));

    return parts;
  }
}

export const ReferencesContext = createContext<References>(new References([]));
