import { type Context, createContext } from 'react';

import type { Reference, Section } from '@/spec';

const REFERENCE_BOUNDARY: string = 'A-Za-z0-9_/-';

export interface ReferenceLink {
  text: string;
  href?: string;
  details?: Section;
}

type ReferenceTarget = Omit<ReferenceLink, 'text'>;

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
  private readonly targets: Map<string, ReferenceTarget>;
  private readonly pattern: RegExp | null;

  private readonly entries: Reference[];

  // Texts left unlinked, such as an open dialog's own name, still match so a shorter name never links inside them.
  private readonly plain: string[];

  constructor(entries: Reference[], plain: string[] = []) {
    this.entries = entries;
    this.plain = plain;
    this.targets = new Map();

    for (const entry of entries) {
      const link = entry.url ? linkAttributes(entry.url) : null;

      if (entry.details) {
        this.targets.set(entry.text, { details: entry.details });
      } else if (link) {
        this.targets.set(entry.text, { href: link.href });
      }
    }

    const texts = [...this.targets.keys(), ...plain].sort((first, second) => second.length - first.length);
    const alternatives = texts.map(escapeRegExp).join('|');

    this.pattern = texts.length
      ? new RegExp(`(?<![${REFERENCE_BOUNDARY}])(?:${alternatives})(?![${REFERENCE_BOUNDARY}])`, 'g')
      : null;
  }

  without(text: string): References {
    return new References(
      this.entries.filter((entry) => entry.text !== text),
      [...this.plain, text],
    );
  }

  split(text: string): (string | ReferenceLink)[] {
    if (!this.pattern) {
      return [text];
    }

    const parts: (string | ReferenceLink)[] = [];
    let start = 0;

    for (const match of text.matchAll(this.pattern)) {
      const target = this.targets.get(match[0]);

      if (!target) {
        continue;
      }

      const index = match.index ?? 0;

      parts.push(text.slice(start, index), { text: match[0], ...target });
      start = index + match[0].length;
    }

    parts.push(text.slice(start));

    return parts;
  }
}

export const ReferencesContext: Context<References> = createContext(new References([]));
