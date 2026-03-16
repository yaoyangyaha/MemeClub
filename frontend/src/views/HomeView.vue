<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api'
import type { Meme } from '@/types'
import MemeCard from '@/components/MemeCard.vue'
import MemeDetailDrawer from '@/components/MemeDetailDrawer.vue'

const route = useRoute()
const list = ref<Meme[]>([])
const total = ref(0)
const page = ref(1)
const detailVisible = ref(false)
const detailPid = ref<number | null>(null)

async function fetchMemes() {
  const { data } = await api.get('/memes', { params: { page: page.value, q: route.query.q || '' } })
  list.value = data.items
  total.value = data.total
}

function openDetail(pid: number) {
  detailPid.value = pid
  detailVisible.value = true
}

watch(
  () => route.query.q,
  () => {
    page.value = 1
    fetchMemes()
  },
)

onMounted(fetchMemes)
</script>

<template>
  <el-row :gutter="12">
    <el-col v-for="item in list" :key="item.pid" :xs="24" :sm="12" :md="8" :lg="6">
      <MemeCard :meme="item" @detail="openDetail(item.pid)" @refresh="fetchMemes" />
    </el-col>
  </el-row>

  <el-pagination
    v-model:current-page="page"
    :page-size="50"
    layout="prev, pager, next, total"
    :total="total"
    @current-change="fetchMemes"
  />

  <MemeDetailDrawer v-model="detailVisible" :pid="detailPid" @updated="fetchMemes" />
</template>
