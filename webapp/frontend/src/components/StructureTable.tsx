import type { StructureFinding } from '../api'

const KIND_TITLE: Record<string, string> = {
  hardcoded_value: 'Number typed over a formula',
  odd_one_out: 'Formula differs from both neighbours',
}

export function StructureTable({ findings }: { findings: StructureFinding[] }) {
  return (
    <div className="card">
      <h2>Structure findings</h2>
      <p className="muted small">Found by rules on the formula layout alone, without the model.</p>
      {findings.length === 0 ? (
        <p className="muted">None.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Cell</th>
              <th>Kind</th>
              <th>Current</th>
              <th>The run implies</th>
              <th>Detail</th>
            </tr>
          </thead>
          <tbody>
            {findings.map((s) => (
              <tr key={`${s.sheet}!${s.addr}`}>
                <td>
                  {s.sheet}!{s.addr}
                </td>
                <td>{KIND_TITLE[s.kind] || s.kind}</td>
                <td>
                  <code>{s.current}</code>
                </td>
                <td>
                  <code>{s.implied_formula}</code>
                </td>
                <td>{s.detail}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
