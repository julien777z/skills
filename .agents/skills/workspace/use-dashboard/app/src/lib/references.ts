import { type Context, createContext } from 'react';

import type { Reference } from '@/spec';

const REFERENCE_BOUNDARY: string = 'A-Za-z0-9_/-';

export interface ReferenceLink {
  text: string;
  href: string;
}

export interface LinkAttributes {
  href: string;
  target: '_blank';
  rel: string;
}

export function linkAttributes(value: string): LinkAttributes | null {
  try {
    const url = new URL(value);

    if (url.protocol !== 'https:' && url.protocol !== 'http:') {
      return null;
    }

    return { href: url.href, target: '_blank', rel: 'noopener noreferrer' };
  } catch (error) {
    if (error instanceof TypeError) {
      return null;
    }

    throw error;
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
      const link = linkAttributes(entry.url);

      if (link) {
        this.urls.set(entry.text, link.href);
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

export const ReferencesContext: Context<References> = createContext(new References([]));
