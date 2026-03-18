<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { api } from '@/api'
import { authState } from '@/state/auth'
import type { Meme } from '@/types'

defineProps<{ meme: Meme }>()
const emit = defineEmits<{ (e: 'detail'): void; (e: 'refresh'): void }>()

async function toggleFavorite(pid: number) {
  if (!authState.uid) {
    ElMessage.warning('请先登录后再收藏')
    return
  }

  try {
    await api.post('/favorite', { pid })
    ElMessage.success('操作成功')
    emit('refresh')
  } catch {
    // handled by axios interceptor
  }
}
</script>

<template>
  <el-card shadow="hover" class="card">
    <el-image :src="meme.image_base64" fit="cover" class="thumb" :preview-src-list="[meme.image_base64]" />
    <h4>{{ meme.title }}</h4>
    <el-rate :model-value="meme.avg_rating" disabled allow-half />
    <el-space>
      <el-button size="small" @click="emit('detail')">详情</el-button>
      <el-button size="small" type="warning" :disabled="!authState.uid" @click="toggleFavorite(meme.pid)">
        {{ meme.is_favorite ? '取消收藏' : '收藏' }}
      </el-button>
    </el-space>
  </el-card>
</template>

<style scoped>
.card { width: 100%; }
.thumb { width: 100%; height: 180px; border-radius: 4px; }
</style>
