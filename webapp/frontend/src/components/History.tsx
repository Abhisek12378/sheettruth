import { useState } from 'react'
import type { Job } from '../api'
import type { Mark } from '../findings'
import { formatTime } from '../labels'
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

function stateText(job: Job): string {
  if (job.status === 'done') {
    const s = job.summary.by_status
    return s ? `${s.confirmed} confirmed · ${s.unverified} to look at` : 'done'
  }
  return job.status
}

function HistoryItem({ job, selected, onSelect }: { job: Job; selected: boolean; onSelect: (id: string) => void }) {
  return (
    <li className={selected ? 'selected' : ''}>
      <button type="button" onClick={() => onSelect(job.id)} aria-current={selected ? 'true' : undefined}>
        <span className="name">{job.filename}</span>
        <span className={`state ${job.status}`}>
          <MarkIcon mark={STATE_MARK[job.status]} />
          {stateText(job)}
        </span>
        <span className="when">{formatTime(job.created_at)}</span>
      </button>
    </li>
  )
}

function DrawerIcon({ open }: { open: boolean }) {
  return (
    <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false">
      <path
        d={open ? 'M8 14l4-4 4 4' : 'M8 10l4 4 4-4'}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

// Earlier audits. A side bar on wide screens; a drawer under the top bar on narrow ones.
export function History({ jobs, selected, onSelect }: Props) {
  const [open, setOpen] = useState(false)

  function choose(id: string) {
    onSelect(id)
    setOpen(false)
  }

  return (
    <aside className={`history${open ? ' open' : ''}`} aria-label="Earlier audits">
      <h2 className="history-title">Audits</h2>
      <button
        type="button"
        className="history-toggle"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="history-list"
      >
        <span>Audits</span>
        <span className="history-count">{jobs.length}</span>
        <DrawerIcon open={open} />
      </button>
      <div className="history-list" id="history-list">
        {jobs.length === 0 && <p className="muted small">Nothing audited yet.</p>}
        <ul>
          {jobs.map((job) => (
            <HistoryItem key={job.id} job={job} selected={job.id === selected} onSelect={choose} />
          ))}
        </ul>
      </div>
    </aside>
  )
}
