import streamlit as st

from lib.trino_client import fqtn, list_first_column, qident, query_df, read_columns
from lib.ui import apply_branding, page_header, render_sidebar, section_header, show_error


st.set_page_config(page_title="Explorateur de schemas", layout="wide")
apply_branding()
render_sidebar()

page_header(
    "Catalogue Trino",
    "Explorateur de sch\u00e9mas",
    "Navigation dans les sources, les sch\u00e9mas et les tables accessibles depuis la plateforme.",
)

try:
    catalogs = list_first_column("SHOW CATALOGS")

    section_header("S\u00e9lection de la source", "Choisis le catalogue, le sch\u00e9ma puis la table \u00e0 inspecter.")
    selector_cols = st.columns(3)
    with selector_cols[0]:
        catalog = st.selectbox("Source de donn\u00e9es", catalogs, index=catalogs.index("iceberg") if "iceberg" in catalogs else 0)

    schemas = list_first_column(f"SHOW SCHEMAS FROM {qident(catalog)}")
    with selector_cols[1]:
        schema = st.selectbox("Sch\u00e9ma", schemas, index=schemas.index("lakehouse") if "lakehouse" in schemas else 0)

    tables = list_first_column(f"SHOW TABLES FROM {qident(catalog)}.{qident(schema)}")
    with selector_cols[2]:
        table = st.selectbox("Table", tables)

    if table:
        section_header("Structure de la table", "Nom des colonnes, types de donn\u00e9es et ordre technique.")
        columns = read_columns(catalog, schema, table)
        st.dataframe(columns, use_container_width=True, hide_index=True)

        section_header("Aper\u00e7u des donn\u00e9es", "Extrait de donn\u00e9es pour valider rapidement le contenu.")
        preview = query_df(f"SELECT * FROM {fqtn(catalog, schema, table)} LIMIT 100")
        st.dataframe(preview, use_container_width=True, hide_index=True)
except Exception as exc:
    show_error("Impossible de charger le sch\u00e9ma s\u00e9lectionn\u00e9.", exc)
