import { useEffect, useState } from 'react'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import MenuItem from '@mui/material/MenuItem'
import Paper from '@mui/material/Paper'
import Snackbar from '@mui/material/Snackbar'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import { Link, useParams } from 'react-router-dom'
import { fetchCurrencies, fetchEmployee, updateEmployee, type Currency, type Employee } from '../api/client'

export function EmployeeDetail() {
  const { id } = useParams<{ id: string }>()

  const [employee, setEmployee] = useState<Employee | null>(null)
  const [currencies, setCurrencies] = useState<Currency[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState<string | null>(null)

  const [department, setDepartment] = useState('')
  const [jobTitle, setJobTitle] = useState('')
  const [salaryAmount, setSalaryAmount] = useState('')
  const [currencyId, setCurrencyId] = useState<number | ''>('')

  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    setLoadError(null)

    Promise.all([fetchEmployee(Number(id)), fetchCurrencies()])
      .then(([fetchedEmployee, fetchedCurrencies]) => {
        setEmployee(fetchedEmployee)
        setCurrencies(fetchedCurrencies)
        setDepartment(fetchedEmployee.department)
        setJobTitle(fetchedEmployee.job_title)
        setSalaryAmount(fetchedEmployee.salary_amount)
        setCurrencyId(fetchedEmployee.currency_id)
      })
      .catch((err: Error) => setLoadError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  const handleSave = () => {
    if (!id || currencyId === '') return

    const amount = Number(salaryAmount)
    if (!Number.isFinite(amount) || amount <= 0) {
      setSaveError('Salary must be a positive number.')
      return
    }

    setSaving(true)
    setSaveError(null)

    updateEmployee(Number(id), {
      department,
      job_title: jobTitle,
      salary_amount: salaryAmount,
      currency_id: currencyId,
    })
      .then((updated) => {
        setEmployee(updated)
        setSaved(true)
      })
      .catch((err: Error) => setSaveError(err.message))
      .finally(() => setSaving(false))
  }

  if (loading) {
    return <CircularProgress />
  }

  if (loadError || !employee) {
    return <Alert severity="error">{loadError ?? 'Employee not found.'}</Alert>
  }

  return (
    <Box>
      <Button component={Link} to="/" sx={{ mb: 2 }}>
        Back to Directory
      </Button>

      <Typography variant="h4" gutterBottom>
        {employee.first_name} {employee.last_name}
      </Typography>

      <Paper sx={{ p: 3, maxWidth: 480 }}>
        <Stack spacing={2}>
          <TextField label="Email" value={employee.email} disabled fullWidth />
          <TextField label="Country" value={employee.country} disabled fullWidth />
          <TextField label="Hire Date" value={employee.hire_date} disabled fullWidth />
          <TextField
            label="Department"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            fullWidth
          />
          <TextField label="Role" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} fullWidth />
          <TextField
            label="Salary Amount"
            value={salaryAmount}
            onChange={(e) => setSalaryAmount(e.target.value)}
            fullWidth
          />
          <TextField
            select
            label="Currency"
            value={currencyId}
            onChange={(e) => setCurrencyId(Number(e.target.value))}
            fullWidth
          >
            {currencies.map((currency) => (
              <MenuItem key={currency.id} value={currency.id}>
                {currency.code} ({currency.symbol})
              </MenuItem>
            ))}
          </TextField>

          {saveError && <Alert severity="error">{saveError}</Alert>}

          <Button variant="contained" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving…' : 'Save'}
          </Button>
        </Stack>
      </Paper>

      <Snackbar open={saved} autoHideDuration={3000} onClose={() => setSaved(false)} message="Employee updated" />
    </Box>
  )
}
