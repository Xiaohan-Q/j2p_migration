import pytest
from typing import List

class Emoji:
    def __init__(self, description: str, supports_fitzpatrick: bool, aliases: List[str], tags: List[str], bytes: bytes) -> None:
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

    def get_tags(self) -> List[str]:
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

@pytest.fixture
def emoji() -> Emoji:
    return Emoji("smiley", False, ["smile"], ["happy"], b"😊")

def test_description(emoji):
    assert emoji.get_description() == "smiley"

def test_tags(emoji):
    assert emoji.get_tags() == ["happy"]

def test_unicode(emoji):
    assert emoji.get_unicode() == "😊"

def test_html_decimal(emoji):
    assert emoji.get_html_decimal() == "&#128516;"

def test_html_hexadecimal(emoji):
    assert emoji.get_html_hexadecimal() == "&#x1F60A;"

def test_str(emoji):
    assert str(emoji) == "Emoji { description='smiley', supports_fitzpatrick=False, aliases=['smile'], tags=['happy'], unicode='😊', html_decimal='&#128516;', html_hexadecimal='&#x1F60A;' }"

def test_repr(emoji):
    assert repr(emoji) == "Emoji { description='smiley', supports_fitzpatrick=False, aliases=['smile'], tags=['happy'], unicode='😊', html_decimal='&#128516;', html_hexadecimal='&#x1F60A;' }"