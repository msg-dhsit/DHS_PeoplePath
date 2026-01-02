'use client'
import { useEffect, useState } from 'react'
import Card from '../components/Card'
import api from '../lib/api'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

export default function DashboardPage() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    api.get('/dashboard/summary').then(res => setData(res.data)).catch(() => setData(null))
  }, [])

  const utilization = data?.utilization || []

  const chartData = {
    labels: utilization.map((item: any) => item.week_start),
    datasets: [
      {
        label: 'Utilization %',
        data: utilization.map((item: any) => item.utilization),
        backgroundColor: '#2563eb'
      }
    ]
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card title="Resources">{data?.summary?.total_resources ?? '-'}</Card>
        <Card title="Available">{data?.summary?.available ?? '-'}</Card>
        <Card title="Pending Timesheets">{data?.summary?.pending_timesheets ?? '-'}</Card>
        <Card title="Fully Allocated">{data?.summary?.fully_allocated ?? '-'}</Card>
      </div>
      <Card title="Utilization">
        <div className="h-64">
          <Bar data={chartData} />
        </div>
      </Card>
    </div>
  )
}
