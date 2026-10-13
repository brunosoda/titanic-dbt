
import getpass

import duckdb
import psycopg2
from psycopg2 import sql


PG_PASSWORD = getpass.getpass("PostgreSQL password: ")

pg_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="titanic_database",
    user="titanic_user",
    password=PG_PASSWORD,
)

duck_conn = duckdb.connect("data/titanic.duckdb")

tables = [
    "titanic_boats",
    "titanic_crew",
    "titanic_passengers",
]


def duckdb_type(column):
    data_type = column["data_type"]
    udt_name = column["udt_name"]

    if data_type == "ARRAY":
        raise ValueError("Array columns need an explicit type mapping.")

    if data_type == "USER-DEFINED":
        return "VARCHAR"

    if data_type == "character varying" or data_type == "text":
        return "VARCHAR"

    if data_type == "character":
        return "VARCHAR"

    if data_type == "smallint":
        return "SMALLINT"

    if data_type == "integer":
        return "INTEGER"

    if data_type == "bigint":
        return "BIGINT"

    if data_type == "boolean":
        return "BOOLEAN"

    if data_type == "real":
        return "FLOAT"

    if data_type == "double precision":
        return "DOUBLE"

    if data_type == "numeric":
        precision = column["numeric_precision"]
        scale = column["numeric_scale"]

        if precision and scale is not None and precision <= 38:
            return f"DECIMAL({precision}, {scale})"

        return "DOUBLE"

    if data_type == "date":
        return "DATE"

    if data_type == "timestamp without time zone":
        return "TIMESTAMP"

    if data_type == "timestamp with time zone":
        return "TIMESTAMPTZ"

    if data_type == "time without time zone":
        return "TIME"

    if data_type == "time with time zone":
        return "TIMETZ"

    if udt_name == "uuid":
        return "UUID"

    if data_type == "json" or data_type == "jsonb":
        return "JSON"

    if data_type == "bytea":
        return "BLOB"

    raise ValueError(
        f"Unsupported PostgreSQL type: {data_type} ({udt_name})"
    )


try:
    pg_cursor = pg_conn.cursor()

    duck_conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    duck_conn.execute("BEGIN TRANSACTION")

    for table in tables:
        # Read column definitions from PostgreSQL
        pg_cursor.execute(
            """
            SELECT column_name, data_type, udt_name,
                   numeric_precision, numeric_scale, ordinal_position
            FROM information_schema.columns
            WHERE table_schema = 'raw'
              AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table,),
        )

        metadata = pg_cursor.fetchall()

        if not metadata:
            raise ValueError(f"Table raw.{table} was not found.")

        columns = [
            {
                "column_name": row[0],
                "data_type": row[1],
                "udt_name": row[2],
                "numeric_precision": row[3],
                "numeric_scale": row[4],
            }
            for row in metadata
        ]

        # Read source data
        pg_cursor.execute(
            sql.SQL("SELECT * FROM {}.{}").format(
                sql.Identifier("raw"),
                sql.Identifier(table),
            )
        )
        rows = pg_cursor.fetchall()
        column_names = [column["column_name"] for column in columns]

        definitions = ", ".join(
            f"{sql.Identifier(column['column_name']).as_string(pg_conn)} "
            f"{duckdb_type(column)}"
            for column in columns
        )

        target = f'raw."{table}"'

        duck_conn.execute(f"DROP TABLE IF EXISTS {target}")
        duck_conn.execute(
            f"CREATE TABLE {target} ({definitions})"
        )

        if rows:
            placeholders = ", ".join(["?"] * len(column_names))
            quoted_columns = ", ".join(
                f'"{name.replace(chr(34), chr(34) * 2)}"'
                for name in column_names
            )

            duck_conn.executemany(
                f"INSERT INTO {target} ({quoted_columns}) "
                f"VALUES ({placeholders})",
                rows,
            )

        copied = duck_conn.execute(
            f"SELECT COUNT(*) FROM {target}"
        ).fetchone()[0]

        if copied != len(rows):
            raise ValueError(
                f"Row count mismatch for {table}: "
                f"source={len(rows)}, target={copied}"
            )

        print(f"raw.{table}: {copied} rows copied")

    duck_conn.execute("COMMIT")
    print("Migration completed successfully.")

except Exception:
    duck_conn.execute("ROLLBACK")
    raise

finally:
    duck_conn.close()
    pg_conn.close()
