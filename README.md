# MemeClub

一个使用 Vue 3 + TypeScript + Element Plus + Vue Router 构建前端，FastAPI + 纯MySQL 构建后端的梗图社区网站。

## 目录结构

```text
MemeClub/
├── backend
├── frontend
└── docs
```

## 后端启动

1. 复制环境变量模板
```bash
cd backend
cp .env.example .env
```
2. 初始化数据库
```bash
mysql -u root -p < init_db.sql
```
3. 安装依赖并启动
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

## VitePress 文档

```bash
cd docs
npm install
npm run docs:dev
```

## 说明

- 全部信息均用数据库存储
- 文本与图片字段按需求以 Base64 字符串形式存储。
- 用户身份由 `users.user_status` 控制，`admin` 为管理员，`user` 为普通用户。
- 如果需要更换头像镜像站，修改 [frontend/src/config.ts](frontend/src/config.ts) 里的 `GRAVATAR_BASE_URL` 即可。
- 如果前端不是从 `http://localhost:5173` 或 `http://127.0.0.1:5173` 启动，记得同步修改后端 `.env` 里的 `FRONTEND_ORIGINS`。
- 本项目遵循`MIT License`

感谢各位的支持！欢迎大家fork项目、提交Issue和PR！

### 贡献者：
<a href="https://github.com/yaoyangyaha/MemeClub/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yaoyangyaha/MemeClub"  alt="Contributors"/>
</a>


### Buy Me A Coffee~
[ClickMe](https://afdian.com/a/YAOYANGYAHA666)
