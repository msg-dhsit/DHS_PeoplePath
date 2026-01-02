'use client'
import { useEffect, useState } from 'react'
import Card from '../../components/Card'
import Table from '../../components/Table'
import WeekPicker from '../../components/WeekPicker'
import Modal from '../../components/Modal'
import api from '../../lib/api'

export default function TimesheetPage() {
  const [entries, setEntries] = useState<any[]>([])
  const [weekStart, setWeekStart] = useState<string>('')
  const [suggestions, setSuggestions] = useState<any | null>(null)
  const [timesheetId, setTimesheetId] = useState<number | null>(null)

  useEffect(() => {
    const today = new Date()
    const monday = new Date(today.setDate(today.getDate() - today.getDay() + 1))
    const iso = monday.toISOString().slice(0, 10)
    setWeekStart(iso)
    loadTimesheet(iso)
  }, [])

  const loadTimesheet = async (week: string) => {
    const res = await api.get('/timesheets', { params: { week_start: week } })
    const ts = res.data[0]
    if (ts) {
      setTimesheetId(ts.id)
      setEntries(ts.entries)
    }
  }

  const requestSuggestion = async () => {
    const res = await api.post('/ai/timesheet/suggest', { resource_id: 1, week_start: weekStart })
    setSuggestions(res.data)
  }

  const applySuggestion = async () => {
    if (!timesheetId || !suggestions) return
    await api.post('/ai/timesheet/apply', { timesheet_id: timesheetId, suggestions: suggestions.entries, confirmation_token: 'CONFIRM' })
    setEntries(suggestions.entries)
    setSuggestions(null)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Timesheet</h2>
        <WeekPicker value={weekStart} onChange={value => { setWeekStart(value); loadTimesheet(value) }} />
      </div>
      <Card>
        <div className="flex justify-between mb-3">
          <p className="text-sm text-gray-600">Inline edit coming soon</p>
          <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={requestSuggestion}>AI Suggest</button>
        </div>
        <Table headers={["Date", "Project", "Task", "Hours", "Comment"]} rows={entries.map((e: any) => [e.date, e.project || e.project_id, e.task, e.hours, e.comment])} />
      </Card>

      <Modal open={!!suggestions} onClose={() => setSuggestions(null)} title="AI Suggestions" actions={
        <>
          <button className="px-3 py-2 rounded border" onClick={() => setSuggestions(null)}>Cancel</button>
          <button className="px-3 py-2 rounded bg-blue-600 text-white" onClick={applySuggestion}>Apply</button>
        </>
      }>
        {suggestions?.entries.map((entry: any, idx: number) => (
          <div key={idx} className="border p-2 rounded">
            <div className="flex justify-between">
              <span className="font-semibold">{entry.date}</span>
              <span className="text-xs text-gray-500">Confidence {entry.confidence}</span>
            </div>
            <p className="text-sm">{entry.project} — {entry.task} — {entry.hours}h</p>
            <p className="text-xs text-gray-600">{entry.comment}</p>
          </div>
        ))}
      </Modal>
    </div>
  )
}
