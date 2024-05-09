from enum import Enum


class CloudAccountType(str, Enum):
    BYOA = "BYOA"
    HOSTED = "HOSTED"

    def __str__(self) -> str:
        return str(self.value)
