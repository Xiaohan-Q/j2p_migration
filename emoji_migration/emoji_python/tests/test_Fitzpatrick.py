import pytest
from typing import Optional

class Fitzpatrick(NamedTuple):
    """
    Enum that represents the Fitzpatrick modifiers supported by the emojis.
    """

    TYPE_1_2: str = "\uD83C\uDFFB"
    TYPE_3: str = "\uD83C\uDFFC"
    TYPE_4: str = "\uD83C\uDFFD"
    TYPE_5: str = "\uD83C\uDFFE"
    TYPE_6: str = "\uD83C\uDFFF"

    def __init__(self, unicode: str) -> None:
        """
        Initialize the Fitzpatrick modifier with a Unicode value.

        Args:
            unicode (str): The Unicode value of the Fitzpatrick modifier.
        """
        self.unicode = unicode

    @classmethod
    def fitzpatrick_from_unicode(cls, unicode: str) -> Optional[Fitzpatrick]:
        """
        Get the Fitzpatrick modifier from a Unicode value.

        Args:
            unicode (str): The Unicode value of the Fitzpatrick modifier.

        Returns:
            typing.Optional[Fitzpatrick]: The Fitzpatrick modifier if found, else None.
        """
        for v in cls:
            if v.unicode == unicode:
                return v
        return None

    @classmethod
    def fitzpatrick_from_type(cls, type: str) -> Optional[Fitzpatrick]:
        """
        Get the Fitzpatrick modifier from a type value.

        Args:
            type (str): The type value of the Fitzpatrick modifier.

        Returns:
            typing.Optional[Fitzpatrick]: The Fitzpatrick modifier if found, else None.
        """
        try:
            return cls(type.upper())
        except ValueError:
            return None