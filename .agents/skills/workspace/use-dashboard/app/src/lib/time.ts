export const MINUTE_MS: number = 60_000;

const MINUTES_PER_DAY: number = 1_440;

export const CLOCK: Intl.DateTimeFormatOptions = { hour: 'numeric', minute: '2-digit', hour12: true };

export const DATE_AND_CLOCK: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric', ...CLOCK };

export function formatMoment(iso: string, now: number): string {
  const then = new Date(iso);
  const sameDay = then.toDateString() === new Date(now).toDateString();

  return then.toLocaleString(undefined, sameDay ? CLOCK : DATE_AND_CLOCK);
}

export function formatSpan(start: string, end: string, now: number): string {
  const sameDay = new Date(start).toDateString() === new Date(end).toDateString();
  const until = new Date(end).toLocaleString(undefined, sameDay ? CLOCK : DATE_AND_CLOCK);

  return `${formatMoment(start, now)} – ${until}`;
}

export function formatDuration(milliseconds: number): string {
  const minutes = Math.round(milliseconds / MINUTE_MS);

  if (minutes < 1) {
    return `${Math.round(milliseconds / 1000)}s`;
  }

  const parts = [
    { value: Math.floor(minutes / MINUTES_PER_DAY), unit: 'd' },
    { value: Math.floor((minutes % MINUTES_PER_DAY) / 60), unit: 'h' },
    { value: minutes % 60, unit: ' min' },
  ];
  const largest = parts.findIndex((part) => part.value > 0);

  return parts
    .slice(largest, largest + 2)
    .filter((part) => part.value > 0)
    .map((part) => `${part.value}${part.unit}`)
    .join(' ');
}

export function relativeTime(iso: string, now: number): string {
  const then = new Date(iso);
  const minutes = Math.round((now - then.getTime()) / MINUTE_MS);

  if (minutes < 1) {
    return 'Updated just now';
  }

  if (minutes < 60) {
    return `Updated ${minutes}m ago`;
  }

  if (minutes < MINUTES_PER_DAY) {
    return `Updated ${Math.round(minutes / 60)}h ago`;
  }

  return `Updated ${formatMoment(iso, now)}`;
}
