import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import type { SalaryDistribution } from '../api/client'
import { formatMoney } from '../utils/format'

// dataviz skill sequential ramp (one hue, blue): near-zero track, mid box, dark marker.
const TRACK_COLOR = '#cde2fb'
const BOX_COLOR = '#2a78d6'
const MEDIAN_COLOR = '#0d366b'

type Props = {
  distribution: SalaryDistribution
}

export function SalaryDistributionSummary({ distribution }: Props) {
  const min = Number(distribution.minimum)
  const max = Number(distribution.maximum)
  const p25 = Number(distribution.p25)
  const median = Number(distribution.median)
  const p75 = Number(distribution.p75)
  const span = max - min || 1

  const toPercent = (value: number) => ((value - min) / span) * 100

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Org-wide Salary Distribution (INR)
      </Typography>

      <Box sx={{ position: 'relative', height: 24, bgcolor: TRACK_COLOR, borderRadius: 1, my: 2 }}>
        <Box
          sx={{
            position: 'absolute',
            left: `${toPercent(p25)}%`,
            width: `${toPercent(p75) - toPercent(p25)}%`,
            height: '100%',
            bgcolor: BOX_COLOR,
            borderRadius: 1,
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            left: `${toPercent(median)}%`,
            width: 3,
            height: '100%',
            bgcolor: MEDIAN_COLOR,
          }}
        />
      </Box>

      <Stack direction="row" useFlexGap sx={{ justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <Typography variant="body2">Min: {formatMoney(min, '₹')}</Typography>
        <Typography variant="body2">P25: {formatMoney(p25, '₹')}</Typography>
        <Typography variant="body2">Median: {formatMoney(median, '₹')}</Typography>
        <Typography variant="body2">P75: {formatMoney(p75, '₹')}</Typography>
        <Typography variant="body2">Max: {formatMoney(max, '₹')}</Typography>
      </Stack>
    </Paper>
  )
}
