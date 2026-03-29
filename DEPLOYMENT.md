# MangaOasis Deployment Guide

## Architecture

| Component | Platform | URL |
|---|---|---|
| Backend API | PythonAnywhere (Free) | `https://samprada1101.pythonanywhere.com` |
| Frontend SPA | Vercel (Free) | `https://mangaoasis.vercel.app` |
| Static Images | PythonAnywhere `/static/` | `https://samprada1101.pythonanywhere.com/static/manga_pics/` |

---

## Backend Deployment (PythonAnywhere)

### 1. Clone the repo

Open a Bash console on PythonAnywhere:

```bash
git clone https://github.com/IllusiveCoder1101/MangaOasis.git
```

### 2. Create virtualenv and install dependencies

```bash
mkvirtualenv --python=/usr/bin/python3.10 mangaoasis
pip install -r ~/MangaOasis/backend_v1/requirements.txt
pip cache purge
```

### 3. Upload the database

The database is in `.gitignore`, so it must be uploaded manually:

- Go to **Files** tab on PythonAnywhere
- Navigate to `/home/<username>/MangaOasis/backend_v1/`
- Create a `database` folder
- Upload `mangaOasis.db` into it

Alternatively, initialize a fresh database from a Bash console:

```bash
cd ~/MangaOasis/backend_v1
mkdir -p database
python -c "from main import app, db; app.app_context().push(); db.create_all(); print('DB created')"
```

Then seed the admin and users:

```python
python -c "
from werkzeug.security import generate_password_hash
import sqlite3
db = sqlite3.connect('database/mangaOasis.db')
c = db.cursor()
c.execute('INSERT INTO admin (admin_name, email, password) VALUES (?, ?, ?)', ('Admin', 'admin2004@gmail.com', generate_password_hash('admin2004')))
c.execute('INSERT INTO user (user_name, email, password, profile_pic, profile_banner) VALUES (?, ?, ?, ?, ?)', ('Akiko Tanaka', 'akiko@gmail.com', generate_password_hash('abcd1234'), 'profile_pic.jpg', 'banner1.jpg'))
c.execute('INSERT INTO user (user_name, email, password, profile_pic, profile_banner) VALUES (?, ?, ?, ?, ?)', ('Yui', 'yui@gmail.com', generate_password_hash('abcd1234'), 'profile_pic.jpg', 'banner1.jpg'))
c.execute('INSERT INTO user (user_name, email, password, profile_pic, profile_banner) VALUES (?, ?, ?, ?, ?)', ('Riku', 'riku@gmail.com', generate_password_hash('abcd1234'), 'profile_pic.jpg', 'banner1.jpg'))
db.commit()
print('Seeded')
"
```

### 4. Upload static images

Static images (manga covers, chapter pages, profile pics) are not in the repo. Upload them manually:

- Zip the `static/` folder locally:
  ```bash
  cd backend_v1
  zip -r static.zip static/
  ```
- Upload `static.zip` via PythonAnywhere **Files** tab to `/home/<username>/MangaOasis/backend_v1/`
- Unzip and clean up:
  ```bash
  cd ~/MangaOasis/backend_v1
  unzip static.zip
  rm static.zip
  ```

### 5. Create the Web App

- Go to **Web** tab > **Add a new web app**
- Choose **Manual configuration**
- Select **Python 3.10**

### 6. Configure the WSGI file

Click the WSGI config file link and replace its contents with:

```python
import sys
import os

project_home = '/home/<username>/MangaOasis/backend_v1'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from main import app as application
```

Replace `<username>` with your PythonAnywhere username.

### 7. Set the virtualenv path

On the **Web** tab under **Virtualenv**, enter:

```
/home/<username>/.virtualenvs/mangaoasis
```

### 8. Configure static files

On the **Web** tab under **Static files**, add:

| URL | Directory |
|---|---|
| `/static/` | `/home/<username>/MangaOasis/backend_v1/static` |

This lets PythonAnywhere serve images directly without going through Flask.

### 9. Reload

Click **Reload** on the Web tab. The backend API is now live.

### PythonAnywhere Notes

- Free tier: 512 MB disk quota
- Image compression (PNG to JPEG) was done to reduce `static/manga_pics/` from 195 MB to 87 MB
- Deleting `frontend_v1/src/assets/manga_pics/` on PythonAnywhere frees ~200 MB (images are served from `backend_v1/static/` instead)
- Free accounts must be refreshed every 3 months (click a button on the dashboard)
- Run `pip cache purge` after installing dependencies to save disk space

---

## Frontend Deployment (Vercel)

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Update the API base URL

Edit `frontend_v1/src/config.js`:

```js
export const API_BASE_URL = "https://<username>.pythonanywhere.com";
```

### 3. Deploy

```bash
cd frontend_v1
vercel
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Your account
- **Link to existing project?** No
- **Project name?** `mangaoasis`
- **Root directory?** `./`
- **Override settings?** No (auto-detects Vue.js)

### 4. Deploy to production

```bash
vercel --prod
```

### SPA Routing

A `vercel.json` file in `frontend_v1/` handles SPA routing so direct URL access (e.g. `/librarian/login`) works:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

Without this, refreshing or directly navigating to any route other than `/` returns a 404.

---

## Updating After Changes

### Backend updates

On PythonAnywhere Bash console:

```bash
cd ~/MangaOasis
git pull origin main
```

Then click **Reload** on the Web tab.

### Frontend updates

From your local machine:

```bash
cd frontend_v1
vercel --prod
```

Or push to GitHub and set up Vercel's GitHub integration for auto-deploys.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Static images return 404 | Check the Static files mapping on the Web tab. Ensure the path matches exactly (case-sensitive on Linux). Click Reload after changes. |
| API returns HTML instead of JSON on errors | The WSGI file may not be configured correctly. Check the error log on the Web tab. |
| Frontend routes return 404 on refresh | Ensure `vercel.json` with the rewrite rule exists in the frontend root. Redeploy with `vercel --prod`. |
| Disk quota exceeded on PythonAnywhere | Run `pip cache purge`, delete `frontend_v1/src/assets/manga_pics/` if still present, compress images. |
| CORS errors in browser console | Ensure `CORS(app, origins="*")` is set in `main.py`. |
