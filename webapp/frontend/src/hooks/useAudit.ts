// Audit state for the page: server health, the list of earlier audits, the selected audit
// and its polling while it runs, and the upload of a new workbook.

import { useCallback, useEffect, useState } from 'react'
import {
  createJob,
  fetchHealth,
  fetchJob,
  fetchJobs,
  type Health,
  type Job,
  type JobDetail,
  type JobStatus,
} from '../api'

const POLL_MS = 2000
const UNREACHABLE_MESSAGE = 'The audit server could not be reached. Check your connection and try again.'

interface PollHandle {
  cancelled: boolean
  timer?: number
}

function isActive(status: JobStatus): boolean {
  return status === 'queued' || status === 'running'
}

// A fetch that never got a response rejects with a TypeError; everything else carries the server's message.
function friendlyMessage(e: Error): string {
  return e instanceof TypeError ? UNREACHABLE_MESSAGE : e.message
}

// Fetches the job, hands it to onJob, and schedules the next fetch while the job is active.
function pollJob(id: string, handle: PollHandle, onJob: (job: JobDetail) => void, onError: (e: Error) => void): void {
  fetchJob(id)
    .then((job) => {
      if (handle.cancelled) return
      onJob(job)
      if (isActive(job.status)) {
        handle.timer = window.setTimeout(() => pollJob(id, handle, onJob, onError), POLL_MS)
      }
    })
    .catch((e: Error) => {
      if (!handle.cancelled) onError(e)
    })
}

function stopPolling(handle: PollHandle): void {
  handle.cancelled = true
  if (handle.timer) window.clearTimeout(handle.timer)
}

export interface AuditState {
  health: Health | null
  unreachable: boolean
  jobs: Job[]
  selectedId: string | null
  selected: JobDetail | null
  uploading: boolean
  error: string
  select: (id: string) => void
  submit: (file: File, threshold: number) => void
  dismissError: () => void
  retry: () => void
  reset: () => void
}

export function useAudit(): AuditState {
  const [health, setHealth] = useState<Health | null>(null)
  const [unreachable, setUnreachable] = useState(false)
  const [jobs, setJobs] = useState<Job[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [selected, setSelected] = useState<JobDetail | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const refreshJobs = useCallback(() => {
    fetchJobs()
      .then(setJobs)
      .catch(() => undefined)
  }, [])

  const refreshHealth = useCallback(() => {
    fetchHealth()
      .then((h) => {
        setHealth(h)
        setUnreachable(false)
      })
      .catch(() => {
        setHealth(null)
        setUnreachable(true)
      })
  }, [])

  const retry = useCallback(() => {
    refreshHealth()
    refreshJobs()
  }, [refreshHealth, refreshJobs])

  useEffect(retry, [retry])

  const onJob = useCallback(
    (job: JobDetail) => {
      setSelected(job)
      setUnreachable(false)
      if (!isActive(job.status)) retry()
    },
    [retry],
  )

  const onPollError = useCallback((e: Error) => {
    setError(friendlyMessage(e))
    if (e instanceof TypeError) setUnreachable(true)
  }, [])

  // Poll the selected audit while it is queued or running.
  useEffect(() => {
    if (!selectedId) return
    const handle: PollHandle = { cancelled: false }
    pollJob(selectedId, handle, onJob, onPollError)
    return () => stopPolling(handle)
  }, [selectedId, onJob, onPollError])

  const submit = useCallback(
    (file: File, threshold: number) => {
      setUploading(true)
      setError('')
      createJob(file, threshold)
        .then((job) => {
          setSelectedId(job.id)
          retry()
        })
        .catch((e: Error) => setError(friendlyMessage(e)))
        .finally(() => setUploading(false))
    },
    [retry],
  )

  const dismissError = useCallback(() => setError(''), [])

  // Closes the open audit and clears any error; the list of earlier audits stays.
  const reset = useCallback(() => {
    setSelectedId(null)
    setSelected(null)
    setError('')
  }, [])

  return {
    health,
    unreachable,
    jobs,
    selectedId,
    selected,
    uploading,
    error,
    select: setSelectedId,
    submit,
    dismissError,
    retry,
    reset,
  }
}
