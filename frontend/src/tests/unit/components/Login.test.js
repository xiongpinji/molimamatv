/**
 * @vitest-environment jsdom
 */

import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import Login from '@/views/Login.vue'
import { useAuthStore } from '@/stores/auth'

const router = {
  push: vi.fn(),
  currentRoute: { value: { query: {} } }
}

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, useRouter: () => router }
})

vi.mock('@/stores/auth', () => ({ useAuthStore: vi.fn() }))

describe('Login.vue', () => {
  let wrapper
  let authStore

  beforeEach(() => {
    vi.clearAllMocks()
    router.currentRoute.value.query = {}
    authStore = { login: vi.fn(), loading: false }
    useAuthStore.mockReturnValue(authStore)
    wrapper = mount(Login, {
      global: {
        plugins: [ElementPlus],
        stubs: { RouterLink: { template: '<a><slot /></a>' } }
      }
    })
  })

  it('renders the current login form', () => {
    expect(wrapper.get('h2').text()).toBe('账户登录')
    expect(wrapper.get('input[type="text"]').attributes('placeholder')).toBe('请输入用户名')
    expect(wrapper.get('input[type="password"]').attributes('placeholder')).toBe('请输入密码')
    expect(wrapper.get('button').text()).toContain('登录')
    expect(wrapper.text()).toContain('还没有账户？')
  })

  it('submits valid credentials and redirects to dashboard', async () => {
    authStore.login.mockResolvedValue({})
    await wrapper.get('input[type="text"]').setValue('testuser')
    await wrapper.get('input[type="password"]').setValue('password123')
    await wrapper.get('button').trigger('click')
    await flushPromises()
    expect(authStore.login).toHaveBeenCalledWith({ username: 'testuser', password: 'password123' })
    expect(router.push).toHaveBeenCalledWith('/dashboard')
  })

  it('uses the intended redirect query', async () => {
    router.currentRoute.value.query = { redirect: '/projects' }
    authStore.login.mockResolvedValue({})
    await wrapper.get('input[type="text"]').setValue('testuser')
    await wrapper.get('input[type="password"]').setValue('password123')
    await wrapper.get('button').trigger('click')
    await flushPromises()
    expect(router.push).toHaveBeenCalledWith('/projects')
  })

  it('does not redirect when login fails', async () => {
    authStore.login.mockRejectedValue(new Error('登录失败'))
    await wrapper.get('input[type="text"]').setValue('testuser')
    await wrapper.get('input[type="password"]').setValue('wrongpass')
    await wrapper.get('button').trigger('click')
    await flushPromises()
    expect(router.push).not.toHaveBeenCalled()
  })
})
