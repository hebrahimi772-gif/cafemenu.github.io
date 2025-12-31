#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cafe Menu HTML Generator (FA / RTL)
Input : cafe.json
Output: output/menu.html + output/style.css

Run:
  python generate_menu.py --input cafe.json --outdir output --title "منو"

Notes:
- Uses Vazirmatn via CDN.
- Pure HTML/CSS (no build tools).
"""

from __future__ import annotations
import argparse
import json
import os
import re
from datetime import datetime
from html import escape
from typing import Any, Dict, List, Optional


PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def to_persian_digits(s: str) -> str:
    return s.translate(PERSIAN_DIGITS)


def is_url(s: str) -> bool:
    return bool(re.match(r"^https?://", s.strip(), flags=re.I))


def norm_text(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def fmt_price(price: Any, currency: str, use_persian_digits: bool) -> str:
    """
    price can be:
      - number: 120000
      - string: "۱۲۰" / "120"
      - "-" for unavailable
    """
    p = norm_text(price)
    if not p or p == "-":
        return "-"
    # keep user formatting if they gave Persian digits already
    out = p
    # add currency suffix if looks like a number
    if re.match(r"^[0-9۰-۹,]+$", p):
        out = f"{p} {currency}".strip()
    if use_persian_digits:
        out = to_persian_digits(out)
    return out


def safe_write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


CSS = r"""
:root{
  --bg: #0b0f14;
  --card: rgba(255,255,255,.06);
  --card2: rgba(255,255,255,.085);
  --text: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.65);
  --line: rgba(255,255,255,.12);
  --accent: #ffd28a;
  --shadow: 0 12px 30px rgba(0,0,0,.35);
  --radius: 18px;
}

*{ box-sizing:border-box; }
html,body{ height:100%; }
body{
  margin:0;
  background:
    radial-gradient(900px 500px at 80% 10%, rgba(255,210,138,.13), transparent 60%),
    radial-gradient(700px 400px at 10% 20%, rgba(138,194,255,.10), transparent 60%),
    var(--bg);
  color: var(--text);
  font-family: "Vazirmatn", system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans Arabic", Arial, sans-serif;
  direction: rtl;
  line-height: 1.65;
}

a{ color: inherit; text-decoration: none; }
a:hover{ opacity:.9; text-decoration: underline; }

.container{
  width:min(1100px, 92vw);
  margin: 0 auto;
  padding: 24px 0 56px;
}

.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding: 10px 0 18px;
}

.badge{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255,255,255,.03);
}

.brand h1{
  margin: 8px 0 4px;
  font-size: clamp(26px, 4vw, 40px);
  letter-spacing: .2px;
}
.brand .subtitle{
  color: var(--muted);
  font-size: 14px;
}

.hero{
  margin-top: 8px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  box-shadow: var(--shadow);
  overflow:hidden;
}

.hero-inner{
  padding: 18px 18px 8px;
  display:grid;
  grid-template-columns: 1.2fr .8fr;
  gap: 14px;
}

@media (max-width: 840px){
  .hero-inner{ grid-template-columns: 1fr; }
}

.quicklinks{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  padding: 10px 18px 18px;
  border-top: 1px solid var(--line);
}

.pill{
  border: 1px solid var(--line);
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,.03);
  color: var(--muted);
}
.pill strong{ color: var(--text); font-weight: 600; }

.info{
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(0,0,0,.18);
  padding: 14px 14px 10px;
}
.info h3{ margin:0 0 6px; font-size: 15px; }
.info .row{ color: var(--muted); font-size: 14px; margin: 6px 0; }
.info .row b{ color: var(--text); font-weight: 600; }

.section{
  margin-top: 22px;
}

.section-title{
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  margin: 0 0 10px;
}
.section-title h2{
  margin:0;
  font-size: 18px;
}
.section-title .hint{
  color: var(--muted);
  font-size: 13px;
}

.grid{
  display:grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
@media (max-width: 840px){
  .grid{ grid-template-columns: 1fr; }
}

.item{
  display:flex;
  gap: 12px;
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 10px 22px rgba(0,0,0,.18);
}

.thumb{
  width: 58px;
  height: 58px;
  border-radius: 14px;
  background:
    radial-gradient(16px 16px at 30% 30%, rgba(255,210,138,.40), transparent 60%),
    radial-gradient(18px 18px at 70% 70%, rgba(138,194,255,.35), transparent 60%),
    rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.12);
  flex: 0 0 auto;
  overflow:hidden;
  display:flex;
  align-items:center;
  justify-content:center;
  color: rgba(255,255,255,.75);
  font-size: 18px;
}

.thumb img{
  width:100%;
  height:100%;
  object-fit: cover;
  display:block;
}

.meta{ flex: 1 1 auto; min-width: 0; }
.meta .name{
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}
.meta .name h4{
  margin:0;
  font-size: 16px;
}
.price{
  white-space:nowrap;
  font-weight: 700;
  color: var(--accent);
}
.desc{
  margin-top: 6px;
  color: var(--muted);
  font-size: 13px;
}

.footer{
  margin-top: 26px;
  color: var(--muted);
  font-size: 12px;
  text-align:center;
  opacity:.9;
}
"""


def render_html(data: Dict[str, Any], page_title: str, use_persian_digits: bool) -> str:
    cafe = data.get("cafe", {})
    menu: List[Dict[str, Any]] = data.get("menu", [])

    cafe_name = escape(norm_text(cafe.get("name", "کافه")))
    subtitle = escape(norm_text(cafe.get("subtitle", "")))
    address = escape(norm_text(cafe.get("address", "")))
    phone = escape(norm_text(cafe.get("phone", "")))
    instagram = norm_text(cafe.get("instagram", ""))
    telegram = norm_text(cafe.get("telegram", ""))
    whatsapp = norm_text(cafe.get("whatsapp", ""))
    maps = norm_text(cafe.get("maps", ""))
    currency = norm_text(cafe.get("currency", "هزار تومان")) or "هزار تومان"

    def link_or_text(label: str, val: str) -> str:
        if not val:
            return ""
        txt = escape(val)
        if is_url(val):
            return f'<div class="row"><b>{escape(label)}:</b> <a href="{escape(val)}" target="_blank" rel="noopener">{txt}</a></div>'
        return f'<div class="row"><b>{escape(label)}:</b> {txt}</div>'

    # quick category anchors
    cat_pills = []
    for idx, cat in enumerate(menu, start=1):
        title = norm_text(cat.get("title", f"دسته {idx}"))
        anchor = f"cat-{idx}"
        cat_pills.append(f'<a class="pill" href="#{anchor}"><strong>{escape(title)}</strong></a>')
    cat_pills_html = "\n".join(cat_pills)

    sections_html = []
    for idx, cat in enumerate(menu, start=1):
        title = escape(norm_text(cat.get("title", f"دسته {idx}")))
        hint = escape(norm_text(cat.get("hint", "")))
        anchor = f"cat-{idx}"
        items: List[Dict[str, Any]] = cat.get("items", [])

        cards = []
        for it in items:
            name = escape(norm_text(it.get("name", ""))) or "بدون نام"
            desc = escape(norm_text(it.get("desc", "")))
            price = fmt_price(it.get("price", ""), currency=currency, use_persian_digits=use_persian_digits)
            price_html = escape(price)

            img = norm_text(it.get("img", ""))
            if img and is_url(img):
                thumb = f'<div class="thumb"><img src="{escape(img)}" alt="{name}"></div>'
            else:
                # simple emoji-ish fallback
                icon = escape(norm_text(it.get("icon", "☕")))
                thumb = f'<div class="thumb">{icon}</div>'

            desc_html = f'<div class="desc">{desc}</div>' if desc else ""
            cards.append(
                f"""
                <div class="item">
                  {thumb}
                  <div class="meta">
                    <div class="name">
                      <h4>{name}</h4>
                      <div class="price">{price_html}</div>
                    </div>
                    {desc_html}
                  </div>
                </div>
                """.strip()
            )

        grid = "\n".join(cards) if cards else '<div class="item"><div class="meta"><div class="desc">فعلاً آیتمی ثبت نشده.</div></div></div>'
        sections_html.append(
            f"""
            <section class="section" id="{anchor}">
              <div class="section-title">
                <h2>{title}</h2>
                <div class="hint">{hint}</div>
              </div>
              <div class="grid">
                {grid}
              </div>
            </section>
            """.strip()
        )

    sections = "\n\n".join(sections_html)

    # optional digits
    phone_disp = to_persian_digits(phone) if (use_persian_digits and phone) else phone

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="color-scheme" content="dark" />
  <title>{escape(page_title)} | {cafe_name}</title>

  <!-- Persian font -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;600;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="style.css" />
</head>

<body>
  <div class="container">
    <div class="topbar">
      <div class="badge">📍 <span>{escape(address) if address else "آدرس را در ورودی وارد کنید"}</span></div>
      <a class="badge" href="#cat-1">🧾 <span>{escape(page_title)}</span></a>
    </div>

    <div class="brand">
      <h1>{cafe_name}</h1>
      <div class="subtitle">{subtitle}</div>
    </div>

    <div class="hero">
      <div class="hero-inner">
        <div>
          <div class="pill">دسته‌ها</div>
          <div style="height:10px"></div>
          <div style="display:flex;flex-wrap:wrap;gap:10px">
            {cat_pills_html}
          </div>
        </div>

        <div class="info">
          <h3>اطلاعات تماس</h3>
          {f'<div class="row"><b>تلفن:</b> {escape(phone_disp)}</div>' if phone else '<div class="row">تلفن را در ورودی وارد کنید.</div>'}
          {link_or_text("اینستاگرام", instagram)}
          {link_or_text("تلگرام", telegram)}
          {link_or_text("واتس‌اپ", whatsapp)}
          {link_or_text("نقشه", maps)}
        </div>
      </div>

      <div class="quicklinks">
        <span class="pill">واحد قیمت: <strong>{escape(currency)}</strong></span>
        <span class="pill">نمایش: <strong>RTL</strong></span>
      </div>
    </div>

    {sections}

    <div class="footer">
      ساخته‌شده با ژنراتور پایتون • {escape(generated_at)}
    </div>
  </div>
</body>
</html>
"""
    return html


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Persian RTL cafe menu HTML from JSON.")
    ap.add_argument("--input", "-i", required=True, help="Path to cafe.json")
    ap.add_argument("--outdir", "-o", default="output", help="Output directory")
    ap.add_argument("--title", default="منو", help="Page title")
    ap.add_argument("--persian-digits", action="store_true", help="Render numbers using Persian digits")
    args = ap.parse_args()

    data = load_json(args.input)

    html = render_html(data, page_title=args.title, use_persian_digits=args.persian_digits)

    out_html = os.path.join(args.outdir, "menu.html")
    out_css = os.path.join(args.outdir, "style.css")

    safe_write(out_css, CSS.strip() + "\n")
    safe_write(out_html, html)

    print("✅ Done")
    print(f"HTML: {out_html}")
    print(f"CSS : {out_css}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
