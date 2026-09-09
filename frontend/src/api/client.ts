// Base URL for the FastAPI backend. Set VITE_API_BASE_URL in production
// (Render deploys frontend/backend as separate services); defaults to the
// local dev backend otherwise.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? `Request to ${path} failed with status ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function apiGet<T>(path: string): Promise<T> {
  return request<T>(path)
}

export function apiPut<T>(path: string, data: unknown): Promise<T> {
  return request<T>(path, { method: 'PUT', body: JSON.stringify(data) })
}

export type Employee = {
  id: number
  first_name: string
  last_name: string
  email: string
  country: string
  department: string
  job_title: string
  salary_amount: string
  currency_id: number
  hire_date: string
}

export type EmployeeListResponse = {
  items: Employee[]
  total: number
  page: number
  page_size: number
}

export type Currency = {
  id: number
  code: string
  symbol: string
}

export type EmployeeListParams = {
  search?: string
  country?: string
  department?: string
  role?: string
  page: number
  page_size: number
}

export function fetchEmployees(params: EmployeeListParams): Promise<EmployeeListResponse> {
  const query = new URLSearchParams()
  if (params.search) query.set('search', params.search)
  if (params.country) query.set('country', params.country)
  if (params.department) query.set('department', params.department)
  if (params.role) query.set('role', params.role)
  query.set('page', String(params.page))
  query.set('page_size', String(params.page_size))

  return apiGet<EmployeeListResponse>(`/api/employees?${query}`)
}

export function fetchCurrencies(): Promise<Currency[]> {
  return apiGet<Currency[]>('/api/currencies')
}

export function fetchEmployee(id: number): Promise<Employee> {
  return apiGet<Employee>(`/api/employees/${id}`)
}

export type EmployeeUpdate = {
  department: string
  job_title: string
  salary_amount: string
  currency_id: number
}

export function updateEmployee(id: number, update: EmployeeUpdate): Promise<Employee> {
  return apiPut<Employee>(`/api/employees/${id}`, update)
}

export type GroupStat = {
  group: string
  average_salary_inr: string
  median_salary_inr: string
  count: number
}

export type SalaryDistribution = {
  minimum: string
  p25: string
  median: string
  p75: string
  maximum: string
}

export type AnalyticsSummary = {
  by_country: GroupStat[]
  by_department: GroupStat[]
  by_role: GroupStat[]
  salary_distribution: SalaryDistribution
}

export function fetchAnalyticsSummary(): Promise<AnalyticsSummary> {
  return apiGet<AnalyticsSummary>('/api/analytics/summary')
}
