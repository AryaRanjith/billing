# Deployment Guide - Render.com

This guide walks through deploying the POS Billing System to Render.com.

---

## Prerequisites

- ✅ Code pushed to GitHub
- ✅ Render.com account (free tier available)
- ✅ Project configured for production

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Commit and Push All Changes

```bash
git add .
git commit -m "Add deployment files for Render"
git push origin main
```

Verify all files are pushed, especially:
- `Procfile` ✅
- `requirements.txt` ✅
- `runtime.txt` ✅ (newly created)
- `build.sh` ✅ (newly created)
- `pos_system/settings.py` ✅

---

## Step 2: Set Up on Render.com

### 2.1 Create a New Web Service

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect"** next to your billing repository
5. Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `billing-pos` (or your preferred name) |
| **Environment** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn pos_system.wsgi` |
| **Instance Type** | `Free` (adequate for testing) |

### 2.2 Configure Environment Variables

Before deploying, set these in Render:

1. In your Web Service, go to **"Environment"** tab
2. Add these variables:

```
SECRET_KEY=your-secure-random-secret-key-here
DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com
```

**⚠️ Important:** Generate a secure SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use: https://djecrety.ir/

### 2.3 Update CSRF Settings

The settings.py already includes Render's domain:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://billing-0v91.onrender.com"
]
```

**Update this to your actual Render URL** after deployment, or make it dynamic:

In `pos_system/settings.py`, replace:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://billing-0v91.onrender.com"
]
```

With:
```python
CSRF_TRUSTED_ORIGINS = [
    os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8000')
] if os.environ.get('RENDER_EXTERNAL_URL') else []
```

---

## Step 3: Deploy

### 3.1 Trigger Deployment

Click **"Deploy"** button on Render. This will:

1. ✅ Install dependencies from `requirements.txt`
2. ✅ Run `build.sh` (migrations + static files)
3. ✅ Start the gunicorn server
4. ✅ Make your app live

### 3.2 Monitor Deployment

Check the **"Logs"** tab to see:
- Build progress
- Migration status
- Any errors

---

## Step 4: Access Your App

After successful deployment:

1. Get your URL from the Render dashboard (typically `https://[app-name].onrender.com`)
2. Visit: `https://[app-name].onrender.com/`
3. Access admin: `https://[app-name].onrender.com/admin/`

Default admin credentials:
- Create them locally with: `python manage.py createsuperuser`
- Or create them in admin panel after deployment

---

## Step 5: Update CSRF Origins (Final Step)

After you have your actual Render URL:

1. In `pos_system/settings.py`, update:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://your-actual-app-name.onrender.com"
]
```

2. Commit and push:
```bash
git add pos_system/settings.py
git commit -m "Update CSRF origins for production URL"
git push origin main
```

3. Render will auto-deploy with the new settings

---

## Troubleshooting

### Issue: 502 Bad Gateway
- **Check logs** in Render dashboard
- Ensure `start_command` is correct: `gunicorn pos_system.wsgi`

### Issue: Static files not loading
- WhiteNoise is already configured
- If missing, ensure `STATICFILES_STORAGE` is set to:
  ```python
  'whitenoise.storage.CompressedManifestStaticFilesStorage'
  ```

### Issue: Database errors
- SQLite works fine on Render (files persist)
- Run migrations: `python manage.py migrate` (build.sh handles this)
- Access shell: `python manage.py shell` via Render

### Issue: Admin login not working
Create superuser:
```bash
# Via Render shell or local:
python manage.py createsuperuser
```

---

## Next Steps

### Enable Features

After deployment:

1. **Admin Dashboard**
   - Add Products with prices
   - Configure price management

2. **Test Features**
   - Manual transaction entry
   - Price updates
   - POS import functionality
   - Daily sales summary

3. **Monitor**
   - Check Render logs regularly
   - Monitor app performance in Render dashboard

---

## Production Checklist

- [ ] Code pushed to GitHub
- [ ] Render Web Service created
- [ ] SECRET_KEY environment variable set
- [ ] Build command set to `./build.sh`
- [ ] Start command set to `gunicorn pos_system.wsgi`
- [ ] CSRF_TRUSTED_ORIGINS updated with your URL
- [ ] Deployment successful (no 502 errors)
- [ ] Admin accessible and working
- [ ] Database migrations completed
- [ ] Static files loading correctly

---

## Support

### Common Commands

```bash
# View logs
render logs [service-id]

# SSH into container (via Render dashboard)
# Then run:
python manage.py shell
python manage.py createsuperuser

# Pull static files
python manage.py collectstatic
```

### Resources
- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [Gunicorn Configuration](https://docs.gunicorn.org/)
