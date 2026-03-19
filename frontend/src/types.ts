export interface UserSummary {
  uid: number
  username: string
  email: string
  user_status: 'admin' | 'user'
  is_banned: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: UserSummary
}

export interface MemeCardItem {
  pid: number
  title: string
  image_base64: string
  created_at: string
  uploader_uid: number
  uploader_name: string
  uploader_email: string
  review_status: 'pending' | 'approved' | 'rejected'
  average_rating: number
  favorite_count: number
  comment_count: number
  is_favorited: boolean
}

export interface MemeListResponse {
  total: number
  page: number
  page_size: number
  items: MemeCardItem[]
}

export interface CommentItem {
  cid: number
  content: string
  created_at: string
  user_uid: number
  username: string
  email: string
}

export interface MemeDetail {
  pid: number
  title: string
  description: string
  image_base64: string
  created_at: string
  review_status: string
  uploader_uid: number
  uploader_name: string
  uploader_email: string
  average_rating: number
  user_rating: number | null
  favorite_count: number
  comment_count: number
  is_favorited: boolean
  comments: CommentItem[]
}

export interface UserProfile {
  user: UserSummary
  submitted_memes: MemeCardItem[]
}
