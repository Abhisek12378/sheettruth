import { downloadUrl, type Job, type Summary as SummaryData } from '../api'
import { STATUS_ORDER, STATUS_TITLE, duration, plural, strictnessLabel } from '../labels'
import { StatusIcon } from './StatusIcon'

interface Props {
  job: Job
  summary: SummaryData
}

function DownloadIcon() {
  return (
    <svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true" focusable="false">
      <path
        d="M12 4v11m-4-4 4 4 4-4M5 20h14"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function headline(summary: SummaryData): string {
  const errors = summary.by_status.confirmed
  if (errors === 0) return 'No confirmed errors'
  return `${plural(errors, 'confirmed error')} found`
}

function statsLine(job: Job, summary: SummaryData): string {
  const parts = [
    `${plural(summary.formula_cells, 'formula')} checked in ${plural(summary.windows, 'group')}`,
    `${strictnessLabel(job.threshold)} strictness`,
    `took ${duration(job)}`,
  ]
  if (summary.out_of_scope > 0) parts.splice(1, 0, `${plural(summary.out_of_scope, 'cell')} skipped`)
  return parts.join(' · ')
}

export function Summary({ job, summary }: Props) {
  const counts = summary.by_status
  return (
    <section className="card summary" aria-labelledby="summary-title">
      <div className="summary-head">
        <div>
          <p className="eyebrow">Audit of {job.filename}</p>
          <h2 id="summary-title">{headline(summary)}</h2>
          <p className="muted">{statsLine(job, summary)}</p>
        </div>
        <nav className="downloads" aria-label="Downloads">
          <a href={downloadUrl(job.id, 'corrected.xlsx')} download className="download-primary">
            <DownloadIcon />
            Corrected workbook
          </a>
          <a href={downloadUrl(job.id, 'report.md')} download>
            <DownloadIcon />
            Report
          </a>
          <a href={downloadUrl(job.id, 'report.json')} download>
            <DownloadIcon />
            Full data
          </a>
        </nav>
      </div>
      <div className="tiles">
        {STATUS_ORDER.map((status) => (
          <div key={status} className={`tile ${status}`}>
            <span className="count">{counts[status]}</span>
            <span className="name">
              <StatusIcon status={status} />
              {STATUS_TITLE[status]}
            </span>
          </div>
        ))}
        <div className="tile structure">
          <span className="count">{summary.structure_findings}</span>
          <span className="name">
            <StatusIcon status="structure" />
            Layout problems
          </span>
        </div>
      </div>
      <p className="muted small">
        The corrected workbook contains only the confirmed fixes, applied to every cell that shares the same formula.
      </p>
    </section>
  )
}
