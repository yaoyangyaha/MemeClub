<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { api, GRAVATAR_BASE_URL } from '@/api'
import type { MemeDetail } from '@/types'
import { md5 } from '@/utils'

const props = defineProps<{ modelValue: boolean; pid: number | null }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: boolean): void; (e: 'updated'): void }>()

const open = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit('update:modelValue', v),
})

const detail = ref<MemeDetail | null>(null)
const currentRate = ref(0)
const commentText = ref('')

watch(
  () => [props.modelValue, props.pid],
  async ([visible, pid]) => {
    if (visible && pid) {
      const { data } = await api.get(`/meme/${pid}`)
      detail.value = data
      currentRate.value = data.user_rating || 0
    }
  },
)

function avatarUrl(seed: string) {
  return `${GRAVATAR_BASE_URL}${md5(seed.toLowerCase())}?s=40&d=identicon`
}

async function submitRate() {
  if (!props.pid || !currentRate.value) return
  await api.post('/rate', { pid: props.pid, rating: currentRate.value })
  ElMessage.success('评分成功')
  emit('updated')
}

async function submitComment() {
  if (!props.pid || !commentText.value.trim()) return
  await api.post('/comment', { pid: props.pid, content: commentText.value.trim() })
  commentText.value = ''
  const { data } = await api.get(`/meme/${props.pid}`)
  detail.value = data
  emit('updated')
}
</script>

<template>
  <el-drawer v-model="open" direction="rtl" size="60%" :with-header="false">
    <template v-if="detail">
      <el-image style="width: 100%; max-height: 360px" :src="detail.image_base64" fit="contain" :preview-src-list="[detail.image_base64]" />
      <h2>{{ detail.title }}</h2>
      <p>{{ detail.description }}</p>
      <p>上传者：{{ detail.uploader_name }} (UID: {{ detail.uploader_uid }})</p>
      <p>上传时间：{{ detail.created_at }}</p>
      <p>综合评分：{{ detail.avg_rating }}</p>
      <el-divider />
      <el-space>
        <el-rate v-model="currentRate" allow-half />
        <el-button type="primary" @click="submitRate">提交评分</el-button>
      </el-space>
      <el-divider />
      <h3>评论区 ({{ detail.comment_count }})</h3>
      <el-input v-model="commentText" type="textarea" :maxlength="100" show-word-limit />
      <el-button class="mt8" type="primary" @click="submitComment">提交评论</el-button>
      <el-divider />
      <el-space direction="vertical" fill style="width: 100%">
        <div v-for="comment in detail.comments" :key="comment.id" class="comment-item">
          <el-avatar :src="avatarUrl(comment.username)" />
          <div>
            <strong>{{ comment.username }}</strong>
            <p>{{ comment.content }}</p>
          </div>
        </div>
      </el-space>
    </template>
  </el-drawer>
</template>

<style scoped>
.comment-item { display: flex; gap: 8px; align-items: flex-start; }
.mt8 { margin-top: 8px; }
</style>
