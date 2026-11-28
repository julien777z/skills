import { ChevronRight } from 'lucide-react';
import { type ReactNode, useRef, useState } from 'react';

import { DialogOpener, RichText, StatusBadge, ToneDot } from '@/components';
import { Stack, Text } from '@/components/primitives';
import { Button } from '@/components/ui/button';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { withKeys } from '@/lib/utils';
import type { TreeNode, TreeSection as TreeSectionSpec } from '@/spec';
import { SectionCard } from './section-card';
import { SectionDialog } from './section-dialog';

const DEFAULT_OPEN_DEPTH: number = 1;

function TreeBranch({ nodes, depth, openDepth }: { nodes: TreeNode[]; depth: number; openDepth: number }): ReactNode {
  const alignWithBranches = nodes.some((node) => (node.children ?? []).length > 0);

  return (
    <Stack as="ul" gap="xs" inset={depth > 0 ? 'branch' : 'none'}>
      {withKeys(nodes, (node) => node.label).map(({ key, item: node }) => (
        <TreeItem key={key} node={node} depth={depth} openDepth={openDepth} alignWithBranches={alignWithBranches} />
      ))}
    </Stack>
  );
}

interface TreeItemProps {
  node: TreeNode;
  depth: number;
  openDepth: number;
  alignWithBranches: boolean;
}

function TreeItem({ node, depth, openDepth, alignWithBranches }: TreeItemProps): ReactNode {
  const [open, setOpen] = useState(depth < openDepth);
  const [showDetails, setShowDetails] = useState(false);
  const opener = useRef<HTMLButtonElement | null>(null);
  const children = node.children ?? [];

  return (
    <Collapsible asChild open={open} onOpenChange={setOpen}>
      <li>
        <Stack direction="row" align="start" gap="sm">
          {children.length > 0 ? (
            <CollapsibleTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                aria-label={node.label}
                className="size-5 text-muted-foreground [&_svg]:transition-transform data-[state=open]:[&_svg]:rotate-90"
              >
                <ChevronRight />
              </Button>
            </CollapsibleTrigger>
          ) : (
            alignWithBranches && <span aria-hidden="true" className="size-5 shrink-0" />
          )}
          {(node.tone || children.length === 0) && <ToneDot tone={node.tone} offset />}
          <Stack gap="none" grow>
            <Text size="sm" breakAnywhere>
              {node.details ? (
                <DialogOpener
                  opener={opener}
                  onOpen={() => setShowDetails(true)}
                  className="text-left focus-visible:underline focus-visible:outline-none"
                >
                  {node.label}
                </DialogOpener>
              ) : (
                <Text as="span" size="sm" weight="medium">
                  <RichText text={node.label} />
                </Text>
              )}
              {node.tag && (
                <>
                  {' '}
                  <StatusBadge label={node.tag} dot={false} />
                </>
              )}
              {node.status && (
                <>
                  {' '}
                  <StatusBadge label={node.status.label} tone={node.status.tone} />
                </>
              )}
            </Text>
            {node.detail && (
              <Text size="sm" tone="muted" breakAnywhere>
                <RichText text={node.detail} />
              </Text>
            )}
          </Stack>
          {(node.meta || node.figure) && (
            <Stack direction="row" gap="md" justify="end" push>
              {node.meta && (
                <Text size="sm" tone="muted" numeric>
                  <RichText text={node.meta} />
                </Text>
              )}
              {node.figure && (
                <Text size="sm" tone="muted" numeric>
                  {node.figure}
                </Text>
              )}
            </Stack>
          )}
        </Stack>
        {children.length > 0 && (
          <CollapsibleContent>
            <TreeBranch nodes={children} depth={depth + 1} openDepth={openDepth} />
          </CollapsibleContent>
        )}
        {node.details && (
          <SectionDialog section={node.details} open={showDetails} onOpenChange={setShowDetails} opener={opener} />
        )}
      </li>
    </Collapsible>
  );
}

export function TreeSection({ section }: { section: TreeSectionSpec }): ReactNode {
  return (
    <SectionCard title={section.title} description={section.description} wide>
      <TreeBranch nodes={section.items} depth={0} openDepth={section.open_depth ?? DEFAULT_OPEN_DEPTH} />
    </SectionCard>
  );
}
