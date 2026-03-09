from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeConfig:
    blog_url: str = "https://endometriose.app/aktuelles-2/"
    output_dir: Path = Path("./output")
    image_model: str = "gpt-image-1"
    image_size: str = "1536x1024"
    image_quality: str = "low"
    n_images: int = 10
    request_delay_seconds: float = 2.0


@dataclass(frozen=True)
class CategoryConfig:
    keywords: list[str]
    metaphor_pool: str
    object_pools: list[str]
    extra_rule: str


CONFIG = RuntimeConfig()

SKIP_PATTERNS = [
    "newsletter",
    "abmeldung",
    "lade die",
    "infos zur endo-app",
    "danke für",
    "coping-typ",
    "herzlich willkommen",
    "freischaltcode",
    "versorgungsumfrage",
]

FALLBACK_TITLES = [
    "Künstliche Wechseljahre – was steckt dahinter und was kannst du tun?",
    "Endometriose kennt kein Alter",
    "Früherkennung bei Endometriose",
    "Autoimmunerkrankungen und Endometriose",
    "Endometriose mit künstlicher Intelligenz früher erkennen",
    "Schmerztherapie bei Endometriose",
    "Sport bei Endometriose: 5 Vorteile",
    "Osteopathie bei Endometriose",
    "Achtsamkeit bei Endometriose",
    "Endometriose: Wie erkläre ich mich meiner Familie?",
]

BASE_STYLE = """\
Create a wide editorial header illustration for a health blog about
endometriosis. The blog is inclusive and addresses all people affected by
endometriosis, not only women.

Visual style:
Modern flat editorial illustration with subtle paper-like grain texture,
soft gradients, rounded organic shapes, minimal but warm, calm and airy.
Not photorealistic, not 3D, not glossy.

Brand palette:
Cream white, dusty rose / blush pink (#E8A0BF), sage green (#9CAF88),
and warm golden yellow (#F5C518) only as a restrained accent.
Yellow must not dominate. No cold blues, no harsh reds, no dark tones.

Composition:
Landscape format. Generous whitespace. One clear focal idea, not crowded."""

STYLE_CONSTRAINTS = """\
Style constraints:
Flat 2D editorial illustration only.
No 3D rendering, no pseudo-3D product mockup look, no clay style, no realistic shading.
Soft flat color fields with minimal tonal variation.
Poster-like or paper-cut layering is acceptable."""

TEXT_CONSTRAINTS = """\
Do not include any readable text, letters, numbers, labels, handwriting,
month names, calendar text, document text, or typographic marks anywhere.
All documents, calendars, score sheets, labels, and cards must be completely
blank — no grid lines, no cell borders, no symbols. Show them as simple
flat colored rectangles only."""

LAYOUT_RULE = """\
Reserve the left third as quiet negative space for headline text overlay.
The main focal element must sit in the center or right portion.
Do not place dense detail, faces, or key objects in the left third."""

COMPOSITION_DISCIPLINE = """\
Use one clear focal element and at most two or three supporting elements.
Avoid catalog-like object arrangements.
Avoid evenly spacing many objects across the frame."""

HUMAN_FIGURE_RULE = """\
Human figure rule:
If a human figure appears, it must be simplified, abstract, and faceless
(no eyes, nose, or mouth). Use gender-neutral body shapes — avoid
emphasizing breasts, narrow waists, or other gendered features.
Figures should feel universal: they could be anyone affected by endometriosis.

Do NOT show a person clutching or holding their stomach or abdomen.
Vary poses: sitting, reading, walking, stretching, resting, conversing.
Many images should have no human figure at all — prefer object-based or
abstract compositions when possible."""

NEGATIVE_STYLE = """\
Avoid all of the following:
- Uterus or reproductive organ icon (use abstract metaphors instead)
- Centered female profile with halo or sun behind head
- Explicitly gendered body shapes (breasts, narrow waist, curvy hips)
- Person clutching their stomach (overused and triggering)
- Thick ribbon crossing the whole image
- Mirrored leaf clusters on both sides
- Monochrome yellow wash
- Any readable text, month names, grid lines on calendars
- 3D render, clay illustration, or product mockup look
- Symmetrical poster composition
- Too many props or cluttered scene
- Generic stock wellness aesthetic
- Pink-equals-female color coding"""

PROMPT_BLOCKS = [
    BASE_STYLE,
    STYLE_CONSTRAINTS,
    TEXT_CONSTRAINTS,
    LAYOUT_RULE,
    COMPOSITION_DISCIPLINE,
    HUMAN_FIGURE_RULE,
]

CATEGORY_CONFIG: dict[str, CategoryConfig] = {
    "treatment": CategoryConfig(
        keywords=[
            "wechseljahre",
            "hormon",
            "pille",
            "therapie",
            "behandlung",
            "medik",
            "wirkstoff",
            "yselty",
            "relugolix",
        ],
        metaphor_pool="regulation",
        object_pools=["care", "body_abstract", "light"],
        extra_rule=(
            "Treatment cues are allowed but keep them symbolic, not literal packaging. "
            "No reproductive organ imagery. Show care pathways, balance, and support."
        ),
    ),
    "pain": CategoryConfig(
        keywords=[
            "schmerz",
            "krampf",
            "fatigue",
            "erschöpf",
            "symptom",
            "narben",
            "verdacht",
            "sex",
        ],
        metaphor_pool="relief",
        object_pools=["comfort", "light", "body_abstract"],
        extra_rule=(
            "Focus on relief, protection, warmth, softening tension. "
            "Do not show a person clutching their stomach. Use objects or abstract metaphors instead."
        ),
    ),
    "research": CategoryConfig(
        keywords=[
            "forschung",
            "grundlagen",
            "ki ",
            "studie",
            "genetik",
            "biomarker",
            "fusobakter",
            "erkennen",
            "zellstud",
        ],
        metaphor_pool="discovery",
        object_pools=["science", "light"],
        extra_rule="Structured analytical composition. Abstract science shapes. No lifestyle props.",
    ),
    "movement": CategoryConfig(
        keywords=[
            "sport",
            "yoga",
            "qigong",
            "bewegung",
            "osteopathie",
            "muskelrelaxation",
            "pmr",
            "autogenes",
            "sitzen",
        ],
        metaphor_pool="mobility",
        object_pools=["movement", "nature"],
        extra_rule="Show calm posture, open space, floor-level composition, breath cues. No anatomy.",
    ),
    "mental_wellbeing": CategoryConfig(
        keywords=[
            "achtsamkeit",
            "selbstliebe",
            "stress",
            "mental",
            "emotion",
            "selbstbewusst",
            "pmds",
            "dysphor",
        ],
        metaphor_pool="calm",
        object_pools=["home", "comfort", "light"],
        extra_rule="Restful space, breath, light, calm interior. No medical anatomy.",
    ),
    "community": CategoryConfig(
        keywords=[
            "interview",
            "experten",
            "gespräch",
            "hilfe",
            "erkläre ich mich",
            "social",
            "who is who",
            "community",
            "selbsthilfe",
        ],
        metaphor_pool="connection",
        object_pools=["shared_space", "care"],
        extra_rule=(
            "Shared space: paired objects, chairs, notebooks, warm meeting atmosphere. "
            "No anatomy."
        ),
    ),
    "fertility": CategoryConfig(
        keywords=[
            "schwanger",
            "kinderwunsch",
            "fruchtbarkeit",
            "egg freezing",
            "eizellenqualität",
            "ovarielle",
        ],
        metaphor_pool="growth",
        object_pools=["growth", "light"],
        extra_rule=(
            "Growth, care, possibility, nurturing symbolism. Hopeful and restrained. "
            "No reproductive organ imagery — use botanical growth metaphors instead."
        ),
    ),
    "diagnosis": CategoryConfig(
        keywords=[
            "früherkennung",
            "diagnose",
            "kennt kein alter",
            "score",
            "enzian",
            "rasrm",
            "tief infiltrier",
            "lymphknoten",
            "blase",
            "darm",
        ],
        metaphor_pool="clarity",
        object_pools=["science", "care"],
        extra_rule=(
            "Diagnostic framing: focus shapes, magnifying glass, spotlight, layered "
            "windows. Prefer abstract body outlines over literal organ diagrams."
        ),
    ),
    "advocacy": CategoryConfig(
        keywords=[
            "politik",
            "wahl",
            "bundestagswahl",
            "forderung",
            "awareness",
            "march",
            "aktiv werden",
            "krankenkasse",
            "kündigung",
            "arbeitgeb",
            "telemedizin",
            "digig",
        ],
        metaphor_pool="voice",
        object_pools=["civic", "shared_space"],
        extra_rule=(
            "Show civic engagement: megaphone shapes, raised hands, checkmarks, ballot cues, "
            "community gathering. No anatomy, no wellness objects."
        ),
    ),
    "nutrition": CategoryConfig(
        keywords=[
            "ernährung",
            "omega",
            "histamin",
            "nahrungsergänzung",
            "reizdarm",
            "verdauung",
            "rezept",
            "gewichtszunahme",
            "gluten",
            "fleisch",
            "grüntee",
            "extrakt",
        ],
        metaphor_pool="nourishment",
        object_pools=["food", "nature"],
        extra_rule="Show wholesome food, bowls, herbs, natural ingredients. Editorial food still-life style. No anatomy.",
    ),
    "reha": CategoryConfig(
        keywords=["reha", "anschluss", "ahb"],
        metaphor_pool="recovery",
        object_pools=["movement", "care", "nature"],
        extra_rule="Rehabilitation pathway: stepping stones, open path, gentle upward motion, care objects. No anatomy.",
    ),
    "daily_life": CategoryConfig(
        keywords=[],
        metaphor_pool="routine",
        object_pools=["care", "home", "comfort"],
        extra_rule="Practical self-care or home routine metaphors. Minimal and editorial.",
    ),
}

METAPHOR_POOLS: dict[str, list[str]] = {
    "regulation": [
        "balancing shapes suggesting regulation and adaptation",
        "layered circles and calm rhythm patterns",
        "a treatment pathway leading toward relief",
        "organized care elements with soft supportive light",
    ],
    "relief": [
        "protective shapes surrounding soft wave-like forms",
        "warmth and release shown through layered flowing forms",
        "a warm compress or comfort object as the calm focal point",
        "tension dissolving into softer rounded shapes",
    ],
    "discovery": [
        "connected dots and soft scientific structures suggesting discovery",
        "microscope-inspired abstract forms with floating organic elements",
        "layered translucent shapes suggesting insight and analysis",
        "data-like constellations transforming into organic patterns",
    ],
    "mobility": [
        "a gentle path or stepping stones showing progress",
        "flowing movement lines in open airy space",
        "strength and mobility shown through uplifted organic curves",
        "a calm mat or floor-level scene with restrained movement cues",
    ],
    "calm": [
        "quiet balance through layered circles and breathing space",
        "a restful interior with sunlight and soft organic forms",
        "self-support shown through protective rounded shapes",
        "calm focus expressed through gentle repetition and open space",
    ],
    "connection": [
        "two chairs and a shared table suggesting dialogue",
        "overlapping abstract shapes showing connection and exchange",
        "care and understanding represented by warm proximity of objects",
        "a shared notebook and paired tea cups in editorial style",
    ],
    "growth": [
        "hope shown through growth, path, and gentle light",
        "nurturing organic shapes with blooming progression",
        "a symbolic journey toward possibility and care",
        "layered seed-like and floral forms in calm composition",
    ],
    "clarity": [
        "recognition through layered windows and focus shapes",
        "insight represented by spotlight-like soft light and pathways",
        "different life stages shown through varied harmonious forms",
        "clarity through ordered, revealing composition",
    ],
    "voice": [
        "megaphone-like shapes radiating gentle waves of change",
        "raised abstract hands and checkmark shapes in civic scene",
        "a podium or ballot-like form with community silhouettes",
        "overlapping speech-like shapes forming collective expression",
    ],
    "nourishment": [
        "a calm editorial food still life with wholesome ingredients",
        "bowls and natural foods arranged in minimal composition",
        "herbs and botanical ingredients on a warm-toned surface",
        "layered organic food shapes suggesting nourishment and care",
    ],
    "recovery": [
        "an upward-winding path through a gentle garden",
        "stepping stones leading from rest toward gentle activity",
        "a suitcase or care bag beside a welcoming open door",
        "strength returning shown through unfurling fern-like forms",
    ],
    "routine": [
        "practical self-care shown through an organized still life",
        "supportive routine expressed with home and wellness objects",
        "everyday management through calm order and soft structure",
        "a lifestyle-editorial scene with care tools and warm light",
    ],
}

OBJECT_POOLS: dict[str, list[str]] = {
    "body_abstract": [
        "gender-neutral abstract torso silhouette (no gendered features, no face)",
        "simplified hand shapes",
        "abstract body outline (could be any person)",
    ],
    "care": [
        "notebook",
        "water bottle",
        "small medicine pouch",
    ],
    "science": [
        "connected nodes",
        "microscope-inspired shape",
        "abstract cells",
        "magnifying glass",
    ],
    "movement": [
        "yoga mat",
        "soft motion arcs",
        "stepping-stone shapes",
    ],
    "comfort": [
        "blanket-like shapes",
        "heating-pad form",
        "tea cup",
        "soft cushion",
    ],
    "home": [
        "window with light",
        "potted plant",
        "folded fabric",
    ],
    "shared_space": [
        "two chairs",
        "small table",
        "paired cups",
        "shared notebook",
    ],
    "growth": [
        "sprouting leaves",
        "blooming shapes",
        "soft orb",
    ],
    "nature": [
        "single botanical element",
        "leaf form",
        "gentle stem",
    ],
    "light": [
        "light beam",
        "soft glow",
        "warm halo-like accent",
    ],
    "civic": [
        "megaphone shape",
        "raised hand silhouette",
        "ballot-like rectangle",
        "checkmark shape",
    ],
    "food": [
        "bowl of ingredients",
        "herbs and leaves",
        "citrus or fruit shapes",
        "small spice jars",
    ],
}

COMPOSITIONS = [
    "object-centered still life",
    "abstract symbolic editorial scene",
    "hands-based composition (simplified, faceless hands only)",
    "interior wellness scene",
    "pathway or journey metaphor",
    "layered collage-like editorial layout",
    "wide landscape scene with small focal element",
]

COLOR_BALANCES = [
    "cream and blush dominant, yellow accent only",
    "cream and sage dominant, blush secondary, yellow minimal",
    "blush and cream dominant with small golden highlights",
    "sage and cream dominant with soft dusty rose accents",
]

OPTIONAL_MOTIFS = [
    "use botanical elements very sparingly (one small leaf or stem)",
    "use gentle curved forms in the background",
    "use soft layered paper-cut shapes",
    "use a subtle window-light effect",
    "use small rounded symbolic accents",
    "use negative space as the dominant design element",
]

GALLERY_STYLE = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'DM Sans', sans-serif;
    background: #FFFBF0;
    color: #3A3028;
    padding: 40px 20px;
  }
  .wrap { max-width: 1000px; margin: 0 auto; }
  h1 {
    font-family: 'Fraunces', serif;
    font-size: 36px;
    text-align: center;
    margin-bottom: 8px;
  }
  .sub {
    text-align: center;
    color: #7A6E5E;
    margin-bottom: 40px;
    font-size: 15px;
  }
  .card {
    background: #fff;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(180,160,120,.10);
    border: 1px solid rgba(232,220,200,.50);
  }
  .card img { width: 100%; height: auto; display: block; }
  .card-title { padding: 16px 20px; font-size: 15px; font-weight: 600; }
  .num {
    display: inline-block;
    background: rgba(245,197,24,.15);
    color: #B8860B;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 10px;
  }
""".strip()