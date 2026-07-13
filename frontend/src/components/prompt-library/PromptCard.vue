<template>
  <div class="prompt-card" @click="$emit('select', prompt)">
    <div class="card-cover">
      <img v-if="prompt.cover_url" :src="prompt.cover_url" :alt="prompt.title" />
      <div v-else class="cover-placeholder">
        <el-icon :size="32"><Picture /></el-icon>
      </div>
    </div>
    <div class="card-content">
      <div class="card-header">
        <span class="card-title" :title="prompt.title">{{ prompt.title }}</span>
        <span class="card-date">{{ formatDate(prompt.updated_at) }}</span>
      </div>
      <p class="card-preview">{{ truncate(prompt.content, 100) }}</p>
      <div class="card-tags">
        <el-tag v-for="tag in prompt.tags?.slice(0, 3)" :key="tag" size="small" type="info">
          {{ tag }}
        </el-tag>
      </div>
    </div>
    <div class="card-actions">
      <el-button type="primary" size="small" @click.stop="$emit('select', prompt)">
        <el-icon><Check /></el-icon>
        使用此提示词
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { Picture, Check } from '@element-plus/icons-vue'

defineProps({
  prompt: { type: Object, required: true }
})

defineEmits(['select'])

const truncate = (str, len) => {
  if (!str) return ''
  return str.length > len ? str.slice(0, len) + '...' : str
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.prompt-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.prompt-card:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-cover {
  aspect-ratio: 4/3;
  background: #f5f7fa;
  overflow: hidden;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #c0c4cc;
}

.card-content {
  padding: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.card-title {
  font-weight: 500;
  font-size: 14px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-date {
  font-size: 12px;
  color: #909399;
  margin-left: 8px;
}

.card-preview {
  font-size: 12px;
  color: #606266;
  line-height: 1.5;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.card-actions {
  padding: 8px 12px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
}
</style>
