import React from 'react'

export default function Card({ title, children }: { title?: string; children: React.ReactNode }) {
  return (
    <div className="bg-white shadow-sm rounded-lg p-4 border border-gray-100">
      {title && <h3 className="text-sm font-semibold text-gray-600 mb-2">{title}</h3>}
      {children}
    </div>
  )
}
