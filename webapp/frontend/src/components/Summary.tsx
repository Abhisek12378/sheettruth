import { downloadUrl, type Job, type Summary as SummaryData } from '../api'
import { STATUS_ORDER, STATUS_TITLE, duration } from '../labels'
import { StatusIcon } from './StatusIcon'

interface Props {
  job: Job
  summary: SummaryData
}

export function Summary({ job, summary }: Props) {
  const counts = summary.by_status
  return (
    <div className="card summary">
      <div className="summary-head">
        <div>
          <h2>{job.filename}</h2>
          <p className="muted small">
            {summary.formula_cells} formula cells in {summary.windows} windows
            {summary.out_of_scope > 0 && ` · ${summary.out_of_scope} out of scope`} · flagged at P(error) ≥{' '}
            {job.threshold} · finished in {duration(job)}
          </p>
        </div>
        <nav className="downloads" aria-label="Downloads">
          <a href={downloadUrl(job.id, 'corrected.xlsx')} download>
            Corrected workbook
          </a>
          <a href={downloadUrl(job.id, 'report.md')} download>
            Report (Markdown)
          </a>
          <a href={downloadUrl(job.id, 'report.json')} download>
            Full detail (JSON)
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
            Structure findings
          </span>
        </div>
      </div>
      <p className="muted small">
        The corrected workbook contains the confirmed fixes only, written into every cell of each affected run.
      </p>
    </div>
  )
}
