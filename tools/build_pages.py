"""Generates the activity pages (guia/, via-ferrata/, ...) from a template and data files.

  tools/activities/_template.html   the HTML of an activity page, with {{placeholders}}
  tools/activities/_shared.toml     settings shared by all pages (booking form activities)
  tools/activities/<slug>.toml      one file per activity -> builds <slug>/index.html

It also writes the booking API documentation for AI agents and developers
(api/index.html, api/booking.json, llms.txt) from the same data, so the list of
activities agents can book always matches the booking form.

To add an activity: copy one of the .toml files, rename it (the name becomes the web
address) and edit it. Then run from anywhere:  python tools/build_pages.py"""
import html, json, os, re, sys, tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root = the website
DATA = os.path.join(ROOT, "tools", "activities")


class TemplateError(Exception):
    pass


# --- A tiny template engine (a small subset of "Mustache") -------------------------
# {{name}} / {{a.b}}   value (HTML-escaped)
# {{#name}}...{{/name}} repeat for each item of a list, or show once if the value is set
# {{^name}}...{{/name}} show only if the value is missing or empty
# {{!-- ... --}}       note, removed
# A section tag alone on its line removes that whole line, so the output stays tidy.
COMMENT = re.compile(r"[ \t]*\{\{!--.*?--\}\}[ \t]*\n?", re.S)
TAG = re.compile(r"(^[ \t]*)?\{\{\s*([#^/]?)\s*([\w.\-]+)\s*\}\}([ \t]*(?:\n|$))?", re.M)


def parse(text):
    root, stack, pos = [], [], 0
    node = root
    for m in TAG.finditer(text):
        indent, kind, name, trail = m.group(1), m.group(2), m.group(3), m.group(4)
        standalone = kind and indent is not None and trail is not None
        if standalone:
            node.append(text[pos:m.start()])
        else:
            node.append(text[pos:m.start() + len(indent or "")])
        pos = m.end() if standalone else m.end() - len(trail or "")
        if kind in ("#", "^"):
            section = (kind, name, [])
            node.append(section)
            stack.append((node, name))
            node = section[2]
        elif kind == "/":
            if not stack or stack[-1][1] != name:
                raise TemplateError(f"{{{{/{name}}}}} does not close an open {{{{#{name}}}}}")
            node = stack.pop()[0]
        else:
            node.append(("=", name))
    if stack:
        raise TemplateError(f"{{{{#{stack[-1][1]}}}}} is never closed with {{{{/{stack[-1][1]}}}}}")
    node.append(text[pos:])
    return root


MISSING = object()


def lookup(ctx, name):
    if name == ".":
        return ctx[-1]
    first, *rest = name.split(".")
    for scope in reversed(ctx):
        if isinstance(scope, dict) and first in scope:
            value = scope[first]
            break
    else:
        return MISSING
    for key in rest:
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, str) and key in ("en", "pt"):
            pass  # plain text, same in both languages
        else:
            return MISSING
    return value


def render(nodes, ctx):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(n)
        elif n[0] == "=":
            value = lookup(ctx, n[1])
            if value is MISSING or isinstance(value, (dict, list)):
                raise TemplateError(f"{{{{{n[1]}}}}} has no text value in the data")
            out.append(html.escape(str(value), quote=False).replace('"', "&quot;"))
        else:
            kind, name, body = n
            value = lookup(ctx, name)
            empty = value is MISSING or not value
            if kind == "^":
                if empty:
                    out.append(render(body, ctx))
            elif isinstance(value, list):
                out.extend(render(body, ctx + [item]) for item in value)
            elif not empty:
                out.append(render(body, ctx + [value]))
    return "".join(out)


# --- Build -------------------------------------------------------------------------
def load(name):
    path = os.path.join(DATA, name)
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        sys.exit(f"Error in {path}: {e}")


def main():
    with open(os.path.join(DATA, "_template.html"), encoding="utf-8") as f:
        template = parse(COMMENT.sub("", f.read()))
    shared = load("_shared.toml")
    pages = []
    for name in sorted(os.listdir(DATA)):
        if name.endswith(".toml") and not name.startswith("_"):
            page = load(name)
            page["slug"] = name[:-len(".toml")]
            pages.append(page)
    pages.sort(key=lambda p: (p.get("order", 999), p["slug"]))

    for page in pages:
        page["other_pages"] = [p for p in pages if p is not page]
        try:
            result = render(template, [shared, page])
        except TemplateError as e:
            sys.exit(f"Error building {page['slug']}.toml: {e}")
        os.makedirs(os.path.join(ROOT, page["slug"]), exist_ok=True)
        path = os.path.join(ROOT, page["slug"], "index.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(result)
        print("wrote", path)

    build_api(shared, pages)


# --- Booking API docs (api/index.html, api/booking.json, llms.txt) -----------------
SITE = "https://freesummitpt.com"


def form_endpoint():
    """The Apps Script URL, read from assets/config.js (never written by this script)."""
    with open(os.path.join(ROOT, "assets", "config.js"), encoding="utf-8") as f:
        m = re.search(r'formEndpoint\s*:\s*"([^"]*)"', f.read())
    url = m.group(1).strip() if m else ""
    if not url.endswith("/exec"):
        sys.exit("assets/config.js has no formEndpoint ending in /exec: cannot write the API docs")
    return url


def text(value, lang="en"):
    return value.get(lang, value.get("en", "")) if isinstance(value, dict) else str(value or "")


def build_api(shared, pages):
    endpoint = form_endpoint()
    base, _, path = endpoint.rpartition("/")
    by_value = {p.get("form_value"): p for p in pages}
    activities = []
    for opt in shared["form_options"]:
        page = by_value.get(opt["value"])
        activities.append({
            "value": opt["value"],
            "page": f"{SITE}/{page['slug']}/" if page else None,
            "from_price": text(page.get("price")) or None if page else None,
            "summary": page.get("description") if page else None,
        })
    act_values = [a["value"] for a in activities]
    types = shared["type_options"]
    transfers = shared["transfer_options"]

    fields = {
        "name": {"type": "string", "maxLength": 200, "description": "Client's full name."},
        "email": {"type": "string", "format": "email", "description": "Client's email. Free Summit replies here."},
        "phone": {"type": "string", "maxLength": 40, "description": "Client's phone or WhatsApp, with country code. Optional."},
        "activity": {"type": "string", "enum": act_values, "description": "Exactly one of the listed values."},
        "date": {"type": "string", "format": "date", "description": "Preferred date, YYYY-MM-DD, today or later. Optional."},
        "people": {"type": "integer", "minimum": 1, "maximum": 20, "default": 2, "description": "Number of participants."},
        "type": {"type": "string", "enum": [t["value"] for t in types], "default": types[0]["value"],
                 "description": "; ".join(f"{t['value']}: {t['en']}" for t in types) + "."},
        "transfer": {"type": "string", "enum": [t["value"] for t in transfers], "default": transfers[0]["value"],
                     "description": "Transport. " + "; ".join(f"{t['value']}: {t['en']}" for t in transfers) + "."},
        "message": {"type": "string", "maxLength": 2000,
                    "description": "Anything else: experience, children's ages, morning or afternoon, questions. Optional."},
        "lang": {"type": "string", "enum": ["en", "pt"], "default": "en", "description": "Language Free Summit should reply in."},
        "agent": {"type": "string", "maxLength": 100,
                  "description": "Name of the AI agent or app sending the request, e.g. 'Claude'. Optional but appreciated."},
    }
    request_schema = {"type": "object", "required": ["name", "email", "activity"],
                      "properties": fields, "additionalProperties": False}
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Free Summit booking requests",
            "version": "1.0.0",
            "description": (
                "Send a booking request for a guided outdoor activity near Lisbon (rock climbing, via ferrata, hiking) "
                "on behalf of a client, without filling in the website form. This creates a REQUEST, not a confirmed "
                "booking: Free Summit replies to the client's email within 24 hours with availability and the price, "
                "and the booking is confirmed when the client replies to accept. "
                f"Human-readable docs: {SITE}/api/"),
            "contact": {"name": "Free Summit", "email": "hello@freesummitpt.com", "url": SITE},
        },
        "servers": [{"url": base}],
        "paths": {
            f"/{path}": {
                "get": {
                    "operationId": "getBookingInfo",
                    "summary": "Check the service is up and get the link to this description.",
                    "responses": {"200": {"description": "Service info", "content": {"application/json": {}}}},
                },
                "post": {
                    "operationId": "createBookingRequest",
                    "summary": "Send a booking request for one activity.",
                    "description": (
                        "Google Apps Script answers with an HTTP 302 redirect; follow it with a GET (curl -L does) to "
                        "read the JSON result. The HTTP status is always 200: check the 'ok' field."),
                    "requestBody": {"required": True, "content": {
                        "application/json": {"schema": request_schema},
                        "application/x-www-form-urlencoded": {"schema": request_schema},
                    }},
                    "responses": {"200": {"description": "Result. ok=true: request saved. ok=false: see errors.",
                                          "content": {"application/json": {"schema": {
                                              "type": "object",
                                              "properties": {
                                                  "ok": {"type": "boolean"},
                                                  "id": {"type": "string", "description": "Reference, e.g. FS-20261121-4F2A"},
                                                  "message": {"type": "string"},
                                                  "errors": {"type": "array", "items": {"type": "object", "properties": {
                                                      "field": {"type": "string"}, "message": {"type": "string"}}}},
                                              }}}}}},
                },
            }
        },
        "x-activities": activities,
    }
    os.makedirs(os.path.join(ROOT, "api"), exist_ok=True)
    write(os.path.join(ROOT, "api", "booking.json"), json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

    example = {"name": "Ana Silva", "email": "ana@example.com", "phone": "+351 912 345 678",
               "activity": act_values[0], "date": "2027-03-14", "people": 2, "type": types[0]["value"],
               "transfer": transfers[0]["value"], "message": "First time climbing. Morning preferred.",
               "lang": "en", "agent": "Claude"}
    curl = (f"curl -L -X POST '{endpoint}' \\\n  -H 'Content-Type: application/json' \\\n"
            f"  -d '{json.dumps(example, ensure_ascii=False)}'")

    # llms.txt: plain-text guide for AI agents (llmstxt.org)
    lines = [
        "# Free Summit",
        "",
        "> Guided rock climbing, via ferrata and hiking near Lisbon, Portugal (Cascais, Sintra, Arrábida, Sesimbra). "
        "Guide, gear and insurance included. AI agents can send booking requests through a simple API instead of the website form.",
        "",
        "## Booking requests for AI agents",
        "",
        f"- Endpoint: POST {endpoint} (JSON or form-encoded). Follow the 302 redirect to read the JSON reply; check the `ok` field.",
        f"- OpenAPI description: {SITE}/api/booking.json",
        f"- Human-readable docs: {SITE}/api/",
        "- Required fields: name, email, activity. Optional: phone, date (YYYY-MM-DD), people, type, transfer, message, lang (en|pt), agent.",
        "- This is a request, not a confirmed booking. Tell the client that Free Summit replies by email within 24 hours "
        "with availability and the price, and the booking is confirmed when the client replies to accept.",
        "- Only send a request the client has asked for, with their real contact details.",
        "",
        "## Activities (use the exact value in the `activity` field)",
        "",
    ]
    for a in activities:
        extra = []
        if a["from_price"]:
            extra.append(f"from {a['from_price']} per person")
        if a["page"]:
            extra.append(a["page"])
        lines.append(f"- {a['value']}" + (f": {', '.join(extra)}" if extra else ""))
    lines += ["", "## Options", ""]
    lines.append("- type: " + "; ".join(f"`{t['value']}` ({t['en']})" for t in types))
    lines.append("- transfer: " + "; ".join(f"`{t['value']}` ({t['en']})" for t in transfers))
    lines += ["", "## Example", "", "```", curl, "```", "",
              "## Contact", "", "- hello@freesummitpt.com", f"- {SITE}", ""]
    write(os.path.join(ROOT, "llms.txt"), "\n".join(lines))

    # api/index.html: the same, for people (English only: the audience is developers and agents)
    e = lambda v: html.escape(str(v))
    rows = "".join(
        f"<tr><td><code>{e(k)}</code></td><td>{'yes' if k in request_schema['required'] else 'no'}</td>"
        f"<td>{e(v['description'])}</td></tr>\n" for k, v in fields.items())
    acts = "".join(
        f"<li><code>{e(a['value'])}</code>"
        + (f" &middot; from {e(a['from_price'])}" if a["from_price"] else "")
        + (f" &middot; <a href=\"{e(a['page'])}\">page</a>" if a["page"] else "") + "</li>\n"
        for a in activities)
    opts = lambda items: "".join(f"<li><code>{e(t['value'])}</code>: {e(t['en'])}</li>" for t in items)
    page = API_PAGE.format(endpoint=e(endpoint), rows=rows, acts=acts, types=opts(types),
                           transfers=opts(transfers), curl=e(curl.replace("\\\n", "\\\n")))
    write(os.path.join(ROOT, "api", "index.html"), page)



def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", path)


API_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Booking API for AI agents · Free Summit</title>
<meta name="description" content="Send Free Summit booking requests from an AI agent or app, without filling in the website form.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#ECEEBF">
<link rel="icon" href="../assets/favicon.png">
<link rel="service-desc" href="booking.json" type="application/json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<style>
  .api{{padding:clamp(40px,6vw,80px) 0;max-width:860px}}
  .api h1{{font-size:clamp(40px,7vw,80px);margin:0 0 24px}}
  .api h2{{font-size:24px;margin:48px 0 12px}}
  .api code,.api pre{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px}}
  .api pre{{background:var(--olive);color:var(--cream);padding:18px;border-radius:4px;overflow-x:auto;white-space:pre-wrap;word-break:break-all}}
  .api table{{width:100%;border-collapse:collapse;font-size:15px}}
  .api td,.api th{{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1.5px solid var(--rule)}}
</style>
</head>
<body data-page="api">
<header class="nav"><div class="wrap"><a class="mark" href="../" aria-label="Free Summit, home">FREE<br>SUMMIT</a></div></header>
<main class="wrap api">
<h1 class="xb">Booking API</h1>
<p>AI agents and apps can send a booking request straight to Free Summit, without filling in the website form.
A request is not a confirmed booking: we reply to the client by email within 24 hours with availability and the price,
and the booking is confirmed when the client replies to accept.</p>
<p>Machine-readable: <a href="booking.json">OpenAPI description</a> &middot; <a href="../llms.txt">llms.txt</a></p>

<h2 class="xb">Endpoint</h2>
<p><code>POST {endpoint}</code></p>
<p>Send JSON (<code>Content-Type: application/json</code>) or form fields. The server answers with a redirect:
follow it (for example <code>curl -L</code>) to read the JSON reply. The HTTP status is always 200, so check
<code>ok</code>: <code>{{"ok": true, "id": "FS-&hellip;"}}</code> means the request was saved;
<code>{{"ok": false, "errors": [&hellip;]}}</code> lists what to fix.</p>

<h2 class="xb">Fields</h2>
<table><thead><tr><th>Field</th><th>Required</th><th>Notes</th></tr></thead><tbody>
{rows}</tbody></table>

<h2 class="xb">Activities</h2>
<p>Use one of these values exactly in <code>activity</code>.</p>
<ul>
{acts}</ul>

<h2 class="xb">Type</h2>
<ul>{types}</ul>
<h2 class="xb">Transfer</h2>
<ul>{transfers}</ul>

<h2 class="xb">Example</h2>
<pre>{curl}</pre>

<h2 class="xb">Please</h2>
<ul>
<li>Only send a request the client asked for, with their real name and email.</li>
<li>One request per activity and date. Put questions in <code>message</code>.</li>
<li>Tell the client to expect an email from hello@freesummitpt.com.</li>
</ul>
<p>Questions: <a href="mailto:hello@freesummitpt.com">hello@freesummitpt.com</a></p>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
