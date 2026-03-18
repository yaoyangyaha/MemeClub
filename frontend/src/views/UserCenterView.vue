<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api, GRAVATAR_BASE_URL } from '@/api'
import { authState, clearAuth } from '@/state/auth'
import { md5 } from '@/utils'
import type { Meme } from '@/types'

const router = useRouter()
const me = reactive({ uid: 0, username: '', email: '', is_banned: false, user_status: '' })
const myMemes = ref<Meme[]>([])
const pendingMemes = ref<Meme[]>([])
const users = ref<Array<{ uid: number; username: string; is_banned: boolean; user_status: string }>>([])
const banForm = reactive({ uid: 0, banned: true })

function avatarUrl(seed: string) {
  return `${GRAVATAR_BASE_URL}${md5(seed.toLowerCase())}?s=120&d=identicon`
}

async function loadMe() {
  try {
    const { data } = await api.get('/me')
    Object.assign(me, data)
    myMemes.value = data.my_memes
    if (authState.userStatus === 'admin') {
      const [pendingRes, usersRes] = await Promise.all([api.get('/admin/pending'), api.get('/admin/users')])
      pendingMemes.value = pendingRes.data.items
      users.value = usersRes.data.items
    }
  } catch {
    router.push('/login')
  }
}

async function logout() {
  try {
    await api.post('/logout')
  } finally {
    clearAuth()
    router.push('/login')
  }
}

async function setBan(uid: number, banned: boolean) {
  try {
    await api.post('/admin/ban', { uid, banned })
    ElMessage.success('用户状态已更新')
    await loadMe()
  } catch {
    // handled by axios interceptor
  }
}

async function review(pid: number, status: 'approved' | 'rejected') {
  try {
    await api.post(`/admin/meme/${pid}/review`, { status })
    ElMessage.success('审核完成')
    await loadMe()
  } catch {
    // handled by axios interceptor
  }
}

async function banUploader(uid: number) {
  try {
    await api.post('/admin/ban-uploader', { uid })
    ElMessage.success('发布者已封禁')
    await loadMe()
  } catch {
    // handled by axios interceptor
  }
}

onMounted(loadMe)
</script>

<template>
  <el-card>
    <el-space>
      <el-avatar :size="80" :src="avatarUrl(me.email || me.username)" />
      <div>
        <h2>{{ me.username }}</h2>
        <p>UID: {{ me.uid }}</p>
        <p>封禁状态: {{ me.is_banned ? '已封禁' : '正常' }}</p>
      </div>
    </el-space>
    <el-button type="danger" plain @click="logout">退出登录</el-button>
  </el-card>

  <el-card class="mt" header="我发布的梗图">
    <el-row :gutter="10">
      <el-col v-for="m in myMemes" :key="m.pid" :xs="24" :md="8">
        <el-card>
          <el-image :src="m.image_base64" fit="cover" style="height: 160px; width: 100%" />
          <div>{{ m.title }}</div>
          <small>状态: {{ m.status }}</small>
        </el-card>
      </el-col>
    </el-row>
  </el-card>

  <template v-if="authState.userStatus === 'admin'">
    <el-card class="mt" header="管理员封禁用户">
      <el-form inline>
        <el-form-item label="UID"><el-input-number v-model="banForm.uid" :min="1" /></el-form-item>
        <el-form-item label="封禁">
          <el-switch v-model="banForm.banned" active-text="封禁" inactive-text="解封" />
        </el-form-item>
        <el-form-item><el-button type="primary" @click="setBan(banForm.uid, banForm.banned)">提交</el-button></el-form-item>
      </el-form>
    </el-card>

    <el-card class="mt" header="待审核图片列表">
      <el-table :data="pendingMemes">
        <el-table-column prop="pid" label="PID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column label="图片">
          <template #default="scope"><el-image :src="scope.row.image_base64" style="width: 80px; height: 80px" fit="cover" /></template>
        </el-table-column>
        <el-table-column label="操作" width="280">
          <template #default="scope">
            <el-button type="success" size="small" @click="review(scope.row.pid, 'approved')">通过</el-button>
            <el-button type="warning" size="small" @click="review(scope.row.pid, 'rejected')">拒绝</el-button>
            <el-button type="danger" size="small" @click="banUploader(scope.row.uploader_uid)">封禁发布者</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card class="mt" header="全部用户列表">
      <el-table :data="users">
        <el-table-column prop="uid" label="UID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="user_status" label="身份" />
        <el-table-column label="封禁状态">
          <template #default="scope">{{ scope.row.is_banned ? '已封禁' : '正常' }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </template>
</template>

<style scoped>
.mt { margin-top: 14px; }
</style>
