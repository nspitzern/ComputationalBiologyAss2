from typing import List


class Memory:
    def __init__(self) -> None:
        self.__records: List[str] = list()
    
    @property
    def records(self):
        return self.__records
    
    @records.setter
    def records(self, records):
        self.__records = list(records[:])
    
    def add(self, record: str):
        self.__records.append(record)
    
    def __contains__(self, item):
        return item in self.__records
