// Derived facts about a finding that the list and the detail panel both show.

import type { Check, Finding } from './api'

export type Mark = 'pass' | 'fail' | 'neutral' | 'skipped' | 'unknown'

// value_plausibility is reported as a hint: it never decides the outcome of a finding.
const HINT_CHECKS = new Set(['value_plausibility'])

export function isHint(check: Check): boolean {
  return HINT_CHECKS.has(check.name)
}

export function isDecisive(check: Check): boolean {
  return (check.result === 'supports' || check.result === 'contradicts') && !isHint(check)
}

const CHECK_MARK: Record<Check['result'], Mark> = {
  supports: 'pass',
  contradicts: 'fail',
  neutral: 'neutral',
  skipped: 'skipped',
}

export function checkMark(check: Check): Mark {
  return CHECK_MARK[check.result]
}

// Decisive checks first, then the rest in the order the verify agent ran them.
export function orderedChecks(finding: Finding): Check[] {
  const checks = finding.verification.checks
  return [...checks.filter(isDecisive), ...checks.filter((c) => !isDecisive(c))]
}

export interface Agreement {
  mark: Mark
  label: string
}

// One-line summary of what the code checks concluded.
export function codeAgreement(finding: Finding): Agreement {
  const decisive = finding.verification.checks.filter(isDecisive)
  const supports = decisive.filter((c) => c.result === 'supports').length
  const contradicts = decisive.length - supports
  if (contradicts > 0)
    return {
      mark: 'fail',
      label: contradicts === 1 ? '1 test against the fix' : `${contradicts} tests against the fix`,
    }
  if (supports > 0)
    return { mark: 'pass', label: supports === 1 ? '1 test backs the fix' : `${supports} tests back the fix` }
  return { mark: 'skipped', label: 'Could not be tested' }
}

const REVIEW_AGREEMENT: Record<string, Agreement> = {
  real_error: { mark: 'pass', label: 'Second opinion agrees' },
  not_error: { mark: 'fail', label: 'Second opinion disagrees' },
  cannot_tell: { mark: 'unknown', label: 'Second opinion unsure' },
}

export function reviewAgreement(finding: Finding): Agreement {
  if (!finding.review) return { mark: 'skipped', label: 'No second opinion' }
  return REVIEW_AGREEMENT[finding.review.verdict] || { mark: 'unknown', label: finding.review.verdict }
}

export function findingKey(finding: Finding): string {
  return `${finding.sheet}!${finding.addr}`
}
