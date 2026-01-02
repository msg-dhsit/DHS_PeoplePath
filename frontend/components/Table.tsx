import React from 'react'

export default function Table({ headers, rows }: { headers: string[]; rows: (string | number | React.ReactNode)[][] }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            {headers.map(h => (
              <th key={h} className="px-4 py-2 text-left text-gray-600 font-semibold">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} className="border-b">
              {row.map((col, cidx) => (
                <td key={cidx} className="px-4 py-2">{col}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
