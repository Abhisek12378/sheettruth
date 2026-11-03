// Human wording for the codes the API uses.

import type { FindingStatus } from './api'

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

export function duration(job: { created_at: number; finished_at: number | null }): string {
  if (!job.finished_at) return ''
  const s = Math.round(job.finished_at - job.created_at)
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${s % 60}s`
}
