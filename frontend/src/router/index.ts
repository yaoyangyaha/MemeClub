import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import AdminReviewPage from '@/views/AdminReviewPage.vue'
import HomePage from '@/views/HomePage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import UploadPage from '@/views/UploadPage.vue'
import UserCenterPage from '@/views/UserCenterPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/login', name: 'login', component: LoginPage, meta: { guestOnly: true } },
    { path: '/register', name: 'register', component: RegisterPage, meta: { guestOnly: true } },
    { path: '/upload', name: 'upload', component: UploadPage, meta: { requiresAuth: true } },
    { path: '/user', name: 'user', component: UserCenterPage, meta: { requiresAuth: true } },
    { path: '/admin/review', name: 'admin-review', component: AdminReviewPage, meta: { requiresAuth: true, requiresAdmin: true } }
  ]
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  await auth.bootstrap()

  if (to.meta.requiresAuth && !auth.user) {
    return { name: 'login' }
  }
  if (to.meta.guestOnly && auth.user) {
    return { name: 'home' }
  }
  if (to.meta.requiresAdmin && auth.user?.user_status !== 'admin') {
    return { name: 'home' }
  }
  return true
})

export default router
