from typing import Union

alphabet = [
    '🟨',
    '🟩',
    '🟪',
    '🟫',
    '🟥',
    '🟦',
    '🟧',
    '⬜',
    '⬛',
]

class TableDict:
    def __init__(
        self,
        default: Union[any,None] = None
    ) -> None:
        self.default = default
        self.data = {}
    
    def __getitem__(self, item):
        if item not in self.data:
            return self.default
        return self.data[item]
    
    def __setitem__(self, key, value):
        self.data[key] = value

