interface Props {
  onClick: () => void
  label?: string
  variant?: 'secondary' | 'primary' | 'link'
}

// Starts a fresh session: clears the open audit and the chosen file and returns to the upload.
export function NewAuditButton({ onClick, label = 'New audit', variant = 'secondary' }: Props) {
  return (
    <button type="button" className={`${variant} new-audit`} onClick={onClick}>
      <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false">
        <path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
      </svg>
      {label}
    </button>
  )
}
