#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from config import CONFIG, FALLBACK_TITLES, GALLERY_STYLE
from utils import (
    PromptMeta,
    build_all_prompts,
    create_contact_sheet,
    generate_images,
    scrape_blog_titles,
)

def print_header() -> None:
    print("=" * 60)
    print("  Header generation for Endo Health blog articles")
    print(f"  Model: {CONFIG.image_model} ({CONFIG.image_quality}) | {CONFIG.image_size}")
    print("=" * 60)

def create_gallery(titles: list[str], images: list[Path | None], output_dir: Path) -> None:
    cards = []
    for idx, (title, img) in enumerate(zip(titles, images), start=1):
        if img and img.exists():
            cards.append(
                f'''  <div class="card">
    <img src="{img.name}" alt="{title}" loading="lazy">
    <div class="card-title"><span class="num">{idx}</span>{title}</div>
  </div>'''
            )

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Header generation for Endo Health blog articles</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Fraunces:wght@600;700&display=swap" rel="stylesheet">
<style>
{GALLERY_STYLE}
</style>
</head>
<body>
<div class="wrap">
  <h1>Endo Health Blog Headers</h1>
  <p class="sub">Generated header images for selected blog titles</p>
{"".join(cards)}
</div>
</body>
</html>"""

    out = output_dir / "gallery.html"
    out.write_text(html, encoding="utf-8")
    print(f"  Gallery: {out.name}")

def create_report(
    titles: list[str],
    images: list[Path | None],
    prompts: list[str],
    metas: list[PromptMeta],
    output_dir: Path,
) -> None:
    lines = [
        "# Header Generation Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Model: {CONFIG.image_model} | Size: {CONFIG.image_size} | Quality: {CONFIG.image_quality}",
        "",
    ]

    for idx, title in enumerate(titles):
        img = images[idx] if idx < len(images) else None
        meta = metas[idx] if idx < len(metas) else None
        status = "ok" if img and img.exists() else "failed"

        lines.extend(
            [
                f"## {idx + 1}. {title}",
                "",
                f"Status: {status}",
                "",
            ]
        )

        if meta:
            lines.extend(
                [
                    f"Category: {meta.category}",
                    f"Metaphor pool: {meta.metaphor_pool}",
                    f"Composition: {meta.composition}",
                    f"Color balance: {meta.color_balance}",
                    f"Objects: {', '.join(meta.objects)}",
                    "",
                ]
            )

        lines.extend(
            [
                "Prompt:",
                "",
                "```text",
                prompts[idx],
                "```",
                "",
            ]
        )

        if img and img.exists():
            lines.extend([f"![{title}](./{img.name})", ""])

        lines.extend(["---", ""])

    out = output_dir / "REPORT.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report:{out.name}")

def main() -> None:
    print_header()
    CONFIG.output_dir.mkdir(parents=True, exist_ok=True)

    titles = scrape_blog_titles(n=CONFIG.n_images)
    if not titles:
        print("Using fallback titles")
        titles = FALLBACK_TITLES[: CONFIG.n_images]
    else:
        print(f"Found {len(titles)} titles")
        for idx, title in enumerate(titles, start=1):
            print(f"  {idx:02d}. {title}")

    print("Using rule-based prompt builder")
    prompts, metas = build_all_prompts(titles)

    print("\nGenerating images...")
    images = generate_images(titles, prompts, CONFIG.output_dir)

    print("\nCreating outputs...")
    contact_sheet = create_contact_sheet(images, CONFIG.output_dir)
    if contact_sheet:
        print(f"  Contact sheet: {contact_sheet.name}")
    create_gallery(titles, images, CONFIG.output_dir)
    create_report(titles, images, prompts, metas, CONFIG.output_dir)

    success_count = sum(1 for img in images if img and img.exists())

    print(f"\n{'=' * 60}")
    print(f"  Done: {success_count}/{len(titles)} images and saved in {CONFIG.output_dir}/")
    print(f"  View: {CONFIG.output_dir / 'gallery.html'}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()