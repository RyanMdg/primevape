# PrimeVape Vercel Deployment Guide

Complete guide to deploy your PrimeVape React frontend to Vercel.

---

## 🎯 What is Vercel?

**Vercel** is the BEST platform for deploying React/Next.js apps:

✅ **FREE Tier** - Generous free plan
✅ **Auto Deploy** - Connects to GitHub, auto-deploys on push
✅ **Global CDN** - Super fast worldwide
✅ **HTTPS** - Automatic SSL certificates
✅ **Custom Domains** - Free custom domain support
✅ **Zero Config** - Detects React/Vite automatically

---

## 📋 Prerequisites

Before deploying to Vercel, you need:

1. ✅ **Frontend Ready** (already done!)
2. ✅ **Backend Deployed** (must do first - see options below)
3. ✅ **GitHub Account** (to connect your repo)
4. ✅ **Vercel Account** (free signup)

---

## 🚀 Deployment Steps

### Step 1: Deploy Your Backend First

**IMPORTANT**: You MUST deploy your Flask backend before deploying the frontend!

**Recommended Backend Hosting Options:**

#### Option A: Railway (Easiest, Recommended)
- **Free Tier**: $5 credit/month
- **Pros**: Postgres included, easy Python deployment
- **URL**: https://railway.app/
- **Guide**: See `RAILWAY_DEPLOYMENT_GUIDE.md` (I'll create this)

#### Option B: Render
- **Free Tier**: Yes (with limitations)
- **Pros**: Simple setup, free PostgreSQL
- **URL**: https://render.com/
- **Guide**: See `RENDER_DEPLOYMENT_GUIDE.md`

#### Option C: Fly.io
- **Free Tier**: Yes
- **Pros**: Good for Flask apps
- **URL**: https://fly.io/

**After deploying backend, you'll get a URL like:**
```
https://primevape-backend.up.railway.app
```

**Save this URL - you'll need it in Step 3!**

---

### Step 2: Push Your Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   cd primevape-frontend
   git init
   git add .
   git commit -m "Initial commit - ready for Vercel"
   ```

2. **Create GitHub Repository**:
   - Go to: https://github.com/new
   - Repository name: `primevape-frontend`
   - Make it **Public** or **Private** (your choice)
   - Click **"Create repository"**

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/primevape-frontend.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 3: Deploy to Vercel

1. **Sign Up for Vercel**:
   - Go to: https://vercel.com/signup
   - Click **"Continue with GitHub"**
   - Authorize Vercel to access your GitHub

2. **Create New Project**:
   - Click **"Add New..."** → **"Project"**
   - Find your **`primevape-frontend`** repository
   - Click **"Import"**

3. **Configure Project**:

   **Framework Preset**: Vite (auto-detected)

   **Root Directory**: `./` (leave default)

   **Build Command**:
   ```
   npm run build
   ```

   **Output Directory**:
   ```
   dist
   ```

   **Install Command**:
   ```
   npm install
   ```

4. **Add Environment Variables**:

   Click **"Environment Variables"** section and add:

   | Name | Value |
   |------|-------|
   | `VITE_API_URL` | `https://your-backend-url.railway.app` |

   **IMPORTANT**: Replace `https://your-backend-url.railway.app` with your actual backend URL from Step 1!

   Example:
   ```
   VITE_API_URL=https://primevape-backend.up.railway.app
   ```

5. **Deploy**:
   - Click **"Deploy"**
   - Wait 2-3 minutes for build to complete
   - You'll get a URL like: `https://primevape-frontend.vercel.app`

---

## 🎉 Your App is Live!

After deployment completes:

**Frontend URL**: `https://primevape-frontend.vercel.app` (or your custom domain)

**Test Your Deployed App**:
1. Open your Vercel URL
2. Browse products (should load from your backend)
3. Test user registration/login
4. Test cart and checkout
5. Test chatbot

---

## 🔧 Update Backend CORS

Your backend needs to allow requests from your Vercel domain!

1. Open `/primevape-backend/.env`

2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=http://localhost:5173,https://primevape-frontend.vercel.app
   ```

3. Redeploy your backend with this change

**Note**: Add any custom domains too!

---

## 🌐 Add Custom Domain (Optional)

Want `primevape.com` instead of `primevape-frontend.vercel.app`?

1. **Buy a Domain**:
   - Namecheap: https://www.namecheap.com/
   - GoDaddy: https://www.godaddy.com/
   - Google Domains: https://domains.google/

2. **Add to Vercel**:
   - Go to your project in Vercel
   - Click **"Settings"** → **"Domains"**
   - Add your domain: `primevape.com`
   - Follow Vercel's DNS instructions

3. **Configure DNS**:
   - Add Vercel's nameservers to your domain registrar
   - Wait 24-48 hours for DNS propagation

4. **Done!** Your site will be at `https://primevape.com`

---

## 🔄 Auto-Deploy on GitHub Push

Vercel automatically redeploys when you push to GitHub!

**Workflow**:
```bash
# Make changes to your code
git add .
git commit -m "Updated homepage"
git push

# Vercel automatically builds and deploys!
```

**Check Deployment**:
- Go to Vercel dashboard
- See deployment status in real-time
- Get unique URL for each deployment

---

## 📊 Monitor Your Deployment

### Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Click your project
3. See:
   - **Deployments**: All deployments history
   - **Analytics**: Page views, performance
   - **Logs**: Build and runtime logs
   - **Settings**: Environment vars, domains

### Check Logs

If something goes wrong:
1. Go to deployment in Vercel
2. Click **"Build Logs"** or **"Function Logs"**
3. Debug errors

---

## 🐛 Troubleshooting

### Error: "Cannot connect to backend"

**Problem**: Frontend can't reach backend API

**Solutions**:
1. Check `VITE_API_URL` is correct in Vercel
2. Make sure backend is deployed and running
3. Test backend URL directly in browser
4. Check backend CORS settings

### Error: "Build failed"

**Problem**: Vercel can't build your React app

**Solutions**:
1. Check build logs in Vercel dashboard
2. Test build locally: `npm run build`
3. Make sure `package.json` has correct scripts
4. Check Node.js version compatibility

### Products Not Loading

**Problem**: API calls failing

**Solutions**:
1. Open browser console (F12)
2. Check Network tab for failed requests
3. Verify `VITE_API_URL` environment variable
4. Test backend URL: `https://your-backend.railway.app/api/products`

### Environment Variables Not Working

**Problem**: `import.meta.env.VITE_API_URL` is undefined

**Solutions**:
1. Environment variables MUST start with `VITE_`
2. Redeploy after adding environment variables
3. Clear cache and redeploy

---

## ✅ Pre-Deployment Checklist

Before deploying to Vercel:

- [ ] Backend deployed and tested
- [ ] Backend URL saved (you'll need it!)
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] `VITE_API_URL` environment variable set
- [ ] Backend CORS updated with Vercel domain
- [ ] Test deployment URL

---

## 🚀 Deployment Workflow Summary

```
1. Deploy Backend (Railway/Render)
   ↓
2. Get Backend URL
   ↓
3. Push Frontend to GitHub
   ↓
4. Import to Vercel
   ↓
5. Add VITE_API_URL environment variable
   ↓
6. Deploy!
   ↓
7. Update Backend CORS
   ↓
8. Test Live Site
   ↓
9. (Optional) Add Custom Domain
```

---

## 💡 Pro Tips

1. **Use Preview Deployments**: Every PR gets its own URL
2. **Environment Variables**: Use different backend URLs for staging/production
3. **Analytics**: Enable Vercel Analytics for free
4. **Custom Domain**: Looks more professional
5. **Edge Functions**: Vercel supports serverless functions if needed

---

## 📚 Resources

- **Vercel Docs**: https://vercel.com/docs
- **Vite Deployment**: https://vitejs.dev/guide/static-deploy.html
- **Custom Domains**: https://vercel.com/docs/concepts/projects/custom-domains
- **Environment Variables**: https://vercel.com/docs/concepts/projects/environment-variables

---

## 🎯 Next Steps

After deploying to Vercel:

1. **Share Your Link!** - `https://primevape-frontend.vercel.app`
2. **Test Everything** - Products, cart, checkout, chatbot
3. **Add Custom Domain** (optional)
4. **Set Up Analytics** - Track visitors
5. **Monitor Performance** - Vercel has built-in analytics

---

## ✅ You're Ready to Deploy!

**Your frontend is now configured for Vercel deployment!**

**Changes Made**:
- ✅ Created `.env.local` for local development
- ✅ Created `.env.production` template
- ✅ Created `src/config.js` for centralized configuration
- ✅ Updated all API calls to use environment variables
- ✅ Ready for Vercel deployment!

**Just follow the steps above and your PrimeVape store will be live!** 🎉
