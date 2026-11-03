// Types and calls for the audit API served by app/server.py.

export type JobStatus = 'queued' | 'running' | 'done' | 'failed'
export type FindingStatus = 'confirmed' | 'unverified' | 'disputed' | 'contradicted'

export interface Step {
  node: string
  label: string
  note: string
  at: number
}

export interface Summary {
  formula_cells: number
  windows: number
  out_of_scope: number
  flagged: number
  by_status: Record<FindingStatus, number>
  structure_findings: number
}

export interface Job {
  id: string
  filename: string
  threshold: number
  created_at: number
  status: JobStatus
  steps: Step[]
  error: string
  summary: Partial<Summary>
  finished_at: number | null
}

export interface Check {
  name: string
  result: 'supports' | 'contradicts' | 'neutral' | 'skipped'
  detail: string
}

export interface Verification {
  outcome: 'passed' | 'failed' | 'no_independent_check'
  checks: Check[]
  old_value?: unknown
  new_value?: unknown
}

export interface Review {
  verdict: 'real_error' | 'not_error' | 'cannot_tell'
  reason: string
}

export interface Finding {
  sheet: string
  addr: string
  run_cells: string[]
  formula: string
  window: string
  type: string | null
  expected: string | null
  reason: string
  p_error: number
  verification: Verification
  review?: Review
  status: FindingStatus
}

export interface StructureFinding {
  sheet: string
  addr: string
  kind: string
  current: string
  implied_formula: string
  detail: string
}

export interface AuditResult {
  workbook: string
  threshold: number
  findings: Finding[]
  structure: StructureFinding[]
  notes: string[]
}

export interface JobDetail extends Job {
  result: AuditResult | null
}

export interface Health {
  model: string
  recalculation: boolean
  reviewer: boolean
  queued: number
}

async function expectOk<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || `${response.status} ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

export function fetchHealth(): Promise<Health> {
  return fetch('/api/health').then((r) => expectOk<Health>(r))
}

export function fetchJobs(): Promise<Job[]> {
  return fetch('/api/audits').then((r) => expectOk<Job[]>(r))
}

export function fetchJob(id: string): Promise<JobDetail> {
  return fetch(`/api/audits/${id}`).then((r) => expectOk<JobDetail>(r))
}

export function createJob(file: File, threshold: number): Promise<Job> {
  const form = new FormData()
  form.append('file', file)
  form.append('threshold', String(threshold))
  return fetch('/api/audits', { method: 'POST', body: form }).then((r) => expectOk<Job>(r))
}

export function downloadUrl(id: string, name: 'report.md' | 'report.json' | 'corrected.xlsx'): string {
  return `/api/audits/${id}/${name}`
}
