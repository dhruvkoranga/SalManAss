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

type CurrencyRate = { exchange_rate_to_inr: string }

// Converts through INR as the common base, same as the backend's salary
// sort/analytics: amount -> INR -> target currency.
export function convertAmount(amount: string | number, from: CurrencyRate, to: CurrencyRate): number {
  const amountInInr = Number(amount) * Number(from.exchange_rate_to_inr)
  return amountInInr / Number(to.exchange_rate_to_inr)
}
