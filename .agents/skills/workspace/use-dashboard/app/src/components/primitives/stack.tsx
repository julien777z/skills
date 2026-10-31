import { cva, type VariantProps } from 'class-variance-authority';
import type { MouseEventHandler, ReactNode } from 'react';

const STACK_VARIANTS = {
  direction: { row: 'flex-row', column: 'flex-col' },
  gap: { none: 'gap-0', xs: 'gap-1', sm: 'gap-2', md: 'gap-3', lg: 'gap-4', xl: 'gap-6' },
  align: { start: 'items-start', center: 'items-center', stretch: 'items-stretch' },
  justify: { start: 'justify-start', center: 'justify-center', between: 'justify-between', end: 'justify-end' },
  wrap: { true: 'flex-wrap', false: 'flex-nowrap' },
  grow: { true: 'flex-1', false: '' },
  divided: { true: 'divide-y border-t', false: '' },
  inset: { none: '', row: 'px-6 py-3', page: 'px-4 lg:px-6', item: 'pb-3 pl-[18px]' },
  surface: {
    none: '',
    panel: 'rounded-lg border bg-muted/30 p-3',
    card: 'rounded-md border bg-card px-3 py-2.5 shadow-xs',
  },
  badge: {
    none: '',
    slot: 'mt-0.5 size-5 shrink-0',
    goodFilled: 'size-5 shrink-0 rounded-full bg-good text-background',
    accentRing: 'size-5 shrink-0 rounded-full border border-info',
  },
  frame: { none: '', page: '@container/page mx-auto w-full max-w-screen-2xl' },
  height: { auto: '', bar: 'h-14' },
  block: { none: '', row: 'py-3', page: 'py-8' },
  push: { true: 'ml-auto shrink-0', false: '' },
  show: { always: '', fromSm: 'hidden sm:flex', fromLg: 'hidden lg:flex', belowLg: 'lg:hidden' },
  scroll: { true: 'overflow-x-auto', false: '' },
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
    divided: false,
    inset: 'none',
    surface: 'none',
    badge: 'none',
    frame: 'none',
    height: 'auto',
    block: 'none',
    push: false,
    show: 'always',
    scroll: false,
    marker: 'none',
  },
});

interface StackProps extends VariantProps<typeof stackVariants> {
  as?: 'div' | 'main' | 'ul' | 'ol' | 'li' | 'nav';
  label?: string;
  onClick?: MouseEventHandler<HTMLElement>;
  children: ReactNode;
}

export function Stack({ as: Element = 'div', label, onClick, children, ...variants }: StackProps): ReactNode {
  return (
    <Element
      aria-label={label}
      onClick={onClick}
      className={stackVariants({ ...variants, class: onClick && 'cursor-pointer' })}
    >
      {children}
    </Element>
  );
}
