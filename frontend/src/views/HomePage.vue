<template>
  <div class="page-block">
    <div class="meme-grid">
      <MemeCard
        v-for="item in memes.items"
        :key="item.pid"
        :item="item"
        @detail="openDetail"
        @favorite="toggleFavorite"
      />
    </div>

    <el-empty v-if="!memes.items.length" description="还没有符合条件的梗图" />

    <div class="pagination-wrap">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="page"
        :page-size="50"
        :total="memes.total"
        @current-change="onPageChange"
      />
    </div>

    <MemeDetailDrawer v-model="drawerVisible" :detail="detail" @refreshed="refreshDetailAndList" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import api from '@/api/client'
import MemeCard from '@/components/MemeCard.vue'
import MemeDetailDrawer from '@/components/MemeDetailDrawer.vue'
import type { MemeDetail, MemeListResponse } from '@/types'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  searchKeyword?: string
}>()

const auth = useAuthStore()
const page = ref(1)
const memes = ref<MemeListResponse>({
  total: 0,
  page: 1,
  page_size: 50,
  items: []
})
const drawerVisible = ref(false)
const detail = ref<MemeDetail | null>(null)
const activePid = ref<number | null>(null)

async function fetchMemes() {
  const { data } = await api.get<MemeListResponse>('/memes', {
    params: {
      page: page.value,
      page_size: 50,
      keyword: props.searchKeyword ?? ''
    }
  })
  memes.value = data
}

async function openDetail(pid: number) {
  const { data } = await api.get<MemeDetail>(`/memes/${pid}`)
  detail.value = data
  activePid.value = pid
  drawerVisible.value = true
}

async function toggleFavorite(pid: number) {
  if (!auth.user) {
    ElMessage.warning('请先登录')
    return
  }
  await api.post(`/memes/${pid}/favorite`)
  ElMessage.success('收藏状态已更新')
  await fetchMemes()
  if (activePid.value === pid && drawerVisible.value) {
    await openDetail(pid)
  }
}

async function refreshDetailAndList() {
  await fetchMemes()
  if (activePid.value) {
    await openDetail(activePid.value)
  }
}

function onPageChange(nextPage: number) {
  page.value = nextPage
  fetchMemes()
}

watch(
  () => props.searchKeyword,
  () => {
    page.value = 1
    fetchMemes()
  }
)

onMounted(fetchMemes)
</script>
