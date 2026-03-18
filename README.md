# MemeClub

基于 **Vue3 + TypeScript + Vite + Vue Router + Element Plus** 和 **FastAPI + MySQL** 的梗图社区。

## 功能覆盖

- 注册、登录（JWT + Cookie，有效期 1 年）
- 首页搜索 / 卡片流 / 50 条分页 / 按 PID 倒序
- 上传梗图（图片 base64 + 标题 + 解释）
- 详情抽屉（大图预览、评分、评论）
- 收藏 / 取消收藏
- 用户中心（头像、UID、封禁状态、我的梗图、退出登录）
- 管理员审核图片（通过/拒绝）
- 管理员按 UID 封禁/解封用户；可直接封禁待审核梗图发布者
- 用户角色通过 `users.user_status` 字段控制：`admin` 或 `user`

## 数据库

使用 `init.sql` 初始化 MySQL：

```bash
mysql -uroot -ppassword < init.sql
```

默认会创建：

- users
- memes
- ratings
- comments
- favorites

并插入一个管理员账号：`admin / admin123`。

## 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

可通过环境变量覆盖数据库：

```bash
export DATABASE_URL='mysql+pymysql://root:password@localhost:3306/meme_site'
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

可配置环境变量：

- `VITE_API_BASE`：后端地址（默认 `http://127.0.0.1:8000`）
- `VITE_GRAVATAR_BASE_URL`：Gravatar 镜像前缀（默认 `https://www.gravatar.com/avatar/`）
- `CORS_ALLOW_ORIGINS`：后端允许跨域来源，逗号分隔（默认已包含 `localhost/127.0.0.1` 的 `5173/4173`）

> 说明：前端除了 `HttpOnly Cookie` 外，也会把登录返回的 token 作为 Bearer Token 附带在请求头中，避免本地开发时因为 `localhost` 和 `127.0.0.1` 混用导致 Cookie 未携带，从而出现上传、评论等接口 401。

## API 概览

- `POST /register`
- `POST /login`
- `POST /logout`
- `GET /me`
- `GET /memes?page=1&q=关键词`
- `GET /meme/{pid}`
- `POST /upload`
- `POST /rate`
- `POST /comment`
- `POST /favorite`
- `GET /admin/pending`
- `POST /admin/meme/{pid}/review`
- `POST /admin/ban`
- `POST /admin/ban-uploader`
- `GET /admin/users`
