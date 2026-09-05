# Getting the site online

Two things need a login, and I can't create accounts or handle passwords —
so those two steps are yours. Everything else is done and committed.

---

## Option 1 — Show them the site tonight (2 minutes, no account)

Gives a public link to the **frontend**. No admin, no calendar, no login —
just the site to look at. Good enough for "what do you think?"

1. Open **https://app.netlify.com/drop**
2. Drag the **`docs`** folder from this project onto the page
3. You get a link like `https://random-name-123.netlify.app` — send that

The `docs` folder is a complete, self-contained copy of the site. It works on
any static host, or even opened from disk.

> The link expires after a while unless you claim it with a free account.
> Re-run `py -3.14 build_static.py` and drag again to update it.

---

## Option 2 — The real thing, with the admin (about 10 minutes)

Gives frontend **and** backend, so the committee can try adding a photo or an
event themselves.

### Step A — fix the GitHub token *(yours to do)*

The token in this repo's remote URL is dead, and it was stored in plaintext
where anything could read it. Replace it:

1. Revoke the old one: **github.com/settings/tokens**
2. Create a new **fine-grained** token with *Contents: read and write* on the
   `el-sobrante-gurdwara-website` repo only
3. Store it in Windows Credential Manager instead of the URL:

```bash
git remote set-url origin https://github.com/Manjot7/el-sobrante-gurdwara-website.git
git config --global credential.helper manager
git push origin main
```

Git will prompt once and remember it. The token never touches the repo again.

### Step B — deploy on Render *(yours to do)*

1. Sign up free at **render.com** with the GitHub account
2. **New → Blueprint**, pick the `el-sobrante-gurdwara-website` repo
3. Render reads `render.yaml` and configures everything itself
4. Before the first deploy, add three environment variables so an admin login
   is created — pick your own password, it stays in Render:
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`
5. Deploy. You get `https://sikh-center-website.onrender.com`

Then add the real hostname so Django accepts it:
`DJANGO_ALLOWED_HOSTS=sikh-center-website.onrender.com`

### What the free plan costs you

- **Sleeps after 15 minutes idle.** The first visitor waits ~50 seconds for it
  to wake. Warn the committee, or open the link yourself just before sending it.
- **Nothing uploaded is kept.** The disk is wiped on every deploy and restart,
  so photos and events added through the admin will disappear. The build
  re-seeds the history photos and programme each time, so the site always comes
  back looking right — but tell the committee their test edits are temporary.

Both go away on the $7/month Starter plan with a disk. See [HOSTING.md](HOSTING.md).

---

## What's already done

- `render.yaml` — Render configures itself from this
- `build.sh` — installs, migrates, seeds content, creates the editor group
- Media serving fixed for production (photos would have 404'd otherwise)
- `docs/` rebuilt with relative paths, so it works on any host
- Everything committed on `main`, ready to push
