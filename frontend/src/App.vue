<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const search = ref('')

const active = computed(() => {
  if (route.path.startsWith('/user')) return '/user'
  if (route.path.startsWith('/upload')) return '/upload'
  return '/'
})

function onSearch() {
  router.push({ path: '/', query: { q: search.value } })
}

function goTab(index: string) {
  router.push(index)
}
</script>

<template>
  <el-container class="layout">
    <el-header class="header">
      <div class="top">
        <el-input v-model="search" placeholder="搜索梗图标题或说明" @keyup.enter="onSearch">
          <template #append>
            <el-button :icon="Search" @click="onSearch" />
          </template>
        </el-input>
      </div>
      <el-menu mode="horizontal" :default-active="active" @select="goTab">
        <el-menu-item index="/">主页</el-menu-item>
        <el-menu-item index="/user">用户中心</el-menu-item>
        <el-menu-item index="/upload">上传梗图</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped>
.layout { min-height: 100vh; }
.header { height: auto; display: flex; flex-direction: column; gap: 10px; padding-top: 10px; }
.top { max-width: 720px; }
</style>
