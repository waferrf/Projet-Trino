import streamlit as st

from lib.trino_client import fqtn, list_first_column, qident, query_df, read_columns
from lib.ui import apply_branding, page_header, render_sidebar, section_header, show_error


st.set_page_config(page_title="Produits de donnees", layout="wide")
apply_branding()
render_sidebar()

page_header(
    "Lakehouse Iceberg",
    "Produits de donn\u00e9es",
    "Suivi des tables analytiques, de leur volume et de leurs m\u00e9tadonn\u00e9es de stockage.",
)

try:
    schemas = list_first_column("SHOW SCHEMAS FROM iceberg")
    default_schema = schemas.index("lakehouse") if "lakehouse" in schemas else 0

    section_header("S\u00e9lection du produit", "Inspection d'une table Iceberg et de ses informations techniques.")
    selector_cols = st.columns(2)
    with selector_cols[0]:
        schema = st.selectbox("Sch\u00e9ma analytique", schemas, index=default_schema)

    tables = list_first_column(f"SHOW TABLES FROM {qident('iceberg')}.{qident(schema)}")
    with selector_cols[1]:
        table = st.selectbox("Table Iceberg", tables)

    if table:
        cols = st.columns(2)
        with cols[0]:
            section_header("Structure de la table", "Colonnes et types d\u00e9clar\u00e9s dans le catalogue.")
            st.dataframe(read_columns("iceberg", schema, table), use_container_width=True, hide_index=True)

        with cols[1]:
            section_header("Volume de donn\u00e9es", "Nombre total de lignes dans la table s\u00e9lectionn\u00e9e.")
            count_df = query_df(f"SELECT count(*) AS lignes FROM {fqtn('iceberg', schema, table)}")
            st.dataframe(count_df, use_container_width=True, hide_index=True)

        tab_data, tab_partitions, tab_snapshots = st.tabs(["Aper\u00e7u", "Partitions", "Snapshots"])

        with tab_data:
            section_header("Aper\u00e7u du produit", "Extrait des 100 premi\u00e8res lignes.")
            data = query_df(f"SELECT * FROM {fqtn('iceberg', schema, table)} LIMIT 100")
            st.dataframe(data, use_container_width=True, hide_index=True)

        with tab_partitions:
            section_header("Partitions Iceberg", "Distribution physique utilis\u00e9e pour optimiser les requ\u00eates.")
            try:
                partitions = query_df(f"SELECT * FROM {fqtn('iceberg', schema, table + '$partitions')}")
                st.dataframe(partitions, use_container_width=True, hide_index=True)
            except Exception as exc:
                show_error("Aucune partition lisible pour cette table.", exc)

        with tab_snapshots:
            section_header("Snapshots Iceberg", "Historique des versions de la table.")
            try:
                snapshots = query_df(f"SELECT * FROM {fqtn('iceberg', schema, table + '$snapshots')}")
                st.dataframe(snapshots, use_container_width=True, hide_index=True)
            except Exception as exc:
                show_error("Aucun snapshot lisible pour cette table.", exc)
except Exception as exc:
    show_error("Impossible de charger les produits de donn\u00e9es.", exc)
