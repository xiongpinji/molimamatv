<template>
  <div v-if="loading" class="auth-loading">
    <el-loading-directive />
  </div>
  <div v-else-if="isAuthenticated">
    <slot />
  </div>
  <div v-else class="auth-fallback">
    <el-result
      icon="warning"
      title="Authentication Required"
      :sub-title="message"
    >
      <template #extra>
        <el-button type="primary" @click="handleLogin">
          Login
        </el-button>
        <el-button @click="handleRegister">
          Register
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  message: {
    type: String,
    default: 'Please login to access this page'
  },
  redirectTo: {
    type: String,
    default: null
  }
})

const router = useRouter()
const authStore = useAuthStore()

const loading = computed(() => authStore.loading)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleLogin = () => {
  const redirect = props.redirectTo || router.currentRoute.value.fullPath
  router.push({ name: 'LoginPage', query: { redirect } })
}

const handleRegister = () => {
  router.push({ name: 'RegisterPage' })
}

onMounted(async () => {
  // 如果有token但没有用户信息，尝试获取用户信息
  if (authStore.token && !authStore.user) {
    try {
      await authStore.getCurrentUser()
    } catch (error) {
      console.error('Failed to get user info:', error)
    }
  }
})
</script>

<style scoped>
.auth-loading {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-fallback {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
