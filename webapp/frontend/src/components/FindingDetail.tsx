import type { Check, Finding } from '../api'
import { checkMark, isHint, orderedChecks } from '../findings'
import { CHECK_RESULT_TITLE, CHECK_TITLE, REVIEW_TITLE } from '../labels'
import { MarkIcon } from './MarkIcon'

function CheckRow({ check }: { check: Check }) {
  const hint = isHint(check) && check.result !== 'skipped'
  const mark = hint ? 'neutral' : checkMark(check)
  return (
    <li className={`check check-${mark}`}>
      <span className="check-result">
        <MarkIcon mark={mark} />
        {hint ? `Hint: ${CHECK_RESULT_TITLE[check.result]}` : CHECK_RESULT_TITLE[check.result]}
      </span>
      <span className="check-name">{CHECK_TITLE[check.name] || check.name}</span>
      <span className="check-detail">{check.detail}</span>
    </li>
  )
}

function ReviewSection({ finding }: { finding: Finding }) {
  if (!finding.review) {
    return (
      <section>
        <h4>Reviewer model</h4>
        <p className="muted">No second opinion was available for this audit.</p>
      </section>
    )
  }
  return (
    <section>
      <h4>{REVIEW_TITLE[finding.review.verdict] || finding.review.verdict}</h4>
      <p>{finding.review.reason}</p>
    </section>
  )
}

export function FindingDetail({ finding, id }: { finding: Finding; id: string }) {
  const checks = orderedChecks(finding)
  return (
    <div className="finding-detail" id={id}>
      <div className="finding-detail-grid">
        <section>
          <h4>Model’s reason</h4>
          <p>{finding.reason || 'No reason given.'}</p>
          {finding.run_cells.length > 1 && (
            <p className="muted small">
              Same formula pattern in {finding.run_cells.length} cells: <code>{finding.run_cells.join(', ')}</code>
            </p>
          )}
        </section>
        <ReviewSection finding={finding} />
      </div>

      <section>
        <h4>Code checks on the workbook</h4>
        {checks.length === 0 ? (
          <p className="muted">No check could test this finding.</p>
        ) : (
          <ul className="checks">
            {checks.map((c) => (
              <CheckRow key={c.name} check={c} />
            ))}
          </ul>
        )}
      </section>

      <section>
        <h4>What the model saw</h4>
        <pre className="window" tabIndex={0}>
          {finding.window}
        </pre>
      </section>
    </div>
  )
}
