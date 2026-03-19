<template>
  <div class="form-page">
    <el-card class="form-card">
      <template #header>上传梗图</template>
      <el-alert
        v-if="auth.user?.is_banned"
        type="error"
        show-icon
        title="当前账号已被封禁，无法提交梗图"
        :closable="false"
      />
      <el-form v-else label-position="top">
        <el-form-item label="图片">
          <input type="file" accept="image/*" @change="handleFile" />
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="form.title" maxlength="60" show-word-limit />
        </el-form-item>
        <el-form-item label="详情解释">
          <el-input v-model="form.description" type="textarea" :rows="5" maxlength="2000" show-word-limit />
        </el-form-item>
        <el-button type="primary" @click="submit">提交审核</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api/client'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const form = reactive({
  title: '',
  description: '',
  image_base64: ''
})

function handleFile(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    form.image_base64 = String(reader.result)
  }
  reader.readAsDataURL(file)
}

async function submit() {
  if (!form.image_base64) {
    ElMessage.warning('请先选择图片')
    return
  }
  await api.post('/memes', form)
  ElMessage.success('上传成功，等待审核')
  form.title = ''
  form.description = ''
  form.image_base64 = ''
}
</script>
