import { useEffect, useState } from 'react'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import { DataGrid, type GridColDef } from '@mui/x-data-grid'
import { useNavigate } from 'react-router-dom'
import { fetchCurrencies, fetchEmployees, type Currency, type Employee } from '../api/client'
import { formatMoney } from '../utils/format'

type Filters = {
  search: string
  country: string
  department: string
  role: string
}

const EMPTY_FILTERS: Filters = { search: '', country: '', department: '', role: '' }

export function EmployeeList() {
  const navigate = useNavigate()

  const [currencies, setCurrencies] = useState<Map<number, Currency>>(new Map())
  const [draftFilters, setDraftFilters] = useState<Filters>(EMPTY_FILTERS)
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS)
  const [page, setPage] = useState(0)
  const [pageSize, setPageSize] = useState(20)

  const [employees, setEmployees] = useState<Employee[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCurrencies()
      .then((list) => setCurrencies(new Map(list.map((currency) => [currency.id, currency]))))
      .catch(() => {
        // Salary column falls back to the raw amount with no symbol.
      })
  }, [])

  useEffect(() => {
    setLoading(true)
    setError(null)

    fetchEmployees({
      search: filters.search || undefined,
      country: filters.country || undefined,
      department: filters.department || undefined,
      role: filters.role || undefined,
      page: page + 1,
      page_size: pageSize,
    })
      .then((response) => {
        setEmployees(response.items)
        setTotal(response.total)
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filters, page, pageSize])

  const applyFilters = () => {
    setPage(0)
    setFilters(draftFilters)
  }

  // Sorting/filtering are disabled per-column: the backend has fixed
  // ordering and its own filter params, so DataGrid's built-in controls
  // would be UI that looks functional but does nothing server-side.
  const columns: GridColDef<Employee>[] = [
    { field: 'first_name', headerName: 'First Name', flex: 1, sortable: false, filterable: false },
    { field: 'last_name', headerName: 'Last Name', flex: 1, sortable: false, filterable: false },
    { field: 'email', headerName: 'Email', flex: 1.5, sortable: false, filterable: false },
    { field: 'country', headerName: 'Country', flex: 1, sortable: false, filterable: false },
    { field: 'department', headerName: 'Department', flex: 1, sortable: false, filterable: false },
    { field: 'job_title', headerName: 'Role', flex: 1, sortable: false, filterable: false },
    {
      field: 'salary_amount',
      headerName: 'Salary',
      flex: 1,
      sortable: false,
      filterable: false,
      renderCell: (params) => {
        const currency = currencies.get(params.row.currency_id)
        return formatMoney(params.row.salary_amount, currency?.symbol)
      },
    },
    { field: 'hire_date', headerName: 'Hire Date', flex: 1, sortable: false, filterable: false },
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Employee Directory
      </Typography>

      <Stack direction="row" spacing={2} useFlexGap sx={{ mb: 2, flexWrap: 'wrap' }}>
        <TextField
          label="Search (name or email)"
          size="small"
          value={draftFilters.search}
          onChange={(e) => setDraftFilters({ ...draftFilters, search: e.target.value })}
        />
        <TextField
          label="Country"
          size="small"
          value={draftFilters.country}
          onChange={(e) => setDraftFilters({ ...draftFilters, country: e.target.value })}
        />
        <TextField
          label="Department"
          size="small"
          value={draftFilters.department}
          onChange={(e) => setDraftFilters({ ...draftFilters, department: e.target.value })}
        />
        <TextField
          label="Role"
          size="small"
          value={draftFilters.role}
          onChange={(e) => setDraftFilters({ ...draftFilters, role: e.target.value })}
        />
        <Button variant="contained" onClick={applyFilters}>
          Search
        </Button>
      </Stack>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 600 }}>
        <DataGrid
          rows={employees}
          columns={columns}
          loading={loading}
          paginationMode="server"
          rowCount={total}
          paginationModel={{ page, pageSize }}
          onPaginationModelChange={(model) => {
            setPage(model.page)
            setPageSize(model.pageSize)
          }}
          pageSizeOptions={[20, 50, 100]}
          disableColumnMenu
          onRowClick={(params) => navigate(`/employees/${params.id}`)}
        />
      </Box>
    </Box>
  )
}
