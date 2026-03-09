from __future__ import annotations

import hashlib
from pathlib import Path

import streamlit as st

from config import CONFIG, FALLBACK_TITLES
from utils import build_all_prompts, scrape_blog_titles, generate_single_image

st.set_page_config(page_title="Endo Health Header Demo", layout="wide")

CACHE_DIR = Path("cache/generated_images")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MAX_TITLES_PER_RUN = 3
MAX_LIVE_GENERATIONS_PER_SESSION = 3


def safe_filename(title: str) -> str:
    digest = hashlib.md5(title.encode("utf-8")).hexdigest()[:12]
    return f"{digest}.png"


@st.cache_data(show_spinner=False)
def load_sample_titles() -> list[str]:
    try:
        titles = scrape_blog_titles(n=20)
        if titles:
            return titles
    except Exception:
        pass
    return FALLBACK_TITLES


def get_cached_image_path(title: str) -> Path:
    return CACHE_DIR / safe_filename(title)


def get_prompt_and_meta(title: str):
    prompts, metas = build_all_prompts([title])
    return prompts[0], metas[0]


def ensure_image_for_title(title: str, cached_only: bool) -> tuple[Path | None, str, str, bool]:
    prompt, meta = get_prompt_and_meta(title)
    output_path = get_cached_image_path(title)

    if output_path.exists():
        return output_path, prompt, meta.category, True

    if cached_only:
        return None, prompt, meta.category, False

    current_live_generations = st.session_state.get("live_generations", 0)
    if current_live_generations >= MAX_LIVE_GENERATIONS_PER_SESSION:
        raise RuntimeError(
            f"Session limit reached: {MAX_LIVE_GENERATIONS_PER_SESSION} live generations."
        )

    generate_single_image(prompt, output_path)
    st.session_state["live_generations"] = current_live_generations + 1
    return output_path, prompt, meta.category, False


def init_session_state() -> None:
    if "live_generations" not in st.session_state:
        st.session_state["live_generations"] = 0


init_session_state()

st.title("Endo Health Blog Header Demo")
st.caption("A prototype for brand-aligned editorial header generation.")

with st.sidebar:
    st.subheader("Usage controls")
    cached_only = st.toggle("Cached results only", value=False)
    st.write(
        f"Live generations used this session: "
        f"{st.session_state['live_generations']} / {MAX_LIVE_GENERATIONS_PER_SESSION}"
    )
    st.write(f"Max titles per run: {MAX_TITLES_PER_RUN}")

tab_generate, tab_prompt = st.tabs(["Generate", "Prompt preview"])

with tab_generate:
    st.subheader("Generate headers")
    sample_titles = load_sample_titles()

    selected_titles = st.multiselect(
        "Choose up to 3 titles",
        options=sample_titles,
        default=sample_titles[:2],
        max_selections=MAX_TITLES_PER_RUN,
    )

    generate_clicked = st.button("Generate selected headers", type="primary")

    if generate_clicked:
        if not selected_titles:
            st.warning("Please select at least one title.")
        else:
            cols = st.columns(len(selected_titles))
            for col, title in zip(cols, selected_titles):
                with col:
                    st.markdown(f"**Title:** {title}")
                    try:
                        with st.spinner("Preparing image..."):
                            image_path, prompt, category, from_cache = ensure_image_for_title(
                                title,
                                cached_only=cached_only,
                            )

                        st.markdown(f"**Category:** {category}")

                        if image_path and image_path.exists():
                            st.image(str(image_path), use_container_width=True)
                            st.caption("Loaded from cache." if from_cache else "Generated live.")
                        else:
                            st.info("No cached image available for this title in cached-only mode.")

                    except Exception as exc:
                        st.error(str(exc))

with tab_prompt:
    st.subheader("Inspect prompt logic")
    preview_title = st.selectbox("Pick a title", options=load_sample_titles())

    if preview_title:
        prompt, meta = get_prompt_and_meta(preview_title)

        st.markdown(f"**Detected category:** {meta.category}")
        st.markdown(f"**Metaphor pool:** {meta.metaphor_pool}")
        st.markdown(f"**Composition:** {meta.composition}")
        st.markdown(f"**Color balance:** {meta.color_balance}")
        st.markdown(f"**Objects:** {', '.join(meta.objects)}")

        with st.expander("Show final prompt"):
            st.code(prompt, language="text")