# Neon Database Setup Guide for PrimeVape

## 🎯 What is Neon?

**Neon** is a serverless Postgres database with amazing features:

✅ **Free Tier** - Generous free plan (3GB storage, 100 hours compute/month)
✅ **Serverless** - Auto-scales, auto-sleeps when not in use
✅ **PostgreSQL** - Full Postgres compatibility (more powerful than SQLite)
✅ **Instant Setup** - Create database in 30 seconds
✅ **Great for Production** - Much better than SQLite for deployed apps
✅ **Branching** - Database branches like Git (perfect for dev/staging/prod)

---

## 📋 Step-by-Step Setup

### Step 1: Create Neon Account

1. Go to: **https://neon.tech/**
2. Click **"Sign Up"** (free account, no credit card needed)
3. Sign up with GitHub or Email

### Step 2: Create New Project

1. After login, click **"Create Project"**
2. **Project Name**: `primevape-db` (or any name you like)
3. **Region**: Choose closest to Philippines (e.g., `ap-southeast-1` Singapore)
4. **Postgres Version**: Use default (latest)
5. Click **"Create Project"**

### Step 3: Get Connection String

1. After project is created, you'll see the **Connection Details** panel
2. Find the **Connection string** that looks like:
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```
3. **Copy this entire connection string** - you'll need it!

**Example connection string format:**
```
postgresql://primevape_user:AbCd1234XyZ@ep-cool-mountain-12345678.ap-southeast-1.aws.neon.tech/primevape?sslmode=require
```

### Step 4: Save Connection String

1. Open file: `/primevape-backend/.env`
2. Find the line: `DATABASE_URL=sqlite:///primevape.db`
3. Replace it with your Neon connection string:
   ```
   DATABASE_URL=postgresql://your-username:your-password@your-endpoint.neon.tech/neondb?sslmode=require
   ```
4. **Save the file**

---

## 🔧 Backend Setup

### Install PostgreSQL Driver

The backend needs `psycopg2` to connect to PostgreSQL:

```bash
cd primevape-backend
source venv/bin/activate
pip install psycopg2-binary
```

**Note:** This is already done for you! The package is installed automatically.

### Database Models

Your current SQLAlchemy models work perfectly with PostgreSQL! No changes needed.

The only difference:
- SQLite uses `INTEGER` for IDs
- PostgreSQL uses `SERIAL` or `BIGSERIAL` (SQLAlchemy handles this automatically)

---

## 📊 Migrate Existing Data (Optional)

If you already have products/users in your SQLite database and want to move them to Neon:

### Option 1: Use Migration Script (Recommended)

A migration script has been created: `/primevape-backend/migrate_to_neon.py`

```bash
cd primevape-backend
source venv/bin/activate
python migrate_to_neon.py
```

This will:
1. Read all data from SQLite (`primevape.db`)
2. Create tables in Neon
3. Copy all users, products, orders, cart items to Neon
4. Preserve all IDs and relationships

### Option 2: Fresh Start (Easier)

If you don't have important data yet:

```bash
cd primevape-backend
source venv/bin/activate
python init_db.py
```

This creates fresh tables in Neon with sample products.

---

## ✅ Verify Connection

### Step 1: Update .env

Make sure `/primevape-backend/.env` has your Neon connection string:

```
DATABASE_URL=postgresql://your-connection-string-here
```

### Step 2: Test Connection

```bash
cd primevape-backend
source venv/bin/activate
python -c "from app import db; print('Connecting...'); db.create_all(); print('✅ Connected to Neon!')"
```

If successful, you'll see: `✅ Connected to Neon!`

### Step 3: Restart Backend

```bash
# Kill old server (Ctrl+C if running)
python app.py
```

### Step 4: Test Your App

1. Open: **http://localhost:5173**
2. Browse products
3. Try adding to cart
4. Test user registration/login

---

## 🎨 Neon Dashboard Features

### View Your Data

1. Go to: **https://console.neon.tech/**
2. Click your project: **primevape-db**
3. Click **"SQL Editor"** in the sidebar
4. Run queries to view data:

```sql
-- View all products
SELECT * FROM product;

-- View all users
SELECT * FROM user;

-- View all orders
SELECT * FROM "order";

-- Count products
SELECT COUNT(*) FROM product;
```

### Monitor Usage

1. Click **"Dashboard"** to see:
   - Storage used
   - Compute hours used
   - Database size
   - Active connections

### Database Branches (Advanced)

Neon lets you create database branches like Git!

**Use cases:**
- `main` branch: Production data
- `dev` branch: Development/testing
- `staging` branch: Pre-production testing

**To create a branch:**
1. Click **"Branches"** in sidebar
2. Click **"Create branch"**
3. Choose parent branch
4. Get a new connection string for the branch!

---

## 💰 Neon Free Tier Limits

**Free Plan Includes:**
- ✅ **3 GB storage** (plenty for your vape shop!)
- ✅ **100 compute hours/month** (database auto-sleeps when not in use)
- ✅ **Unlimited projects** (1 active, unlimited archived)
- ✅ **1 database branch** (upgrade for more)
- ✅ **7 days point-in-time restore**

**For PrimeVape, you'll probably use:**
- ~10-50 MB storage (unless you store lots of product images)
- ~20-40 compute hours/month (auto-sleeps saves hours)

**If you exceed limits:**
- Database pauses until next month, OR
- Upgrade to **Launch** plan ($19/month) for unlimited

---

## 🔒 Security Best Practices

### Protect Your Connection String

**DO:**
- ✅ Keep connection string in `.env` file only
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Never commit `.env` to GitHub
- ✅ Use different databases for dev/production

**DON'T:**
- ❌ Hardcode connection string in code
- ❌ Share connection string publicly
- ❌ Commit `.env` file to Git

### Rotate Password (If Exposed)

If you accidentally expose your connection string:

1. Go to: **https://console.neon.tech/**
2. Click your project
3. Click **"Settings"** → **"Reset password"**
4. Update `.env` with new connection string

---

## 🐛 Troubleshooting

### "SSL connection required" Error

**Solution:** Make sure your connection string includes `?sslmode=require`:

```
postgresql://user:pass@host.neon.tech/db?sslmode=require
```

### "Connection timeout" Error

**Problem:** Neon database is sleeping (hasn't been used recently)

**Solution:** Wait 5-10 seconds and try again. First connection wakes up the database.

### "Authentication failed" Error

**Problem:** Wrong username/password in connection string

**Solution:**
1. Go to Neon dashboard
2. Click **"Connection Details"**
3. Copy the full connection string again
4. Update `.env` file

### "Too many connections" Error

**Problem:** You have too many open connections

**Solution:**
1. Check for connection leaks in code
2. Close old background Flask servers
3. Restart your backend server

### "Relation does not exist" Error

**Problem:** Tables not created in Neon database

**Solution:**
```bash
cd primevape-backend
source venv/bin/activate
python init_db.py
```

---

## 📊 SQLite vs Neon (PostgreSQL)

| Feature | SQLite | Neon (PostgreSQL) |
|---------|--------|-------------------|
| **Type** | File-based | Server-based |
| **Concurrent Users** | Limited | Unlimited |
| **Performance** | Good for small apps | Great for any size |
| **Data Size** | Limited | Up to 3GB (free tier) |
| **Production Ready** | Not recommended | ✅ Yes! |
| **Backup** | Manual file copy | Automatic |
| **Scalability** | Poor | Excellent |
| **Cost** | Free | Free (3GB) |
| **Best For** | Local dev/testing | Production apps |

**Verdict:** Neon is MUCH better for a deployed e-commerce site!

---

## 🚀 Deployment Benefits

When you deploy PrimeVape (Vercel, Netlify, Railway, etc.):

**With SQLite:**
- ❌ File-based database doesn't work well with serverless
- ❌ Data lost on redeployment
- ❌ No concurrent connections
- ❌ Difficult to backup

**With Neon:**
- ✅ Works perfectly with serverless deployments
- ✅ Data persists forever
- ✅ Handles many users simultaneously
- ✅ Automatic backups
- ✅ Easy to scale

---

## 📚 Resources

- **Neon Console**: https://console.neon.tech/
- **Neon Docs**: https://neon.tech/docs/introduction
- **Connection Guide**: https://neon.tech/docs/connect/connect-from-any-app
- **SQLAlchemy Guide**: https://neon.tech/docs/guides/sqlalchemy
- **Pricing**: https://neon.tech/pricing

---

## ✅ Quick Setup Checklist

- [ ] Create Neon account at https://neon.tech/
- [ ] Create new project named "primevape-db"
- [ ] Copy connection string from dashboard
- [ ] Update `.env` file with `DATABASE_URL=postgresql://...`
- [ ] Install psycopg2: `pip install psycopg2-binary`
- [ ] Run migration script OR initialize fresh database
- [ ] Restart backend server
- [ ] Test app at http://localhost:5173

---

## 🎉 You're Ready!

Once you complete the setup:

1. **Your app works exactly the same** - No code changes needed!
2. **Data is in the cloud** - Safe, backed up, always available
3. **Ready for production** - Deploy to Vercel/Railway anytime
4. **Free forever** - As long as you stay under 3GB

**Neon is the perfect database for your PrimeVape e-commerce site!** 🚀
