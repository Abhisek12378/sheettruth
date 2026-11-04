import type { Finding } from '../api'
import { codeAgreement, reviewAgreement, type Agreement } from '../findings'
import { percent, typeTitle } from '../labels'
import { FindingDetail } from './FindingDetail'
import { MarkIcon } from './MarkIcon'

interface Props {
  finding: Finding
  detailId: string
  open: boolean
  onToggle: () => void
}

function AgreementChip({ agreement }: { agreement: Agreement }) {
  return (
    <span className={`agree agree-${agreement.mark}`}>
      <MarkIcon mark={agreement.mark} />
      {agreement.label}
    </span>
  )
}

function Chevron() {
  return (
    <svg className="chevron" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false">
      <path
        d="M8 10l4 4 4-4"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function FindingRow({ finding, detailId, open, onToggle }: Props) {
  const extra = finding.run_cells.length - 1
  return (
    <li className={`finding${open ? ' open' : ''}`}>
      <button type="button" className="finding-head" onClick={onToggle} aria-expanded={open} aria-controls={detailId}>
        <span className="cell">
          <span className="cell-addr">
            {finding.sheet}!{finding.addr}
          </span>
          {extra > 0 && (
            <span className="run-count" title={`Same formula in ${extra + 1} cells`}>
              +{extra}
            </span>
          )}
        </span>
        <span className="type">{typeTitle(finding.type)}</span>
        <span className="formulas">
          <code className="before">{finding.formula}</code>
          {finding.expected && (
            <>
              <span className="arrow" aria-label="becomes">
                →
              </span>
              <code className="after">{finding.expected}</code>
            </>
          )}
        </span>
        <span className="prob" title="The model's error probability">
          <span className="prob-bar" aria-hidden="true">
            <span style={{ width: percent(finding.p_error) }} />
          </span>
          <span className="prob-text">{percent(finding.p_error)}</span>
        </span>
        <span className="agreement">
          <AgreementChip agreement={codeAgreement(finding)} />
          <AgreementChip agreement={reviewAgreement(finding)} />
        </span>
        <Chevron />
      </button>
      {open && <FindingDetail finding={finding} id={detailId} />}
    </li>
  )
}
