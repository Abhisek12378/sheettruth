import { useEffect, useRef, useState } from 'react'
import type { Health } from '../api'
import { plural } from '../labels'
import { MarkIcon } from './MarkIcon'

interface Props {
  health: Health | null
  unreachable: boolean
}

type Level = 'ready' | 'limited' | 'offline'

function level(health: Health | null, unreachable: boolean): Level {
  if (unreachable || !health) return 'offline'
  return health.recalculation && health.reviewer ? 'ready' : 'limited'
}

const LEVEL_TEXT: Record<Level, string> = {
  ready: 'All systems ready',
  limited: 'Running with limits',
  offline: 'Server offline',
}

interface Line {
  ok: boolean
  label: string
  detail: string
  title?: string
}

function lines(health: Health): Line[] {
  return [
    { ok: true, label: 'Formula model', detail: 'Ready', title: health.model },
    {
      ok: health.recalculation,
      label: 'Recalculation',
      detail: health.recalculation ? 'Fixes are recalculated' : 'Off: fixes are not recalculated',
    },
    {
      ok: health.reviewer,
      label: 'Second opinion',
      detail: health.reviewer ? 'Reviewer model on' : 'Off: no reviewer model',
    },
    {
      ok: health.queued === 0,
      label: 'Queue',
      detail: health.queued === 0 ? 'Nothing waiting' : `${plural(health.queued, 'audit')} waiting`,
    },
  ]
}

// Closes the menu on a click outside it or on Escape.
function useCloseOnOutside(open: boolean, close: () => void, root: HTMLElement | null): void {
  useEffect(() => {
    if (!open) return
    const onClick = (event: MouseEvent) => !root?.contains(event.target as Node) && close()
    const onKey = (event: KeyboardEvent) => event.key === 'Escape' && close()
    document.addEventListener('mousedown', onClick)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onClick)
      document.removeEventListener('keydown', onKey)
    }
  }, [open, close, root])
}

export function StatusMenu({ health, unreachable }: Props) {
  const [open, setOpen] = useState(false)
  const rootRef = useRef<HTMLDivElement>(null)
  const current = level(health, unreachable)
  useCloseOnOutside(open, () => setOpen(false), rootRef.current)

  return (
    <div className="status-menu" ref={rootRef}>
      <button
        type="button"
        className={`status-pill ${current}`}
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-haspopup="dialog"
      >
        <span className="status-dot" aria-hidden="true" />
        {LEVEL_TEXT[current]}
      </button>
      {open && (
        <div className="status-panel" role="dialog" aria-label="Server status">
          {health ? (
            <ul>
              {lines(health).map((line) => (
                <li key={line.label} title={line.title}>
                  <MarkIcon mark={line.ok ? 'pass' : 'neutral'} />
                  <span className="status-label">{line.label}</span>
                  <span className="status-detail">{line.detail}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted small">The audit server did not answer. Uploads will not work until it is back.</p>
          )}
        </div>
      )}
    </div>
  )
}
