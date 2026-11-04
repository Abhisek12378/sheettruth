import { useRef, useState, type ChangeEvent, type DragEvent, type FormEvent, type KeyboardEvent } from 'react'
import { STRICTNESS, formatKilobytes } from '../labels'

interface Props {
  busy: boolean
  onSubmit: (file: File, threshold: number) => void
}

const DEFAULT_THRESHOLD = 0.5
const WORKBOOK_SUFFIXES = ['.xlsx', '.xlsm']
const WRONG_TYPE_MESSAGE = 'That is not an Excel workbook. Choose a file that ends in .xlsx or .xlsm.'

function isWorkbook(file: File): boolean {
  const name = file.name.toLowerCase()
  return WORKBOOK_SUFFIXES.some((suffix) => name.endsWith(suffix))
}

function WorkbookIcon() {
  return (
    <svg className="dropzone-icon" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true" focusable="false">
      <path
        d="M6 3h8l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm8 0v5h5M8 12h8M8 16h8M8 12v4m4-4v4m4-4v4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function StrictnessPicker({ value, onChange }: { value: number; onChange: (t: number) => void }) {
  return (
    <fieldset className="strictness">
      <legend>Strictness</legend>
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
            <span>{option.label}</span>
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
        <span className="muted small">{formatKilobytes(file.size)} · drop another file to replace it</span>
      </div>
    )
  }
  return (
    <div className="dropzone-text">
      <strong>Drop a workbook here</strong>
      <span className="muted small">or click to choose an .xlsx or .xlsm file</span>
    </div>
  )
}

export function UploadCard({ busy, onSubmit }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [threshold, setThreshold] = useState(DEFAULT_THRESHOLD)
  const [dragging, setDragging] = useState(false)
  const [message, setMessage] = useState('')
  const input = useRef<HTMLInputElement>(null)

  function choose(candidate: File | undefined) {
    if (!candidate) return
    if (!isWorkbook(candidate)) {
      setMessage(WRONG_TYPE_MESSAGE)
      return
    }
    setMessage('')
    setFile(candidate)
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
        className={`dropzone${dragging ? ' dragging' : ''}`}
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
        <input ref={input} type="file" accept=".xlsx,.xlsm" hidden onChange={pick} aria-label="Workbook file" />
        <WorkbookIcon />
        <DropzoneText file={file} />
      </div>

      <StrictnessPicker value={threshold} onChange={setThreshold} />

      <button type="submit" className="primary" disabled={!file || busy}>
        {busy ? 'Uploading…' : 'Audit workbook'}
      </button>

      {message && (
        <p id="upload-message" className="upload-message" role="alert">
          {message}
        </p>
      )}
    </form>
  )
}
