import { useCallback, useEffect, useState } from 'react'
import {
  createJob,
  fetchHealth,
  fetchJob,
  fetchJobs,
  type Health,
  type Job,
  type JobDetail,
  type Summary as SummaryData,
} from './api'
import { Findings } from './components/Findings'
import { History } from './components/History'
import { Progress } from './components/Progress'
import { StructureTable } from './components/StructureTable'
import { Summary } from './components/Summary'
import { UploadCard } from './components/UploadCard'

const POLL_MS = 2000

function HealthBar({ health }: { health: Health | null }) {
  if (!health) return null
  return (
    <div className="health">
      <span className="chip on">{health.model}</span>
      <span className={`chip ${health.recalculation ? 'on' : 'off'}`}>
        {health.recalculation ? 'LibreOffice recalculation' : 'no recalculation'}
      </span>
      <span className={`chip ${health.reviewer ? 'on' : 'off'}`}>
        {health.reviewer ? 'reviewer model' : 'no reviewer'}
      </span>
    </div>
  )
}

export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [selected, setSelected] = useState<JobDetail | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const refreshJobs = useCallback(() => {
    fetchJobs().then(setJobs).catch(() => undefined)
  }, [])

  useEffect(() => {
    fetchHealth().then(setHealth).catch(() => setHealth(null))
    refreshJobs()
  }, [refreshJobs])

  // Poll the selected audit while it is queued or running.
  useEffect(() => {
    if (!selectedId) return
    let cancelled = false
    let timer: number | undefined

    function tick() {
      fetchJob(selectedId as string)
        .then((job) => {
          if (cancelled) return
          setSelected(job)
          if (job.status === 'queued' || job.status === 'running') {
            timer = window.setTimeout(tick, POLL_MS)
          } else {
            refreshJobs()
          }
        })
        .catch((e: Error) => {
          if (!cancelled) setError(e.message)
        })
    }

    tick()
    return () => {
      cancelled = true
      if (timer) window.clearTimeout(timer)
    }
  }, [selectedId, refreshJobs])

  function submit(file: File, threshold: number) {
    setUploading(true)
    setError('')
    createJob(file, threshold)
      .then((job) => {
        setSelectedId(job.id)
        refreshJobs()
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setUploading(false))
  }

  // A finished job always carries a full summary; only unfinished jobs have an empty one.
  const result = selected?.status === 'done' ? selected.result : null
  const summary = selected?.status === 'done' ? (selected.summary as SummaryData) : null

  return (
    <div className="layout">
      <header>
        <div className="brand">
          <h1>SheetTruth</h1>
          <p>Finds formulas that compute the wrong thing, then checks each finding against the workbook itself.</p>
        </div>
        <HealthBar health={health} />
      </header>

      <History jobs={jobs} selected={selectedId} onSelect={setSelectedId} />

      <main>
        <UploadCard busy={uploading} onSubmit={submit} />
        {error && <p className="error">{error}</p>}

        {selected && selected.status !== 'done' && <Progress job={selected} />}

        {selected && result && summary && (
          <>
            <Summary job={selected} summary={summary} />
            <Findings findings={result.findings} />
            <StructureTable findings={result.structure} />
            <details className="card run-log">
              <summary>Run log</summary>
              <ul>
                {result.notes.map((note, i) => (
                  <li key={i}>{note}</li>
                ))}
              </ul>
            </details>
          </>
        )}
      </main>
    </div>
  )
}
