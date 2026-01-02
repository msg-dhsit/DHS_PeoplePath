import { render, screen } from '@testing-library/react'
import Card from '../Card'

it('renders card title', () => {
  render(<Card title="Test">content</Card>)
  expect(screen.getByText('Test')).toBeInTheDocument()
})
