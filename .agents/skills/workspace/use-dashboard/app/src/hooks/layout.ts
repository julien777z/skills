import { type RefObject, useEffect, useState } from 'react';

export function useContentOverflows(frame: RefObject<HTMLElement | null>): boolean {
  const [overflows, setOverflows] = useState(false);

  useEffect(() => {
    const element = frame.current;

    if (!element) {
      return;
    }

    const measure = () => setOverflows(element.scrollWidth > element.clientWidth);
    const observer = new ResizeObserver(measure);

    observer.observe(element);

    for (const child of element.children) {
      observer.observe(child);
    }

    measure();

    return () => observer.disconnect();
  }, [frame]);

  return overflows;
}
