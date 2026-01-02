'use client'
import { useEffect, useState } from 'react'
import Card from '../../components/Card'
import Table from '../../components/Table'
import api from '../../lib/api'

export default function ApprovalsPage() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    api.get('/timesheets').then(res => {
      const pending = res.data.filter((t: any) => t.status === 'submitted')
      setItems(pending)
    })
  }, [])

  const approve = async (id: number) => {
    await api.post(`/timesheets/${id}/approve`, { approver_id: 2 })
    setItems(items.filter(i => i.id !== id))
  }

  const reject = async (id: number) => {
    await api.post(`/timesheets/${id}/reject`, { approver_id: 2, comments: 'Adjust entries' })
    setItems(items.filter(i => i.id !== id))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Approvals</h2>
      <Card>
        <Table
          headers={["Resource", "Week", "Status", "Actions"]}
          rows={items.map(item => [
            item.resource_id,
            item.week_start_date,
            item.status,
            <div key={item.id} className="space-x-2">
              <button onClick={() => approve(item.id)} className="px-3 py-1 bg-green-600 text-white rounded">Approve</button>
              <button onClick={() => reject(item.id)} className="px-3 py-1 bg-red-600 text-white rounded">Reject</button>
            </div>
          ])}
        />
      </Card>
    </div>
  )
}
