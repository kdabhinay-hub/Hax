# 🚀 Deploy on Heroku - Automatic

## One-Click Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kdabhinay-hub/Hax)

## Manual Deploy

### 1. Install Heroku CLI
```bash
npm install -g heroku
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create App
```bash
heroku create your-app-name
```

### 4. Set Environment Variables
```bash
heroku config:set BOT_TOKEN=your_token
heroku config:set CHAT_ID=your_chat_id
heroku config:set MONGODB_URI=your_mongodb_uri
```

### 5. Deploy
```bash
git push heroku main
```

### 6. View Logs
```bash
heroku logs --tail
```

---

**Bot is now live on Heroku! 🤖✨**
