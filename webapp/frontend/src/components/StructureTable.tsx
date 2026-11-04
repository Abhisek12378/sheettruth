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
          <StatusIcon status="structure" /> Layout problems
        </h2>
        <p className="muted small">
          Found by simple rules, without the model: numbers typed where a formula should be, and formulas that break the
          pattern of their neighbours.
        </p>
      </div>
      {findings.length === 0 ? (
        <p className="muted">No layout problems were found.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Cell</th>
                <th scope="col">Problem</th>
                <th scope="col">What is there now</th>
                <th scope="col">What the pattern suggests</th>
                <th scope="col">Why</th>
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
