
from sqlalchemy import create_engine, Table, MetaData, text, insert, values, table, column, Integer
import pandas as pd


class DataManager:
    def __init__(self, database_conf: dict):
        # conn = SqlAlchemyConnector.load("scrappy-sql-connector")
        # self.engine = create_engine('postgresql://scrappy_user:idaho777@localhost:5435/spy')
        # TODO need to check if it works the same way for bigquery and mysql
        self.engine = create_engine(
            f"{database_conf.get('database_type')}://{database_conf.get('user')}:{database_conf.get('password')}@{database_conf.get('host')}:{database_conf.get('port')}/{database_conf.get('database')}")
        self.conn = self.engine.connect()

    def select_query(self, query: str):
        return pd.read_sql_query(query, con=self.engine)

    def select_all_from(self, schema, table, columns:list = None):
        return pd.read_sql_table( table_name=table, con=self.engine, schema=schema, columns=columns)

    def _clean_data_type(self, table, data_dic):
        for col in table.columns:
            val = data_dic.get(col.name)
            if val is not None:
                data_dic[col.name] = col.type.python_type(val)

    def insert_into(self, schema: str, table_name: str, data_dic: dict):
        try:
            _table = Table(table_name, MetaData(), schema=schema, autoload_with=self.engine)
            data_dic = self._clean_data_type(table, data_dic)
            query = insert(_table).values(data_dic)
            # self.conn.rollback()
            row_id = self.conn.execute(query).inserted_primary_key[0]
            self.conn.commit()
            return row_id
        except Exception as e:
            self.conn.rollback()
            return None

    def insert_into_with_query(self, sql_statement: str, returning: str = None, autocommit: bool = True):
        try:
            if returning is None:
                returning = 'RETURNING *'
            result = self.conn.execute(text(f'{sql_statement} {returning}')).all()
            if autocommit:
                self.conn.commit()
            return result[0][0], result[0]
        except Exception as e:
            if autocommit:
                self.conn.rollback()
            raise Exception(e)

    def update_with_query(self, sql_update_statement: str, returning: str = None, autocommit: bool = True):
        return self.insert_into_with_query(sql_update_statement, returning=returning, autocommit=autocommit)

