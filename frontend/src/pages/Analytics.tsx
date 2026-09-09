import { useEffect, useState } from 'react'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { fetchAnalyticsSummary, type AnalyticsSummary } from '../api/client'
import { SalaryByCategoryChart } from '../components/SalaryByCategoryChart'
import { SalaryDistributionSummary } from '../components/SalaryDistributionSummary'
import { formatMoney } from '../utils/format'

function StatTile({ label, value }: { label: string; value: string }) {
  return (
    <Paper sx={{ p: 2, minWidth: 220 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="h5">{value}</Typography>
    </Paper>
  )
}

export function Analytics() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchAnalyticsSummary()
      .then(setSummary)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <CircularProgress />
  }

  if (error || !summary) {
    return <Alert severity="error">{error ?? 'No analytics available.'}</Alert>
  }

  // by_country and by_department and by_role all partition the same employees,
  // so any one of them sums to the total headcount.
  const totalEmployees = summary.by_country.reduce((sum, stat) => sum + stat.count, 0)

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <Stack direction="row" spacing={2} useFlexGap sx={{ mb: 4, flexWrap: 'wrap' }}>
        <StatTile label="Total Employees" value={totalEmployees.toLocaleString('en-US')} />
        <StatTile label="Org-wide Median Salary" value={formatMoney(summary.salary_distribution.median, '₹')} />
        <StatTile
          label="Org-wide Range"
          value={`${formatMoney(summary.salary_distribution.minimum, '₹')} – ${formatMoney(summary.salary_distribution.maximum, '₹')}`}
        />
      </Stack>

      <Stack spacing={4}>
        <SalaryByCategoryChart title="Average vs. Median Salary by Country" stats={summary.by_country} />
        <SalaryByCategoryChart title="Average vs. Median Salary by Department" stats={summary.by_department} />
        <SalaryByCategoryChart title="Average vs. Median Salary by Role" stats={summary.by_role} />
        <SalaryDistributionSummary distribution={summary.salary_distribution} />
      </Stack>
    </Box>
  )
}
