<template>
  <el-card class="meme-card" shadow="hover">
    <div class="meme-thumb-wrap">
      <img :src="item.image_base64" :alt="item.title" class="meme-thumb" />
    </div>
    <div class="meme-meta">
      <h3>{{ item.title }}</h3>
      <div class="meta-row">
        <el-tag :type="statusType">{{ statusText }}</el-tag>
      </div>
      <div class="meta-row">发布者：{{ item.uploader_name }}（UID {{ item.uploader_uid }}）</div>
      <div class="meta-row">
        <el-rate :model-value="item.average_rating" disabled allow-half />
        <span>{{ item.average_rating.toFixed(1) }}</span>
      </div>
      <div class="meta-row">评论 {{ item.comment_count }} 条 · 收藏 {{ item.favorite_count }}</div>
      <div class="card-actions">
        <el-button type="primary" plain @click="$emit('detail', item.pid)">详情</el-button>
        <el-button
          :type="item.is_favorited ? 'warning' : 'success'"
          :disabled="item.review_status !== 'approved'"
          @click="$emit('favorite', item.pid)"
        >
          {{ item.is_favorited ? '取消收藏' : '收藏' }}
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { MemeCardItem } from '../types'

const props = defineProps<{
  item: MemeCardItem
}>()

defineEmits<{
  detail: [pid: number]
  favorite: [pid: number]
}>()

const statusText = computed(() => {
  if (props.item.review_status === 'approved') {
    return '已发布'
  }
  if (props.item.review_status === 'rejected') {
    return '已拒绝'
  }
  return '待审核'
})

const statusType = computed(() => {
  if (props.item.review_status === 'approved') {
    return 'success'
  }
  if (props.item.review_status === 'rejected') {
    return 'danger'
  }
  return 'warning'
})
</script>
