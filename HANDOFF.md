# Looking after the website

Written for committee members, not developers. Nothing here needs any
technical knowledge.

There are only **two** places anything is ever changed:

1. **Google Calendar** — paths, bookings, anything with a date
2. **The website admin** — photos, the daily programme, phone numbers

That's it. Nothing else on the site needs touching.

---

## 1. Google Calendar — paths and bookings

The website shows the Gurdwara's Google Calendar. Whatever is entered there
appears on the website within a few minutes. Visitors can see it but **cannot
change anything**.

### To add a booking

Open Google Calendar as normal (phone or computer), add the event, done. For
example: *"Akhand Paath — Singh family"*, 4 Sept to 6 Sept, Main Hall.

Put the family name in the title if it should be public. It will be visible to
anyone on the website.

### One-time setup

1. Create the calendar on the **Gurdwara's own Google account**, not a
   personal one.
2. Settings → click the calendar → **Access permissions** → tick
   **"Make available to public"**, and set it to **"See all event details"**.
   This is what lets the sangat view it without being able to edit.
3. Under **"Share with specific people"**, add each committee member who
   should be able to add bookings, with **"Make changes to events"**.
4. Settings → **Integrate calendar** → copy the **Calendar ID**.
5. Paste that ID into the website admin under **Gurdwara details**.

### Gurpurab and Nanakshahi dates

Already handled. A public Nanakshahi calendar is layered on top, so Gurpurabs
and Sangrand dates appear automatically and update themselves every year.
Nobody needs to enter them.

---

## 2. The website admin — photos and text

Go to **yoursite.com/admin** and log in.

You'll see four things:

### Photos on the website
Add a photo, then pick where it goes:
- **Home page slideshow** — the big photos at the top of the homepage
- **History (About section)** — the old photos in the history carousel
- **Khalsa Academy gallery** — class photos

Big photos straight off a phone are fine — they're shrunk automatically.

To reorder, change the **Order** numbers (lower shows first).
To hide a photo, untick **Show on the website** — don't delete it, that way
it can be brought back.

### Events & posters
For major events — Vaisakhi, Gurpurabs, camps — the ones that deserve a poster
on the homepage.

Add a title, a date, and a poster image if you have one. Tick **Highlight this
event** to make it stand out.

**Events disappear from the website by themselves once the date passes.** You
never have to go back and tidy up.

> Routine path bookings go in Google Calendar, not here. This is only for the
> handful of big events each year.

### Daily programme
The morning / evening / Wednesday & Friday programme shown on the Schedule
page, the Livestream page and in the footer. Edit the text here and it changes
in all three places at once.

### Gurdwara details
Name, address, phone numbers, email, the Google Calendar ID, the YouTube
channel. Change a phone number here and it updates everywhere on the site.

---

## The livestream looks after itself

The Livestream page follows the **YouTube channel**, not one particular video.
Whenever you go live, the website shows it. When you're not live, YouTube shows
its own "no stream" message.

**There is nothing to update when you start a new stream.**

---

## Adding a new committee member to the admin

Ask whoever maintains the site. They'll create the login and add it to the
**"Website editors"** group, which gives access to the four things above and
nothing else — no ability to change accounts or break the site.

---

## If something looks wrong

- **A photo isn't showing** — check *Show on the website* is ticked.
- **The calendar is empty** — check the Calendar ID under *Gurdwara details*,
  and that the calendar is set to public.
- **An old event is still showing** — check its date; it hides itself the day
  after it finishes.
- **Anything else** — nothing you can do in the admin will break the site
  permanently. Untick rather than delete, and ask for help.

---

## For the developer

```bash
py -3.14 manage.py runserver          # local
py -3.14 manage.py createsuperuser    # first login
py -3.14 manage.py setup_editors      # create the editors group
py -3.14 manage.py seed_content       # re-fill programme + history photos (safe to re-run)
py -3.14 build_static.py              # snapshot to docs/ for GitHub Pages review
```

Deployment and backups: see [HOSTING.md](HOSTING.md).
Outstanding placeholders: see [COMMITTEE-QUESTIONS.md](COMMITTEE-QUESTIONS.md).
