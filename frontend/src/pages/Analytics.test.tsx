import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Analytics } from './Analytics'

const SUMMARY = {
  by_country: [
    { group: 'India', average_salary_inr: '1500000.00', median_salary_inr: '1400000.00', count: 4000 },
    { group: 'United States', average_salary_inr: '2000000.00', median_salary_inr: '1900000.00', count: 6000 },
  ],
  by_department: [
    { group: 'Engineering', average_salary_inr: '1800000.00', median_salary_inr: '1700000.00', count: 5000 },
  ],
  by_role: [
    { group: 'Software Engineer', average_salary_inr: '1200000.00', median_salary_inr: '1150000.00', count: 3000 },
  ],
  salary_distribution: {
    minimum: '400000.00',
    p25: '900000.00',
    median: '1600000.00',
    p75: '2200000.00',
    maximum: '4200000.00',
  },
}

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({ ok: true, json: async () => SUMMARY }),
  )
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('Analytics', () => {
  it('shows org-wide stat tiles computed from the fetched summary', async () => {
    render(<Analytics />)

    expect(await screen.findByText('10,000')).toBeInTheDocument()
    expect(screen.getByText('₹1,600,000.00')).toBeInTheDocument()
  })

  it('renders a chart section per breakdown', async () => {
    render(<Analytics />)

    await screen.findByText('10,000')
    expect(screen.getByText('Average vs. Median Salary by Country')).toBeInTheDocument()
    expect(screen.getByText('Average vs. Median Salary by Department')).toBeInTheDocument()
    expect(screen.getByText('Average vs. Median Salary by Role')).toBeInTheDocument()
    expect(screen.getByText('Org-wide Salary Distribution (INR)')).toBeInTheDocument()
  })
})
