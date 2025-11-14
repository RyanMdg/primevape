# Railway Deployment Guide - PrimeVape Backend

Complete guide to deploy your Flask backend to Railway with PostgreSQL.

---

## 🎯 What is Railway?

**Railway** is a modern platform for deploying apps:

✅ **$5 Free Credit** - Monthly free usage
✅ **PostgreSQL Included** - Free database addon
✅ **Auto Deploy** - Connects to GitHub
✅ **HTTPS** - Automatic SSL certificates
✅ **Easy Setup** - Detects Python/Flask automatically
✅ **Great for Neon** - Works perfectly with your Neon database

---

## 💰 Railway Pricing

**Free Trial**:
- $5 credit/month (enough for development)
- Resets every month
- Credit card required (but won't charge unless you exceed free tier)

**What $5 Gets You**:
- Backend running 24/7: ~$3/month
- **Neon Database** (external, stays free!)
- Enough for testing and small-scale production

---

## 🚀 Deployment Steps

### Step 1: Sign Up for Railway

1. Go to: **https://railway.app/**
2. Click **"Start a New Project"**
3. Sign in with **GitHub**
4. Authorize Railway to access your repositories

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`RyanMdg/primevape`** repository
4. Railway will detect your project

### Step 3: Configure Deployment

Railway will auto-detect Python/Flask, but let's configure it:

1. **Root Directory**: Click "Settings" → Set root directory to: `primevape-backend`

2. **Build Command** (auto-detected):
   ```
   pip install -r requirements.txt
   ```

3. **Start Command** (from Procfile):
   ```
   gunicorn app:app
   ```

### Step 4: Add Environment Variables

Click **"Variables"** tab and add these:

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `FLASK_ENV` | `production` | Production mode |
| `SECRET_KEY` | `your-secret-key-here-change-this` | Generate random string |
| `JWT_SECRET_KEY` | `your-jwt-secret-key-here-change-this` | Generate random string |
| `DATABASE_URL` | `postgresql://...` | Your Neon connection string |
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` | Your frontend URL |
| `HUGGINGFACE_API_KEY` | `hf_your_key_here` | Your HF key (optional) |

**IMPORTANT**: Use your actual Neon database URL from earlier!

**Example**:
```
DATABASE_URL=postgresql://neondb_owner:npg_cmRnUVfx47jK@ep-frosty-recipe-add19s87-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
CORS_ORIGINS=https://primevape-frontend.vercel.app,http://localhost:5173
```

### Step 5: Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Railway will show you the deployment URL

**Your backend URL will be**:
```
https://primevape-backend-production.up.railway.app
```

---

## 🗄️ Initialize Database

After first deployment, you need to create tables in Neon:

**Option 1: Via Railway CLI** (Recommended)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login:
   ```bash
   railway login
   ```

3. Link to your project:
   ```bash
   railway link
   ```

4. Run init script:
   ```bash
   railway run python init_db.py
   ```

**Option 2: Add Init on Startup** (Automatic)

We'll modify `app.py` to auto-create tables on first run (already done in your code!):

```python
# In app.py
with app.app_context():
    db.create_all()  # This creates tables automatically
```

Then manually run seed data:
1. Go to Railway dashboard
2. Click **"Deploy Logs"**
3. Once deployed, use Railway shell to run `python init_db.py`

---

## ✅ Verify Deployment

### Test Your API

1. **Health Check**:
   ```
   https://your-app.up.railway.app/health
   ```
   Should return: `{"status": "healthy"}`

2. **Get Products**:
   ```
   https://your-app.up.railway.app/api/products
   ```
   Should return list of products

3. **Check Root**:
   ```
   https://your-app.up.railway.app/
   ```
   Should return API info

---

## 🔧 Update Frontend to Use Railway Backend

1. **Go to Vercel Dashboard**
2. **Click your frontend project**
3. **Go to Settings → Environment Variables**
4. **Update `VITE_API_URL`**:
   ```
   VITE_API_URL=https://your-app.up.railway.app
   ```
5. **Redeploy frontend**

---

## 🔄 Auto-Deploy Setup

Railway automatically redeploys when you push to GitHub!

**Workflow**:
```bash
# Make changes to backend
cd primevape-backend
git add .
git commit -m "Updated API endpoint"
git push

# Railway automatically builds and deploys!
```

---

## 📊 Monitor Your Deployment

### Railway Dashboard

1. **Deployment Logs**: See build and runtime logs
2. **Metrics**: CPU, memory, network usage
3. **Usage**: Check remaining credit

### View Logs

Click **"Deployments"** → **"View Logs"** to see:
- Build logs
- Application logs
- Error messages

---

## 🐛 Troubleshooting

### Error: "Application failed to respond"

**Problem**: App not starting

**Solutions**:
1. Check build logs for errors
2. Verify `Procfile` exists: `web: gunicorn app:app`
3. Ensure `requirements.txt` has all dependencies
4. Check `runtime.txt` has correct Python version

### Error: "Database connection failed"

**Problem**: Can't connect to Neon

**Solutions**:
1. Verify `DATABASE_URL` environment variable
2. Check Neon connection string is correct
3. Ensure `?sslmode=require` is in connection string
4. Test Neon connection from Neon dashboard

### Error: "Module not found"

**Problem**: Missing Python packages

**Solutions**:
1. Add missing package to `requirements.txt`
2. Commit and push to trigger redeploy
3. Check Railway build logs

### Products Not Loading

**Problem**: Database tables don't exist

**Solutions**:
1. Run `python init_db.py` via Railway CLI
2. Check `db.create_all()` is in `app.py`
3. Verify Neon database has tables (use SQL Editor)

### CORS Errors

**Problem**: Frontend can't access backend

**Solutions**:
1. Update `CORS_ORIGINS` environment variable
2. Add your Vercel URL: `https://your-app.vercel.app`
3. Redeploy Railway app

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use strong secret keys** - Generate random strings
3. **Rotate secrets regularly** - Update in Railway dashboard
4. **Limit CORS origins** - Only allow your frontend domains
5. **Monitor usage** - Check Railway dashboard weekly

---

## 💡 Pro Tips

1. **Use Neon Database**: Free PostgreSQL, perfect with Railway
2. **Set up monitoring**: Railway has built-in metrics
3. **Enable auto-deploy**: Push to GitHub = auto-deploy
4. **Use staging**: Create separate Railway project for testing
5. **Check logs regularly**: Catch errors early

---

## 📚 Railway CLI Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run commands
railway run python init_db.py

# Open dashboard
railway open

# Deploy
railway up
```

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Procfile created
- [ ] runtime.txt created
- [ ] railway.json configured
- [ ] requirements.txt updated with gunicorn
- [ ] All environment variables ready
- [ ] Neon database URL copied
- [ ] GitHub repository up to date
- [ ] `.env` not committed (check `.gitignore`)

After deploying:

- [ ] Test health endpoint
- [ ] Test products endpoint
- [ ] Initialize database
- [ ] Verify tables exist in Neon
- [ ] Update frontend with backend URL
- [ ] Test full app functionality

---

## 🎯 Deployment Workflow Summary

```
1. Push backend code to GitHub
   ↓
2. Railway auto-detects changes
   ↓
3. Railway builds Python app
   ↓
4. Railway runs gunicorn
   ↓
5. App connects to Neon database
   ↓
6. Backend is live!
   ↓
7. Update Vercel with Railway URL
   ↓
8. Full stack deployed!
```

---

## 📦 What We Deployed

✅ **Flask Backend** - Running on Railway
✅ **Gunicorn Server** - Production WSGI server
✅ **Neon PostgreSQL** - Cloud database
✅ **Auto SSL** - HTTPS enabled
✅ **Environment Variables** - Secure configuration
✅ **Auto-deploy** - GitHub integration

---

## 🎉 You're Ready to Deploy!

**Files Created for Railway**:
- ✅ `Procfile` - Tells Railway how to start your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Updated with gunicorn

**Just follow the steps above and your backend will be live!** 🚀

---

## 📚 Resources

- **Railway Docs**: https://docs.railway.app/
- **Python Deployment**: https://docs.railway.app/guides/python
- **PostgreSQL**: https://docs.railway.app/databases/postgresql
- **Environment Variables**: https://docs.railway.app/develop/variables

---

**Ready to deploy? Let's get your backend live!** 🎉
