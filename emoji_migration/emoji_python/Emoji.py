# coding=utf-8
import typing

class Emoji:
    """
    This class represents an emoji.

    Attributes:
        description: The description of the emoji.
        supports_fitzpatrick: Whether the emoji supports Fitzpatrick modifiers or not.
        aliases: The aliases for this emoji.
        tags: The tags associated with this emoji.
        unicode: The unicode representation of the emoji.
        html_decimal: The HTML decimal representation of the emoji.
        html_hexadecimal: The HTML hexadecimal representation of the emoji.
    """

    def __init__(self, description: str, supports_fitzpatrick: bool, aliases: typing.List[str], tags: typing.List[str], bytes: bytes) -> None:
        self.description = description
        self.supports_fitzpatrick = supports_fitzpatrick
        self.aliases = aliases
        self.tags = tags
        try:
            self.unicode = bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            raise ValueError('Invalid unicode bytes') from e
        self.html_decimal = ''.join(f'&#{ord(c)};' for c in self.unicode)
        self.html_hexadecimal = ''.join(f'&#x{ord(c):04X};' for c in self.unicode)

    def get_description(self) -> str:
        """Returns the description of the emoji."""
        return self.description

    def get_tags(self) -> typing.List[str]:
        """Returns the tags associated with this emoji."""
        return self.tags

    def get_unicode(self) -> str:
        """Returns the unicode representation of the emoji."""
        return self.unicode

    def get_html_decimal(self) -> str:
        """Returns the HTML decimal representation of the emoji."""
        return self.html_decimal

    def get_html_hexadecimal(self) -> str:
        """Returns the HTML hexadecimal representation of the emoji."""
        return self.html_hexadecimal

    def __str__(self) -> str:
        """Returns a string representation of this object."""
        return f'Emoji {{ description="{self.description}", supports_fitzpatrick={self.supports_fitzpatrick}, aliases={self.aliases}, tags={self.tags}, unicode="{self.unicode}", html_decimal="{self.html_decimal}", html_hexadecimal="{self.html_hexadecimal}" }}'