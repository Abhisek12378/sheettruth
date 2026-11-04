import type { Job, Step } from '../api'
import { useElapsed } from '../hooks/useElapsed'
import { COLD_START_NOTE, formatSeconds } from '../labels'
import { MarkIcon } from './MarkIcon'

// The audit pipeline in the order the server runs it.
const PIPELINE = [
  { node: 'load_workbook', label: 'Opening the workbook' },
  { node: 'structure_checks', label: 'Structure checks' },
  { node: 'build_windows', label: 'Building context windows' },
  { node: 'score_windows', label: 'Model verdicts' },
  { node: 'select_findings', label: 'Selecting findings' },
  { node: 'verify_findings', label: 'Verify agent' },
  { node: 'second_opinion', label: 'Second opinion' },
  { node: 'write_report', label: 'Writing the report' },
]

// The step whose first run after idle waits for the model server to start.
const COLD_START_NODE = 'score_windows'

type StepState = 'done' | 'active' | 'pending' | 'failed'

function activeIndex(job: Job): number {
  const finished = new Set(job.steps.map((s) => s.node))
  return PIPELINE.findIndex((p) => !finished.has(p.node))
}

function stepState(job: Job, index: number, active: number): StepState {
  if (active === -1 || index < active) return 'done'
  if (index > active) return 'pending'
  if (job.status === 'failed') return 'failed'
  return job.status === 'running' ? 'active' : 'pending'
}

// Seconds a finished step took, measured from the previous step or the job start.
function stepSeconds(job: Job, step: Step | undefined, index: number): number | null {
  if (!step) return null
  const previous = index === 0 ? job.created_at : job.steps[index - 1]?.at
  return previous ? step.at - previous : null
}

// Adds a full stop to a server message that has none, so it reads as a sentence.
function sentence(text: string): string {
  const trimmed = text.trim()
  return /[.!?]$/.test(trimmed) ? trimmed : `${trimmed}.`
}

function title(job: Job): string {
  if (job.status === 'queued') return 'Waiting for the worker'
  if (job.status === 'failed') return 'The audit failed'
  return 'Auditing'
}

function StepMarker({ state }: { state: StepState }) {
  if (state === 'done') return <MarkIcon mark="pass" />
  if (state === 'failed') return <MarkIcon mark="fail" />
  return <span className="step-dot" aria-hidden="true" />
}

function StepRow({ job, index, active }: { job: Job; index: number; active: number }) {
  const step = PIPELINE[index]
  const state = stepState(job, index, active)
  const record = job.steps.find((s) => s.node === step.node)
  const seconds = stepSeconds(job, record, index)
  return (
    <li className={`step ${state}`} aria-current={state === 'active' ? 'step' : undefined}>
      <span className="step-marker">
        <StepMarker state={state} />
      </span>
      <span className="step-label">
        {step.label}
        <span className="visually-hidden">{`, ${state}`}</span>
      </span>
      <span className="step-note">{record?.note}</span>
      <span className="step-time">{seconds !== null && formatSeconds(seconds)}</span>
    </li>
  )
}

export function Progress({ job }: { job: Job }) {
  const running = job.status === 'queued' || job.status === 'running'
  const elapsed = useElapsed(job.created_at, running)
  const shown = job.finished_at ? job.finished_at - job.created_at : elapsed
  const active = activeIndex(job)
  const coldStart = running && PIPELINE[active]?.node === COLD_START_NODE
  return (
    <section className="card progress" aria-labelledby="progress-title">
      <div className="progress-head">
        <div>
          <h2 id="progress-title">
            {title(job)} <span className="progress-file">{job.filename}</span>
          </h2>
          <p className="muted small">
            {job.status === 'queued' ? 'Another audit is running; yours starts as soon as the worker is free.' : ''}
            {job.status === 'running' ? 'Each step reports when it finishes.' : ''}
          </p>
        </div>
        <span className="elapsed" title={job.finished_at ? 'How long the audit ran' : 'Time since the upload'}>
          {formatSeconds(shown)}
        </span>
      </div>

      <ol className="steps" aria-live="polite">
        {PIPELINE.map((step, index) => (
          <StepRow key={step.node} job={job} index={index} active={active} />
        ))}
      </ol>

      {coldStart && <p className="notice">{COLD_START_NOTE}</p>}

      {job.status === 'failed' && (
        <div className="error" role="alert">
          <strong>The audit stopped.</strong> {sentence(job.error || 'The server gave no reason')} Check that the file
          is an ordinary Excel workbook and try again.
        </div>
      )}
    </section>
  )
}
