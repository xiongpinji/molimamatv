<template>
  <el-dialog
    v-model="visible"
    title="提示词库"
    width="1040px"
    :close-on-click-modal="true"
    @close="handleClose"
  >
    <div class="dialog-search">
      <el-input
        v-model="keyword"
        placeholder="搜索提示词..."
        :prefix-icon="Search"
        clearable
        size="large"
      />
    </div>

    <div class="dialog-filter">
      <span class="filter-label">分类</span>
      <div class="filter-tags">
        <el-check-tag
          v-for="cat in categories"
          :key="cat.slug"
          :checked="selectedCategory === cat.slug"
          @change="selectedCategory = cat.slug"
        >
          {{ cat.name }}
        </el-check-tag>
      </div>
    </div>

    <div class="dialog-filter">
      <span class="filter-label">类型</span>
      <div class="filter-tags">
        <el-check-tag
          v-for="tag in useCaseTags"
          :key="tag.value"
          :checked="selectedUseCase === tag.value"
          @change="selectedUseCase = tag.value"
        >
          {{ tag.label }}
        </el-check-tag>
      </div>
    </div>

    <div class="prompt-grid" v-loading="loading">
      <PromptCard
        v-for="prompt in filteredPrompts"
        :key="prompt.id"
        :prompt="prompt"
        @select="handleSelect"
      />
      <el-empty v-if="filteredPrompts.length === 0 && !loading" description="没有找到匹配的提示词" />
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import PromptCard from './PromptCard.vue'
import promptLibraryApi from '@/services/promptLibrary'

const props = defineProps({
  modelValue: Boolean,
  useCase: { type: String, default: 'text2img' }
})

const emit = defineEmits(['update:modelValue', 'select'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const keyword = ref('')
const selectedCategory = ref('all')
const selectedUseCase = ref('all')
const loading = ref(false)
const prompts = ref([])
const categories = ref([])

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
    categories.value = [{ name: '全部', slug: 'all' }, ...(categoriesRes || [])]
  } finally {
    loading.value = false
  }
}

const handleSelect = (prompt) => {
  emit('select', prompt.content)
  visible.value = false
}

const handleClose = () => {
  keyword.value = ''
  selectedCategory.value = 'all'
  selectedUseCase.value = 'all'
}

watch(visible, (val) => {
  if (val) loadData()
})
</script>

<style scoped>
.dialog-search {
  margin-bottom: 16px;
  max-width: 672px;
  margin-left: auto;
  margin-right: auto;
}

.dialog-filter {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.filter-label {
  font-size: 13px;
  color: #666;
  min-width: 40px;
  padding-top: 6px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.prompt-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  max-height: 520px;
  overflow-y: auto;
  padding: 16px 0;
}

@media (max-width: 768px) {
  .prompt-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .prompt-grid {
    grid-template-columns: 1fr;
  }
}
</style>
