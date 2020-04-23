from typing import List, Dict, Iterable


class Database:
    
    def __init__(self):
        pass
    
    def insert(self, table_name: str, rows: Iterable[Dict]):
        InsertBuffer(db=self, table_name=table_name, size=500).run(rows)


class InsertBuffer:

    def __init__(self, db: Database, table_name: str, size: int):
        self.db = db
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
        # db batch insert
        print('Done.')
        self.data = []

    def run(self, iterable: Iterable):

        for item in iterable:
            self.__append(item)

        self.__flush()
