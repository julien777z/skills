import { ChevronRight } from 'lucide-react';
import { type ReactNode, useRef, useState } from 'react';

import { RichText, StatusBadge, ToneDot } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { cn, withKeys } from '@/lib/utils';
import type { TreeNode, TreeSection as TreeSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

const DEFAULT_OPEN_DEPTH: number = 1;

function TreeBranch({ nodes, depth, openDepth }: { nodes: TreeNode[]; depth: number; openDepth: number }): ReactNode {
  return (
    <Stack as="ul" gap="xs" inset={depth > 0 ? 'branch' : 'none'}>
      {withKeys(nodes, (node) => node.label).map(({ key, item: node }) => (
        <TreeItem key={key} node={node} depth={depth} openDepth={openDepth} />
      ))}
    </Stack>
  );
}

function TreeItem({ node, depth, openDepth }: { node: TreeNode; depth: number; openDepth: number }): ReactNode {
  const [open, setOpen] = useState(depth < openDepth);
  const [showDetails, setShowDetails] = useState(false);
  const opener = useRef<HTMLButtonElement | null>(null);
  const children = node.children ?? [];

  return (
    <li>
      <Stack direction="row" align="start" gap="sm">
        {children.length > 0 ? (
          <button
            type="button"
            aria-expanded={open}
            aria-label={node.label}
            onClick={() => setOpen(!open)}
            className="mt-0.5 rounded-sm text-muted-foreground hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
          >
            <ChevronRight className={cn('size-4 transition-transform', open && 'rotate-90')} />
          </button>
        ) : null}
        {(node.tone || children.length === 0) && <ToneDot tone={node.tone} offset />}
        <Stack gap="none" grow>
          <Text size="sm" breakAnywhere>
            {node.details ? (
              <button
                ref={opener}
                type="button"
                onClick={() => setShowDetails(true)}
                className="text-left font-medium underline-offset-4 hover:underline focus-visible:underline focus-visible:outline-none"
              >
                {node.label}
              </button>
            ) : (
              <Text as="span" size="sm" weight="medium">
                <RichText text={node.label} />
              </Text>
            )}
            {node.figure && (
              <>
                {' '}
                <StatusBadge label={node.figure} dot={false} />
              </>
            )}
            {node.meta && (
              <Text as="span" size="sm" tone="muted" numeric>
                {' '}
                <RichText text={node.meta} />
              </Text>
            )}
          </Text>
          {node.detail && (
            <Text size="sm" tone="muted" breakAnywhere>
              <RichText text={node.detail} />
            </Text>
          )}
        </Stack>
      </Stack>
      {open && children.length > 0 && <TreeBranch nodes={children} depth={depth + 1} openDepth={openDepth} />}
      {node.details && (
        <SectionDialog section={node.details} open={showDetails} onOpenChange={setShowDetails} opener={opener} />
      )}
    </li>
  );
}

export function TreeSection({ section }: { section: TreeSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <TreeBranch nodes={section.items} depth={0} openDepth={section.open_depth ?? DEFAULT_OPEN_DEPTH} />
    </SectionCard>
  );
}
