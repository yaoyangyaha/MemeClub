<template>
  <div class="auth-wrap">
    <el-card class="auth-card">
      <template #header>登录</template>
      <el-form :model="form" label-position="top" @submit.prevent="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-button type="primary" class="full-btn" @click="submit">登录</el-button>
        <div class="auth-switch">
          没有账号？<router-link to="/register">去注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import api from '../api/client'
import { useAuthStore } from '../stores/auth'
import type { AuthResponse } from '../types'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({
  username: '',
  password: ''
})

async function submit() {
  const { data } = await api.post<AuthResponse>('/auth/login', form)
  auth.setAuth(data)
  ElMessage.success('登录成功')
  router.push('/')
}
</script>
