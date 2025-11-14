# Render Deployment Guide - PrimeVape Backend

Complete guide to deploy your Flask backend to Render with PostgreSQL (100% FREE).

---

## 🎯 What is Render?

**Render** is a modern cloud platform for deploying apps:

✅ **Completely FREE** - Free tier for web services and databases
✅ **PostgreSQL Included** - Free PostgreSQL database (750 hours/month)
✅ **Auto Deploy** - Connects to GitHub for automatic deployments
✅ **HTTPS** - Automatic SSL certificates
✅ **Easy Setup** - Detects Python/Flask automatically
✅ **Great for Production** - Reliable and fast

---

## 💰 Render Pricing

**Free Tier** (Perfect for your project):
- Web Service: FREE (with limitations)
- PostgreSQL Database: FREE (750 hours/month)
- HTTPS: FREE
- Custom domains: FREE
- No credit card required

**Free Tier Limitations**:
- Services spin down after 15 minutes of inactivity
- Spins up when accessed (takes ~30 seconds)
- 750 hours/month free (enough for continuous operation)

**Perfect for**:
- Development and testing
- Portfolio projects
- Low to medium traffic sites
- Learning and experimentation

---

## 🚀 Deployment Steps

### Step 1: Sign Up for Render

1. Go to: **https://render.com/**
2. Click **"Get Started"**
3. Sign up with **GitHub**
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select **`RyanMdg/primevape`** repository
5. Click **"Connect"**

### Step 3: Configure Web Service

Render will show configuration form:

**Basic Settings**:
- **Name**: `primevape-backend`
- **Region**: Choose closest to you (e.g., Singapore)
- **Branch**: `main`
- **Root Directory**: `primevape-backend`

**Build Settings**:
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

Render should auto-detect these from your `render.yaml`!

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `FLASK_ENV` | `production` | Production mode |
| `SECRET_KEY` | Click "Generate" | Auto-generate secure key |
| `JWT_SECRET_KEY` | Click "Generate" | Auto-generate secure key |
| `DATABASE_URL` | (See Step 5) | Your Neon connection string |
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` | Your frontend URL |
| `HUGGINGFACE_API_KEY` | `hf_your_key_here` | Your HF key (optional) |

**IMPORTANT**: We'll add `DATABASE_URL` in the next step after setting up Neon!

### Step 5: Set Up Neon Database

You already have Neon set up! Use your existing connection string:

```
postgresql://neondb_owner:npg_cmRnUVfx47jK@ep-frosty-recipe-add19s87-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

Add this as the `DATABASE_URL` environment variable in Render.

**Why use Neon instead of Render's PostgreSQL?**
- Neon is serverless (always available, no spin down)
- Neon has more generous free tier limits
- You already have it configured with your data!

### Step 6: Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. Wait 3-5 minutes for initial deployment
4. You'll see build logs in real-time

**Your backend URL will be**:
```
https://primevape-backend.onrender.com
```

Or similar (Render will show you the exact URL).

---

## 🗄️ Database is Already Set Up!

Good news! Your Neon database is already initialized with:
- ✅ All tables created
- ✅ 11 products
- ✅ 3 categories
- ✅ 1 admin user

**No additional setup needed!** Just make sure `DATABASE_URL` environment variable is set correctly in Render.

---

## ✅ Verify Deployment

### Test Your API

1. **Health Check**:
   ```
   https://primevape-backend.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

2. **Get Products**:
   ```
   https://primevape-backend.onrender.com/api/products
   ```
   Should return list of 11 products

3. **Check Root**:
   ```
   https://primevape-backend.onrender.com/
   ```
   Should return API info

**Note**: First request after inactivity takes ~30 seconds (free tier spin-up time).

---

## 🔧 Update Frontend to Use Render Backend

### Option 1: Via Vercel Dashboard

1. Go to **Vercel Dashboard**
2. Click your frontend project
3. Go to **Settings → Environment Variables**
4. Update `VITE_API_URL`:
   ```
   VITE_API_URL=https://primevape-backend.onrender.com
   ```
5. Go to **Deployments** → Click **"Redeploy"**

### Option 2: Update `.env.production` and Push

1. Update `/primevape-frontend/.env.production`:
   ```
   VITE_API_URL=https://primevape-backend.onrender.com
   ```

2. Commit and push:
   ```bash
   git add .
   git commit -m "Update production API URL for Render"
   git push
   ```

3. Vercel will auto-deploy with new environment variable

---

## 🔄 Auto-Deploy Setup

Render automatically redeploys when you push to GitHub!

**Workflow**:
```bash
# Make changes to backend
cd primevape-backend
# Edit your files
git add .
git commit -m "Updated API endpoint"
git push

# Render automatically builds and deploys!
```

**Auto-deploy settings**:
- ✅ Already enabled by default
- ✅ Watches `main` branch
- ✅ Deploys on every push
- ✅ Shows build status in dashboard

---

## 📊 Monitor Your Deployment

### Render Dashboard Features

1. **Logs**: Real-time application logs
2. **Events**: Deployment history
3. **Metrics**: CPU, memory, network usage
4. **Shell**: Access to your running service

### View Logs

1. Go to Render Dashboard
2. Click your service
3. Click **"Logs"** tab
4. See real-time logs from your app

### Access Shell (for debugging)

1. Click **"Shell"** tab
2. Opens terminal into your running container
3. Run commands like `python init_db.py` if needed

---

## 🐛 Troubleshooting

### Error: "Build failed"

**Problem**: Dependencies not installing

**Solutions**:
1. Check `requirements.txt` is in `primevape-backend` folder
2. Verify root directory is set to `primevape-backend`
3. Check build logs for specific error
4. Ensure Python 3.13 is compatible (try 3.11 in `runtime.txt` if issues)

### Error: "Application failed to respond"

**Problem**: App not starting correctly

**Solutions**:
1. Verify start command: `gunicorn app:app`
2. Check `app.py` exists in `primevape-backend`
3. Review logs for Python errors
4. Ensure all environment variables are set

### Error: "Database connection failed"

**Problem**: Can't connect to Neon

**Solutions**:
1. Verify `DATABASE_URL` environment variable is correct
2. Check Neon connection string includes `?sslmode=require`
3. Test Neon connection from Neon dashboard
4. Ensure Neon database is not suspended (check Neon dashboard)

### Slow Response Times

**Problem**: First request takes 30+ seconds

**Explanation**: This is normal for free tier!
- Services spin down after 15 minutes of inactivity
- First request wakes up the service (~30 seconds)
- Subsequent requests are fast

**Solutions** (if you need faster response):
1. Upgrade to Render paid tier ($7/month - no spin down)
2. Use a service like UptimeRobot to ping your API every 14 minutes
3. Accept the delay (normal for free hosting)

### Products Not Loading

**Problem**: API returns empty products

**Solutions**:
1. Check `DATABASE_URL` is pointing to your Neon database
2. Verify Neon database has data (use Neon SQL Editor)
3. Run `init_db.py` again if needed via Shell tab

### CORS Errors in Frontend

**Problem**: Frontend can't access backend

**Solutions**:
1. Update `CORS_ORIGINS` environment variable in Render
2. Add your Vercel URL: `https://your-app.vercel.app`
3. Multiple origins: `https://app1.vercel.app,https://app2.vercel.app`
4. Redeploy service after updating

---

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit `.env` files (already in `.gitignore`)
2. **Secret Keys**: Use Render's "Generate" button for secrets
3. **CORS Origins**: Only allow your specific frontend domains
4. **Database**: Neon uses SSL by default (`?sslmode=require`)
5. **HTTPS**: Render provides free SSL automatically

---

## 💡 Pro Tips

1. **Use Neon Database**: Free, serverless, and always available
2. **Monitor Logs**: Check regularly for errors
3. **Set up notifications**: Render can email you on deploy failures
4. **Use custom domain**: Free on Render (add in Settings)
5. **Check service status**: Render has status page for outages

---

## 📱 Render CLI (Optional)

Install Render CLI for advanced features:

```bash
# Install
npm install -g @render/cli

# Login
render login

# View logs
render logs primevape-backend

# Run commands
render shell primevape-backend
```

---

## 🔧 Configuration Files

Your project includes these Render config files:

### `render.yaml`
Defines your service configuration:
- Service type (web)
- Environment (python)
- Build and start commands
- Environment variables
- Region

### `build.sh`
Build script that runs during deployment:
- Installs Python dependencies
- Runs before start command

### `Procfile`
Alternative process definition:
- Tells Render how to start your app
- `web: gunicorn app:app`

---

## ✅ Deployment Checklist

**Before deploying**:

- [x] Procfile created
- [x] runtime.txt created (Python 3.13.0)
- [x] render.yaml configured
- [x] build.sh created
- [x] requirements.txt includes gunicorn, psycopg2-binary
- [x] Neon database set up and populated
- [x] GitHub repository up to date
- [x] `.env` not committed (in `.gitignore`)

**After deploying**:

- [ ] Create Web Service on Render
- [ ] Set root directory to `primevape-backend`
- [ ] Add all environment variables
- [ ] Wait for build to complete
- [ ] Test health endpoint
- [ ] Test products endpoint
- [ ] Update Vercel with Render backend URL
- [ ] Redeploy frontend
- [ ] Test full app functionality

---

## 🎯 Deployment Workflow Summary

```
1. Push backend code to GitHub
   ↓
2. Render detects changes automatically
   ↓
3. Render runs build.sh (installs dependencies)
   ↓
4. Render starts gunicorn server
   ↓
5. App connects to Neon PostgreSQL
   ↓
6. Backend is live at https://yourapp.onrender.com
   ↓
7. Update Vercel frontend with Render URL
   ↓
8. Full stack deployed! 🎉
```

---

## 📦 What You're Deploying

✅ **Flask Backend** - Running on Render (FREE)
✅ **Gunicorn Server** - Production WSGI server
✅ **Neon PostgreSQL** - Serverless database (FREE)
✅ **Auto SSL/HTTPS** - Secure by default
✅ **Environment Variables** - Secure configuration
✅ **Auto-deploy** - GitHub integration
✅ **Real-time Logs** - Debug and monitor

---

## 🆚 Render vs Railway

| Feature | Render (FREE) | Railway (PAID) |
|---------|---------------|----------------|
| Cost | $0/month | $5/month minimum |
| Web Service | ✅ Free | ❌ Requires credit |
| PostgreSQL | ✅ Free (750hrs) | ✅ Included |
| Auto-deploy | ✅ Yes | ✅ Yes |
| HTTPS | ✅ Free | ✅ Free |
| Custom Domain | ✅ Free | ✅ Free |
| Spin Down | After 15 min | No |
| Perfect for | Development, portfolios | Production apps |

**Recommendation**: Start with Render (free), upgrade to Railway if you need 24/7 uptime.

---

## 🎉 You're Ready to Deploy!

**Files Ready for Render**:
- ✅ `render.yaml` - Service configuration
- ✅ `build.sh` - Build script
- ✅ `Procfile` - Process definition
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies with gunicorn

**Just follow the steps above and your backend will be live for FREE!** 🚀

---

## 📚 Useful Resources

- **Render Docs**: https://render.com/docs
- **Python on Render**: https://render.com/docs/deploy-flask
- **Environment Variables**: https://render.com/docs/environment-variables
- **Free Tier**: https://render.com/docs/free
- **Neon + Render**: https://neon.tech/docs/guides/render

---

## 🚨 Common Questions

### Q: Why does my API take 30 seconds to respond sometimes?

**A**: Free tier services spin down after 15 minutes of inactivity. First request wakes it up. This is normal!

### Q: Can I keep my service always running?

**A**: Yes! Upgrade to Render's paid tier ($7/month) or use UptimeRobot to ping every 14 minutes.

### Q: Do I need to create a new database on Render?

**A**: No! Use your existing Neon database - it's better and always available.

### Q: Will I be charged anything?

**A**: No! Render's free tier doesn't require a credit card and won't charge you.

### Q: How do I check if my service is sleeping?

**A**: Look at the Render dashboard - it shows service status (sleeping/active).

---

**Ready to deploy? Your backend will be live and FREE on Render!** 🎊
