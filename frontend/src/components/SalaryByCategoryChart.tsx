import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { BarChart } from '@mui/x-charts/BarChart'
import type { GroupStat } from '../api/client'

// dataviz skill categorical slots 1 & 2 (blue, orange) - fixed order, not cycled.
const AVERAGE_COLOR = '#2a78d6'
const MEDIAN_COLOR = '#eb6834'

type Props = {
  title: string
  stats: GroupStat[]
}

export function SalaryByCategoryChart({ title, stats }: Props) {
  const categories = stats.map((stat) => stat.group)
  const averages = stats.map((stat) => Number(stat.average_salary_inr))
  const medians = stats.map((stat) => Number(stat.median_salary_inr))

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <BarChart
        layout="horizontal"
        height={Math.max(220, categories.length * 36 + 80)}
        yAxis={[{ data: categories, scaleType: 'band', width: 'auto' }]}
        series={[
          { data: averages, label: 'Average (INR)', color: AVERAGE_COLOR },
          { data: medians, label: 'Median (INR)', color: MEDIAN_COLOR },
        ]}
      />
    </Box>
  )
}
