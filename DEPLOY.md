# Hosting the site for free — frontend and backend

This puts the **whole site online**, including the admin, so the committee can
log in and try adding a photo themselves.

Host: **Render free plan**. The repo already contains `render.yaml`, so Render
configures itself — you don't have to fill in build commands.

**Roughly 10 minutes.** You need a browser and your GitHub login.

---

## Before you start — two things to know

**1. The site sleeps.** On the free plan it shuts down after 15 minutes with no
visitors, and the next person to open it waits about 50 seconds for it to wake.
Open the link yourself a minute before you send it to anyone.

**2. Uploads don't survive.** The free plan wipes its disk on every restart and
deploy. Photos or events added through the admin **will disappear**. The site
rebuilds its starting content automatically each time, so it always comes back
looking right — but tell the committee their test uploads are temporary.

Both problems go away on the $7/month Starter plan with a disk attached
(see [HOSTING.md](HOSTING.md)). Everything else works identically, so this is a
genuine preview, not a mock-up.

---

## Step 1 — Create the Render account

1. Go to **https://render.com**
2. **Get Started** → **GitHub** → sign in
3. Authorise Render. When it asks which repositories, you can grant access to
   **only** `el-sobrante-gurdwara-website`

No card is required for the free plan.

## Step 2 — Create the service from the blueprint

1. In the Render dashboard: **New +** → **Blueprint**
2. Pick the **`el-sobrante-gurdwara-website`** repository
3. Render reads `render.yaml` and shows a service called
   **`sikh-center-website`** on the **Free** plan
4. **Don't deploy yet** — do step 3 first, or you'll have no way to log in

> If Render doesn't offer "Blueprint", use **New + → Web Service** instead, pick
> the repo, and set: Runtime **Python 3**, Build Command **`./build.sh`**,
> Start Command **`gunicorn gurdwara_site.wsgi:application`**, Plan **Free**.

## Step 3 — Set the admin login

Still on the setup screen, open **Environment** / **Environment Variables** and
add three:

| Key | Value |
|---|---|
| `DJANGO_SUPERUSER_USERNAME` | `admin` (or whatever you like) |
| `DJANGO_SUPERUSER_EMAIL` | your email |
| `DJANGO_SUPERUSER_PASSWORD` | **a password you choose** |

This is how the admin account gets created. The password lives only in Render —
it is never in the repo, and nobody else sees it.

Pick something real. This login can change the live website.

`DJANGO_SECRET_KEY` and `DJANGO_DEBUG` are already handled by `render.yaml`;
you don't need to add them.

## Step 4 — Deploy

Click **Apply** / **Create**. The first build takes 3–5 minutes — it installs
Django, sets up the database, loads the history photos and daily programme, and
creates your admin login.

Watch the log. It's finished when you see something like
`Your service is live 🎉`.

You'll get a URL like:

```
https://sikh-center-website.onrender.com
```

## Step 5 — Check it works

1. Open the URL. The homepage should show the photo slideshow and the nine
   history photos.
2. Go to **`/admin`** and log in with the username and password from step 3.
3. Try it: **Photos on the website → Add**, upload any photo, set *Where it
   appears* to **Home page slideshow**, save, then reload the homepage.

If the admin login gives a **CSRF** error, add one more environment variable
and redeploy — replace with your actual URL:

```
DJANGO_CSRF_TRUSTED_ORIGINS=https://sikh-center-website.onrender.com
```

---

## Sending it to the committee

Give them **two** links and a warning:

```
The website: https://sikh-center-website.onrender.com

Please note it can take up to a minute to load the first time,
as the free hosting puts it to sleep when nobody is using it.
```

Only share the `/admin` link with whoever should be editing, along with their
own login — don't reuse yours. To add someone:

1. `/admin` → you'll need to create the user (Users are hidden from the normal
   admin on purpose)
2. Easier: send me the name and I'll add a management command for it

---

## Updating the site later

Every push to `main` redeploys automatically:

```bash
git add -A; if ($?) { git commit -m "Update site"; git push origin main }
```

Remember that a redeploy wipes uploaded photos on the free plan.

---

## What this does *not* include

- **The Google Calendar** still shows "not connected yet" until you paste the
  Calendar ID into *Gurdwara details* in the admin (see
  [COMMITTEE-QUESTIONS.md](COMMITTEE-QUESTIONS.md), task B)
- **The donate page** — not built, waiting on the committee's decision
- **A custom domain.** `thesikhcenter.com` can be pointed at Render later, but
  a custom domain on the free plan still sleeps

---

## If you'd rather it never slept

**PythonAnywhere** has a free plan with no sleeping *and* a disk that keeps
uploaded photos — better for a demo in those two ways. The trade-off is that
setup is manual (no `render.yaml` equivalent, you configure the web app by
hand) and updates need a manual pull rather than a git push. Worth it if the
committee will be poking at the site over several days rather than one sitting.
Say the word and I'll write those steps out.

---

# Putting the site on the gurdwara's own domain

## Do this first: leave the free plan

The free plan is fine for showing people a preview. It is **not** fine once
the site is at the gurdwara's real address:

- **It sleeps.** After 15 idle minutes the next visitor waits ~50 seconds
  looking at nothing. Most people assume the site is broken and leave.
- **Uploads are deleted.** Every restart and deploy wipes the disk. A Vaisakhi
  poster added in the admin will disappear without warning.

Fix both at once — Render → the service → **Settings**:

1. **Instance Type** → **Starter** (~$7/month). Stops the sleeping.
2. **Disks** → **Add Disk**, mount path `/data`, 1 GB. Keeps the uploads.
3. **Environment** → add `DJANGO_DATA_DIR` = `/data`

> Step 3 moves the database onto the new disk, which starts empty — so
> anything already added through the admin is left behind. Do this **before**
> the committee starts adding content, not after. The build re-seeds the
> history photos and programme, and recreates the admin login from the
> `DJANGO_SUPERUSER_*` variables.

## Then point the domain

Replace `YOURDOMAIN.org` with the real one throughout.

### 1. Tell Render about the domain

Service → **Settings** → **Custom Domains** → **Add Custom Domain**.

Add **both**:
- `YOURDOMAIN.org`
- `www.YOURDOMAIN.org`

Render then shows the exact DNS records to create. Use the values Render
displays — don't copy them from anywhere else, they differ per service.

### 2. Tell Django about the domain — *do this before the DNS*

Environment → add:

```
DJANGO_ALLOWED_HOSTS=YOURDOMAIN.org,www.YOURDOMAIN.org
```

Django refuses any hostname not in this list with a bare **"Bad Request
(400)"**. Setting it first means the site works the instant DNS resolves,
rather than serving errors while you work out why.

Nothing else is needed — form submissions and admin logins are trusted for
every host in this list automatically.

### 3. Add the DNS records at GoDaddy

**My Products** → the domain → **DNS** → **Manage DNS**.

| Type | Name | Value |
|---|---|---|
| CNAME | `www` | the `.onrender.com` hostname Render showed you |
| A | `@` | the IP address Render showed you |

Then **delete any existing `A` or `CNAME` records for `@` and `www`** that
GoDaddy created for its parking page. Leaving them causes the domain to
resolve intermittently to the wrong place, which is confusing to debug.

Do **not** use GoDaddy's "Forwarding" feature. That points the domain at
another URL instead of hosting the site, and breaks HTTPS.

### 4. Wait for the certificate

Render issues a free SSL certificate automatically once it can see the DNS.
Usually a few minutes; occasionally up to an hour. The custom domain shows as
**Verified** in Render when it's done.

Until then the site may show a certificate warning. That's expected — don't
send the link to anyone yet.

## Checking it worked

- `https://YOURDOMAIN.org` loads with a padlock, no warning
- `https://www.YOURDOMAIN.org` does the same
- `/admin` lets you log in (a CSRF error here means step 2 was missed)
- Upload a photo, redeploy, confirm it is still there — proves the disk works

## What about thesikhcenter.com?

Separate decision. It currently runs a different site on someone else's
server. Options: leave it alone, redirect it to the new domain, or move it
across. Redirecting needs whoever administers that server, not GoDaddy.
