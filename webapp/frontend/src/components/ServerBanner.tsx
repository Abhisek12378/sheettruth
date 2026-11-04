interface Props {
  onRetry: () => void
}

export function ServerBanner({ onRetry }: Props) {
  return (
    <div className="banner" role="alert">
      <span>
        <strong>The audit server is not responding.</strong> Uploads and earlier audits are unavailable until it is
        back. If it was just deployed, give it a moment.
      </span>
      <button type="button" className="secondary" onClick={onRetry}>
        Try again
      </button>
    </div>
  )
}
