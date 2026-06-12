import re

import requests


FORBIDDEN_SQL = {
    "alter",
    "call",
    "create",
    "delete",
    "drop",
    "insert",
    "merge",
    "truncate",
    "update",
}

READ_ONLY_STARTS = ("select", "with", "show", "describe", "explain")


def generate_sql(
    prompt: str,
    model: str = "qwen2.5-coder:1.5b",
    base_url: str = "http://localhost:11434",
) -> str:
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
            },
        },
        timeout=120,
    )
    response.raise_for_status()
    return clean_sql(response.json().get("response", ""))


def clean_sql(text: str) -> str:
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        text = fenced.group(1)

    text = text.strip()
    text = re.sub(r"^sql\s*:\s*", "", text, flags=re.IGNORECASE)
    text = text.strip().rstrip(";").strip()
    return text


def is_read_only_sql(sql: str) -> bool:
    normalized = re.sub(r"\s+", " ", sql.strip().lower())
    if not normalized.startswith(READ_ONLY_STARTS):
        return False

    tokens = set(re.findall(r"[a-z_]+", normalized))
    return not bool(tokens.intersection(FORBIDDEN_SQL))
