<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api } from '@/api'
import { setAuth } from '@/state/auth'

const router = useRouter()
const form = reactive({ username: '', password: '' })

async function submit() {
  const { data } = await api.post('/login', form)
  setAuth(data.uid, data.username, data.user_status)
  ElMessage.success('登录成功')
  router.push('/')
}
</script>

<template>
  <el-card class="box">
    <h2>登录</h2>
    <el-form @submit.prevent="submit">
      <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
      <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
      <el-button type="primary" @click="submit">登录</el-button>
      <el-button link @click="router.push('/register')">去注册</el-button>
    </el-form>
  </el-card>
</template>

<style scoped>
.box { max-width: 420px; margin: 40px auto; }
</style>
