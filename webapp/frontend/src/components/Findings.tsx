import { useState } from 'react'
import type { Finding, FindingStatus } from '../api'
import { findingKey } from '../findings'
import { STATUS_HELP, STATUS_ORDER, STATUS_TITLE } from '../labels'
import { FindingRow } from './FindingRow'
import { StatusIcon } from './StatusIcon'

function StatusGroup({ status, findings }: { status: FindingStatus; findings: Finding[] }) {
  const [openKey, setOpenKey] = useState<string | null>(null)
  if (findings.length === 0) return null
  return (
    <section className={`group ${status}`} aria-labelledby={`group-${status}`}>
      <div className="group-head">
        <h3 id={`group-${status}`}>
          <StatusIcon status={status} />
          {STATUS_TITLE[status]}
          <span className="count">{findings.length}</span>
        </h3>
        <p className="muted small">{STATUS_HELP[status]}</p>
      </div>
      <ul className="findings">
        {findings.map((f) => (
          <FindingRow
            key={findingKey(f)}
            finding={f}
            detailId={`detail-${status}-${findingKey(f)}`}
            open={openKey === findingKey(f)}
            onToggle={() => setOpenKey(openKey === findingKey(f) ? null : findingKey(f))}
          />
        ))}
      </ul>
    </section>
  )
}

export function Findings({ findings }: { findings: Finding[] }) {
  return (
    <div className="card findings-card">
      <div className="card-head">
        <h2>Formula findings</h2>
        <p className="muted small">
          {findings.length === 0
            ? 'No formula looked wrong at this strictness. Try the Sensitive setting to look harder.'
            : 'Each row is one formula, or one group of cells sharing it. Open a row to see why it was flagged, the tests that were run, the second opinion and the exact cells the model read.'}
        </p>
      </div>
      {STATUS_ORDER.map((status) => (
        <StatusGroup key={status} status={status} findings={findings.filter((f) => f.status === status)} />
      ))}
    </div>
  )
}
