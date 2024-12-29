import psycopg2
from urllib.parse import urlparse
from io import StringIO
import pandas

def parse_conn_params(database_url: str):
    parsed = urlparse(database_url)
    return {
        'dbname': parsed.path[1:],
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port or 5432
    }

def create_table_query(table_name: str):
    return f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT
    );
    """


def df_to_postgres(df: pandas.DataFrame, table_name: str, conn_params: dict):
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute(create_table_query(table_name))

            buffer = StringIO()
            df.to_csv(buffer, header=False, index=False)
            buffer.seek(0)

            cur.copy_from(
                buffer,
                table_name,
                sep=',',
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
    except Exception as e:
        print(f"Ошибка при записи данных: {e}")
    finally:
        conn.close()
