# Free Summit website

The website for [freesummitpt.com](https://freesummitpt.com). Plain HTML, CSS and JavaScript, published by GitHub Pages
from the `main` branch. Anything pushed to `main` is live about a minute later, so test on your computer first.

## Test the website on your computer

This runs the site on your own computer. Nothing is published, and all links, buttons and the PT / EN toggle work
like on the real site.

1. In VS Code, open a terminal (**Terminal → New Terminal**). It opens in the `freesummit-site` folder.
2. Start a small web server:
   ```
   python -m http.server 8080
   ```
3. Open **http://localhost:8080** in your browser.
4. After a change, refresh the page with **Ctrl+F5**.
   If you changed a file in `tools/activities/` (a `.toml` file or `_template.html`), first rebuild the activity pages
   in a second terminal:
   ```
   python tools/build_pages.py
   ```
5. When you are done, click in the terminal and press **Ctrl+C** to stop the server.

Notes:
- Use port **8080**, not 8000. The Google Workspace connector used by Claude already runs on port 8000; if you
  open `localhost:8000` you get `{"detail":"Not Found"}` instead of the website.
- Don't open `index.html` by double-clicking it. Without the server, the "Know more" buttons show a folder listing
  instead of the activity page.

## Test on your phone

Your phone must be on the **same Wi-Fi** as your computer.

1. Start the server so other devices can reach it:
   ```
   python -m http.server 8080 --bind 0.0.0.0
   ```
2. Find your computer's address: in a second terminal run `ipconfig` and look for **IPv4 Address**
   (for example `192.168.1.20`).
3. On your phone, open `http://192.168.1.20:8080` (with your own address).
4. If Windows asks whether to let Python through the firewall, allow it on **private networks** only.
5. Press **Ctrl+C** in the terminal to stop the server when you are done.

If the phone can't connect, check that both devices are on the same Wi-Fi and that the computer's network is set to
**Private** in Windows settings.

## The booking form sends real requests

Even on your computer, the booking form sends to the real Google Sheet **Booking Requests** and emails the
admin account. When you test it, write **TEST** as the name, then delete that row from the sheet.

## Checklist before publishing

- Every "Know more" button on the homepage opens the right page.
- The **PT / EN** button switches all the text, on the homepage and on the activity pages.
- On an activity page, the booking form already has that activity selected.
- The "More activities" buttons at the bottom of each activity page work.
- Prices match the **Free Summit – Activity Pricing** sheet.
- Photos load on every activity page.
- The page looks right on the phone, not only on the computer.

## Publish

When everything looks right, commit and push to `main`. GitHub Pages publishes in about a minute; hard refresh
(**Ctrl+F5**) to see the change on freesummitpt.com.
