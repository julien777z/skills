import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const gridVariants = cva('grid', {
  variants: {
    columns: {
      single: 'grid-cols-1',
      narrow: 'grid-cols-[repeat(auto-fit,minmax(min(100%,220px),1fr))]',
      medium: 'grid-cols-[repeat(auto-fit,minmax(min(100%,340px),1fr))]',
      wide: 'grid-cols-[repeat(auto-fit,minmax(min(100%,380px),1fr))]',
      steps: 'sm:grid-cols-[repeat(auto-fill,minmax(min(100%,300px),1fr))]',
      figureBesideSteps: 'grid-cols-1 lg:grid-cols-[auto_minmax(300px,1fr)]',
      stats2: 'grid-cols-1 @xl/main:grid-cols-2',
      stats3: 'grid-cols-1 @xl/main:grid-cols-2 @5xl/main:grid-cols-3',
      stats4: 'grid-cols-1 @xl/main:grid-cols-2 @5xl/main:grid-cols-4',
      stats5: 'grid-cols-1 @xl/main:grid-cols-2 @5xl/main:grid-cols-5',
      stats6: 'grid-cols-1 @xl/main:grid-cols-2 @5xl/main:grid-cols-6',
    },
    gap: { sm: 'gap-3', md: 'gap-4', lg: 'gap-4 md:gap-6', loose: 'gap-x-8 gap-y-6' },
    inset: { none: '', page: 'px-4 lg:px-6' },
    align: { start: 'items-start', stretch: 'items-stretch' },
    divider: { none: '', top: 'border-t pt-4', side: 'border-t pt-4 lg:border-t-0 lg:border-l lg:pt-0 lg:pl-7' },
  },
  defaultVariants: { columns: 'single', gap: 'md', inset: 'none', align: 'start', divider: 'none' },
});

interface GridProps extends VariantProps<typeof gridVariants> {
  as?: 'div' | 'ol';
  children: ReactNode;
}

export function Grid({ as: Element = 'div', children, ...variants }: GridProps): ReactNode {
  return <Element className={gridVariants(variants)}>{children}</Element>;
}
