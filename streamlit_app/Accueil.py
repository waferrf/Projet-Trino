import streamlit as st

from lib.trino_client import query_df
from lib.ui import (
    apply_branding,
    metric_card,
    page_header,
    render_sidebar,
    section_header,
    service_status,
    show_error,
    status_card,
)


st.set_page_config(
    page_title="Plateforme Lakehouse & GenAI",
    page_icon=None,
    layout="wide",
)

apply_branding()
render_sidebar()

page_header(
    "Modern Data Stack",
    "Plateforme Data Lakehouse & GenAI",
    "Pilotage local de Trino, Apache Iceberg, ClickHouse, MinIO, Hive Metastore et de l'assistant Text-to-SQL.",
)

trino_ok, ollama_ok = service_status()

section_header("Etat des services", "Disponibilit\u00e9 des composants principaux de la plateforme.")
status_cols = st.columns(2)
with status_cols[0]:
    status_card("Moteur SQL f\u00e9d\u00e9r\u00e9 - Trino", trino_ok, "Point d'entr\u00e9e unique pour interroger Iceberg et ClickHouse.")
with status_cols[1]:
    status_card("Assistant SQL local - Ollama", ollama_ok, "G\u00e9n\u00e8re des requ\u00eates SQL \u00e0 partir de questions m\u00e9tier.")

if trino_ok:
    try:
        catalogs = query_df("SHOW CATALOGS")
        schemas = query_df("SHOW SCHEMAS FROM iceberg")
        tables = query_df("SHOW TABLES FROM iceberg.lakehouse")

        section_header("Vue d'ensemble", "Indicateurs rapides sur les sources disponibles dans Trino.")
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Sources f\u00e9d\u00e9r\u00e9es", len(catalogs), "Catalogues expos\u00e9s par le moteur Trino.", "teal")
        with col2:
            metric_card("Sch\u00e9mas Iceberg", len(schemas), "Espaces logiques disponibles dans le lakehouse.", "blue")
        with col3:
            metric_card("Tables Lakehouse", len(tables), "Tables analytiques pr\u00eates \u00e0 \u00eatre interrog\u00e9es.", "amber")

        section_header("Catalogue des sources de donn\u00e9es", "Inventaire des connecteurs disponibles.")
        st.dataframe(catalogs, use_container_width=True, hide_index=True)

        section_header("Tables analytiques Iceberg", "Tables stock\u00e9es dans le lakehouse et consultables depuis Trino.")
        st.dataframe(tables, use_container_width=True, hide_index=True)
    except Exception as exc:
        show_error("Impossible de lire les m\u00e9tadonn\u00e9es Trino.", exc)
else:
    st.info("D\u00e9marre la stack Docker avant d'utiliser la plateforme.")
