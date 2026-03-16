<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

const form = reactive({ title: '', description: '', image_base64: '' })

function onFileChange(file: File) {
  const reader = new FileReader()
  reader.onload = () => {
    form.image_base64 = String(reader.result || '')
  }
  reader.readAsDataURL(file)
}

async function submit() {
  await api.post('/upload', form)
  ElMessage.success('上传成功，等待管理员审核')
  form.title = ''
  form.description = ''
  form.image_base64 = ''
}
</script>

<template>
  <el-card class="box">
    <h2>上传梗图</h2>
    <el-form>
      <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
      <el-form-item label="详情解释"><el-input v-model="form.description" type="textarea" /></el-form-item>
      <el-form-item label="图片">
        <el-upload :auto-upload="false" :show-file-list="false" accept="image/*" :on-change="(f) => onFileChange(f.raw!)">
          <el-button>选择图片</el-button>
        </el-upload>
      </el-form-item>
      <el-image v-if="form.image_base64" :src="form.image_base64" style="width: 200px; margin-bottom: 8px" />
      <el-button type="primary" @click="submit">提交审核</el-button>
    </el-form>
  </el-card>
</template>

<style scoped>
.box { max-width: 700px; margin: 24px auto; }
</style>
