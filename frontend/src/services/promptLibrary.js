/**
 * 提示词库 API 服务
 */
import api from './api'

export default {
  /**
   * 获取提示词列表
   */
  getPrompts(params = {}) {
    return api.get('/prompt-library/', { params })
  },

  /**
   * 获取单个提示词
   */
  getPromptById(id) {
    return api.get(`/prompt-library/${id}`)
  },

  /**
   * 创建提示词
   */
  createPrompt(data) {
    return api.post('/prompt-library/', data)
  },

  /**
   * 更新提示词
   */
  updatePrompt(id, data) {
    return api.put(`/prompt-library/${id}`, data)
  },

  /**
   * 删除提示词
   */
  deletePrompt(id) {
    return api.delete(`/prompt-library/${id}`)
  },

  /**
   * 收藏/取消收藏
   */
  toggleFavorite(id) {
    return api.post(`/prompt-library/${id}/favorite`)
  },

  /**
   * 获取收藏列表
   */
  getFavorites(params = {}) {
    return api.get('/prompt-library/favorites', { params })
  },

  /**
   * 获取分类列表
   */
  getCategories() {
    return api.get('/prompt-library/categories')
  },

  /**
   * 获取标签列表
   */
  getTags() {
    return api.get('/prompt-library/tags')
  },

  /**
   * 使用提示词（增加使用次数）
   */
  usePrompt(id) {
    return api.post(`/prompt-library/${id}/use`)
  }
}
