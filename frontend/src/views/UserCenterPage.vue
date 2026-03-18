<template>
  <div class="page-block">
    <el-card class="profile-card" v-if="profile">
      <div class="profile-head">
        <el-avatar :size="120" :src="getGravatarUrl(profile.user.email, 240)" />
        <div>
          <h2>{{ profile.user.username }}</h2>
          <div>UID：{{ profile.user.uid }}</div>
          <div>封禁状态：{{ profile.user.is_banned ? '已封禁' : '正常' }}</div>
          <div>身份：{{ profile.user.user_status === 'admin' ? '管理员' : '普通用户' }}</div>
          <el-button type="danger" plain class="logout-btn" @click="logout">退出登录</el-button>
        </div>
      </div>
    </el-card>

    <el-card v-if="profile?.user.user_status === 'admin'" class="admin-tools">
      <template #header>管理员操作</template>
      <div class="admin-ban-row">
        <el-input-number v-model="banUid" :min="1" />
        <el-switch v-model="banValue" active-text="封禁" inactive-text="解封" />
        <el-button type="primary" @click="submitBan">提交</el-button>
      </div>
    </el-card>

    <el-card class="profile-card">
      <template #header>我提交的梗图</template>
      <div class="meme-grid">
        <MemeCard
          v-for="item in profile?.submitted_memes ?? []"
          :key="item.pid"
          :item="item"
          @detail="openDetail"
          @favorite="toggleFavorite"
        />
      </div>
    </el-card>

    <MemeDetailDrawer v-model="drawerVisible" :detail="detail" @refreshed="refreshProfile" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import api from '@/api/client'
import MemeCard from '@/components/MemeCard.vue'
import MemeDetailDrawer from '@/components/MemeDetailDrawer.vue'
import { useAuthStore } from '@/stores/auth'
import type { MemeDetail, UserProfile } from '@/types'
import { getGravatarUrl } from '@/utils/gravatar'

const router = useRouter()
const auth = useAuthStore()
const profile = ref<UserProfile | null>(null)
const drawerVisible = ref(false)
const detail = ref<MemeDetail | null>(null)
const banUid = ref<number | undefined>(undefined)
const banValue = ref(true)

async function refreshProfile() {
  const { data } = await api.get<UserProfile>('/users/me')
  profile.value = data
  auth.user = data.user
}

async function logout() {
  await auth.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

async function openDetail(pid: number) {
  const { data } = await api.get<MemeDetail>(`/memes/${pid}`)
  detail.value = data
  drawerVisible.value = true
}

async function toggleFavorite(pid: number) {
  await api.post(`/memes/${pid}/favorite`)
  ElMessage.success('收藏状态已更新')
  await refreshProfile()
}

async function submitBan() {
  if (!banUid.value) {
    ElMessage.warning('请输入要操作的 UID')
    return
  }
  await api.post('/admin/ban-user', { uid: banUid.value, banned: banValue.value })
  ElMessage.success('用户状态已更新')
}

onMounted(refreshProfile)
</script>
