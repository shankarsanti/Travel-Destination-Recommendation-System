# 🚀 Quick Deployment to Vercel

## Method 1: One-Command Deploy (Easiest)

```bash
./deploy.sh
```

## Method 2: Manual Deploy

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel --prod
```

## ⚠️ IMPORTANT: Database Warning

**Vercel uses serverless functions, which means:**
- Your SQLite database will be **reset on every deployment**
- Data is **not persistent** between requests
- This is **NOT suitable for production**

### Solutions:

1. **For Testing Only**: Deploy as-is (data will reset)

2. **For Production**: Use a cloud database
   - **Recommended**: Supabase (PostgreSQL) - Free tier available
   - **Alternative**: MongoDB Atlas, PlanetScale, Railway

## After Deployment

Your app will be live at:
```
https://your-project-name.vercel.app
```

## Need Help?

Read the full guide: `DEPLOYMENT.md`
