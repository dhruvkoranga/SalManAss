import { describe, expect, it } from 'vitest'
import { convertAmount, formatMoney } from './format'

const USD = { id: 2, code: 'USD', symbol: '$', exchange_rate_to_inr: '83' }
const INR = { id: 1, code: 'INR', symbol: '₹', exchange_rate_to_inr: '1' }

describe('formatMoney', () => {
  it('formats with a fixed locale regardless of the runtime locale', () => {
    expect(formatMoney('120000', '$')).toBe('$120,000.00')
  })
})

describe('convertAmount', () => {
  it('converts through INR as the common base', () => {
    // 20,000 USD * 83 (INR/USD) = 1,660,000 INR
    expect(convertAmount('20000', USD, INR)).toBeCloseTo(1_660_000, 5)
  })

  it('converts back from INR to another currency', () => {
    // 1,660,000 INR / 83 (INR/USD) = 20,000 USD
    expect(convertAmount('1660000', INR, USD)).toBeCloseTo(20_000, 5)
  })

  it('is a no-op when converting a currency to itself', () => {
    expect(convertAmount('45000', USD, USD)).toBeCloseTo(45_000, 5)
  })
})
