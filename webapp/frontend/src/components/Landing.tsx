import { HOW_IT_WORKS, STATUS_LEGEND, STATUS_ORDER, STATUS_TITLE, TAGLINE } from '../labels'
import { StatusIcon } from './StatusIcon'

export function Landing() {
  return (
    <section className="landing" aria-labelledby="landing-title">
      <div className="landing-copy">
        <h2 id="landing-title">Find the formulas that compute the wrong thing.</h2>
        <p>{TAGLINE}</p>
      </div>

      <ol className="how" aria-label="How it works">
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

      <ul className="legend" aria-label="What the statuses mean">
        {STATUS_ORDER.map((status) => (
          <li key={status} className={status}>
            <StatusIcon status={status} />
            <span className="legend-title">{STATUS_TITLE[status]}</span>
            <span className="legend-text">{STATUS_LEGEND[status]}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}
