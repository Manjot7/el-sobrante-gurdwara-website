# Deploying the site

Host: **Fly.io**, about **$3.50/month** — $3.32 for an always-on 512 MB machine
plus $0.15 for a 1 GB volume. Render stays configured as a fallback; see the
end of this file.

Everything needed is already in the repo: `Dockerfile`, `fly.toml`,
`docker-entrypoint.sh`, and a GitHub Action for automatic deploys.

---

## Who does what

**The gurdwara** — browser only, about five minutes:

1. Create the account at [fly.io](https://fly.io) — **no card needed yet**
2. Organization dropdown → **Team** → invite the developer's Fly email as a **Member**
3. Later, once the site is confirmed working, add the payment card

**The developer** — once, from a terminal: everything below.

> If Fly asks the invited member for *their own* card, stop and fall back to
> Render. Nobody should be putting a personal card on the gurdwara's project.

---

## Trying it out first on a personal account

Worth doing before the real thing. Two rules:

**Do not use the name `sfsikhcenter` for the test.** Fly app names are unique
across all of Fly — organizations do not namespace them, because every app
gets `<name>.fly.dev`. Testing under the real name burns it, and the
gurdwara's account then cannot have it.

```bash
fly apps create sfsikhcenter-test --org personal
```

Pass `--app sfsikhcenter-test` to the rest of the commands rather than editing
`fly.toml`, so nothing needs reverting afterwards.

**Do not add `FLY_API_TOKEN` to GitHub yet.** With it set, every push
auto-deploys to the throwaway app. Deploy by hand with `fly deploy` while
testing.

What to expect on the free trial: 2 VM-hours total or 7 days, whichever comes
first, and trial machines stop after 5 minutes of running. Enough to confirm
the build works and click around the admin; not enough to leave up.

Don't enter real content — photos, events, wording. None of it transfers, and
the seed data comes back by itself on the real deployment.

When finished:

```bash
fly apps destroy sfsikhcenter-test
```

That stops it billing if a card is ever added to that account.

> If you do end up testing under the real name, `fly apps move <app> --org
> <org>` moves an app with its volume data, secrets and certificates intact.
> It works, but it occasionally errors and needs membership of both orgs — the
> throwaway name avoids the problem rather than handling it.

---

## One-time deployment

### 1. Install flyctl and sign in

```bash
iwr https://fly.io/install.ps1 -useb | iex
```

```bash
fly auth login
```

### 2. Create the app in the gurdwara's organization

`fly.toml` already holds the configuration, so this just registers the name.
Get the organization slug from `fly orgs list`.

```bash
fly apps create sfsikhcenter --org <org-slug>
```

If the name is taken, pick another and change `app =` at the top of `fly.toml`.

### 3. Create the volume

This is what keeps the database and the uploaded photos. Without it,
everything the committee adds is wiped on the next deploy.

```bash
fly volumes create sikh_center_data --region sjc --size 1 --app sfsikhcenter
```

### 4. Set the secrets

These create the admin login. Pick a real password — this account can change
the live website. The values live in Fly, never in the repo.

```bash
fly secrets set DJANGO_SECRET_KEY="$(python -c 'import secrets;print(secrets.token_urlsafe(50))')" DJANGO_SUPERUSER_USERNAME="admin" DJANGO_SUPERUSER_EMAIL="someone@example.com" --app sfsikhcenter
```

Then the password on its own, so it doesn't sit in shell history:

```bash
fly secrets set DJANGO_SUPERUSER_PASSWORD --app sfsikhcenter
```

### 5. Deploy

```bash
fly deploy
```

The first build takes a few minutes. On start the container migrates the
database, loads the history photos, programme and page text, creates the
editors group, and creates the admin login. Watch the log for
`==> Admin login created`.

### 6. Check it

```bash
fly open
```

- The site loads at `https://sfsikhcenter.fly.dev`
- `/admin` accepts the username and password from step 4
- Upload a photo, run `fly deploy` again, confirm it survived — that proves
  the volume is working

---

## Pointing sfsikhcenter.com at it

### 1. Tell Django the domain — do this first

```bash
fly secrets set DJANGO_ALLOWED_HOSTS="sfsikhcenter.com,www.sfsikhcenter.com" --app sfsikhcenter
```

Django refuses any hostname not in this list with a bare **Bad Request (400)**.
Setting it first means the site works the moment DNS resolves, instead of
serving errors while you work out why. Nothing else is needed — every host in
this list is trusted for admin logins automatically.

### 2. Get the addresses

```bash
fly ips list --app sfsikhcenter
```

Fly allocates a shared IPv4 and a dedicated IPv6 by default. The shared IPv4
is fine; a dedicated one costs $2/month and this site doesn't need it.

### 3. Add the DNS records at GoDaddy

**My Products** → the domain → **DNS** → **Manage DNS**.

| Type | Name | Value |
|---|---|---|
| A | `@` | the IPv4 from `fly ips list` |
| AAAA | `@` | the IPv6 from `fly ips list` |
| CNAME | `www` | `sfsikhcenter.fly.dev` |

**Delete GoDaddy's existing parking-page records for `@` and `www` first.**
Leaving them makes the domain resolve intermittently to the wrong place, which
is miserable to diagnose.

Do **not** use GoDaddy's "Forwarding" feature — it breaks HTTPS.

> To issue a certificate Fly must verify the domain, using the AAAA record, a
> `_acme-challenge` CNAME, or a `_fly-ownership` TXT record. The AAAA record
> above covers it. `fly certs show` prints what it's still waiting for.

### 4. Request the certificates

```bash
fly certs add sfsikhcenter.com --app sfsikhcenter
```

```bash
fly certs add www.sfsikhcenter.com --app sfsikhcenter
```

```bash
fly certs check sfsikhcenter.com --app sfsikhcenter
```

Usually a few minutes. Don't send the link to anyone until both show as
issued, or they'll get a certificate warning.

---

## Updating the site afterwards

Push to `main` and the GitHub Action deploys automatically — no terminal.

One-time setup for that:

```bash
fly tokens create deploy -x 8760h --app sfsikhcenter
```

Add the output as a repository secret named **`FLY_API_TOKEN`** under
*Settings → Secrets and variables → Actions*. The token lasts a year.

To deploy by hand instead: `fly deploy`.

---

## Things worth knowing

- **A deploy costs a few seconds of downtime.** A volume attaches to exactly
  one machine, so the old one stops before the new one starts. Unavoidable at
  this price on any host, and deploys will be rare.
- **Never scale past one machine.** The database is SQLite on that one volume;
  a second machine would get its own empty volume and serve different content.
  `fly scale count 1` if it ever drifts.
- **Backups are automatic.** Fly snapshots volumes daily, and snapshot storage
  is free under 10 GB — this volume is 1 GB. List them with
  `fly volumes snapshots list <volume-id>`.
- **The machine must never sleep.** `auto_stop_machines = false` and
  `min_machines_running = 1` in `fly.toml` are exactly what you're paying for.
  Fly's defaults are the opposite.

## Useful commands

```bash
fly logs --app sfsikhcenter
```

```bash
fly status --app sfsikhcenter
```

```bash
fly ssh console --app sfsikhcenter
```

---

## Three settings that look wrong but aren't

Anyone tidying this config later will be tempted to "fix" these. Don't.

**`DJANGO_DEBUG=false` during `collectstatic` in the Dockerfile.** With DEBUG
on, `settings.py` selects the plain static-files backend, no
`staticfiles.json` manifest is written, and the container then crashes at
runtime when the manifest backend looks for it. Verified in both directions.

**`DJANGO_SSL_REDIRECT=false` in `fly.toml`.** Fly's `force_https` already
redirects at the edge. Doing it in Django as well means Fly's internal health
checks, which arrive over plain HTTP, get a 301 back and can mark a perfectly
healthy container as failing.

**Migrations run in the entrypoint, not a Fly `release_command`.** A
release-command machine doesn't mount the volume, so it would migrate a
throwaway database and leave the real one untouched.

---

## Fallback: Render

`render.yaml` and `build.sh` are still in the repo and still work. Render is
~$7.25/month, deploys from a web dashboard rather than a CLI, and handles the
apex domain with a single A record. Use it if Fly turns out to be awkward —
the application code is identical either way.

Render setup: **New → Blueprint** → pick the repo → fill in the three
`DJANGO_SUPERUSER_*` values → set **Instance Type: Starter** and add a 1 GB
disk at `/data` with `DJANGO_DATA_DIR=/data`.
