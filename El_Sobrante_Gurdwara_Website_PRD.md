# El Sobrante Gurdwara Website — Product Requirements Document

**Version:** 1.1
**Status:** Draft for committee review

---

## 1. Overview

A custom website for the El Sobrante gurdwara, modeled loosely on gurudwaradubai.com, built with a Django + Wagtail backend and a Tailwind CSS frontend. The core requirement driving the architecture: non-technical committee members (taskers) must be able to update the weekly schedule and other content themselves, with no code changes and no developer involvement after launch. Taskers will be given login credentials with no formal training session, so the admin experience must be self-explanatory.

Design principle for this version: keep every tasker-facing concept as simple as possible. Where a feature would require taskers to learn a distinction (e.g. recurring vs. one-off entries) that doesn't match how they actually work, drop the distinction rather than build it "just in case."

## 2. Goals

- Give the sangat a clean, mobile-friendly site with current schedule, livestream access, and Khalsa School info
- Let non-technical volunteers update the schedule and announcements through a simple admin interface, with no training walkthrough to lean on
- Avoid the PDF-upload pattern (schedule must be structured, readable data, not a scanned/uploaded document)
- Keep the codebase maintainable by a single developer or handed off to a future volunteer
- Minimize the number of concepts/decisions a tasker has to hold in their head when editing content

## 3. Non-goals (for v1)

- Online donation processing: not in scope. Depends on a separate decision about how manual donations/bookings currently work. Can be revisited as v2 once that process is settled
- User accounts/login for the sangat
- Multi-language toggle (confirm with committee if needed later; not requested yet)
- Recurring schedule entries: the committee updates the schedule weekly regardless of whether it repeats, so a recurring/one-off distinction adds complexity without payoff. Revisit if committee habits change (see section 7 and Open Questions)
- Contact form: listed contact details only, no form to build or maintain
- Live/offline detection for the YouTube embed: no YouTube Data API key, no server-side "is it live" logic
- Week/month toggle on the Schedule page: one weekly view only

## 4. Users

| User | Needs |
|---|---|
| Sangat (site visitor) | Find schedule, watch livestream, get directions, learn about Khalsa School, contact the gurdwara |
| Committee tasker (editor) | Update the weekly schedule, swap livestream link, edit contact info, without touching code |
| Developer (you) | Build once, hand off cleanly, minimal ongoing maintenance |

## 5. Sitemap

Confirmed page list from committee:

1. **Home** (doubles as the About page — this is the default/landing page)
2. **Schedule**
3. **School** (Khalsa School)
4. **Livestream**
5. **Contact**

Navigation bar: `Home | Schedule | School | Livestream | Contact` — 5 items, flat structure, no dropdowns needed at this scale.

## 6. Page-by-Page Layout

### 6.1 Home / About (default landing page)

- **Hero section**: full-width photo of the gurdwara building, gurdwara name, a short welcome line (Sat Sri Akal / Waheguru Ji Ka Khalsa greeting)
- **About blurb**: 2-3 short paragraphs — history, mission, founding, community role (editable text block)
- **Quick links row**: 3-4 cards linking to Schedule, Livestream, School, Contact, so visitors don't have to hunt for the nav on mobile
- **Today/this week at a glance**: pulls the next 2-3 upcoming schedule entries directly from the Schedule data (auto-updating from the same weekly entries the committee maintains — no separate content to update)
- **Mini map + address**: small embedded Google Map with the gurdwara pin, click-through to full Google Maps directions (see 6.6)
- **Footer**: address, phone, email, social links, repeated across all pages

### 6.2 Schedule

Highest-priority page functionally. Structured as live data instead of a static post or PDF.

- **Model**: a flat list of schedule entries, each with its own specific date. No recurring/auto-repeating entries — the committee updates the list weekly, so every entry is entered for the week it applies to
- **Layout**: a clean table/grid grouped by day, showing time, event name, and optional notes (e.g., "Sunday — 9:00 AM — Asa Di Var", "Sunday — 12:00 PM — Langar")
- Special entries (Vaisakhi, Gurpurab, etc.) can be flagged to stand out visually (badge/highlight color) — same entry type as everything else, just a checkbox
- Past entries (date already passed) simply stop appearing on the site automatically — no manual cleanup needed
- Mobile view collapses the table into stacked day-cards rather than a horizontal-scroll table

### 6.3 School (Khalsa School)

- Overview of the program (mission, age groups, what's taught)
- Class schedule: reuses the same Schedule entries, filtered by category = "School," so it's not a second thing to maintain separately
- Registration info (form, fee, contact person) — static content for now
- Photos from past classes/events (simple gallery block)

### 6.4 Livestream

- Plain embedded YouTube iframe pointed at the channel's live tab (not a fixed video ID). YouTube's own embed natively shows an "offline" state when nothing is streaming — no custom logic, no API key, nothing for anyone to maintain
- Short note on regular streaming days/times
- Link to the YouTube channel directly as a fallback for visitors

### 6.5 Contact

- Address, phone, email (editable content blocks)
- Full-size embedded Google Map, click-through to Google Maps for directions (see 6.6)
- No contact form — listed details only, to avoid owning spam handling or email delivery config

### 6.6 Location / Map component (shared)

A reusable component appearing on Home (small) and Contact (large):

- Embedded Google Map centered on the gurdwara's coordinates, using the Google Maps Embed API (no API billing key needed for basic embeds, just an iframe with the address)
- Clicking the map opens `https://www.google.com/maps/search/?api=1&query=<address>` in a new tab, handing off to Google Maps for turn-by-turn directions
- No custom map library needed — this keeps it lightweight and avoids maintaining a Maps API key/billing account

## 7. Schedule Data Model (the core of the "no PDF" requirement)

```
ScheduleEntry
- title            (e.g., "Asa Di Var")
- date             (specific calendar date — every entry has one, no recurring flag)
- start_time
- end_time (optional)
- location          (e.g., "Main Hall", "Langar Hall")
- category          (Diwan / Langar / School / Special Event — single dropdown, no separate tagging system)
- is_featured        (boolean — for highlighting special events, just a checkbox)
- notes            (free text, optional)
```

Editing experience for taskers (via Wagtail admin):

- A simple list view of schedule entries, sortable by date
- "Add new entry" form with plain fields: title, date, start time, end time, location, category dropdown, featured checkbox, notes
- Entered weekly by the committee; entries with a past date simply stop showing on the public site automatically (not deleted, just filtered out of the display query — so nothing is lost if they want to look back)

**Revisit note:** if the committee's actual weekly rhythm turns out to be "same schedule every week, we're only really updating exceptions," a recurring-entry model (enter once, repeats automatically, with one-off overrides) would save them re-entry effort. Worth a quick check-in with the 1-2 people actually doing the data entry after a few weeks of real use, per the Open Questions below.

## 8. Technical Architecture

- **Backend**: Django + Wagtail (Wagtail provides the non-technical-friendly admin/CMS layer on top of Django)
- **Frontend**: Django templates styled with Tailwind CSS — one codebase, no separate frontend deployment, no JS framework
- **Interactivity**: none required for v1 — no filtering/toggle UI, so no HTMX or JS framework needed. Keeps the codebase simpler for whoever maintains it after handoff
- **Database**: PostgreSQL (or SQLite for early development, PostgreSQL for production)
- **Hosting**: Render or Railway are both good fits for a small Django app with a Postgres add-on and a low/free-tier cost
- **Maps**: Google Maps Embed (iframe), no billing key required at basic tier
- **Timezone**: `TIME_ZONE` set explicitly to `America/Los_Angeles` in settings — a one-time dev setup step, invisible to taskers, but required so schedule times display correctly regardless of server location
- **Tasker permissions**: taskers are given a custom Wagtail permission group scoped to only the Schedule entries and basic page content blocks — not the full page tree, site settings, or user management. This is what makes handing over credentials with no training session safe

## 9. Content Needed From Committee

Before backend build starts, collect:

- Final About/history text
- Current weekly schedule (all entries with day/time for the upcoming week, to seed the first real data)
- Any known upcoming special events
- Khalsa School program details (schedule, fees, registration process, photos)
- YouTube channel link
- Confirmed address for the map
- Logo and any brand colors/fonts they want reflected
- Photos (building exterior/interior, events, school)

## 10. Rollout Plan

1. **Design phase (current)**: build all 5 pages as Django templates with placeholder/dummy data, styled in Tailwind, deployed somewhere clickable (Render free tier or local + screen share). No Wagtail, no database models, no admin, no backend logic of any kind at this stage — plain Django project used only as a vehicle to render templates. Specific requirements for this phase:
   - **Placeholder data must match the real model shape.** Dummy Schedule entries should use the exact fields from section 7's `ScheduleEntry` (title, date, start_time, end_time, location, category, is_featured, notes), hardcoded in the template or a plain Python list/dict. This means swapping in real Wagtail data later is just wiring the same template to a queryset, not a template rewrite
   - **Mobile views required, not just desktop.** The Schedule page's stacked day-cards (section 6.2) are a different layout from the desktop table, not a responsive reflow — the committee needs to see both before signing off
   - **Realistic placeholder content, not lorem ipsum.** About blurb, School section, and Schedule entries should use real Punjabi/Sikh community context (e.g. Asa Di Var, Langar, Vaisakhi) so the committee reacts to something that reads like their actual site
   - **Maps/YouTube as static iframes only**, with placeholder address/channel, no API wiring beyond the embed itself
2. **Committee review**: walk taskers through the live mockup, focused specifically on the Schedule page usability, not just visual approval
3. **Backend build**: implement Wagtail models (ScheduleEntry, page content blocks), tasker permission group, wire templates to real data
4. **Content migration**: replace placeholder content with real text/photos/schedule from the committee
5. **Access handoff**: taskers are given backend login credentials directly, no formal training session planned. The admin interface's clarity and simplicity is a hard requirement, not a nice-to-have, since there's no walkthrough to fall back on if something is confusing
6. **Launch**

## 11. Open Questions for the Committee

- Should special/one-off events be visually distinct from the regular weekly schedule? (Current plan: yes, via a featured checkbox)
- Who are the 1-2 people who will actually be entering schedule updates? Since there's no formal training planned, it's worth knowing their comfort level with basic web forms ahead of time so the admin UI can be kept as simple as possible for them specifically
- After a few weeks of real weekly use: does the schedule mostly repeat the same week-to-week, or genuinely change often? This determines whether a future recurring-entry model (section 7 revisit note) would actually save the taskers effort, or whether the flat weekly list continues to be the simpler fit
