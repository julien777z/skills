import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const STACK_VARIANTS = {
  direction: { row: 'flex-row', column: 'flex-col' },
  gap: { none: 'gap-0', xs: 'gap-1', sm: 'gap-2', md: 'gap-3', lg: 'gap-4', xl: 'gap-6', page: 'gap-4 md:gap-6' },
  align: { start: 'items-start', center: 'items-center', stretch: 'items-stretch' },
  justify: { start: 'justify-start', center: 'justify-center', between: 'justify-between', end: 'justify-end' },
  wrap: { true: 'flex-wrap', false: 'flex-nowrap' },
  grow: { true: 'flex-1', false: '' },
  shrink: { always: '', belowLg: 'lg:shrink-0' },
  divided: { true: 'divide-y border-t', false: '' },
  inset: {
    none: '',
    row: 'px-6 py-3',
    card: 'px-6',
    page: 'px-4 sm:px-6 lg:px-10',
    item: 'pb-3 pl-[18px]',
    branch: 'ml-2 border-l pl-4',
  },
  surface: {
    none: '',
    panel: 'rounded-lg border bg-muted/30 p-3',
    card: 'rounded-md border bg-card px-3 py-2.5 shadow-xs',
  },
  badge: {
    none: '',
    slot: 'mt-0.5 size-5 shrink-0',
  },
  frame: { none: '', page: '@container/main w-full max-w-6xl', readable: 'max-w-4xl' },
  height: { auto: '', bar: 'min-h-14' },
  block: { none: '', row: 'py-3', page: 'py-6 md:py-10' },
  push: { true: 'ml-auto shrink-0', false: '' },
  trail: { true: 'ml-auto max-w-[50%] text-right', false: '' },
  show: { always: '', fromSm: 'hidden sm:flex', belowSm: 'sm:hidden', fromLg: 'hidden lg:flex', belowLg: 'lg:hidden' },
  marker: {
    none: 'list-none',
    bullet: 'list-disc pl-5 marker:text-muted-foreground',
    number: 'list-decimal pl-5 marker:text-muted-foreground',
  },
} as const;

const stackVariants: ReturnType<typeof cva<typeof STACK_VARIANTS>> = cva('flex min-w-0', {
  variants: STACK_VARIANTS,
  defaultVariants: {
    direction: 'column',
    gap: 'none',
    align: 'stretch',
    justify: 'start',
    wrap: false,
    grow: false,
    shrink: 'always',
    divided: false,
    inset: 'none',
    surface: 'none',
    badge: 'none',
    frame: 'none',
    height: 'auto',
    block: 'none',
    push: false,
    trail: false,
    show: 'always',
    marker: 'none',
  },
});

interface StackProps extends VariantProps<typeof stackVariants> {
  as?: 'div' | 'main' | 'ul' | 'ol' | 'li' | 'nav' | 'figure';
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
