import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const gridVariants = cva('grid items-start', {
  variants: {
    columns: {
      single: 'grid-cols-1',
      narrow: 'grid-cols-[repeat(auto-fit,minmax(min(100%,220px),1fr))]',
      medium: 'grid-cols-[repeat(auto-fit,minmax(min(100%,340px),1fr))]',
      wide: 'grid-cols-[repeat(auto-fit,minmax(min(100%,380px),1fr))]',
    },
    gap: { md: 'gap-4', lg: 'gap-4 md:gap-6', loose: 'gap-x-8 gap-y-6' },
    inset: { none: '', page: 'px-4 lg:px-6' },
  },
  defaultVariants: { columns: 'single', gap: 'md', inset: 'none' },
});

interface GridProps extends VariantProps<typeof gridVariants> {
  children: ReactNode;
}

export function Grid({ children, ...variants }: GridProps): ReactNode {
  return <div className={gridVariants(variants)}>{children}</div>;
}
