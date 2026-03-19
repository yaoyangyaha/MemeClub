<template>
  <el-drawer v-model="visible" size="55%" direction="rtl" :destroy-on-close="true">
    <template #header>
      <div class="drawer-title">{{ detail?.title || '梗图详情' }}</div>
    </template>

    <div v-if="detail" class="drawer-body">
      <el-image
        :src="detail.image_base64"
        :preview-src-list="[detail.image_base64]"
        fit="contain"
        class="detail-image"
      />
      <h2>{{ detail.title }}</h2>
      <p class="detail-copy">{{ detail.description }}</p>
      <div class="detail-line">上传者：{{ detail.uploader_name }}（UID {{ detail.uploader_uid }}）</div>
      <div class="detail-line">上传时间：{{ formatTime(detail.created_at) }}</div>
      <div class="detail-line">
        综合评分：
        <el-rate :model-value="detail.average_rating" allow-half disabled />
        <span>{{ detail.average_rating.toFixed(1) }}</span>
      </div>
      <el-divider />

      <div class="rating-row">
        <el-rate v-model="ratingValue" allow-half />
        <el-button type="primary" @click="submitRating">提交评分</el-button>
      </div>

      <div class="comment-box">
        <div class="comment-header">评论区（{{ detail.comment_count }}）</div>
        <el-input
          v-model="commentText"
          maxlength="100"
          show-word-limit
          type="textarea"
          :rows="3"
          placeholder="请输入评论，最多 100 字"
        />
        <el-button type="primary" class="comment-submit" @click="submitComment">提交评论</el-button>
      </div>

      <div class="comment-list">
        <div v-for="comment in detail.comments" :key="comment.cid" class="comment-item">
          <el-avatar :src="getGravatarUrl(comment.email, 72)" />
          <div class="comment-content">
            <div class="comment-user">
              {{ comment.username }}（UID {{ comment.user_uid }}）
            </div>
            <div class="comment-text">{{ comment.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api/client'
import type { MemeDetail } from '../types'
import { getGravatarUrl } from '../utils/gravatar'

const props = defineProps<{
  modelValue: boolean
  detail: MemeDetail | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  refreshed: []
}>()

const visible = ref(false)
const ratingValue = ref(0)
const commentText = ref('')

watch(
  () => props.modelValue,
  (value) => {
    visible.value = value
  },
  { immediate: true }
)

watch(visible, (value) => emit('update:modelValue', value))

watch(
  () => props.detail,
  (value) => {
    ratingValue.value = value?.user_rating ?? 0
    commentText.value = ''
  }
)

function formatTime(value: string) {
  return new Date(value).toLocaleString()
}

async function submitRating() {
  if (!props.detail || ratingValue.value <= 0) {
    ElMessage.warning('请先选择评分')
    return
  }
  await api.post(`/memes/${props.detail.pid}/ratings`, { score: ratingValue.value })
  ElMessage.success('评分成功')
  emit('refreshed')
}

async function submitComment() {
  if (!props.detail || !commentText.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  await api.post(`/memes/${props.detail.pid}/comments`, { content: commentText.value.trim() })
  ElMessage.success('评论成功')
  commentText.value = ''
  emit('refreshed')
}
</script>
