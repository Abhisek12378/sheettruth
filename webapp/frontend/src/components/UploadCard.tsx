import { useRef, useState, type DragEvent, type FormEvent } from 'react'
import { STRICTNESS } from '../labels'

interface Props {
  busy: boolean
  onSubmit: (file: File, threshold: number) => void
}

export function UploadCard({ busy, onSubmit }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [threshold, setThreshold] = useState(0.5)
  const [dragging, setDragging] = useState(false)
  const input = useRef<HTMLInputElement>(null)

  function submit(event: FormEvent) {
    event.preventDefault()
    if (file) onSubmit(file, threshold)
  }

  function drop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setDragging(false)
    const dropped = event.dataTransfer.files[0]
    if (dropped) setFile(dropped)
  }

  function dragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setDragging(true)
  }

  return (
    <form className="card upload" onSubmit={submit}>
      <div
        className={`dropzone${dragging ? ' dragging' : ''}`}
        onDrop={drop}
        onDragOver={dragOver}
        onDragLeave={() => setDragging(false)}
        onClick={() => input.current?.click()}
      >
        <input
          ref={input}
          type="file"
          accept=".xlsx,.xlsm"
          hidden
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        {file ? (
          <div>
            <strong>{file.name}</strong>
            <span className="muted"> · {(file.size / 1024).toFixed(0)} KB</span>
          </div>
        ) : (
          <div>
            <strong>Drop a workbook here</strong>
            <span className="muted"> or click to choose (.xlsx)</span>
          </div>
        )}
      </div>

      <fieldset className="strictness">
        <legend>Strictness</legend>
        {STRICTNESS.map((option) => (
          <label key={option.threshold} className={threshold === option.threshold ? 'selected' : ''}>
            <input
              type="radio"
              name="strictness"
              checked={threshold === option.threshold}
              onChange={() => setThreshold(option.threshold)}
            />
            <span>{option.label}</span>
            <small>{option.help}</small>
          </label>
        ))}
      </fieldset>

      <button type="submit" className="primary" disabled={!file || busy}>
        {busy ? 'Uploading…' : 'Audit workbook'}
      </button>
    </form>
  )
}
