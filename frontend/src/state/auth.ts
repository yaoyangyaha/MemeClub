import { reactive } from 'vue'

export const authState = reactive({
  uid: Number(localStorage.getItem('uid') || 0),
  username: localStorage.getItem('username') || '',
  userStatus: localStorage.getItem('user_status') || '',
})

export function setAuth(uid: number, username: string, userStatus: string) {
  authState.uid = uid
  authState.username = username
  authState.userStatus = userStatus
  localStorage.setItem('uid', String(uid))
  localStorage.setItem('username', username)
  localStorage.setItem('user_status', userStatus)
}

export function clearAuth() {
  authState.uid = 0
  authState.username = ''
  authState.userStatus = ''
  localStorage.removeItem('uid')
  localStorage.removeItem('username')
  localStorage.removeItem('user_status')
}
