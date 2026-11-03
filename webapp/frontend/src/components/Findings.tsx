import { useState } from 'react'
import type { Finding, FindingStatus } from '../api'
import { STATUS_HELP, STATUS_ORDER, STATUS_TITLE, percent, typeTitle } from '../labels'
import { FindingDetail } from './FindingDetail'

function findingKey(f: Finding): string {
  return `${f.sheet}!${f.addr}`
}

function FindingRow({ finding, open, onToggle }: { finding: Finding; open: boolean; onToggle: () => void }) {
  return (
    <li className={`finding${open ? ' open' : ''}`}>
      <button type="button" className="finding-head" onClick={onToggle}>
        <span className="cell">
          {finding.sheet}!{finding.addr}
          {finding.run_cells.length > 1 && <small> +{finding.run_cells.length - 1}</small>}
        </span>
        <span className="type">{typeTitle(finding.type)}</span>
        <span className="formulas">
          <code>{finding.formula}</code>
          {finding.expected && (
            <>
              <span className="arrow">→</span>
              <code>{finding.expected}</code>
            </>
          )}
        </span>
        <span className="prob" title="Model's error probability">
          {percent(finding.p_error)}
        </span>
      </button>
      {open && <FindingDetail finding={finding} />}
    </li>
  )
}

function StatusGroup({ status, findings }: { status: FindingStatus; findings: Finding[] }) {
  const [openKey, setOpenKey] = useState<string | null>(null)
  if (findings.length === 0) return null
  return (
    <section className={`group ${status}`}>
      <h3>
        {STATUS_TITLE[status]} <span className="count">{findings.length}</span>
      </h3>
      <p className="muted small">{STATUS_HELP[status]}</p>
      <ul className="findings">
        {findings.map((f) => (
          <FindingRow
            key={findingKey(f)}
            finding={f}
            open={openKey === findingKey(f)}
            onToggle={() => setOpenKey(openKey === findingKey(f) ? null : findingKey(f))}
          />
        ))}
      </ul>
    </section>
  )
}

export function Findings({ findings }: { findings: Finding[] }) {
  if (findings.length === 0) {
    return (
      <div className="card">
        <h2>Model findings</h2>
        <p className="muted">No formula was flagged at this strictness.</p>
      </div>
    )
  }
  return (
    <div className="card">
      <h2>Model findings</h2>
      {STATUS_ORDER.map((status) => (
        <StatusGroup key={status} status={status} findings={findings.filter((f) => f.status === status)} />
      ))}
    </div>
  )
}
