import type { Health } from '../api'

interface ChipProps {
  on: boolean
  label: string
  title: string
}

function Chip({ on, label, title }: ChipProps) {
  return (
    <span className={`chip ${on ? 'on' : 'off'}`} title={title}>
      <span className="chip-dot" aria-hidden="true" />
      {label}
    </span>
  )
}

function queueLabel(queued: number): string {
  if (queued === 0) return 'Queue empty'
  return queued === 1 ? '1 audit queued' : `${queued} audits queued`
}

export function HealthBar({ health }: { health: Health | null }) {
  if (!health) {
    return (
      <div className="health" aria-label="Server status">
        <Chip on={false} label="Server unreachable" title="The audit server did not answer" />
      </div>
    )
  }
  return (
    <div className="health" aria-label="Server status">
      <Chip on label={health.model} title="The fine-tuned model that reads each window" />
      <Chip
        on={health.recalculation}
        label={health.recalculation ? 'Recalculation on' : 'No recalculation'}
        title="Whether corrected formulas are recalculated with a spreadsheet engine"
      />
      <Chip
        on={health.reviewer}
        label={health.reviewer ? 'Reviewer model on' : 'No reviewer'}
        title="Whether a second, independent model reviews each finding"
      />
      <Chip on={health.queued === 0} label={queueLabel(health.queued)} title="Audits waiting for the worker" />
    </div>
  )
}
