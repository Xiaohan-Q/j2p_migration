import pytest
from typing import List, Optional
from emoji_trie import EmojiTrie, Emoji

# Fixtures for testing the EmojiTrie class
@pytest.fixture
def emojis() -> List[Emoji]:
    return [
        Emoji("😀"),
        Emoji("😃"),
        Emoji("😄"),
        Emoji("😁"),
        Emoji("😆"),
        Emoji("😅"),
        Emoji("😂"),
        Emoji("🤣"),
    ]

@pytest.fixture
def unicode_str() -> str:
    return "😀😃😄😁😆😅😂"

# Test the constructor of EmojiTrie class
def test_constructor(emojis):
    emoji_trie = EmojiTrie(emojis)
    assert isinstance(emoji_trie, EmojiTrie)
    assert len(emoji_trie.root.children) == 10
    assert emoji_trie.max_depth == 6

# Test the is_emoji method with a valid sequence of characters
def test_is_emoji_valid(emojis):
    emoji_trie = EmojiTrie(emojis)
    assert emoji_trie.is_emoji("😀") is True
    assert emoji_trie.is_emoji("😃") is True
    assert emoji_trie.is_emoji("😄") is True
    assert emoji_trie.is_emoji("😁") is True
    assert emoji_trie.is_emoji("😆") is True
    assert emoji_trie.is_emoji("😅") is True
    assert emoji_trie.is_emoji("😂") is True
    assert emoji_trie.is_emoji("🤣") is True

# Test the is_emoji method with an invalid sequence of characters
def test_is_emoji_invalid(emojis):
    emoji_trie = EmojiTrie(emojis)
    assert emoji_trie.is_emoji("😢") is False
    assert emoji_trie.is_emoji("😣") is False
    assert emoji_trie.is_emoji("😤") is False
    assert emoji_trie.is_emoji("😦") is False
    assert emoji_trie.is_emoji("😧") is False
    assert emoji_trie.is_emoji("😨") is False
    assert emoji_trie.is_emoji("😩") is False
    assert emoji_trie.is_emoji("😪") is False
    assert emoji_trie.is_emoji("😫") is False
    assert emoji_trie.is_emoji("😬") is False

# Test the get_emoji method with a valid Unicode string
def test_get_emoji_valid(unicode_str):
    emoji_trie = EmojiTrie([Emoji(unicode_str)])
    assert emoji_trie.get_emoji(unicode_str) == Emoji(unicode_str)

# Test the get_emoji method with an invalid Unicode string
def test_get_emoji_invalid(emojis):
    emoji_trie = EmojiTrie(emojis)
    assert emoji_trie.get_emoji("😢") == None
    assert emoji_trie.get_emoji("😣") == None
    assert emoji_trie.get_emoji("😤") == None
    assert emoji_trie.get_emoji("😦") == None
    assert emoji_trie.get_emoji("😧") == None
    assert emoji_trie.get_emoji("😨") == None
    assert emoji_trie.get_emoji("😩") == None
    assert emoji_trie.get_emoji("😪") == None
    assert emoji_trie.get_emoji("😫") == None
    assert emoji_trie.get_emoji("😬") == None