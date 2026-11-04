// Human wording for the codes the API uses, and the fixed product copy.

import type { FindingStatus } from './api'

export const PRODUCT_NAME = 'SheetTruth'
export const TAGLINE =
  'Finds the formulas in a workbook that compute the wrong thing, then checks every finding against the workbook itself before reporting it.'

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

export const STATUS_HELP: Record<FindingStatus, string> = {
  confirmed: 'A code check on the workbook supports the fix, or the reviewer agrees it is a real error.',
  unverified: 'No code check applied and the reviewer could not tell. Read the window and decide.',
  disputed: 'No code check applied; the reviewer thinks the formula is intended as written.',
  contradicted: 'A code check on the workbook speaks against the fix. Most likely not an error.',
}

// One short line per status for the legend on the landing section.
export const STATUS_LEGEND: Record<FindingStatus, string> = {
  confirmed: 'Checks or the reviewer back the fix',
  unverified: 'Nothing could test it; read and decide',
  disputed: 'The reviewer thinks it is intended',
  contradicted: 'A code check speaks against it',
}

// The six stages of the audit, as shown in the "how it works" strip.
export const HOW_IT_WORKS = [
  {
    title: 'Structure checks',
    text: 'Rules scan the whole workbook for numbers typed over formulas and odd ones out.',
  },
  {
    title: 'Context windows',
    text: 'Each run of identical formulas becomes one window: the formula, its inputs, the labels around them.',
  },
  {
    title: 'Model verdicts',
    text: 'A fine-tuned model reads each window and proposes a corrected formula with a probability.',
  },
  {
    title: 'Code verification',
    text: 'An agent tests each finding: recalculation, neighbours, sibling sheets, double counts, signs.',
  },
  { title: 'Second opinion', text: 'An independent reviewer model judges every finding again.' },
  { title: 'Report', text: 'Four statuses, a readable report, and a corrected copy with the confirmed fixes only.' },
]

export const TYPE_TITLE: Record<string, string> = {
  wrong_function: 'Wrong function',
  skipped_rows: 'Range stops short',
  extra_rows: 'Range reaches too far',
  double_count: 'Counted twice',
  wrong_sign: 'Wrong sign',
  wrong_reference: 'Wrong reference',
  missing_term: 'Missing term',
  wrong_operator: 'Wrong operator',
  missing_factor: 'Missing factor',
}

export const CHECK_TITLE: Record<string, string> = {
  recalculated_fix: 'Recalculated fix',
  value_change: 'Value change',
  peer_pattern: 'Neighbouring formulas',
  sibling_sheets: 'Same cell on other sheets',
  range_delta: 'Cells added or dropped',
  double_count: 'Double count',
  sign_convention: 'Sign convention',
  value_plausibility: 'Value plausibility',
}

export const REVIEW_TITLE: Record<string, string> = {
  real_error: 'Reviewer: real error',
  not_error: 'Reviewer: not an error',
  cannot_tell: 'Reviewer: cannot tell',
}

export const STRICTNESS = [
  { label: 'Sensitive', threshold: 0.3, help: 'More findings, more false alarms' },
  { label: 'Balanced', threshold: 0.5, help: 'The default' },
  { label: 'Strict', threshold: 0.7, help: 'Only the model’s surest findings' },
]

export function typeTitle(type: string | null): string {
  return type ? TYPE_TITLE[type] || type : 'Error'
}

export function percent(p: number): string {
  return `${Math.round(p * 100)}%`
}

export function formatTime(seconds: number): string {
  return new Date(seconds * 1000).toLocaleString()
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
