/**
 * Free Summit – booking form receiver (Google Apps Script)
 *
 * What it does: every request sent from the website form is added as a row
 * to the Google Sheet this script is attached to, and you get an email.
 * Replying to that email replies straight to the client.
 *
 * Setup (5 minutes, signed in as admin@freesummitpt.com):
 *  (Column "Page" shows which landing page the request came from: home, guia, via-ferrata, caminhada-arrabida.)
 *
 *  1. Create a new Google Sheet, e.g. "Free Summit – Booking requests".
 *  2. In the Sheet: Extensions → Apps Script. Delete the sample code and paste this file.
 *  3. Click Deploy → New deployment → type "Web app".
 *       Execute as: Me    ·    Who has access: Anyone
 *     Authorise when asked (Google will warn that the app is unverified: Advanced → Go to project).
 *  4. Copy the Web app URL (ends in /exec).
 *  5. In index.html, paste it into:  const FORM_ENDPOINT = "…/exec";
 *  If you edit this script later, use Deploy → Manage deployments → Edit → New version,
 *  so the URL stays the same.
 */

const NOTIFY_EMAIL = 'admin@freesummitpt.com';
const SHEET_NAME = 'Pedidos';
const FIELDS = ['name', 'email', 'phone', 'activity', 'date', 'people', 'type', 'transfer', 'message', 'lang', 'source'];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return ok_(); // spam trap filled in: ignore silently

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow(['Received', 'Name', 'Email', 'Phone', 'Activity', 'Date', 'People',
                       'Type', 'Transfer', 'Message', 'Language', 'Page', 'Status']);
      sheet.setFrozenRows(1);
    }
    const row = [new Date()].concat(FIELDS.map(f => String(p[f] || '').slice(0, 2000)), ['New']);
    sheet.appendRow(row);
  } finally {
    lock.releaseLock();
  }

  const lines = FIELDS.map(f => f.charAt(0).toUpperCase() + f.slice(1) + ': ' + (p[f] || '—'));
  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    replyTo: p.email || NOTIFY_EMAIL,
    subject: 'Novo pedido: ' + (p.activity || 'actividade') + ' – ' + (p.name || ''),
    body: lines.join('\n') + '\n\nVer todos os pedidos: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
  });

  return ok_();
}

function ok_() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
