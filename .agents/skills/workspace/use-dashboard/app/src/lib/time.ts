const MINUTE_MS: number = 60_000;

const MINUTES_PER_DAY: number = 1_440;

const CLOCK: Intl.DateTimeFormatOptions = { hour: 'numeric', minute: '2-digit', hour12: true };

const DATE_AND_CLOCK: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric', ...CLOCK };

export function formatMoment(iso: string, now: number): string {
  const then = new Date(iso);
  const sameDay = then.toDateString() === new Date(now).toDateString();

  return then.toLocaleString(undefined, sameDay ? CLOCK : DATE_AND_CLOCK);
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
