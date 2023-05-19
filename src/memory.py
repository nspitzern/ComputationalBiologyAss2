from typing import Dict


class Memory:
    def __init__(self) -> None:
        self.__records: Dict[int, str] = dict()
    
    def add(self, record: str):
        self.__records[hash(record)] = record
    
    def __contains__(self, item):
        return hash(item) in self.__records
