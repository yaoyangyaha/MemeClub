export interface Meme {
  pid: number
  title: string
  description: string
  image_base64: string
  uploader_uid: number
  uploader_name: string
  status: string
  created_at: string
  avg_rating: number
  is_favorite: boolean
  user_rating: number | null
}

export interface CommentItem {
  id: number
  uid: number
  username: string
  content: string
  created_at: string
}

export interface MemeDetail extends Meme {
  comment_count: number
  comments: CommentItem[]
}
