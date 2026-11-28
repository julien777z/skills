export function withKeys<T>(items: readonly T[], identify: (item: T) => string): { key: string; item: T }[] {
  const seen = new Map<string, number>();

  return items.map((item) => {
    const identity = identify(item);
    const occurrence = seen.get(identity) ?? 0;

    seen.set(identity, occurrence + 1);

    return { key: `${identity}#${occurrence}`, item };
  });
}

export function sectionAnchor(title: string): { 'data-section-title': string } {
  return { 'data-section-title': title };
}

export function scrollToSection(title: string): void {
  document
    .querySelector(`[data-section-title="${CSS.escape(title)}"]`)
    ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

const STEP_KEYS: Record<string, number> = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };

export function steppedIndex(key: string, current: number, count: number): number | undefined {
  const step = STEP_KEYS[key];

  if (key === 'Home') {
    return 0;
  }

  if (key === 'End') {
    return count - 1;
  }

  if (step === undefined) {
    return undefined;
  }

  if (current < 0) {
    return step > 0 ? 0 : count - 1;
  }

  return (current + step + count) % count;
}
