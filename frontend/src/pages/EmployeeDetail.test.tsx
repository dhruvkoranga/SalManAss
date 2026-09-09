import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { EmployeeDetail } from './EmployeeDetail'

const CURRENCIES = [
  { id: 1, code: 'USD', symbol: '$' },
  { id: 2, code: 'EUR', symbol: '€' },
]

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
  return vi.fn((url: string, init?: RequestInit) => {
    if (url.includes('/api/currencies')) {
      return Promise.resolve({ ok: true, json: async () => CURRENCIES })
    }
    if (init?.method === 'PUT') {
      const body = JSON.parse(init.body as string)
      return Promise.resolve({ ok: true, json: async () => ({ ...EMPLOYEE, ...body }) })
    }
    return Promise.resolve({ ok: true, json: async () => EMPLOYEE })
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
    <MemoryRouter initialEntries={['/employees/42']}>
      <Routes>
        <Route path="/employees/:id" element={<EmployeeDetail />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('EmployeeDetail', () => {
  it('loads and displays the employee', async () => {
    renderPage()

    expect(await screen.findByText('Jane Doe')).toBeInTheDocument()
    expect(screen.getByDisplayValue('jane.doe@acme.example')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Software Engineer')).toBeInTheDocument()
  })

  it('rejects a non-positive salary before calling the API', async () => {
    renderPage()
    await screen.findByText('Jane Doe')

    fireEvent.change(screen.getByLabelText('Salary Amount'), { target: { value: '0' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByText(/must be a positive number/i)).toBeInTheDocument()
    const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
    expect(calls.some((call) => call[1]?.method === 'PUT')).toBe(false)
  })

  it('saves an updated salary', async () => {
    renderPage()
    await screen.findByText('Jane Doe')

    fireEvent.change(screen.getByLabelText('Salary Amount'), { target: { value: '150000' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => {
      const calls = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls
      const putCall = calls.find((call) => call[1]?.method === 'PUT')
      expect(putCall).toBeDefined()
      const body = JSON.parse(putCall![1]!.body as string)
      expect(body.salary_amount).toBe('150000')
      expect(body.currency_id).toBe(1)
    })

    expect(await screen.findByText('Employee updated')).toBeInTheDocument()
  })
})
