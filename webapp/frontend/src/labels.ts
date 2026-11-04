// Human wording for the codes the API uses, and the fixed product copy.

import type { FindingStatus } from './api'

export const PRODUCT_NAME = 'SheetTruth'
export const EYEBROW = 'Spreadsheet formula auditor'
export const HEADLINE = 'Catch the formulas that quietly get it wrong.'
export const TAGLINE =
  'Upload an Excel workbook. SheetTruth reads every formula, flags the ones that look wrong, tests each fix against your own numbers, and gives you a corrected copy.'

// Shown while the model step runs: the model server starts cold after a quiet spell.
export const COLD_START_NOTE =
  'The first audit after a quiet spell takes an extra minute or two on this step while the model server wakes up. Nothing is stuck.'

// The two models behind an audit.
export const MODEL_MAKER = 'Meta'
export const MEANING_MODEL = 'Muse Glimmer 30B'
export const REVIEWER_MODEL = 'Muse Spark 1.3'
export const MODELS: { kind: 'meaning' | 'reviewer'; name: string; role: string }[] = [
  { kind: 'meaning', name: MEANING_MODEL, role: 'Fine-tuned by SheetTruth to read formulas and propose fixes' },
  { kind: 'reviewer', name: REVIEWER_MODEL, role: 'Gives an independent second opinion on every finding' },
]

// Links shown in the footer. An empty string hides the link.
export const GITHUB_URL = 'https://github.com/Abhisek12378/sheettruth'
export const ADAPTER_URL = 'https://huggingface.co/Abhisek987/sheettruth-glimmer-30b-lora'

export const STATUS_ORDER: FindingStatus[] = ['confirmed', 'unverified', 'disputed', 'contradicted']

export const STATUS_TITLE: Record<FindingStatus, string> = {
  confirmed: 'Confirmed',
  unverified: 'Needs a look',
  disputed: 'Disputed',
  contradicted: 'Contradicted',
}

// Longer explanation shown above each group of findings.
export const STATUS_HELP: Record<FindingStatus, string> = {
  confirmed: 'A test on your workbook backs the fix, or the second opinion agrees. Treat these as real errors.',
  unverified: 'No test could settle this one and the second opinion was unsure. Read the cells and decide yourself.',
  disputed: 'No test applied, and the second opinion thinks the formula is written that way on purpose.',
  contradicted: 'A test on your workbook says the fix would be wrong. Most likely not an error.',
}

// One short line per status for the legend.
export const STATUS_LEGEND: Record<FindingStatus, string> = {
  confirmed: 'Tested or reviewed: a real error',
  unverified: 'Could not be tested: you decide',
  disputed: 'Reviewer thinks it is on purpose',
  contradicted: 'A test says the fix would be wrong',
}

// The six stages of the audit, in plain words.
export const HOW_IT_WORKS = [
  {
    title: 'Scan the layout',
    text: 'Simple rules look for numbers typed over formulas and formulas that break the pattern of their neighbours.',
  },
  {
    title: 'Read every formula',
    text: 'Identical formulas are grouped and read together with the cells they use and the labels around them.',
  },
  {
    title: 'Spot likely errors',
    text: `${MEANING_MODEL}, fine-tuned on spreadsheet mistakes, flags formulas that look wrong and proposes a corrected version.`,
  },
  {
    title: 'Test each fix',
    text: 'Code recalculates the fix and compares it with neighbouring formulas, other sheets and the labels.',
  },
  {
    title: 'Get a second opinion',
    text: `${REVIEWER_MODEL} judges every finding again as an independent reviewer, without seeing the first verdict.`,
  },
  {
    title: 'Report and repair',
    text: 'You get findings sorted by how sure we are, plus a corrected copy containing only the confirmed fixes.',
  },
]

export const TYPE_TITLE: Record<string, string> = {
  wrong_function: 'Wrong function',
  skipped_rows: 'Range stops short',
  extra_rows: 'Range reaches too far',
  double_count: 'Counted twice',
  wrong_sign: 'Wrong sign',
  wrong_reference: 'Wrong cell referenced',
  missing_term: 'Something left out',
  wrong_operator: 'Wrong operator',
  missing_factor: 'Missing multiplier',
}

export const CHECK_TITLE: Record<string, string> = {
  recalculated_fix: 'Recalculated the fix',
  value_change: 'Change in value',
  peer_pattern: 'Neighbouring formulas',
  sibling_sheets: 'Same cell on other sheets',
  range_delta: 'Cells added or dropped',
  double_count: 'Double counting',
  sign_convention: 'Plus or minus convention',
  value_plausibility: 'Is the new value plausible',
}

export const CHECK_RESULT_TITLE: Record<string, string> = {
  supports: 'Supports the fix',
  contradicts: 'Against the fix',
  neutral: 'No verdict',
  skipped: 'Not applicable',
}

export const REVIEW_TITLE: Record<string, string> = {
  real_error: 'Second opinion: a real error',
  not_error: 'Second opinion: not an error',
  cannot_tell: 'Second opinion: cannot tell',
}

export const STRICTNESS = [
  { label: 'Sensitive', threshold: 0.3, help: 'Flags more formulas, with more false alarms' },
  { label: 'Balanced', threshold: 0.5, help: 'A good middle ground for most workbooks' },
  { label: 'Strict', threshold: 0.7, help: 'Only the findings the model is surest about' },
]

export function strictnessLabel(threshold: number): string {
  const match = STRICTNESS.find((option) => Math.abs(option.threshold - threshold) < 0.001)
  return match ? match.label : `custom (${threshold})`
}

export function typeTitle(type: string | null): string {
  return type ? TYPE_TITLE[type] || type : 'Error'
}

export function percent(p: number): string {
  return `${Math.round(p * 100)}%`
}

export function formatTime(seconds: number): string {
  return new Date(seconds * 1000).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })
}

export function formatSeconds(total: number): string {
  const s = Math.max(0, Math.round(total))
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, '0')}s`
}

export function duration(job: { created_at: number; finished_at: number | null }): string {
  if (!job.finished_at) return ''
  return formatSeconds(job.finished_at - job.created_at)
}

export function formatKilobytes(bytes: number): string {
  return `${Math.max(1, Math.round(bytes / 1024))} KB`
}

export function plural(count: number, noun: string): string {
  return `${count} ${noun}${count === 1 ? '' : 's'}`
}
