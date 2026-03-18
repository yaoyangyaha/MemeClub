import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UploadView from '@/views/UploadView.vue'
import UserCenterView from '@/views/UserCenterView.vue'
import { authState } from '@/state/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/upload', name: 'upload', component: UploadView },
    { path: '/user', name: 'user', component: UserCenterView },
  ],
})

router.beforeEach((to) => {
  if (['upload', 'user'].includes(String(to.name)) && !authState.uid) {
    return { name: 'login' }
  }
  return true
})

export default router
