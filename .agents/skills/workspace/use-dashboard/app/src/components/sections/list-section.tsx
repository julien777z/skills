import { Fragment, type ReactNode, useId, useState } from 'react';

import { Stack, Text } from '@/components/primitives';
import { NativeSelect, NativeSelectOption } from '@/components/ui/native-select';
import { withKeys } from '@/lib/utils';
import { Paged } from './paged';
import { SectionCard } from './section-card';

const ALL_GROUPS: string = '';

interface ListRowContent {
  icon?: ReactNode;
  title: ReactNode;
  detail?: ReactNode;
  aside?: ReactNode;
  body?: ReactNode;
}

interface GroupedItem {
  group?: string;
}

interface ListSectionProps<Item extends GroupedItem> {
  title: string;
  description?: string;
  summary: (items: Item[]) => ReactNode;
  items: Item[];
  pageSize?: number;
  groupLabel?: string;
  row: (item: Item) => ListRowContent;
}

interface GroupFilterProps {
  label: string;
  groups: string[];
  selected: string;
  onSelect: (group: string) => void;
}

function ListRow({ icon, title, detail, aside, body }: ListRowContent): ReactNode {
  return (
    <Stack as="li" direction="row" align="start" gap="md" inset="row">
      {icon && (
        <Stack align="center" justify="center" badge="slot">
          {icon}
        </Stack>
      )}
      <Stack grow gap="xs">
        <Text weight="medium" breakAnywhere>
          {title}
        </Text>
        {detail && (
          <Text size="sm" tone="muted" breakAnywhere>
            {detail}
          </Text>
        )}
        {body}
      </Stack>
      {aside}
    </Stack>
  );
}

function GroupFilter({ label, groups, selected, onSelect }: GroupFilterProps): ReactNode {
  const id = useId();

  return (
    <Stack direction="row" align="center" gap="sm" wrap inset="card">
      <Text labelFor={id} size="sm" tone="muted">
        {label}
      </Text>
      <NativeSelect id={id} size="sm" value={selected} onChange={(event) => onSelect(event.target.value)}>
        <NativeSelectOption value={ALL_GROUPS}>All</NativeSelectOption>
        {groups.map((group) => (
          <NativeSelectOption key={group} value={group}>
            {group}
          </NativeSelectOption>
        ))}
      </NativeSelect>
    </Stack>
  );
}

export function ListSection<Item extends GroupedItem>({
  title,
  description,
  summary,
  items,
  pageSize,
  groupLabel,
  row,
}: ListSectionProps<Item>): ReactNode {
  const [selected, setSelected] = useState(ALL_GROUPS);

  const groups = [...new Set(items.flatMap((item) => (item.group ? [item.group] : [])))];
  const grouped = groups.length ? groups.flatMap((group) => items.filter((item) => item.group === group)) : items;
  const headed = selected === ALL_GROUPS;
  const shown = headed ? grouped : grouped.filter((item) => item.group === selected);
  const filterable = groupLabel !== undefined && groups.length > 1;

  return (
    <SectionCard title={title} description={description} summary={summary(shown)} flush>
      <Stack gap="md">
        {filterable && <GroupFilter label={groupLabel} groups={groups} selected={selected} onSelect={setSelected} />}
        <Stack>
          <Paged key={selected} items={shown} pageSize={pageSize} label={title} flush>
            {(visible) => (
              <Stack as="ul" divided>
                {withKeys(visible, (item) => JSON.stringify(item)).map(({ key, item }, index) => (
                  <Fragment key={key}>
                    {headed && item.group !== visible[index - 1]?.group && (
                      <Stack as="li" inset="row">
                        <Text size="xs" tone="muted" weight="medium">
                          {item.group}
                        </Text>
                      </Stack>
                    )}
                    <ListRow {...row(item)} />
                  </Fragment>
                ))}
              </Stack>
            )}
          </Paged>
        </Stack>
      </Stack>
    </SectionCard>
  );
}
