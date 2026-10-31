import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function withKeys<T>(items: readonly T[], identify: (item: T) => string): { key: string; item: T }[] {
  const seen = new Map<string, number>();

  return items.map((item) => {
    const identity = identify(item);
    const occurrence = seen.get(identity) ?? 0;

    seen.set(identity, occurrence + 1);

    return { key: `${identity}#${occurrence}`, item };
  });
}
