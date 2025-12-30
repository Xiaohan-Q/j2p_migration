```
import json
from typing import IO, List, Optional

import pytest

from emoji_loader import EmojiLoader
from emoji_loader.typing import Emoji


class TestEmojiLoader:
    def test_load_emojis(self):
        """Test the load_emojis method with a valid JSON file."""
        loader = EmojiLoader()
        with open("test/data/emojis.json") as stream:
            emojis = loader.load_emojis(stream)
        assert len(emojis) == 3
        assert isinstance(emojis[0], Emoji)
        assert emojis[0].emoji == "😀"
        assert emojis[1].description == "Face with tears of joy"
        assert not emojis[2].supports_fitzpatrick
        assert len(emojis[2].aliases) == 2
        assert len(emojis[2].tags) == 3

    def test_load_emojis_with_invalid_json(self):
        """Test the load_emojis method with an invalid JSON file."""
        loader = EmojiLoader()
        with open("test/data/invalid_emojis.json") as stream:
            with pytest.raises(ValueError):
                loader.load_emojis(stream)

    def test_build_emoji_from_json(self):
        """Test the build_emoji_from_json method with a valid JSON object."""
        loader = EmojiLoader()
        json = {"emoji": "😀", "description": "Face with tears of joy", "supports_fitzpatrick": True, "aliases": ["tears of joy"], "tags": ["happy"]}
        emoji = loader.build_emoji_from_json(json)
        assert isinstance(emoji, Emoji)
        assert emoji.emoji == "😀"
        assert emoji.description == "Face with tears of joy"
        assert emoji.supports_fitzpatrick
        assert len(emoji.aliases) == 1
        assert len(emoji.tags) == 1

    def test_build_emoji_from_json_with_invalid_json(self):
        """Test the build_emoji_from_json method with an invalid JSON object."""
        loader = EmojiLoader()
        json = {"foo": "bar"}
        with pytest.raises(KeyError):
            loader.build_emoji_from_json(json)
```