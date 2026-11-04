import type { Summary as SummaryData } from './api'
import { Findings } from './components/Findings'
import { Footer } from './components/Footer'
import { HealthBar } from './components/HealthBar'
import { History } from './components/History'
import { Landing } from './components/Landing'
import { Progress } from './components/Progress'
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
      <summary>Run log</summary>
      <ul>
        {notes.map((note, i) => (
          <li key={i}>{note}</li>
        ))}
      </ul>
    </details>
  )
}

export default function App() {
  const audit = useAudit()
  const { theme, toggle } = useTheme()
  const { selected } = audit

  // A finished job always carries a full summary; only unfinished jobs have an empty one.
  const result = selected?.status === 'done' ? selected.result : null
  const summary = selected?.status === 'done' ? (selected.summary as SummaryData) : null

  return (
    <div className="layout">
      <a className="skip-link" href="#upload">
        Skip to upload
      </a>
      <header className="topbar">
        <div className="brand">
          <img src="/favicon.svg" alt="" width="28" height="28" />
          <h1>{PRODUCT_NAME}</h1>
        </div>
        <div className="topbar-right">
          <HealthBar health={audit.health} />
          <ThemeToggle theme={theme} onToggle={toggle} />
        </div>
      </header>

      <History jobs={audit.jobs} selected={audit.selectedId} onSelect={audit.select} />

      <main>
        <Landing />
        <UploadCard busy={audit.uploading} onSubmit={audit.submit} />
        {audit.error && (
          <p className="error" role="alert">
            {audit.error}
          </p>
        )}

        {selected && selected.status !== 'done' && <Progress job={selected} />}

        {selected && result && summary && (
          <>
            <Summary job={selected} summary={summary} />
            <Findings findings={result.findings} />
            <StructureTable findings={result.structure} />
            <RunLog notes={result.notes} />
          </>
        )}
        <Footer />
      </main>
    </div>
  )
}
