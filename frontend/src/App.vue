<template>
  <div class="app-shell">
    <AppHeader @search="onSearch" />
    <main class="page-shell">
      <router-view v-slot="{ Component, route }">
        <component :is="Component" :search-keyword="route.name === 'home' ? keyword : undefined" />
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import AppHeader from '@/components/AppHeader.vue'

const keyword = ref('')

function onSearch(value: string) {
  keyword.value = value
}
</script>
