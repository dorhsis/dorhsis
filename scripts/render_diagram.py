"""Renders assets/stack-dark.svg and assets/stack-light.svg from one layout.

GitHub picks the variant through <picture> + prefers-color-scheme, so both
files must stay in sync; edit the layout here and rerun:

    python3 scripts/render_diagram.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

WIDTH, HEIGHT = 880, 424
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
MONO_CHAR_WIDTH = 0.6  # em; holds for the monospace fonts above

# GitHub Primer colours, so the diagram sits on the profile page natively.
THEMES = {
    "dark": {
        "text": "#e6edf3",
        "muted": "#9198a1",
        "line": "#3d444d",
        "box": "#151b23",
        "accent": "#3fb950",
        "chip": "#3fb95026",
    },
    "light": {
        "text": "#1f2328",
        "muted": "#59636e",
        "line": "#d1d9e0",
        "box": "#f6f8fa",
        "accent": "#1a7f37",
        "chip": "#1a7f371f",
    },
}

COLUMN_X = (20, 308, 596)
COLUMN_W = 264
CARD_H = 68
CLIENTS = (
    ("Student web app", "Next.js 16 · React 19"),
    ("Teacher & admin workspace", "Angular 17 · TypeScript"),
    ("Mobile app", "Flutter · Dart"),
)
API_TITLE = "Spring Boot 3.5 API"
API_SUBTITLE = "Java 21 · Spring Security · JWT · Flyway"
API_MODULES = (
    "live lessons",
    "homework & grading",
    "adaptive test · 3PL IRT",
    "course catalog",
    "notifications",
)
STORAGE = (
    ("PostgreSQL 15", "schema via Flyway migrations"),
    ("MinIO · S3", "audio, lesson files, covers"),
    ("Firebase Cloud Messaging", "push to the mobile app"),
)
TRANSPORT_LABEL = "REST · WebSocket (STOMP)"


def text(x, y, value, *, size, fill, family=SANS, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def box(x, y, w, h, *, fill, stroke, width=1):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def line(x1, y1, x2, y2, *, stroke):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.5"/>'


def card(x, y, title, subtitle, c):
    return [
        box(x, y, COLUMN_W, CARD_H, fill=c["box"], stroke=c["line"]),
        text(x + 20, y + 28, title, size=16, fill=c["text"], weight=600),
        text(x + 20, y + 49, subtitle, size=13, fill=c["muted"], family=MONO),
    ]


def chips(x, y, labels, c, *, size=12.5, pad=12, gap=10):
    parts = []
    for label in labels:
        w = len(label) * size * MONO_CHAR_WIDTH + 2 * pad
        parts.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="28" rx="14" fill="{c["chip"]}"/>')
        parts.append(text(f"{x + pad:.1f}", y + 18.5, label, size=size, fill=c["text"], family=MONO))
        x += w + gap
    return parts, x - gap


def render(c):
    centers = [x + COLUMN_W // 2 for x in COLUMN_X]
    parts = []

    for x, (title, subtitle) in zip(COLUMN_X, CLIENTS):
        parts += card(x, 20, title, subtitle, c)

    bus_y = 130
    parts += [line(cx, 20 + CARD_H, cx, bus_y, stroke=c["line"]) for cx in centers]
    parts.append(line(centers[0], bus_y, centers[-1], bus_y, stroke=c["line"]))
    parts.append(line(centers[1], bus_y, centers[1], 168, stroke=c["line"]))
    parts.append(text(centers[1] + 12, 154, TRANSPORT_LABEL, size=12.5, fill=c["muted"], family=MONO))

    parts.append(box(20, 168, 840, 120, fill=c["box"], stroke=c["accent"], width=1.5))
    parts.append(text(44, 201, API_TITLE, size=18, fill=c["text"], weight=600))
    parts.append(text(44, 223, API_SUBTITLE, size=13, fill=c["muted"], family=MONO))
    chip_parts, chips_right = chips(44, 242, API_MODULES, c)
    if chips_right > 840:
        raise ValueError(f"module chips overflow the API box: right edge at {chips_right:.0f}px")
    parts += chip_parts

    parts += [line(cx, 288, cx, 336, stroke=c["line"]) for cx in centers]
    for x, (title, subtitle) in zip(COLUMN_X, STORAGE):
        parts += card(x, 336, title, subtitle, c)

    body = "\n  ".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Just to Study platform architecture</title>
  <desc id="desc">A Next.js student app, an Angular teacher and admin workspace and a Flutter mobile app talk to a Spring Boot API over REST and WebSocket. The API covers live lessons, homework, the adaptive placement test, the course catalog and notifications, and stores data in PostgreSQL, files in MinIO and sends push through Firebase Cloud Messaging.</desc>
  {body}
</svg>
"""


def main():
    assets = Path(__file__).resolve().parent.parent / "assets"
    for name, colours in THEMES.items():
        (assets / f"stack-{name}.svg").write_text(render(colours), encoding="utf-8")


if __name__ == "__main__":
    main()
