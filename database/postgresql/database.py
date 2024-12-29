from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import app.database.postgresql.utils as utils
import pandas

class Database:
    def __init__(self, database_url: str):
        self._db_url = database_url
        self._conn_params = utils.parse_conn_params(database_url)
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def get_session(self):
        return self.Session()

    def get_selected_columns(self, table_name, columns):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = select(*[table.c[column] for column in columns])
        with self.get_session() as session:
            results = session.execute(stmt).fetchall()
            return results

    def df_to_postgres(self, df: pandas.DataFrame, table_name: str):
        utils.df_to_postgres(df, table_name, self._conn_params)


# тест

# Конфигурация базы данных
# DATABASE_URL = "postgresql://postgres:12345678@localhost/binance"
#
# # Создание экземпляра класса Database
# db = Database(DATABASE_URL)
#
# # Имя таблицы и колонки для выборки
# table_name = 'adausdt1d'
# columns = ['open', 'high', 'low', 'close', 'volume']
#
# # Получение данных из таблицы
# data = db.get_selected_columns(table_name, columns)
# for row in data:
#     print(f"Open: {row.open}, High: {row.high}, Low: {row.low}, Close: {row.close}, Volume: {row.volume}")
