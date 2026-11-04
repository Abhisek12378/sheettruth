// Small icons that accompany each status colour, so colour is never the only signal.

import type { FindingStatus } from '../api'

export type IconStatus = FindingStatus | 'structure'

const PATHS: Record<IconStatus, string> = {
  // exclamation in a circle
  confirmed: 'M12 3a9 9 0 1 1 0 18 9 9 0 0 1 0-18Zm0 4.5v5.5m0 3.2v.3',
  // question mark in a circle
  unverified: 'M12 3a9 9 0 1 1 0 18 9 9 0 0 1 0-18Zm-2.6 6.3a2.7 2.7 0 1 1 3.9 2.4c-.9.5-1.3 1-1.3 1.9m0 3.1v.3',
  // two opposing arrows
  disputed: 'M4 9h13m0 0-3.5-3.5M17 9l-3.5 3.5M20 15H7m0 0 3.5-3.5M7 15l3.5 3.5',
  // minus in a circle
  contradicted: 'M12 3a9 9 0 1 1 0 18 9 9 0 0 1 0-18ZM8 12h8',
  // grid
  structure: 'M4 4h16v16H4V4Zm0 5.3h16M4 14.7h16M9.3 4v16M14.7 4v16',
}

export function StatusIcon({ status }: { status: IconStatus }) {
  return (
    <svg
      className={`status-icon ${status}`}
      viewBox="0 0 24 24"
      width="16"
      height="16"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d={PATHS[status]}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}
