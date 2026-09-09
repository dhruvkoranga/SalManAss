import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { EmployeeList } from './EmployeeList'

const CURRENCIES = [{ id: 1, code: 'USD', symbol: '$' }]

const EMPLOYEE = {
  id: 42,
  first_name: 'Jane',
  last_name: 'Doe',
  email: 'jane.doe@acme.example',
  country: 'United States',
  department: 'Engineering',
  job_title: 'Software Engineer',
  salary_amount: '120000.00',
  currency_id: 1,
  hire_date: '2023-01-15',
}

function mockFetch() {
  return vi.fn((url: string) => {
    if (url.includes('/api/currencies')) {
      return Promise.resolve({ ok: true, json: async () => CURRENCIES })
    }
    return Promise.resolve({
      ok: true,
      json: async () => ({ items: [EMPLOYEE], total: 1, page: 1, page_size: 20 }),
    })
  })
}

beforeEach(() => {
  vi.stubGlobal('fetch', mockFetch())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

function renderPage() {
  return render(
    <BrowserRouter>
      <EmployeeList />
    </BrowserRouter>,
  )
}

describe('EmployeeList', () => {
  it('renders fetched employees with the currency symbol applied', async () => {
    renderPage()

    expect(await screen.findByText('Jane')).toBeInTheDocument()
    expect(await screen.findByText('$120,000.00')).toBeInTheDocument()
  })

  it('re-fetches with the country filter when Search is clicked', async () => {
    renderPage()
    await screen.findByText('Jane')

    fireEvent.change(screen.getByLabelText('Country'), { target: { value: 'Germany' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => {
      const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
      const employeeCalls = calls.filter((call) => (call[0] as string).includes('/api/employees'))
      const lastCall = employeeCalls.at(-1)
      expect(lastCall?.[0]).toContain('country=Germany')
    })
  })

  it('re-fetches sorted ascending then descending when the First Name header is clicked', async () => {
    renderPage()
    await screen.findByText('Jane')

    const header = screen.getByRole('columnheader', { name: 'First Name' })
    fireEvent.click(header)

    await waitFor(() => {
      const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
      const lastCall = calls.filter((call) => (call[0] as string).includes('/api/employees')).at(-1)
      expect(lastCall?.[0]).toContain('sort_by=first_name')
      expect(lastCall?.[0]).toContain('sort_order=asc')
    })

    fireEvent.click(header)

    await waitFor(() => {
      const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
      const lastCall = calls.filter((call) => (call[0] as string).includes('/api/employees')).at(-1)
      expect(lastCall?.[0]).toContain('sort_order=desc')
    })
  })

  it('does not make the Email column sortable', async () => {
    renderPage()
    await screen.findByText('Jane')

    const header = screen.getByRole('columnheader', { name: 'Email' })
    expect(header).toHaveAttribute('aria-sort', 'none')

    fireEvent.click(header)

    await new Promise((resolve) => setTimeout(resolve, 0))
    const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
    const lastCall = calls.filter((call) => (call[0] as string).includes('/api/employees')).at(-1)
    expect(lastCall?.[0]).not.toContain('sort_by')
  })
})
