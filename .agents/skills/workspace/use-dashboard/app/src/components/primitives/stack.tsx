import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const stackVariants = cva('flex min-w-0', {
  variants: {
    direction: { row: 'flex-row', column: 'flex-col' },
    gap: { none: 'gap-0', xs: 'gap-1', sm: 'gap-2', md: 'gap-3', lg: 'gap-4', xl: 'gap-6' },
    align: { start: 'items-start', center: 'items-center', baseline: 'items-baseline', stretch: 'items-stretch' },
    justify: { start: 'justify-start', between: 'justify-between', end: 'justify-end' },
    wrap: { true: 'flex-wrap', false: 'flex-nowrap' },
    grow: { true: 'flex-1', false: '' },
    divided: { true: 'divide-y border-t', false: '' },
    inset: { none: '', row: 'px-6 py-3', page: 'px-4 lg:px-6', panel: 'p-3', card: 'px-3 py-2.5' },
    surface: { none: '', panel: 'rounded-lg border bg-muted/30', card: 'rounded-md border bg-card shadow-xs' },
    marker: {
      none: 'list-none',
      bullet: 'list-disc pl-5 marker:text-muted-foreground',
      number: 'list-decimal pl-5 marker:text-muted-foreground',
    },
  },
  defaultVariants: {
    direction: 'column',
    gap: 'none',
    align: 'stretch',
    justify: 'start',
    wrap: false,
    grow: false,
    divided: false,
    inset: 'none',
    surface: 'none',
    marker: 'none',
  },
});

interface StackProps extends VariantProps<typeof stackVariants> {
  as?: 'div' | 'section' | 'ul' | 'ol' | 'li' | 'nav' | 'span';
  label?: string;
  children: ReactNode;
}

export function Stack({ as: Element = 'div', label, children, ...variants }: StackProps): ReactNode {
  return (
    <Element aria-label={label} className={stackVariants(variants)}>
      {children}
    </Element>
  );
}
