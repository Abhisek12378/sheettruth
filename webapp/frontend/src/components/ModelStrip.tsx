import { MODELS, MODEL_MAKER } from '../labels'

function ModelIcon({ kind }: { kind: 'meaning' | 'reviewer' }) {
  const path =
    kind === 'meaning'
      ? 'M4 5h16v14H4V5Zm0 4.7h16M4 14.3h16M9.3 5v14M14.7 5v14'
      : 'M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9L12 3Z'
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">
      <path d={path} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  )
}

// Credits the two models behind an audit, next to the upload card.
export function ModelStrip() {
  return (
    <section className="models" aria-label={`Models from ${MODEL_MAKER}`}>
      <p className="models-lead">
        Built on two <strong>{MODEL_MAKER}</strong> models
      </p>
      <ul>
        {MODELS.map((model) => (
          <li key={model.name}>
            <span className="models-icon">
              <ModelIcon kind={model.kind} />
            </span>
            <span className="models-text">
              <span className="models-name">{model.name}</span>
              <span className="models-role">{model.role}</span>
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}
