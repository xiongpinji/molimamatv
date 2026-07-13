import { vi } from 'vitest'

// 模拟浏览器API - Node.js环境需要
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}

global.sessionStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}

// 模拟window对象
global.window = global.window || {}
global.window.location = { href: 'http://localhost' }

// 模拟File对象（在Node.js环境中不存在）
global.File = class File {
  constructor(chunks, filename, options = {}) {
    this.name = filename
    this.size = chunks.reduce((acc, chunk) => acc + chunk.length, 0)
    this.type = options.type || ''
  }
}

// 设置环境变量
process.env.NODE_ENV = 'test'
process.env.VITEST = 'true'
