import type { Check, Finding } from '../api'
import { checkMark, isHint, orderedChecks } from '../findings'
import { CHECK_RESULT_TITLE, CHECK_TITLE, MEANING_MODEL, REVIEWER_MODEL, REVIEW_TITLE } from '../labels'
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
        <h4>Second opinion</h4>
        <p className="muted">No reviewer model was available for this audit.</p>
      </section>
    )
  }
  return (
    <section>
      <h4>
        {REVIEW_TITLE[finding.review.verdict] || finding.review.verdict}
        <span className="by-model">{REVIEWER_MODEL}</span>
      </h4>
      <p>{finding.review.reason}</p>
    </section>
  )
}

export function FindingDetail({ finding, id }: { finding: Finding; id: string }) {
  const checks = orderedChecks(finding)
  return (
    <div className="finding-detail" id={id}>
      <section>
        <h4>Current formula and proposed fix</h4>
        <p className="formula-pair">
          <code className="before">{finding.formula}</code>
          {finding.expected && (
            <>
              <span className="arrow" aria-label="becomes">
                →
              </span>
              <code className="after">{finding.expected}</code>
            </>
          )}
        </p>
      </section>

      <div className="finding-detail-grid">
        <section>
          <h4>
            Why it was flagged
            <span className="by-model">{MEANING_MODEL}</span>
          </h4>
          <p>{finding.reason || 'No reason given.'}</p>
          {finding.run_cells.length > 1 && (
            <p className="muted small">
              The same formula appears in {finding.run_cells.length} cells: <code>{finding.run_cells.join(', ')}</code>
            </p>
          )}
        </section>
        <ReviewSection finding={finding} />
      </div>

      <section>
        <h4>Tests on your workbook</h4>
        {checks.length === 0 ? (
          <p className="muted">No test could be applied to this finding.</p>
        ) : (
          <ul className="checks">
            {checks.map((c) => (
              <CheckRow key={c.name} check={c} />
            ))}
          </ul>
        )}
      </section>

      <section>
        <h4>The exact cells the model read</h4>
        <pre className="window" tabIndex={0}>
          {finding.window}
        </pre>
      </section>
    </div>
  )
}
