<template>
  <div class="page-block">
    <el-card>
      <template #header>待审核梗图</template>
      <el-empty v-if="!items.length" description="暂无待审核内容" />
      <div v-else class="meme-grid">
        <el-card v-for="item in items" :key="item.pid" class="meme-card">
          <img :src="item.image_base64" :alt="item.title" class="meme-thumb" />
          <h3>{{ item.title }}</h3>
          <div>发布者：{{ item.uploader_name }}（UID {{ item.uploader_uid }}）</div>
          <div class="review-actions">
            <el-button type="success" @click="review(item.pid, 'approve', false)">允许展示</el-button>
            <el-button type="danger" plain @click="review(item.pid, 'reject', false)">拒绝显示</el-button>
            <el-button type="danger" @click="review(item.pid, 'reject', true)">拒绝并封禁发布者</el-button>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

import api from '@/api/client'
import type { MemeCardItem } from '@/types'

const items = ref<MemeCardItem[]>([])

async function fetchPending() {
  const { data } = await api.get<MemeCardItem[]>('/admin/pending-memes')
  items.value = data
}

async function review(pid: number, action: 'approve' | 'reject', banUploader: boolean) {
  await api.post(`/admin/memes/${pid}/review`, { action, ban_uploader: banUploader })
  ElMessage.success('审核完成')
  await fetchPending()
}

onMounted(fetchPending)
</script>
