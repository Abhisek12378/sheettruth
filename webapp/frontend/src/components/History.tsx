import type { Job } from '../api'
import { formatTime } from '../labels'

interface Props {
  jobs: Job[]
  selected: string | null
  onSelect: (id: string) => void
}

function statusText(job: Job): string {
  if (job.status === 'done') {
    const s = job.summary.by_status
    return s ? `${s.confirmed} confirmed · ${s.unverified} to look at` : 'done'
  }
  return job.status
}

export function History({ jobs, selected, onSelect }: Props) {
  return (
    <aside className="history">
      <h2>Audits</h2>
      {jobs.length === 0 && <p className="muted small">Nothing audited yet.</p>}
      <ul>
        {jobs.map((job) => (
          <li key={job.id} className={job.id === selected ? 'selected' : ''}>
            <button type="button" onClick={() => onSelect(job.id)}>
              <span className="name">{job.filename}</span>
              <span className={`state ${job.status}`}>{statusText(job)}</span>
              <span className="when">{formatTime(job.created_at)}</span>
            </button>
          </li>
        ))}
      </ul>
    </aside>
  )
}
