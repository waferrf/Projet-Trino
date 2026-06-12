import os

import streamlit as st

from lib.ollama_client import generate_sql, is_read_only_sql
from lib.trino_client import column_context, fqtn, list_first_column, qident, query_df, read_columns
from lib.ui import apply_branding, page_header, render_sidebar, section_header, show_error


st.set_page_config(page_title="Assistant SQL", layout="wide")
apply_branding()
settings = render_sidebar()

page_header(
    "GenAI local",
    "Assistant SQL intelligent",
    "Transformation d'une question m\u00e9tier en requ\u00eate Trino ex\u00e9cutable sur le lakehouse.",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def build_prompt(question: str, catalog: str, schema: str, table: str) -> str:
    columns = read_columns(catalog, schema, table)
    return f"""
You are a Trino SQL generator.
Return only one SQL query. Do not return markdown. Do not explain.
The query must be read-only.
Use this fully qualified table name unless the user explicitly asks for metadata:
{fqtn(catalog, schema, table)}

Columns:
{column_context(columns)}

Rules:
- Use Trino SQL syntax.
- Quote identifiers with double quotes when needed.
- For row-level previews, include LIMIT 100.
- Prefer aggregations for KPI questions.

User question:
{question}
""".strip()


try:
    catalogs = list_first_column("SHOW CATALOGS")
    catalog_default = catalogs.index("iceberg") if "iceberg" in catalogs else 0
    catalog = st.sidebar.selectbox("Catalogue cible", catalogs, index=catalog_default)

    schemas = list_first_column(f"SHOW SCHEMAS FROM {qident(catalog)}")
    schema_default = schemas.index("lakehouse") if "lakehouse" in schemas else 0
    schema = st.sidebar.selectbox("Sch\u00e9ma cible", schemas, index=schema_default)

    tables = list_first_column(f"SHOW TABLES FROM {qident(catalog)}.{qident(schema)}")
    table = st.sidebar.selectbox("Table cible", tables)

    section_header("Contexte de g\u00e9n\u00e9ration", "La requ\u00eate sera construite uniquement \u00e0 partir de cette table.")
    st.dataframe(read_columns(catalog, schema, table), use_container_width=True, hide_index=True)

    section_header("Conversation SQL", "Pose une question m\u00e9tier, l'assistant propose une requ\u00eate puis affiche le r\u00e9sultat.")
    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(item["question"])
        with st.chat_message("assistant"):
            st.code(item["sql"], language="sql")
            st.dataframe(item["result"], use_container_width=True, hide_index=True)

    question = st.chat_input("Pose une question m\u00e9tier sur la table s\u00e9lectionn\u00e9e")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            prompt = build_prompt(question, catalog, schema, table)
            sql = generate_sql(
                prompt=prompt,
                model=settings["model"],
                base_url=os.getenv("OLLAMA_URL", settings["ollama_url"]),
            )

            st.code(sql, language="sql")

            if not is_read_only_sql(sql):
                st.warning("La requ\u00eate g\u00e9n\u00e9r\u00e9e a \u00e9t\u00e9 refus\u00e9e car elle n'est pas en lecture seule.")
            else:
                result = query_df(sql)
                st.dataframe(result, use_container_width=True, hide_index=True)
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "sql": sql,
                        "result": result,
                    }
                )
except Exception as exc:
    show_error("Impossible d'utiliser l'assistant SQL.", exc)
