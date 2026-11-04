import { HOW_IT_WORKS, STATUS_LEGEND, STATUS_ORDER, STATUS_TITLE } from '../labels'
import { StatusIcon } from './StatusIcon'

export function HowItWorks() {
  return (
    <section className="explain" aria-labelledby="how-title">
      <div className="section-head">
        <h2 id="how-title">How an audit works</h2>
        <p className="muted">
          Six steps, from the first scan to the corrected copy. Most audits take one to three minutes.
        </p>
      </div>

      <ol className="how">
        {HOW_IT_WORKS.map((step, index) => (
          <li key={step.title}>
            <span className="how-number" aria-hidden="true">
              {index + 1}
            </span>
            <span className="how-title">{step.title}</span>
            <span className="how-text">{step.text}</span>
          </li>
        ))}
      </ol>

      <div className="section-head">
        <h3 id="legend-title">What the four results mean</h3>
      </div>
      <ul className="legend" aria-labelledby="legend-title">
        {STATUS_ORDER.map((status) => (
          <li key={status} className={status}>
            <StatusIcon status={status} />
            <span>
              <span className="legend-title">{STATUS_TITLE[status]}</span>
              <span className="legend-text">{STATUS_LEGEND[status]}</span>
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}
