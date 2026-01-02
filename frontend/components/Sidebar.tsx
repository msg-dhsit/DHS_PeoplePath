'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  { href: '/', label: 'Dashboard' },
  { href: '/resources', label: 'Resources' },
  { href: '/timesheets', label: 'Timesheet' },
  { href: '/approvals', label: 'Approvals' }
]

export default function Sidebar() {
  const path = usePathname()
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 hidden md:block">
      <h1 className="text-xl font-semibold mb-6">PeoplePath</h1>
      <nav className="space-y-2">
        {links.map(link => (
          <Link key={link.href} href={link.href} className={`block px-3 py-2 rounded hover:bg-gray-100 ${path === link.href ? 'bg-gray-100 font-semibold' : ''}`}>
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  )
}
