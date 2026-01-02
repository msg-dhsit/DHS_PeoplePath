'use client'
import { useEffect, useState } from 'react'
import Card from '../../components/Card'
import Table from '../../components/Table'
import api from '../../lib/api'
import Link from 'next/link'

export default function ResourcesPage() {
  const [resources, setResources] = useState<any[]>([])
  useEffect(() => {
    api.get('/resources').then(res => setResources(res.data))
  }, [])

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Resources</h2>
      <Card>
        <Table
          headers={["Name", "Title", "Skills", "Status"]}
          rows={resources.map(r => [
            <Link key={r.id} href={`/resources/${r.id}`} className="text-blue-600">{r.id}</Link>,
            r.title,
            (r.skills || []).join(', '),
            r.status
          ])}
        />
      </Card>
    </div>
  )
}
