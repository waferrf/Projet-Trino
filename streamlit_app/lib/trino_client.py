import os
from typing import Iterable

import pandas as pd
import trino


def trino_settings() -> dict[str, str | int]:
    return {
        "host": os.getenv("TRINO_HOST", "localhost"),
        "port": int(os.getenv("TRINO_PORT", "8080")),
        "user": os.getenv("TRINO_USER", "analyst"),
        "http_scheme": os.getenv("TRINO_SCHEME", "http"),
    }


def get_connection(catalog: str | None = None, schema: str | None = None):
    settings = trino_settings()
    return trino.dbapi.connect(
        host=settings["host"],
        port=settings["port"],
        user=settings["user"],
        http_scheme=settings["http_scheme"],
        catalog=catalog,
        schema=schema,
    )


def query_df(sql: str, catalog: str | None = None, schema: str | None = None) -> pd.DataFrame:
    connection = get_connection(catalog=catalog, schema=schema)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description or []]
    return pd.DataFrame(rows, columns=columns)


def list_first_column(sql: str) -> list[str]:
    df = query_df(sql)
    if df.empty:
        return []
    return [str(value) for value in df.iloc[:, 0].dropna().tolist()]


def qident(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def qliteral(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def fqtn(catalog: str, schema: str, table: str) -> str:
    return ".".join(qident(part) for part in (catalog, schema, table))


def read_columns(catalog: str, schema: str, table: str) -> pd.DataFrame:
    return query_df(
        f"""
        SELECT
            column_name,
            data_type,
            ordinal_position
        FROM {qident(catalog)}.information_schema.columns
        WHERE table_schema = {qliteral(schema)}
          AND table_name = {qliteral(table)}
        ORDER BY ordinal_position
        """
    )


def column_context(columns: pd.DataFrame) -> str:
    if columns.empty:
        return "No columns were found."

    parts: Iterable[str] = (
        f"- {row.column_name}: {row.data_type}"
        for row in columns.itertuples(index=False)
    )
    return "\n".join(parts)
