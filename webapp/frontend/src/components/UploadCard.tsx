import {
  useCallback,
  useRef,
  useState,
  type ChangeEvent,
  type DragEvent,
  type FormEvent,
  type KeyboardEvent,
} from 'react'
import { SAMPLE_WORKBOOK, useSampleWorkbook } from '../hooks/useSampleWorkbook'
import { STRICTNESS, formatKilobytes } from '../labels'

interface Props {
  busy: boolean
  onSubmit: (file: File, threshold: number) => void
}

const DEFAULT_THRESHOLD = 0.5
const WORKBOOK_SUFFIXES = ['.xlsx', '.xlsm', '.xls']
const LEGACY_SUFFIX = '.xls'
const WRONG_TYPE_MESSAGE = 'That file is not an Excel workbook. Please choose a file that ends in .xlsx, .xlsm or .xls.'
const LEGACY_NOTE = 'older Excel format · it will be converted to .xlsx for the audit'

function isWorkbook(file: File): boolean {
  const name = file.name.toLowerCase()
  return WORKBOOK_SUFFIXES.some((suffix) => name.endsWith(suffix))
}

function isLegacy(file: File): boolean {
  return file.name.toLowerCase().endsWith(LEGACY_SUFFIX)
}

function UploadIcon() {
  return (
    <svg className="dropzone-icon" viewBox="0 0 48 48" width="44" height="44" aria-hidden="true" focusable="false">
      <rect x="8" y="6" width="32" height="36" rx="5" fill="none" stroke="currentColor" strokeWidth="2.5" />
      <path d="M8 16h32M8 26h32M19 16v26M30 16v26" stroke="currentColor" strokeWidth="2" opacity="0.35" />
      <circle cx="35" cy="35" r="9.5" fill="var(--card)" stroke="currentColor" strokeWidth="2.5" />
      <path
        d="M35 40v-9m-4 4 4-4 4 4"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function StrictnessPicker({ value, onChange }: { value: number; onChange: (t: number) => void }) {
  return (
    <fieldset className="strictness">
      <legend>How strict should the audit be?</legend>
      <div className="strictness-options">
        {STRICTNESS.map((option) => (
          <label key={option.threshold} className={value === option.threshold ? 'selected' : ''}>
            <input
              type="radio"
              name="strictness"
              value={option.threshold}
              checked={value === option.threshold}
              onChange={() => onChange(option.threshold)}
            />
            <span className="strictness-name">{option.label}</span>
            <small>{option.help}</small>
          </label>
        ))}
      </div>
    </fieldset>
  )
}

function DropzoneText({ file }: { file: File | null }) {
  if (file) {
    return (
      <div className="dropzone-text">
        <strong>{file.name}</strong>
        <span className="muted">
          {formatKilobytes(file.size)} · {isLegacy(file) ? LEGACY_NOTE : 'drop another file to replace it'}
        </span>
      </div>
    )
  }
  return (
    <div className="dropzone-text">
      <strong>Drop your workbook here</strong>
      <span className="muted">or click to choose a file · .xlsx, .xlsm or .xls, up to 25 MB</span>
    </div>
  )
}

export function UploadCard({ busy, onSubmit }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [threshold, setThreshold] = useState(DEFAULT_THRESHOLD)
  const [dragging, setDragging] = useState(false)
  const [message, setMessage] = useState('')
  const input = useRef<HTMLInputElement>(null)

  const accept = useCallback((candidate: File) => {
    setMessage('')
    setFile(candidate)
  }, [])
  const sample = useSampleWorkbook(accept, setMessage)

  function choose(candidate: File | undefined) {
    if (!candidate) return
    if (!isWorkbook(candidate)) {
      setMessage(WRONG_TYPE_MESSAGE)
      return
    }
    accept(candidate)
  }

  function submit(event: FormEvent) {
    event.preventDefault()
    if (file) onSubmit(file, threshold)
  }

  function drop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setDragging(false)
    choose(event.dataTransfer.files[0])
  }

  function dragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setDragging(true)
  }

  function pick(event: ChangeEvent<HTMLInputElement>) {
    choose(event.target.files?.[0])
    event.target.value = ''
  }

  function keyOpen(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      input.current?.click()
    }
  }

  return (
    <form id="upload" className="card upload" onSubmit={submit} aria-label="Audit a workbook">
      <div
        className={`dropzone${dragging ? ' dragging' : ''}${file ? ' has-file' : ''}`}
        role="button"
        tabIndex={0}
        aria-label={file ? `Chosen workbook ${file.name}. Choose another.` : 'Choose a workbook to audit'}
        aria-describedby={message ? 'upload-message' : undefined}
        onDrop={drop}
        onDragOver={dragOver}
        onDragLeave={() => setDragging(false)}
        onClick={() => input.current?.click()}
        onKeyDown={keyOpen}
      >
        <input ref={input} type="file" accept=".xlsx,.xlsm,.xls" hidden onChange={pick} aria-label="Workbook file" />
        <UploadIcon />
        <DropzoneText file={file} />
      </div>

      <div className="sample">
        <button type="button" className="secondary" onClick={sample.load} disabled={sample.loading || busy}>
          {sample.loading ? 'Loading the sample…' : 'Try a sample workbook'}
        </button>
        <span className="muted small">{SAMPLE_WORKBOOK.description}</span>
        {file?.name === SAMPLE_WORKBOOK.name && (
          <a className="sample-download" href={SAMPLE_WORKBOOK.path} download={SAMPLE_WORKBOOK.name}>
            Download the sample to your computer
          </a>
        )}
      </div>

      {message && (
        <p id="upload-message" className="upload-message" role="alert">
          {message}
        </p>
      )}

      <div className="upload-controls">
        <StrictnessPicker value={threshold} onChange={setThreshold} />
        <button type="submit" className="primary" disabled={!file || busy}>
          {busy ? 'Uploading…' : 'Audit this workbook'}
        </button>
      </div>
      <p className="muted small upload-note">
        Your file is only used for this audit. Nothing is changed in the original; fixes go into a separate corrected
        copy.
      </p>
    </form>
  )
}
