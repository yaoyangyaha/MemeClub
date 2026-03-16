<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

const router = useRouter()
const form = reactive({ username: '', password: '', email: '' })

async function submit() {
  await api.post('/register', form)
  ElMessage.success('注册成功，请登录')
  router.push('/login')
}
</script>

<template>
  <el-card class="box">
    <h2>注册</h2>
    <el-form @submit.prevent="submit">
      <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
      <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
      <el-button type="primary" @click="submit">注册</el-button>
      <el-button link @click="router.push('/login')">去登录</el-button>
    </el-form>
  </el-card>
</template>

<style scoped>
.box { max-width: 460px; margin: 40px auto; }
</style>
