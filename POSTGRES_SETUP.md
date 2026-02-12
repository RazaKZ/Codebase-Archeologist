# 🐘 PostgreSQL Setup on Railway

## Step-by-Step Guide

### 1. Understand the Two Database URLs

Railway provides **two** database URLs:

- **`DATABASE_URL`** (Internal) - ✅ **Use This One!**
  - Faster, more secure
  - Only accessible within Railway network
  - Best for backend services on Railway
  
- **`DATABASE_PUBLIC_URL`** (Public)
  - Accessible from internet
  - Uses proxy (slower)
  - Only use if connecting from outside Railway

### 2. Connect Database to Backend (Recommended Method)

**Use Railway's Variable Reference** (Best way - automatic sync):

1. Go to your **Backend/FastAPI** service in Railway
2. Click on **Variables** tab
3. Click **+ New Variable**
4. Click **"Variable Reference"** (purple banner mein mention hai)
5. Select your **Postgres** service
6. Select **`DATABASE_URL`** from dropdown
7. Save

✅ **Benefits:**
- Automatically syncs if database URL changes
- No need to copy-paste
- Railway's recommended method

### 2b. Alternative: Manual Copy-Paste

If Variable Reference doesn't work:

1. Go to **Postgres** service → **Variables** tab
2. Find **`DATABASE_URL`** (hidden - click eye icon to reveal)
3. Copy the value
4. Go to **Backend** service → **Variables** tab
5. Click **+ New Variable**
6. Add:
   - **Name:** `DATABASE_URL`
   - **Value:** Paste the connection string
7. Save

### 3. Verify Other Environment Variables

Make sure these are also set in your backend service:

```
DATABASE_URL=postgresql://... (from Postgres service)
CORS_ORIGINS=https://codebase-archeologist.vercel.app,http://localhost:5173
GEMINI_API_KEY=your_key_here (optional)
```

### 4. Redeploy Backend

- Railway will **automatically redeploy** when you add/update variables
- Or manually: **Settings** → **Redeploy**

### 5. Check Logs

After deployment:
1. Go to **Deployments** tab
2. Click on latest deployment
3. Check logs for:
   - ✅ "Application startup complete"
   - ✅ No database connection errors
   - ❌ If you see errors, check DATABASE_URL format

### 6. Test Database Connection

Visit in browser:
```
https://your-backend-url.up.railway.app/health
```

Should return: `{"status": "healthy"}`

### 7. Verify Tables Created

The database tables will be **automatically created** on first startup.

To verify:
1. Go to Postgres service → **Database** tab → **Data** sub-tab
2. You should see tables:
   - `projects`
   - `analyses`
   - `dependencygraphs`

## ✅ Troubleshooting

### Problem: "Connection refused" or "Database not found"
- **Solution:** Double-check DATABASE_URL format
- Make sure it starts with `postgresql://` (not `postgres://`)
- Verify the connection string is from the Postgres service, not backend

### Problem: Tables not created
- **Solution:** Check backend logs for errors
- Tables are created on startup via `Base.metadata.create_all()`
- If errors, check if `psycopg2` or `psycopg2-binary` is in requirements.txt

### Problem: "No module named psycopg2"
- **Solution:** Add to `backend/requirements.txt`:
  ```
  psycopg2-binary
  ```
- Redeploy backend

## 🎉 Success!

Once setup is complete:
- ✅ Database persists data (unlike SQLite)
- ✅ No more 404 errors for projects
- ✅ Analysis results will be saved properly

