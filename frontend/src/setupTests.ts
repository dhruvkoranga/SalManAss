import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach } from 'vitest'

// Vitest doesn't run in "globals" mode here, so RTL's automatic cleanup
// (which hooks a global afterEach) never registers. Without this, a
// component rendered in one test stays mounted into the next.
afterEach(() => {
  cleanup()
})

// jsdom has no layout engine: elements always report 0 width/height and
// ResizeObserver doesn't exist. MUI's DataGrid uses both to size and
// virtualize columns, so without these shims every column beyond the
// first collapses to zero width and never renders its cells.
class ResizeObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}
window.ResizeObserver = ResizeObserverStub

Object.defineProperty(HTMLElement.prototype, 'offsetWidth', { configurable: true, value: 1000 })
Object.defineProperty(HTMLElement.prototype, 'offsetHeight', { configurable: true, value: 600 })
