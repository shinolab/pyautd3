from typing import Self


class EtherCATAdapter:
    desc: str
    name: str

    def __init__(self: Self, name: str, desc: str) -> None:
        self.desc = desc
        self.name = name

    def __repr__(self: Self) -> str:
        return f"{self.desc}, {self.name}"
