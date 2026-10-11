"""Generates the activity pages (guia/, via-ferrata/, ...) from a template and data files.

  tools/activities/_template.html   the HTML of an activity page, with {{placeholders}}
  tools/activities/_shared.toml     settings shared by all pages (booking form activities)
  tools/activities/<slug>.toml      one file per activity -> builds <slug>/index.html

To add an activity: copy one of the .toml files, rename it (the name becomes the web
address) and edit it. Then run from anywhere:  python tools/build_pages.py"""
import html, os, re, sys, tomllib

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


if __name__ == "__main__":
    main()
