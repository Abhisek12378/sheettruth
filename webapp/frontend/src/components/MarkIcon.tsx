// Pass, fail, neutral, skipped and unknown marks. Each mark has its own shape, so the
// meaning never depends on colour alone.

import type { Mark } from '../findings'

const PATHS: Record<Mark, string> = {
  pass: 'M5 12.5l4.5 4.5L19 7',
  fail: 'M6 6l12 12M18 6 6 18',
  neutral: 'M6 12h12',
  skipped: 'M8 12h.01M12 12h.01M16 12h.01',
  unknown: 'M9.5 9.3a2.6 2.6 0 1 1 3.8 2.3c-.8.5-1.3 1-1.3 1.9m0 3.2v.3',
}

export function MarkIcon({ mark }: { mark: Mark }) {
  return (
    <svg
      className={`mark mark-${mark}`}
      viewBox="0 0 24 24"
      width="14"
      height="14"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d={PATHS[mark]}
        fill="none"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}
