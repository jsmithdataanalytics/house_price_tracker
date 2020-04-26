from typing import List, Dict, Iterable
import sqlite3
from airflow.hooks.sqlite_hook import SqliteHook

db_filename = SqliteHook.get_connection('property_db').host


def select_all(table_name: str):
    connection = sqlite3.connect(db_filename)
    connection.row_factory = sqlite3.Row

    with connection:
        cursor = connection.execute(f'SELECT * FROM `{table_name}`')
        result = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return result

    
def insert_or_replace(table_name: str, items: Iterable[Dict]):
    InsertOrReplaceBuffer(table_name=table_name, size=500).run(items)


class InsertOrReplaceBuffer:

    def __init__(self, table_name: str, size: int):
        self.table_name = table_name
        self.size = size
        self.data: List[Dict] = []

    def __len__(self):
        return len(self.data)

    def __is_full(self):
        return len(self) >= self.size

    def __append(self, item: Dict):

        if self.__is_full():
            self.__flush()

        self.data.append(item)

    def __flush(self):
        print(f'Uploading batch of {len(self)} {self.table_name.lower()} to database...')
        column_names = list(self.data[0].keys())
        values = [tuple(item[column_name] for column_name in column_names) for item in self.data]

        column_names_string = ', '.join([f'`{column_name}`' for column_name in column_names])
        placeholders_string = ', '.join(['?'] * len(column_names))
        query = f'REPLACE INTO `{self.table_name}` ({column_names_string}) VALUES ({placeholders_string})'

        connection = sqlite3.connect(db_filename)

        with connection:
            connection.executemany(query, values)

        connection.close()

        print('Done.')
        self.data = []

    def run(self, iterable: Iterable):

        for item in iterable:
            self.__append(item)

        self.__flush()
