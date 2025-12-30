import typing
from typing import List, Optional

class Emoji:
    def __init__(self, unicode: str) -> None:
        self.unicode = unicode

class Node:
    def __init__(self) -> None:
        self.children = {}  # type: Dict[str, Node]
        self.emoji = None  # type: Optional[Emoji]

    def set_emoji(self, emoji: Emoji) -> None:
        self.emoji = emoji

    def get_emoji(self) -> Optional[Emoji]:
        return self.emoji

    def has_child(self, child: str) -> bool:
        return child in self.children

    def add_child(self, child: str) -> None:
        self.children[child] = Node()

    def get_child(self, child: str) -> Optional[Node]:
        if child in self.children:
            return self.children[child]
        else:
            return None

    def is_end_of_emoji(self) -> bool:
        return self.emoji is not None

class EmojiTrie:
    def __init__(self, emojis: List[Emoji]) -> None:
        self.root = Node()
        self.max_depth = 0
        for emoji in emojis:
            tree = self.root
            chars = list(emoji.unicode)
            self.max_depth = max(self.max_depth, len(chars))
            for c in chars:
                if not tree.has_child(c):
                    tree.add_child(c)
                tree = tree.get_child(c)
            tree.set_emoji(emoji)

    def is_emoji(self, sequence: List[str]) -> bool:
        """Checks if a sequence of chars contains an emoji."""
        tree = self.root
        for c in sequence:
            if not tree.has_child(c):
                return False
            tree = tree.get_child(c)
        return tree.is_end_of_emoji()

    def get_emoji(self, unicode: str) -> Optional[Emoji]:
        """Finds an emoji instance from a given Unicode string."""
        chars = list(unicode)
        tree = self.root
        for c in chars:
            if not tree.has_child(c):
                return None
            tree = tree.get_child(c)
        return tree.get_emoji()