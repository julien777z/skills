export function relativeTime(iso: string, now: number): string {
  const then = new Date(iso);

  if (Number.isNaN(then.getTime())) {
    return '';
  }

  const minutes = Math.round((now - then.getTime()) / 60000);

  if (minutes < 1) {
    return 'Updated just now';
  }

  if (minutes < 60) {
    return `Updated ${minutes} min ago`;
  }

  if (minutes < 1440) {
    return `Updated ${Math.round(minutes / 60)} h ago`;
  }

  return `Updated ${then.toLocaleDateString()}`;
}
