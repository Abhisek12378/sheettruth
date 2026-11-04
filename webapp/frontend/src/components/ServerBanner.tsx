interface Props {
  onRetry: () => void
}

export function ServerBanner({ onRetry }: Props) {
  return (
    <div className="banner" role="alert">
      <span>
        <strong>The audit server is not responding.</strong> You cannot upload or open earlier audits until it is back.
        If it was just restarted, give it a moment.
      </span>
      <button type="button" className="secondary" onClick={onRetry}>
        Try again
      </button>
    </div>
  )
}
