import type { Check, Finding } from '../api'
import { CHECK_TITLE, REVIEW_TITLE } from '../labels'

// value_plausibility is reported as a hint: it never decides the outcome of a finding.
const HINT_CHECKS = new Set(['value_plausibility'])

function isDecisive(check: Check): boolean {
  return (check.result === 'supports' || check.result === 'contradicts') && !HINT_CHECKS.has(check.name)
}

function CheckRow({ check }: { check: Check }) {
  const hint = HINT_CHECKS.has(check.name) && check.result !== 'skipped'
  return (
    <li className={`check ${hint ? 'hint' : check.result}`}>
      <span className="result">{hint ? `hint: ${check.result}` : check.result}</span>
      <span className="name">{CHECK_TITLE[check.name] || check.name}</span>
      <span className="detail">{check.detail}</span>
    </li>
  )
}

export function FindingDetail({ finding }: { finding: Finding }) {
  const decisive = finding.verification.checks.filter(isDecisive)
  const others = finding.verification.checks.filter((c) => !isDecisive(c))
  return (
    <div className="finding-detail">
      <section>
        <h4>Model's reason</h4>
        <p>{finding.reason || 'No reason given.'}</p>
        {finding.run_cells.length > 1 && (
          <p className="muted small">
            Same formula pattern in {finding.run_cells.length} cells: {finding.run_cells.join(', ')}
          </p>
        )}
      </section>

      <section>
        <h4>Code checks on the workbook</h4>
        {decisive.length === 0 && <p className="muted">No check could test this finding on its own.</p>}
        <ul className="checks">
          {decisive.map((c) => (
            <CheckRow key={c.name} check={c} />
          ))}
        </ul>
        {others.length > 0 && (
          <details>
            <summary className="muted small">{others.length} other checks</summary>
            <ul className="checks">
              {others.map((c) => (
                <CheckRow key={c.name} check={c} />
              ))}
            </ul>
          </details>
        )}
      </section>

      {finding.review && (
        <section>
          <h4>{REVIEW_TITLE[finding.review.verdict] || finding.review.verdict}</h4>
          <p>{finding.review.reason}</p>
        </section>
      )}

      <section>
        <h4>What the model saw</h4>
        <pre className="window">{finding.window}</pre>
      </section>
    </div>
  )
}
