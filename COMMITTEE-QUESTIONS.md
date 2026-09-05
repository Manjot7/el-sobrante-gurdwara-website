# Placeholders, open questions, and what the Gurdwara needs to do

Three lists:

1. **[Placeholders on the site](#1-placeholders-currently-on-the-site)** — things standing in for real content
2. **[Tasks for the Gurdwara](#2-tasks-for-the-gurdwara)** — jobs only the committee can do
3. **[WhatsApp message](#3-message-for-the-whatsapp-group)** — copy-paste ready

---

## 1. Placeholders currently on the site

| # | Placeholder | Where it is | What it needs |
|---|---|---|---|
| 1 | **Only one photo** in the homepage slideshow, taken from Wikipedia under a licence that forces a credit line into the footer | `Photo` records, category *Home page slideshow* | Real photos of the building, hall, langar hall and grounds. Once added, delete the Wikipedia one and the credit disappears |
| 2 | **No Academy photos at all** — that section and the class-photo column hide themselves entirely | `Photo`, category *Khalsa Academy gallery* | Any class or event photos |
| 3 | **Academy coordinator contact removed.** The mockup had an invented name, phone and email. Page now says to call the Gurdwara | `templates/academy.html` | Real name, phone, email |
| 4 | **Academy fee amount removed.** Mockup said "$40 per child"; unverified | `templates/academy.html` | The correct amount, or leave it off |
| 5 | **"Khalsa Academy"** — renamed from "Khalsa School" for the registration concern | Throughout | Confirmation this wording is acceptable |
| 6 | **Calendar not connected.** Events page shows a "not connected yet" notice instead of a calendar | *Gurdwara details* → Google Calendar ID | The Calendar ID (task B below) |
| 7 | **No events listed.** The Events page shows its empty state until someone adds one in the admin | `Event` records | A few real upcoming events |
| 8 | **Class levels** — Beginners 5–7, Intermediate 8–10, Advanced 11–14 | `templates/academy.html` | Confirm or correct |
| 9 | **Founding year 1969.** Wikipedia says the Center formed 31 Dec 1968, building opened May 1979 | `templates/home.html` | Decide which to print |
| 10 | **Donate page not built** — deliberately, pending the decisions in task E | — | Answers to task E |
| 11 | ~~Security key / DEBUG~~ — **done.** The host generates its own `SECRET_KEY` and runs with `DEBUG=false`. The development defaults apply only to a local machine | — | nothing |

Details that were carried over from the mockup and are **believed correct**, but nobody has confirmed: phone numbers (510) 223-9987 and (510) 223-1102, email info@thesikhcenter.com, address 3550 Hillcrest Rd, opening hours 5:00 AM – 8:30 PM, YouTube channel, Facebook page.

---

## 2. Tasks for the Gurdwara

### A. Send photos — *blocks the site looking right*
Exterior and domes, Darbar Sahib / main hall, langar hall, the grounds and view, and any Academy class photos. Originals from a phone, not screenshots.

### B. Create the Google Calendar — *blocks the Events page*
1. Use the **Gurdwara's own Google account**, not anyone's personal account.
2. Create a calendar, e.g. "Gurdwara Programs & Bookings".
3. Settings → the calendar → **Access permissions** → tick **"Make available to public"** and set **"See all event details"**. *This is what lets the sangat view it without being able to change it.*
4. **Share with specific people** → add each committee member who should be able to add bookings, with **"Make changes to events"**.
5. Settings → **Integrate calendar** → copy the **Calendar ID** and send it over.

Gurpurab and Nanakshahi dates are already handled — a public Nanakshahi calendar is layered on top and updates itself every year.

### C. Decide who edits what
- **Google Calendar:** names + Gmail addresses of whoever adds path bookings.
- **Website admin:** names of the 1–2 people who will add photos and events. They get a login limited to photos, events, the programme and Gurdwara details — they cannot change accounts or break the site.

### D. Confirm the Academy details
The name "Khalsa Academy", the coordinator's contact details, the fee, and the class levels. See placeholders 3, 4, 5 and 8.

### E. Decide on donations
- How are donations taken today — cash, check, Zelle, something else?
- Is the Gurdwara a registered 501(c)(3)? If so, what is the EIN?
- Which route do you want?

| Option | Fee | Needs |
|---|---|---|
| **Zelle** | none | Just a phone number or email to display |
| **PayPal Giving Fund** | none | Verified 501(c)(3) |
| **Givebutter** | none (donors asked for an optional tip) | An account |
| **Stripe** | ~2.2% + 30¢ | An account and bank details |

Recommendation: **Zelle**, if the Gurdwara already uses it — it costs nothing and needs no integration.

### F. Approve the wording
Read the About text on the homepage and the Academy page and flag anything to be worded differently.

### G. Choose hosting and a domain — *blocks going live*
See [HOSTING.md](HOSTING.md). Recommended: Render Starter, about $7/month. Also confirm whether `thesikhcenter.com` is still controlled by the Gurdwara and who has access to the domain settings.

---

## 3. Message for the WhatsApp group

Everything below is plain text with short lines, so it survives being pasted into a group chat.

---

Sat Sri Akal everyone. The new website is ready to look at. We need a few things from the committee before it can go live. Numbered so replies are easy.

*PHOTOS*

1. We need current photos of the Gurdwara — the building and domes from outside, the main hall, the langar hall, and the grounds. Phone photos are fine, please send the originals and not screenshots.

2. The homepage slideshow currently has only ONE photo, taken from Wikipedia. It is free to use but we must print a credit line at the bottom of every page. If we use our own photos that credit goes away.

3. We have no photos of the Khalsa Academy classes, so that section is hidden for now.

4. The History section has the 9 old scanned photos. Are they correct, in the right order, and is anything missing?

*KHALSA ACADEMY*

5. We changed the name from "Khalsa School" to "Khalsa Academy" because we are not a registered school. Please confirm with whoever raised this that "Academy" is acceptable. It means much the same thing in English, so if the worry was about sounding like a registered institution it may not fully solve it. Other options: "Punjabi and Gurmat Classes", "Gurmat Classes", "Punjabi Classes".

6. The old draft listed a coordinator by name with a phone number and email. Those were invented by the designer as an example. We have REMOVED them so nobody calls a wrong number. Please send the real coordinator's name, phone and email. For now the page just says to call the Gurdwara.

7. The old draft said the fee is $40 per child per year. We could not confirm this, so the page now mentions a fee without naming the amount. What is the correct amount?

8. The page lists three class levels — Beginners 5-7, Intermediate 8-10, Advanced 11-14. Is this right?

*CALENDAR AND BOOKINGS*

9. We need a Google Calendar created on the Gurdwara's own Google account, then set to public view-only, then the Calendar ID sent to us. After that the committee just enters paths and bookings in Google Calendar as normal and the website shows them automatically. The sangat can see the calendar but cannot change anything. Gurpurab and Nanakshahi dates are added automatically every year.

10. Who should be able to add bookings? Please send names and Gmail addresses.

11. Who should be able to add photos and events to the website? Please send 1 or 2 names.

12. Bookings are NOT taken on the website, as agreed. The page tells people to call. Is the main number right for this?

*DONATIONS*

13. We have NOT built the donate page yet, waiting on your answers.
    - How are donations taken today? Cash, check, Zelle, something else?
    - Are we a registered 501(c)(3)? If yes, what is the EIN?
    - Which do you want on the website?
      Zelle - no fees, we just show the number
      PayPal Giving Fund - no fees, needs the 501(c)(3) confirmed
      Givebutter - no fees, donors asked for an optional tip
      Stripe - about 2.2% plus 30 cents per donation
    Recommendation: Zelle if we already use it, since it costs nothing.

*GENERAL*

14. The name on the site is now "Sikh Center of SF Bay Area" with "Gurdwara Sahib El Sobrante" underneath. Correct?

15. The site says established 1969. Wikipedia says the Center was formed on 31 December 1968 and the building opened in May 1979. Which should we print?

16. Please confirm: phones (510) 223-9987 and (510) 223-1102, email info@thesikhcenter.com, address 3550 Hillcrest Rd, open daily 5:00 AM to 8:30 PM.

17. The Events section is empty until we add some. Please send a few upcoming programs and we will put them in.

18. Please read the About text on the homepage and the Academy page and tell us anything you want worded differently.

19. Hosting will cost about $7 a month. Someone needs to approve that, and confirm who controls thesikhcenter.com.

Thank you. Once we have these we can put the site live.

---

## Notes for whoever picks this up next

**Still to do once the answers arrive**

2. Upload real photos; delete the Wikipedia photo — its credit line disappears from the footer automatically once no active photo has a credit.
3. Paste the Google Calendar ID into *Gurdwara details*.
4. Restore the Academy coordinator block with real details.
5. Build the donate page once a processor is chosen.
6. Deploy per [HOSTING.md](HOSTING.md), and set `DJANGO_SECRET_KEY` / `DJANGO_DEBUG=false`.
7. `El_Sobrante_Gurdwara_Website_PRD.md` is now out of date — it describes Wagtail and a `ScheduleEntry` model that were not built.
