export function EmptyState({ hasHistory }: { hasHistory: boolean }) {
  return (
    <section className="card empty" aria-label="No audit open">
      <svg viewBox="0 0 64 64" width="56" height="56" aria-hidden="true" focusable="false">
        <rect x="8" y="10" width="48" height="44" rx="6" fill="none" stroke="currentColor" strokeWidth="2.5" />
        <path d="M8 22h48M8 34h48M24 22v32M40 22v32" stroke="currentColor" strokeWidth="2" opacity="0.45" />
        <circle cx="46" cy="44" r="9" fill="var(--card)" stroke="var(--accent)" strokeWidth="2.5" />
        <path
          d="M42 44l3 3 5-6"
          fill="none"
          stroke="var(--accent)"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <h2>No audit open yet</h2>
      <p className="muted">
        Drop a workbook above to start. The audit usually takes a minute or two.
        {hasHistory ? ' You can also open an earlier audit from the list.' : ''}
      </p>
    </section>
  )
}
