import { beforeEach, describe, expect, it, vi } from 'vitest'

const authStore = vi.hoisted(() => ({
  isAuthenticated: false,
  user: null,
  getCurrentUser: vi.fn(),
  logout: vi.fn()
}))

vi.mock('@/stores/auth', () => ({
  useAuthStore: () => authStore
}))

import { setupAuthGuard } from '@/router/guards'

function createGuard() {
  let guard
  const router = {
    beforeEach: vi.fn((callback) => {
      guard = callback
    }),
    afterEach: vi.fn()
  }

  setupAuthGuard(router)
  return guard
}

describe('authentication route guard', () => {
  beforeEach(() => {
    authStore.isAuthenticated = false
    authStore.user = null
    authStore.getCurrentUser.mockReset()
    authStore.logout.mockReset()
  })

  it('redirects unauthenticated users to the login page child route', async () => {
    const guard = createGuard()
    const next = vi.fn()

    await guard(
      { meta: { requiresAuth: true }, fullPath: '/dashboard' },
      {},
      next
    )

    expect(next).toHaveBeenCalledWith({
      name: 'LoginPage',
      query: { redirect: '/dashboard' }
    })
  })

  it('redirects authenticated guests to the dashboard page child route', async () => {
    authStore.isAuthenticated = true
    authStore.user = { id: 'user-1' }
    const guard = createGuard()
    const next = vi.fn()

    await guard(
      { meta: { requiresGuest: true }, fullPath: '/login' },
      {},
      next
    )

    expect(next).toHaveBeenCalledWith({ name: 'DashboardPage' })
  })
})
