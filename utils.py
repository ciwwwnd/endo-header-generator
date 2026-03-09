from __future__ import annotations

import base64
import os
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from config import (
    CATEGORY_CONFIG,
    COLOR_BALANCES,
    COMPOSITIONS,
    CONFIG,
    METAPHOR_POOLS,
    NEGATIVE_STYLE,
    OBJECT_POOLS,
    OPTIONAL_MOTIFS,
    PROMPT_BLOCKS,
    SKIP_PATTERNS,
)

try:
    import requests
    from bs4 import BeautifulSoup

    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False

try:
    from openai import OpenAI
except ImportError:
    sys.exit("Missing required dependency: openai")

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@dataclass
class PromptPlan:
    composition: str
    metaphor: str
    color_balance: str
    objects: list[str] = field(default_factory=list)
    optional_motif: str = ""
    extra_rule: str = ""


@dataclass
class PromptMeta:
    category: str
    metaphor_pool: str
    composition: str
    color_balance: str
    objects: list[str] = field(default_factory=list)
    source: str = "rules"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def title_is_valid(title: str, seen: set[str]) -> bool:
    return bool(
        title
        and len(title) > 10
        and title not in seen
        and not any(pattern in title.lower() for pattern in SKIP_PATTERNS)
    )


def classify_title(title: str) -> str:
    lower = normalize(title)
    for category, cfg in CATEGORY_CONFIG.items():
        if any(keyword in lower for keyword in cfg.keywords):
            return category
    return "daily_life"


def collect_unique_pool_items(pool_names: list[str]) -> list[str]:
    items: list[str] = []
    seen: set[str] = set()

    for pool_name in pool_names:
        for item in OBJECT_POOLS.get(pool_name, []):
            if item not in seen:
                seen.add(item)
                items.append(item)

    return items


def sample_objects_from_pools(
    pool_names: list[str],
    k_range: tuple[int, int] = (2, 3),
) -> list[str]:
    candidates = collect_unique_pool_items(pool_names)
    if not candidates:
        return []

    k = min(random.randint(*k_range), len(candidates))
    return random.sample(candidates, k)


def choose_composition(used_counts: dict[str, int]) -> str:
    ranked = sorted(COMPOSITIONS, key=lambda comp: used_counts.get(comp, 0))
    top_choices = ranked[: min(2, len(ranked))]
    chosen = random.choice(top_choices)
    used_counts[chosen] = used_counts.get(chosen, 0) + 1
    return chosen


def build_anatomy_directive(title: str) -> str:
    organ_keywords = ["gebärmutter", "eierstock", "ovar", "uterus", "eileiter"]
    title_mentions_organ = any(keyword in normalize(title) for keyword in organ_keywords)

    if title_mentions_organ:
        return (
            "The title mentions a specific organ. A small, subtle, abstracted "
            "organ shape is acceptable — but do NOT make it the dominant focal "
            "element. Prefer showing it as a secondary background element."
        )

    return (
        "Do NOT include any uterus, ovary, fallopian tube, or reproductive "
        "organ symbol anywhere in this image. Not even as a small background "
        "element. Use indirect metaphor, abstract shapes, or objects instead."
    )


def build_prompt_plan(category: str, used_compositions: dict[str, int]) -> PromptPlan:
    cfg = CATEGORY_CONFIG[category]

    return PromptPlan(
        composition=choose_composition(used_compositions),
        metaphor=random.choice(METAPHOR_POOLS[cfg.metaphor_pool]),
        color_balance=random.choice(COLOR_BALANCES),
        objects=sample_objects_from_pools(cfg.object_pools, k_range=(2, 3)),
        optional_motif=random.choice(OPTIONAL_MOTIFS),
        extra_rule=cfg.extra_rule,
    )


def render_prompt(title: str, category: str, plan: PromptPlan, anatomy_directive: str) -> str:
    sections = [
        *PROMPT_BLOCKS,
        f'Article: "{title}"',
        f"Category: {category}",
        "Anatomy directive:",
        anatomy_directive,
        "Creative direction:",
        f"Composition type: {plan.composition}.",
        f"Main metaphor: {plan.metaphor}.",
        f'Supporting elements (use only these): {", ".join(plan.objects)}.',
        f"{plan.optional_motif}.",
        f"Color balance: {plan.color_balance}.",
        plan.extra_rule,
        NEGATIVE_STYLE,
    ]
    return "\n\n".join(section for section in sections if section.strip())


def build_prompt(title: str, used_compositions: dict[str, int]) -> tuple[str, PromptMeta]:
    category = classify_title(title)
    cfg = CATEGORY_CONFIG[category]
    plan = build_prompt_plan(category, used_compositions)
    anatomy_directive = build_anatomy_directive(title)
    prompt = render_prompt(title, category, plan, anatomy_directive)

    meta = PromptMeta(
        category=category,
        metaphor_pool=cfg.metaphor_pool,
        composition=plan.composition,
        color_balance=plan.color_balance,
        objects=plan.objects,
    )
    return prompt, meta


def build_all_prompts(titles: list[str]) -> tuple[list[str], list[PromptMeta]]:
    used_compositions: dict[str, int] = {}
    prompts: list[str] = []
    metas: list[PromptMeta] = []

    for title in titles:
        prompt, meta = build_prompt(title, used_compositions)
        prompts.append(prompt)
        metas.append(meta)

    return prompts, metas


def scrape_blog_titles(url: str = CONFIG.blog_url, n: int = CONFIG.n_images) -> list[str] | None:
    if not HAS_SCRAPING:
        return None

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; EndoHeaderGen/1.0)"},
        timeout=15,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    titles: list[str] = []
    seen: set[str] = set()

    for h3 in soup.find_all("h3"):
        link = h3.find("a")
        title = link.get_text(strip=True) if link else h3.get_text(strip=True)

        if title_is_valid(title, seen):
            seen.add(title)
            titles.append(title)

    if not titles:
        return None

    return random.sample(titles, min(n, len(titles)))


def generate_image_bytes(client: OpenAI, prompt: str) -> bytes:
    response = client.images.generate(
        model=CONFIG.image_model,
        prompt=prompt,
        size=CONFIG.image_size,
        quality=CONFIG.image_quality,
        n=1,
    )
    return base64.b64decode(response.data[0].b64_json)


def generate_images(
    titles: list[str],
    prompts: list[str],
    output_dir: Path,
    delay_seconds: float | None = None,
) -> list[Path | None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    output_dir.mkdir(parents=True, exist_ok=True)

    if delay_seconds is None:
        delay_seconds = CONFIG.request_delay_seconds

    results: list[Path | None] = []

    for idx, (title, prompt) in enumerate(zip(titles, prompts), start=1):
        filepath = output_dir / f"header_{idx:02d}.png"

        try:
            image_bytes = generate_image_bytes(client, prompt)
            filepath.write_bytes(image_bytes)
            results.append(filepath)
        except Exception:
            results.append(None)

        if idx < len(prompts):
            time.sleep(delay_seconds)

    return results


def generate_single_image(prompt: str, output_path: Path) -> Path:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image_bytes = generate_image_bytes(client, prompt)
    output_path.write_bytes(image_bytes)
    return output_path


def create_contact_sheet(images: list[Path | None], output_dir: Path) -> Path | None:
    if not HAS_PIL:
        return None

    valid_images = [path for path in images if path and path.exists()]
    if len(valid_images) < 2:
        return None

    max_items = min(len(valid_images), 10)
    cols = 2
    rows = (max_items + cols - 1) // cols
    thumb_w, thumb_h = 768, 512

    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (255, 251, 240))

    for idx, path in enumerate(valid_images[:max_items]):
        img = Image.open(path).resize((thumb_w, thumb_h), Image.LANCZOS)
        row, col = divmod(idx, cols)
        sheet.paste(img, (col * thumb_w, row * thumb_h))

    out = output_dir / "contact_sheet.png"
    sheet.save(out, quality=95)
    return out
