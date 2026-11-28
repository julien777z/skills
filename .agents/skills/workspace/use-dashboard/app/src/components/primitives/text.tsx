import { cva, type VariantProps } from 'class-variance-authority';
import type { ReactNode } from 'react';

const TEXT_VARIANTS = {
  size: {
    xs: 'text-xs',
    sm: 'text-sm',
    detail: 'text-[0.8125rem] leading-5',
    figure: 'text-2xl @[250px]/card:text-3xl',
    title: 'text-2xl tracking-tight sm:text-3xl',
  },
  tone: { default: '', muted: 'text-muted-foreground', strong: 'text-foreground' },
  weight: { medium: 'font-medium', semibold: 'font-semibold', bold: 'font-bold' },
  numeric: { true: 'tabular-nums', false: '' },
  breakAnywhere: { true: '[overflow-wrap:anywhere]', false: '' },
  nowrap: { true: 'shrink-0 whitespace-nowrap', false: '' },
  measure: { true: 'max-w-[75ch]', false: '' },
  srOnly: { true: 'sr-only', false: '' },
} as const;

const textVariants: ReturnType<typeof cva<typeof TEXT_VARIANTS>> = cva('', {
  variants: TEXT_VARIANTS,
  defaultVariants: {
    tone: 'default',
    numeric: false,
    breakAnywhere: false,
    nowrap: false,
    measure: false,
    srOnly: false,
  },
});

interface TextProps extends VariantProps<typeof textVariants> {
  as?: 'span' | 'p' | 'h1' | 'h3' | 'b' | 'li' | 'figcaption';
  labelFor?: string;
  children: ReactNode;
}

export function Text({ as: Element = 'span', labelFor, children, ...variants }: TextProps): ReactNode {
  if (labelFor) {
    return (
      <label htmlFor={labelFor} className={textVariants({ ...variants, class: 'cursor-pointer' })}>
        {children}
      </label>
    );
  }

  return <Element className={textVariants(variants)}>{children}</Element>;
}
