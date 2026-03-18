<template>
  <header class="topbar">
    <div class="brand">MemeClub</div>
    <el-input
      v-model="searchText"
      class="search-box"
      placeholder="搜索梗图标题、解释或用户"
      clearable
      @keyup.enter="emitSearch"
      @clear="emitSearch"
    >
      <template #append>
        <el-button @click="emitSearch">搜索</el-button>
      </template>
    </el-input>
    <el-menu mode="horizontal" :ellipsis="false" :router="true" class="nav-menu">
      <el-menu-item index="/">主页</el-menu-item>
      <el-menu-item index="/user">用户</el-menu-item>
      <el-menu-item index="/upload">上传梗图</el-menu-item>
      <el-menu-item v-if="auth.user?.user_status === 'admin'" index="/admin/review">审核台</el-menu-item>
    </el-menu>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{
  search: [value: string]
}>()

const auth = useAuthStore()
const searchText = ref('')

function emitSearch() {
  emit('search', searchText.value.trim())
}
</script>
