# Deployment Guide - Travel Destination Recommendation System

## 🚀 Deploy to Vercel

### Prerequisites
1. A Vercel account (sign up at https://vercel.com)
2. Git installed on your computer
3. Your project pushed to GitHub, GitLab, or Bitbucket

### Step-by-Step Deployment

#### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**
   ```bash
   cd "/Users/shankarlaxmansanti/clg project/TRAVEL DESTINATION RECOMMENDATION SYSTEM"
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name? `travel-destination` (or your preferred name)
   - In which directory is your code located? `./`
   - Want to override settings? `N`

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

#### Option 2: Deploy via Vercel Dashboard

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/dashboard
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect the Flask app
   - Click "Deploy"

### ⚠️ Important Notes

#### Database Limitations on Vercel
Vercel is a **serverless platform**, which means:
- SQLite databases are **ephemeral** (reset on each deployment)
- Data is stored in `/tmp` and cleared periodically
- **Not suitable for production with SQLite**

#### Recommended Solutions:

1. **Use a Cloud Database** (Recommended for Production)
   - **PostgreSQL**: Supabase, Neon, Railway
   - **MySQL**: PlanetScale, Railway
   - **MongoDB**: MongoDB Atlas

2. **Migrate to PostgreSQL** (Best Option)
   ```bash
   pip install psycopg2-binary
   ```
   Update `database.py` to use PostgreSQL instead of SQLite

3. **Use Vercel Postgres** (Vercel's managed database)
   - Add Vercel Postgres from the Vercel dashboard
   - Update connection string in environment variables

### Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

```
SECRET_KEY=your-secret-key-here-change-this
VERCEL=1
```

### Post-Deployment

After deployment, your app will be available at:
```
https://your-project-name.vercel.app
```

### Troubleshooting

**Issue: Database resets on every request**
- Solution: Migrate to a persistent database (PostgreSQL, MySQL)

**Issue: Static files not loading**
- Check that `static/` folder is included in deployment
- Verify paths in templates use `url_for('static', filename='...')`

**Issue: 500 Internal Server Error**
- Check Vercel logs: `vercel logs`
- Verify all dependencies are in `requirements.txt`

**Issue: Cold starts are slow**
- This is normal for serverless functions
- Consider upgrading to Vercel Pro for better performance

### Alternative Deployment Options

If Vercel doesn't work well with SQLite:

1. **Railway** (https://railway.app) - Better for SQLite
2. **Render** (https://render.com) - Supports persistent storage
3. **PythonAnywhere** (https://www.pythonanywhere.com) - Good for Flask + SQLite
4. **Heroku** (https://heroku.com) - Classic PaaS option

### Need Help?

- Vercel Documentation: https://vercel.com/docs
- Flask on Vercel: https://vercel.com/guides/using-flask-with-vercel
- Contact: shankarsanti2005@gmail.com
