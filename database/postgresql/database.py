from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import app.database.postgresql.utils as utils
import pandas as pd
from app.database.models.datasource import DataSource


class Database(DataSource):
    def __init__(self, database_url: str, table_name: str):
        self._db_url = database_url
        self._conn_params = utils.parse_conn_params(database_url)
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self._table_name = table_name

    def get_session(self):
        return self.Session()

    def get_selected_columns(self, table_name, columns):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = select(*[table.c[column] for column in columns])
        with self.get_session() as session:
            results = session.execute(stmt).fetchall()
            return results

    def df_to_postgres(self, df: pd.DataFrame, table_name: str):
        utils.df_to_postgres(df, table_name, self._conn_params)

    def get_ohlcv_data(self) -> dict[str, list]:
        data = self.get_selected_columns(
            table_name=self._table_name,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df = pd.DataFrame(data)
        return df.to_dict(orient='list')
