<template>
  <div class="prompt-library-page">
    <div class="page-header">
      <h1>提示词库</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        创建提示词
      </el-button>
    </div>

    <div class="page-content">
      <div class="sidebar">
        <div class="sidebar-section">
          <h3>分类</h3>
          <el-menu :default-active="selectedCategory" @select="selectedCategory = $event">
            <el-menu-item index="all">全部</el-menu-item>
            <el-menu-item v-for="cat in categories" :key="cat.slug" :index="cat.slug">
              {{ cat.name }}
            </el-menu-item>
          </el-menu>
        </div>

        <div class="sidebar-section">
          <h3>类型</h3>
          <el-menu :default-active="selectedUseCase" @select="selectedUseCase = $event">
            <el-menu-item v-for="tag in useCaseTags" :key="tag.value" :index="tag.value">
              {{ tag.label }}
            </el-menu-item>
          </el-menu>
        </div>
      </div>

      <div class="main-content">
        <div class="search-bar">
          <el-input
            v-model="keyword"
            placeholder="搜索提示词..."
            :prefix-icon="Search"
            clearable
            size="large"
          />
        </div>

        <div class="prompt-grid" v-loading="loading">
          <PromptCard
            v-for="prompt in filteredPrompts"
            :key="prompt.id"
            :prompt="prompt"
            @select="handleSelect"
          />
          <el-empty v-if="filteredPrompts.length === 0 && !loading" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Search } from '@element-plus/icons-vue'
import PromptCard from '@/components/prompt-library/PromptCard.vue'
import promptLibraryApi from '@/services/promptLibrary'

const keyword = ref('')
const selectedCategory = ref('all')
const selectedUseCase = ref('all')
const loading = ref(false)
const prompts = ref([])
const categories = ref([])
const showCreateDialog = ref(false)

const useCaseTags = [
  { label: '全部', value: 'all' },
  { label: '文生图', value: 'text2img' },
  { label: '图生图', value: 'img2img' },
  { label: '图转视频', value: 'img2video' },
  { label: '音频/TTS', value: 'tts' }
]

const filteredPrompts = computed(() => {
  return prompts.value.filter(p => {
    const matchCategory = selectedCategory.value === 'all' || p.category === selectedCategory.value
    const matchUseCase = selectedUseCase.value === 'all' || p.use_case === selectedUseCase.value
    const matchKeyword = !keyword.value ||
      p.title?.toLowerCase().includes(keyword.value.toLowerCase()) ||
      p.content?.toLowerCase().includes(keyword.value.toLowerCase())
    return matchCategory && matchUseCase && matchKeyword
  })
})

const loadData = async () => {
  loading.value = true
  try {
    const [promptsRes, categoriesRes] = await Promise.all([
      promptLibraryApi.getPrompts({ page: 1, page_size: 100 }),
      promptLibraryApi.getCategories()
    ])
    prompts.value = promptsRes.items || []
    categories.value = categoriesRes || []
  } finally {
    loading.value = false
  }
}

const handleSelect = (prompt) => {
  console.log('选中提示词:', prompt)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.prompt-library-page {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
}

.page-content {
  flex: 1;
  display: flex;
  gap: 24px;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  flex-shrink: 0;
}

.sidebar-section {
  margin-bottom: 24px;
}

.sidebar-section h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.search-bar {
  margin-bottom: 16px;
}

.prompt-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  overflow-y: auto;
}
</style>
