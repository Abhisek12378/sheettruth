import type { Job } from '../api'

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

function stepState(job: Job, index: number): 'done' | 'active' | 'pending' | 'skipped' {
  const finished = new Set(job.steps.map((s) => s.node))
  const node = PIPELINE[index].node
  if (finished.has(node)) return 'done'
  if (job.status === 'done') return 'skipped'
  const nextIndex = PIPELINE.findIndex((p) => !finished.has(p.node))
  return index === nextIndex && job.status === 'running' ? 'active' : 'pending'
}

export function Progress({ job }: { job: Job }) {
  return (
    <div className="card progress">
      <h2>
        {job.status === 'queued' ? 'Waiting for the worker' : job.status === 'running' ? 'Auditing' : 'Audit steps'}
        <span className="muted"> · {job.filename}</span>
      </h2>
      <ol>
        {PIPELINE.map((step, index) => {
          const state = stepState(job, index)
          const note = job.steps.find((s) => s.node === step.node)?.note
          return (
            <li key={step.node} className={state}>
              <span className="dot" />
              <span className="label">{step.label}</span>
              {note && <span className="note">{note}</span>}
            </li>
          )
        })}
      </ol>
      {job.status === 'failed' && <p className="error">Failed: {job.error}</p>}
    </div>
  )
}
