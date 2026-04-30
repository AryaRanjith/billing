# Quick Deployment Checklist

Complete these steps in order to deploy your POS Billing System to Render.

---

## ✅ Step 1: Prepare Your Code (LOCAL - Do This Now)

### 1.1 Verify all files exist:
```
✓ Procfile
✓ requirements.txt
✓ runtime.txt (newly created)
✓ build.sh (newly created)
✓ DEPLOYMENT_GUIDE.md (newly created)
```

### 1.2 Commit and push to GitHub:
```bash
cd c:\Users\medac\OneDrive\Desktop\billing

git add .
git commit -m "Add deployment configuration for Render"
git push origin main
```

**Verify push succeeded** by visiting GitHub and checking the files are there.

---

## ✅ Step 2: Create Render Web Service (RENDER.COM)

### 2.1 Visit Render.com
- Go to https://render.com
- Sign in with GitHub (or create account)

### 2.2 Connect Your Repository
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect"** next to your `billing` repo
4. Click **"Connect"** when prompted

### 2.3 Configure the Service

Fill in these exact values:

| Setting | Value |
|---------|-------|
| Name | `billing-pos` |
| Environment | `Python 3` |
| Build Command | `./build.sh` |
| Start Command | `gunicorn pos_system.wsgi` |
| Instance Type | `Free` |

Then click **"Create Web Service"**

---

## ✅ Step 3: Set Environment Variables (RENDER.COM)

### 3.1 Add SECRET_KEY

Go to your service page in Render:
1. Click **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add these **exact** variables:

**Variable 1:**
- Key: `SECRET_KEY`
- Value: Copy from below (or generate at https://djecrety.ir/):
  ```
  generated-secret-key-here
  ```

**Variable 2:**
- Key: `DEBUG`
- Value: `False`

**Variable 3:**
- Key: `DJANGO_ALLOWED_HOSTS`
- Value: `*`

After adding, click **"Save"**

---

## ✅ Step 4: Deploy

1. Render will auto-start deployment after you save env vars
2. Go to **"Logs"** tab to watch the build
3. Wait until you see: **"✓ Deploy complete"**

---

## ✅ Step 5: Test Your Deployment

Once deployment is complete:

1. **Get Your URL**
   - In Render, you'll see a URL like: `https://billing-pos.onrender.com`
   - Click the URL to visit your app

2. **Test the Site**
   - Homepage should load
   - Admin should be at: `https://billing-pos.onrender.com/admin/`

3. **If You See an Error**
   - Check the "Logs" tab in Render
   - Look for error messages
   - Common issues are in DEPLOYMENT_GUIDE.md troubleshooting section

---

## ✅ Step 6: Create Admin User (Optional but Recommended)

### Via Render Shell:

1. In Render, go to your Web Service
2. Scroll down and click **"Shell"** button
3. In the terminal that opens, run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts (username, email, password)
5. Go to admin: `https://your-app-name.onrender.com/admin/`
6. Log in with your credentials

### Or Do It Locally First:

```bash
python manage.py createsuperuser
git add db.sqlite3
git commit -m "Add superuser"
git push origin main
# Render auto-redeploys
```

---

## 🎉 You're Done!

Your app is now live at: `https://billing-pos.onrender.com`

You can now:
- ✅ Add products and prices
- ✅ Use price management feature
- ✅ Import transactions from POS
- ✅ View daily sales summary
- ✅ Generate reports

---

## 🆘 Need Help?

See **DEPLOYMENT_GUIDE.md** for:
- Troubleshooting (502 errors, static files, etc.)
- How to run commands in production
- Advanced configuration options

---

## Key Files for Reference

- **Procfile** - Tells Render how to start the app
- **runtime.txt** - Specifies Python 3.11.8 version
- **build.sh** - Runs migrations and collects static files
- **requirements.txt** - All Python dependencies
- **pos_system/settings.py** - Django configuration (already optimized)

All set for deployment! ✅
