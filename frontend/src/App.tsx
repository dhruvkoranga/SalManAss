import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Container from '@mui/material/Container'
import CssBaseline from '@mui/material/CssBaseline'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { Link, Route, Routes } from 'react-router-dom'
import { Analytics } from './pages/Analytics'
import { EmployeeDetail } from './pages/EmployeeDetail'
import { EmployeeList } from './pages/EmployeeList'

const theme = createTheme()

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            SalManAss
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Employees
          </Button>
          <Button color="inherit" component={Link} to="/analytics">
            Analytics
          </Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 4 }}>
        <Box>
          <Routes>
            <Route path="/" element={<EmployeeList />} />
            <Route path="/employees/:id" element={<EmployeeDetail />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
