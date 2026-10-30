export type Tone = 'good' | 'warning' | 'critical' | 'accent' | 'done';

export type Change = 'added' | 'changed' | 'removed';

export type PullRequestState = 'open' | 'draft' | 'merged' | 'closed';

export interface Label {
  label: string;
  tone?: Tone;
}

export interface Segment extends Label {
  weight?: number;
}

export interface ProgressSummary {
  value: number;
  label: string;
  detail?: string;
  segments?: Segment[];
}

export interface Metric {
  label: string;
  value: string;
  detail?: string;
}

export interface Card {
  title: string;
  detail?: string;
  meta?: string;
  tag?: string;
  url?: string;
}

export interface BoardColumn {
  title: string;
  tone?: Tone;
  page_size?: number;
  items: Card[];
}

export interface Question {
  question: string;
  status: 'open' | 'answered';
  context?: string;
  options?: string[];
  recommendation?: string;
  answer?: string;
  meta?: string;
}

export interface LinkItem {
  label: string;
  url: string;
  detail?: string;
  status?: string;
  tone?: Tone;
  state?: PullRequestState;
}

export interface ChangeItem {
  name: string;
  change: Change;
  detail?: string;
}

export interface OutlineItem {
  title: string;
  detail: string;
  tone?: Tone;
  tag?: string;
  meta?: string;
}

export interface OutlineGroup {
  title: string;
  items: OutlineItem[];
}

export interface DiagramNode {
  id: string;
  label: string;
  detail?: string;
  pr?: string;
  change?: Change;
}

export interface DiagramEdge {
  from: string;
  to: string;
  label?: string;
  step?: number;
  change?: Change;
}

export interface DiagramPullRequest {
  ref: string;
  url: string;
}

interface SectionBase {
  title: string;
}

export interface BoardSection extends SectionBase {
  type: 'board';
  columns: BoardColumn[];
}

export interface QuestionsSection extends SectionBase {
  type: 'questions';
  items: Question[];
  page_size?: number;
}

export interface LinksSection extends SectionBase {
  type: 'links';
  items: LinkItem[];
  page_size?: number;
}

export interface ChangesSection extends SectionBase {
  type: 'changes';
  items: ChangeItem[];
  page_size?: number;
}

export interface TableSection extends SectionBase {
  type: 'table';
  columns: string[];
  rows: string[][];
}

export interface NotesSection extends SectionBase {
  type: 'notes';
  items: string[];
}

export interface OutlineSection extends SectionBase {
  type: 'outline';
  groups: OutlineGroup[];
}

export interface CalloutSection extends SectionBase {
  type: 'callout';
  body: string;
  tone?: Tone;
}

export interface DiagramSection extends SectionBase {
  type: 'diagram';
  nodes: DiagramNode[];
  edges: DiagramEdge[];
  prs?: DiagramPullRequest[];
  steps?: string[];
}

export type Section =
  | BoardSection
  | QuestionsSection
  | LinksSection
  | ChangesSection
  | TableSection
  | NotesSection
  | OutlineSection
  | CalloutSection
  | DiagramSection;

export type PageIcon =
  | 'overview'
  | 'list'
  | 'chart'
  | 'diagram'
  | 'document'
  | 'shield'
  | 'people'
  | 'data'
  | 'settings'
  | 'alert'
  | 'check'
  | 'calendar';

export interface Page {
  title: string;
  icon?: PageIcon;
  layout?: 'columns' | 'rows';
  sections: Section[];
}

export interface Reference {
  text: string;
  url: string;
}

export interface Dashboard {
  title: string;
  subtitle?: string;
  updated_at: string;
  status?: Label;
  progress?: ProgressSummary;
  metrics?: Metric[];
  pages: Page[];
  references?: Reference[];
}
