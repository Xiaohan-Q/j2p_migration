import enum

class Fitzpatrick(enum.Enum):
    """
    Enum that represents the Fitzpatrick modifiers supported by the emojis.
    
    Attributes:
        TYPE_1_2 (Fitzpatrick): Fitzpatrick modifier of type 1/2 (pale white/white)
        TYPE_3 (Fitzpatrick): Fitzpatrick modifier of type 3 (cream white)
        TYPE_4 (Fitzpatrick): Fitzpatrick modifier of type 4 (moderate brown)
        TYPE_5 (Fitzpatrick): Fitzpatrick modifier of type 5 (dark brown)
        TYPE_6 (Fitzpatrick): Fitzpatrick modifier of type 6 (black)
    """
    
    TYPE_1_2 = "\uD83C\uDFFB"
    TYPE_3 = "\uD83C\uDFFC"
    TYPE_4 = "\uD83C\uDFFD"
    TYPE_5 = "\uD83C\uDFFE"
    TYPE_6 = "\uD83C\uDFFF"
    
    def __init__(self, unicode: str):
        self.unicode = unicode
    
    @classmethod
    def fitzpatrick_from_unicode(cls, unicode: str) -> "Fitzpatrick":
        """
        Return the Fitzpatrick modifier for a given Unicode representation.
        
        Args:
            unicode (str): The Unicode representation of the Fitzpatrick modifier.
        
        Returns:
            Fitzpatrick: The corresponding Fitzpatrick modifier, or None if it is not found.
        """
        for v in cls:
            if v.unicode == unicode:
                return v
        return None
    
    @classmethod
    def fitzpatrick_from_type(cls, type: str) -> "Fitzpatrick":
        """
        Return the Fitzpatrick modifier for a given type.
        
        Args:
            type (str): The type of the Fitzpatrick modifier.
        
        Returns:
            Fitzpatrick: The corresponding Fitzpatrick modifier, or None if it is not found.
        """
        try:
            return cls(type)
        except ValueError:
            return None