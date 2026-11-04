import { useEffect, useRef, type ReactNode } from 'react'

interface Props {
  open: boolean
  title: string
  onClose: () => void
  action?: ReactNode
  children: ReactNode
}

// Closes on Escape and keeps the page from scrolling while the drawer is open.
function useDrawerBehaviour(open: boolean, onClose: () => void, closeButton: HTMLButtonElement | null): void {
  useEffect(() => {
    if (!open) return
    const onKey = (event: KeyboardEvent) => event.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    document.body.style.overflow = 'hidden'
    closeButton?.focus()
    return () => {
      document.removeEventListener('keydown', onKey)
      document.body.style.overflow = ''
    }
  }, [open, onClose, closeButton])
}

export function Drawer({ open, title, onClose, action, children }: Props) {
  const closeRef = useRef<HTMLButtonElement>(null)
  useDrawerBehaviour(open, onClose, closeRef.current)

  return (
    <div className={`drawer-root${open ? ' open' : ''}`} aria-hidden={!open}>
      <div className="drawer-backdrop" onClick={onClose} />
      <aside className="drawer" role="dialog" aria-modal="true" aria-label={title}>
        <div className="drawer-head">
          <h2>{title}</h2>
          <button ref={closeRef} type="button" className="icon-button" onClick={onClose} aria-label="Close">
            <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">
              <path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>
        </div>
        {action && <div className="drawer-action">{action}</div>}
        <div className="drawer-body">{children}</div>
      </aside>
    </div>
  )
}
