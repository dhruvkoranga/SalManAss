// A fixed locale, not the runtime's default: money formatting must stay
// consistent regardless of the server/browser's locale settings (undefined
// locale previously picked up Indian-style digit grouping in this environment).
export function formatMoney(amount: string | number, symbol = ''): string {
  const value = Number(amount).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
  return `${symbol}${value}`
}
