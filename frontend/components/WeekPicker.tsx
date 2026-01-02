'use client'
import React from 'react'

export default function WeekPicker({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <input
      type="date"
      value={value}
      onChange={e => onChange(e.target.value)}
      className="border rounded px-3 py-2"
    />
  )
}
