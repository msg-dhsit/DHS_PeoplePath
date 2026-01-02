'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Card from '../../../components/Card'
import Table from '../../../components/Table'
import api from '../../../lib/api'

export default function ResourceDetail() {
  const params = useParams()
  const id = params?.id as string
  const [resource, setResource] = useState<any>(null)

  useEffect(() => {
    if (id) {
      api.get(`/resources/${id}`).then(res => setResource(res.data))
    }
  }, [id])

  if (!resource) return <p>Loading...</p>

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">{resource.name}</h2>
      <Card title="Profile">
        <p className="text-sm">{resource.title} • {resource.location}</p>
        <p className="text-sm text-gray-600">Skills: {(resource.skills || []).join(', ')}</p>
        <p className="text-sm text-gray-600">Team: {resource.team}</p>
      </Card>
      <Card title="Allocations">
        <Table headers={["Project", "Start", "End", "%"]} rows={(resource.allocations || []).map((a: any) => [a.project_name, a.start_date, a.end_date, a.allocation_percent])} />
      </Card>
    </div>
  )
}
