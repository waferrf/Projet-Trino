import os
from html import escape

import requests
import streamlit as st


def apply_branding() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-main: #0f1117;
            --bg-panel: #171a22;
            --bg-panel-soft: #1c202b;
            --border-soft: rgba(255, 255, 255, 0.10);
            --text-muted: #aeb6c8;
            --text-soft: #d9deeb;
            --accent-teal: #2dd4bf;
            --accent-blue: #60a5fa;
            --accent-amber: #f59e0b;
            --accent-coral: #fb7185;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--bg-main);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, p, span, label {
            letter-spacing: 0;
        }

        .app-header {
            border: 1px solid var(--border-soft);
            border-left: 5px solid var(--accent-teal);
            border-radius: 8px;
            background: var(--bg-panel);
            padding: 1.45rem 1.6rem;
            margin-bottom: 1.5rem;
        }

        .app-kicker {
            color: var(--accent-teal);
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .app-title {
            color: #ffffff;
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0;
        }

        .app-subtitle {
            color: var(--text-muted);
            font-size: 1rem;
            line-height: 1.55;
            margin: 0.65rem 0 0;
            max-width: 980px;
        }

        .section-heading {
            border-bottom: 1px solid var(--border-soft);
            margin: 1.7rem 0 0.8rem;
            padding-bottom: 0.7rem;
        }

        .section-heading h2 {
            color: #ffffff;
            font-size: 1.25rem;
            font-weight: 750;
            margin: 0;
        }

        .section-heading p {
            color: var(--text-muted);
            font-size: 0.92rem;
            margin: 0.25rem 0 0;
        }

        .status-card,
        .metric-card {
            min-height: 118px;
            border: 1px solid var(--border-soft);
            border-radius: 8px;
            background: var(--bg-panel);
            padding: 1rem 1.1rem;
        }

        .status-card {
            border-left: 5px solid var(--accent-red);
        }

        .status-card.ok {
            border-left-color: var(--accent-green);
        }

        .card-label {
            color: var(--text-muted);
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        .card-value {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.45rem;
        }

        .card-detail {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            border-radius: 999px;
            color: #ffffff;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 0.2rem 0.55rem;
            background: rgba(239, 68, 68, 0.24);
        }

        .status-card.ok .status-pill {
            background: rgba(34, 197, 94, 0.22);
        }

        .metric-card.teal {
            border-top: 4px solid var(--accent-teal);
        }

        .metric-card.blue {
            border-top: 4px solid var(--accent-blue);
        }

        .metric-card.amber {
            border-top: 4px solid var(--accent-amber);
        }

        .metric-card.coral {
            border-top: 4px solid var(--accent-coral);
        }

        .selection-label {
            color: var(--text-muted);
            font-size: 0.82rem;
            font-weight: 700;
            margin: 0 0 0.25rem;
            text-transform: uppercase;
        }

        [data-testid="stSidebar"] {
            background: #252833;
            border-right: 1px solid var(--border-soft);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #ffffff;
        }

        [data-testid="stSidebar"] label {
            color: var(--text-soft);
            font-weight: 650;
        }

        [data-testid="stSidebar"] [data-testid="stTextInput"] input {
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: #10131b;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-soft);
            border-radius: 8px;
            overflow: hidden;
        }

        [data-testid="stSelectbox"] > div {
            border-radius: 8px;
        }

        [data-testid="stTabs"] button {
            font-weight: 650;
        }

        [data-testid="stChatInput"] {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <section class="app-header">
            <div class="app-kicker">{escape(kicker)}</div>
            <h1 class="app-title">{escape(title)}</h1>
            <p class="app-subtitle">{escape(subtitle)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="section-heading">
            <h2>{escape(title)}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str | int, detail: str, tone: str = "teal") -> None:
    st.markdown(
        f"""
        <div class="metric-card {escape(tone)}">
            <div class="card-label">{escape(label)}</div>
            <div class="card-value">{escape(str(value))}</div>
            <div class="card-detail">{escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_card(label: str, ok: bool, detail: str) -> None:
    status = "Op\u00e9rationnel" if ok else "Indisponible"
    status_class = "ok" if ok else ""
    st.markdown(
        f"""
        <div class="status-card {status_class}">
            <div class="card-label">{escape(label)}</div>
            <div class="card-value">{escape(status)}</div>
            <div class="card-detail">{escape(detail)}</div>
            <div style="height: .65rem;"></div>
            <span class="status-pill">{escape(status)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> dict[str, str]:
    with st.sidebar:
        st.header("Param\u00e8tres de connexion")
        st.caption("Configuration locale utilis\u00e9e par le tableau de bord.")

        trino_host = st.text_input("H\u00f4te Trino", os.getenv("TRINO_HOST", "localhost"))
        trino_port = st.text_input("Port Trino", os.getenv("TRINO_PORT", "8080"))
        trino_user = st.text_input("Utilisateur Trino", os.getenv("TRINO_USER", "analyst"))
        ollama_url = st.text_input("URL Ollama", os.getenv("OLLAMA_URL", "http://localhost:11434"))
        model = st.text_input("Mod\u00e8le IA local", os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b"))

    os.environ["TRINO_HOST"] = trino_host
    os.environ["TRINO_PORT"] = trino_port
    os.environ["TRINO_USER"] = trino_user
    os.environ["OLLAMA_URL"] = ollama_url
    os.environ["OLLAMA_MODEL"] = model

    return {
        "trino_host": trino_host,
        "trino_port": trino_port,
        "trino_user": trino_user,
        "ollama_url": ollama_url,
        "model": model,
    }


def service_status() -> tuple[bool, bool]:
    trino_ok = False
    ollama_ok = False

    try:
        import lib.trino_client as trino_client

        trino_client.query_df("SELECT 1")
        trino_ok = True
    except Exception:
        trino_ok = False

    try:
        response = requests.get(f"{os.getenv('OLLAMA_URL', 'http://localhost:11434').rstrip('/')}/api/tags", timeout=5)
        ollama_ok = response.ok
    except Exception:
        ollama_ok = False

    return trino_ok, ollama_ok


def show_error(message: str, error: Exception) -> None:
    st.error(message)
    with st.expander("D\u00e9tails techniques"):
        st.code(str(error))
