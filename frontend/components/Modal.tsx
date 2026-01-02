'use client'
import React from 'react'

export default function Modal({ open, onClose, title, children, actions }: { open: boolean; onClose: () => void; title: string; children: React.ReactNode; actions?: React.ReactNode }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-2xl p-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">{title}</h3>
          <button onClick={onClose} className="text-gray-500">✕</button>
        </div>
        <div className="space-y-3">{children}</div>
        {actions && <div className="mt-4 flex justify-end space-x-2">{actions}</div>}
      </div>
    </div>
  )
}
