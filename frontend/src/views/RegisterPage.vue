<template>
  <div class="auth-wrap">
    <el-card class="auth-card">
      <template #header>注册</template>
      <el-form :model="form" label-position="top" @submit.prevent="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-button type="primary" class="full-btn" @click="submit">注册并登录</el-button>
        <div class="auth-switch">
          已有账号？<router-link to="/login">去登录</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import type { AuthResponse } from '@/types'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({
  username: '',
  email: '',
  password: ''
})

async function submit() {
  const { data } = await api.post<AuthResponse>('/auth/register', form)
  auth.setAuth(data)
  ElMessage.success('注册成功')
  router.push('/')
}
</script>
