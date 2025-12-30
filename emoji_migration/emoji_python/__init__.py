"""
emoji-python: Python port of emoji-java library
A lightweight Python library for working with emojis.
"""

__version__ = '0.1.0'
__author__ = 'Auto-generated from emoji-java'

# Import main classes
from .Emoji import *
from .EmojiLoader import *
from .EmojiManager import *
from .EmojiParser import *
from .EmojiTrie import *
from .Fitzpatrick import *

__all__ = [
    'Emoji',
    'EmojiLoader',
    'EmojiManager',
    'EmojiParser',
    'EmojiTrie',
    'Fitzpatrick',
]
