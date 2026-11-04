import type { Job } from '../api'
import type { Mark } from '../findings'
import { formatTime, plural, strictnessLabel } from '../labels'
import { MarkIcon } from './MarkIcon'

interface Props {
  jobs: Job[]
  selected: string | null
  onSelect: (id: string) => void
}

const STATE_MARK: Record<Job['status'], Mark> = {
  done: 'pass',
  failed: 'fail',
  running: 'neutral',
  queued: 'skipped',
}

const STATE_TEXT: Record<Job['status'], string> = {
  done: 'Finished',
  failed: 'Failed',
  running: 'Running',
  queued: 'Waiting',
}

function resultText(job: Job): string {
  const s = job.summary.by_status
  if (job.status !== 'done' || !s) return STATE_TEXT[job.status]
  const confirmed = plural(s.confirmed, 'confirmed error')
  return s.unverified > 0 ? `${confirmed} · ${s.unverified} to look at` : confirmed
}

function HistoryItem({ job, selected, onSelect }: { job: Job; selected: boolean; onSelect: (id: string) => void }) {
  return (
    <li className={selected ? 'selected' : ''}>
      <button type="button" onClick={() => onSelect(job.id)} aria-current={selected ? 'true' : undefined}>
        <span className="name">{job.filename}</span>
        <span className={`state ${job.status}`}>
          <MarkIcon mark={STATE_MARK[job.status]} />
          {resultText(job)}
        </span>
        <span className="when">
          {formatTime(job.created_at)} · {strictnessLabel(job.threshold)}
        </span>
      </button>
    </li>
  )
}

// The list of earlier audits shown inside the drawer.
export function History({ jobs, selected, onSelect }: Props) {
  if (jobs.length === 0) {
    return <p className="muted history-empty">Nothing has been audited yet. Your audits will be listed here.</p>
  }
  return (
    <ul className="history-list">
      {jobs.map((job) => (
        <HistoryItem key={job.id} job={job} selected={job.id === selected} onSelect={onSelect} />
      ))}
    </ul>
  )
}
