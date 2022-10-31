from dataclasses import dataclass


@dataclass
class Item:
    name: str
    max_stack: int
    lore: str
