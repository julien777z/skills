import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const TEXT_VARIANTS = {
  size: {
    xxs: 'text-[11px]',
    xs: 'text-xs',
    sm: 'text-sm',
    figure: 'text-2xl @[250px]/card:text-3xl',
    title: 'text-2xl tracking-tight sm:text-3xl',
  },
  tone: { default: '', muted: 'text-muted-foreground', accent: 'text-info' },
  weight: { medium: 'font-medium', semibold: 'font-semibold', bold: 'font-bold' },
  numeric: { true: 'tabular-nums', false: '' },
  breakAnywhere: { true: '[overflow-wrap:anywhere]', false: '' },
  truncate: { true: 'truncate', false: '' },
  caps: { true: 'uppercase tracking-wide', false: '' },
  measure: { true: 'max-w-[75ch]', false: '' },
} as const;

const textVariants: ReturnType<typeof cva<typeof TEXT_VARIANTS>> = cva('', {
  variants: TEXT_VARIANTS,
  defaultVariants: {
    tone: 'default',
    numeric: false,
    breakAnywhere: false,
    truncate: false,
    caps: false,
    measure: false,
  },
});

interface TextProps extends VariantProps<typeof textVariants> {
  as?: 'span' | 'p' | 'h1' | 'h3' | 'b' | 'li';
  children: ReactNode;
}

export function Text({ as: Element = 'span', children, ...variants }: TextProps): ReactNode {
  return <Element className={textVariants(variants)}>{children}</Element>;
}
