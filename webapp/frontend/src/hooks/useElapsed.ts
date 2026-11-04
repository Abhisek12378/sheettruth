// Seconds elapsed since a server timestamp, updated once a second while running is true.

import { useEffect, useState } from 'react'

function secondsSince(startedAt: number): number {
  return Math.max(0, Date.now() / 1000 - startedAt)
}

export function useElapsed(startedAt: number, running: boolean): number {
  const [elapsed, setElapsed] = useState(() => secondsSince(startedAt))

  useEffect(() => {
    setElapsed(secondsSince(startedAt))
    if (!running) return
    const timer = window.setInterval(() => setElapsed(secondsSince(startedAt)), 1000)
    return () => window.clearInterval(timer)
  }, [startedAt, running])

  return elapsed
}
