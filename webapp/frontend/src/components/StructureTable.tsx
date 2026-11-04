import type { StructureFinding } from '../api'
import { StatusIcon } from './StatusIcon'

const KIND_TITLE: Record<string, string> = {
  hardcoded_value: 'Number typed over a formula',
  odd_one_out: 'Formula differs from both neighbours',
}

export function StructureTable({ findings }: { findings: StructureFinding[] }) {
  return (
    <div className="card">
      <div className="card-head">
        <h2>
          <StatusIcon status="structure" /> Structure findings
        </h2>
        <p className="muted small">Found by rules on the formula layout alone, without the model.</p>
      </div>
      {findings.length === 0 ? (
        <p className="muted">No structure problems were found.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Cell</th>
                <th scope="col">Kind</th>
                <th scope="col">Current</th>
                <th scope="col">The run implies</th>
                <th scope="col">Detail</th>
              </tr>
            </thead>
            <tbody>
              {findings.map((s) => (
                <tr key={`${s.sheet}!${s.addr}`}>
                  <td className="mono">
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
        </div>
      )}
    </div>
  )
}
