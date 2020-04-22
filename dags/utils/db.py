from typing import List, Dict, Iterable


class Database:
    pass


class InsertBuffer:

    def __init__(self, size: int, table_name: str):
        self.size = size
        self.table_name = table_name
        self.db = Database()
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
        print(f'Inserting batch of {len(self)} to {self.table_name} table...')
        # db upload
        print('Done.')
        self.data = []

    def run(self, iterable: Iterable):

        for item in iterable:
            self.__append(item)

        self.__flush()
