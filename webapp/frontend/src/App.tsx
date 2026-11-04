import { useCallback, useEffect, useState } from 'react'
import type { Summary as SummaryData } from './api'
import { Drawer } from './components/Drawer'
import { Findings } from './components/Findings'
import { Footer } from './components/Footer'
import { Hero } from './components/Hero'
import { History } from './components/History'
import { HowItWorks } from './components/HowItWorks'
import { Progress } from './components/Progress'
import { ServerBanner } from './components/ServerBanner'
import { StatusMenu } from './components/StatusMenu'
import { StructureTable } from './components/StructureTable'
import { Summary } from './components/Summary'
import { ThemeToggle } from './components/ThemeToggle'
import { UploadCard } from './components/UploadCard'
import { useAudit } from './hooks/useAudit'
import { useTheme } from './hooks/useTheme'
import { PRODUCT_NAME } from './labels'

function RunLog({ notes }: { notes: string[] }) {
  return (
    <details className="card run-log">
      <summary>Technical log of this audit</summary>
      <ul>
        {notes.map((note, i) => (
          <li key={i}>{note}</li>
        ))}
      </ul>
    </details>
  )
}

function ErrorNotice({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  return (
    <div className="error error-notice" role="alert">
      <span>{message}</span>
      <button type="button" className="link-button" onClick={onDismiss}>
        Dismiss
      </button>
    </div>
  )
}

function AuditsButton({ count, running, onClick }: { count: number; running: boolean; onClick: () => void }) {
  return (
    <button type="button" className="audits-button" onClick={onClick} aria-haspopup="dialog">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">
        <path d="M4 6h16M4 12h16M4 18h10" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>
      <span>Audits</span>
      {count > 0 && <span className={`audits-count${running ? ' running' : ''}`}>{count}</span>}
    </button>
  )
}

// Brings the results into view once a newly selected audit has loaded.
function scrollToResults(): void {
  document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

export default function App() {
  const audit = useAudit()
  const { theme, toggle } = useTheme()
  const [drawerOpen, setDrawerOpen] = useState(false)
  const { selected } = audit

  const openAudit = useCallback(
    (id: string) => {
      audit.select(id)
      setDrawerOpen(false)
    },
    [audit.select],
  )

  const closeDrawer = useCallback(() => setDrawerOpen(false), [])

  // Scroll once the chosen audit has loaded, not on every poll of the same audit.
  const loadedId = selected?.id
  useEffect(() => {
    if (loadedId) scrollToResults()
  }, [loadedId])

  // A finished job always carries a full summary; only unfinished jobs have an empty one.
  const result = selected?.status === 'done' ? selected.result : null
  const summary = selected?.status === 'done' ? (selected.summary as SummaryData) : null
  const running = audit.jobs.some((job) => job.status === 'running' || job.status === 'queued')

  return (
    <div className="app">
      <a className="skip-link" href="#upload">
        Skip to upload
      </a>
      <header className="topbar">
        <div className="topbar-left">
          <AuditsButton count={audit.jobs.length} running={running} onClick={() => setDrawerOpen(true)} />
          <div className="brand">
            <img src="/favicon.svg" alt="" width="28" height="28" />
            <h1>{PRODUCT_NAME}</h1>
          </div>
        </div>
        <div className="topbar-right">
          <StatusMenu health={audit.health} unreachable={audit.unreachable} />
          <ThemeToggle theme={theme} onToggle={toggle} />
        </div>
      </header>

      <Drawer open={drawerOpen} title="Earlier audits" onClose={closeDrawer}>
        <History jobs={audit.jobs} selected={audit.selectedId} onSelect={openAudit} />
      </Drawer>

      <main>
        <div className="hero-band">
          {audit.unreachable && <ServerBanner onRetry={audit.retry} />}
          <Hero />
          <UploadCard busy={audit.uploading} onSubmit={audit.submit} />
          {audit.error && <ErrorNotice message={audit.error} onDismiss={audit.dismissError} />}
        </div>

        <div id="results" className="results">
          {selected && selected.status !== 'done' && <Progress job={selected} />}
          {selected && result && summary && (
            <>
              <Summary job={selected} summary={summary} />
              <Findings findings={result.findings} />
              <StructureTable findings={result.structure} />
              <RunLog notes={result.notes} />
            </>
          )}
        </div>

        <HowItWorks />
        <Footer />
      </main>
    </div>
  )
}
