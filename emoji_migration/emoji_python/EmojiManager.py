import typing

class EmojiManager:
    """
    Holds the loaded emojis and provides search functions.
    
    Attributes:
        EMOJIS_BY_ALIAS (dict): A map of alias to emojis
        EMOJIS_BY_TAG (dict): A map of tags to emojis
        ALL_EMOJIS (list): A list of all loaded emojis
        EMOJI_TRIE (EmojiTrie): An EmojiTrie object containing the loaded emojis
    """
    
    def __init__(self) -> None:
        """
        Initializes the EmojiManager with the given resources.
        """
        self.EMOJIS_BY_ALIAS = {}
        self.EMOJIS_BY_TAG = {}
        self.ALL_EMOJIS = []
        self.EMOJI_TRIE = EmojiTrie(self.ALL_EMOJIS)
    
    def getForTag(self, tag: str) -> typing.Set[Emoji]:
        """
        Returns all the Emojis for a given tag.
        
        Args:
            tag (str): The tag to search for
            
        Returns:
            set: A set of matching emojis, None if the tag is unknown
        """
        if not tag:
            return None
        return self.EMOJIS_BY_TAG.get(tag)
    
    def getForAlias(self, alias: str) -> Emoji:
        """
        Returns the Emoji for a given alias.
        
        Args:
            alias (str): The alias to search for
            
        Returns:
            emoji: The matching emoji, None if the alias is unknown
        """
        if not alias or not alias.strip():
            return None
        return self.EMOJIS_BY_ALIAS.get(alias)
    
    def getByUnicode(self, unicode: str) -> Emoji:
        """
        Returns the Emoji for a given unicode.
        
        Args:
            unicode (str): The unicode to search for
            
        Returns:
            emoji: The matching emoji, None if the unicode is unknown
        """
        return self.EMOJI_TRIE.getEmoji(unicode)
    
    def getAll(self) -> typing.List[Emoji]:
        """
        Returns all the loaded Emojis.
        
        Returns:
            list: A list of all loaded emojis
        """
        return self.ALL_EMOJIS
    
    @staticmethod
    def isEmoji(string: str) -> bool:
        """
        Tests if a given String is an emoji.
        
        Args:
            string (str): The string to test
            
        Returns:
            bool: True if the string is an emoji, False otherwise
        """
        return EmojiParser.getNextUnicodeCandidate(string.toCharArray(), 0) != None and EmojiParser.getNextUnicodeCandidate(string.toCharArray(), 0).emojiStartIndex == 0 and EmojiParser.getNextUnicodeCandidate(string.toCharArray(), 0).fitzpatrickEndIndex == len(string)
    
    @staticmethod
    def containsEmoji(string: str) -> bool:
        """
        Tests if a given String contains an emoji.
        
        Args:
            string (str): The string to test
            
        Returns:
            bool: True if the string contains an emoji, False otherwise
        """
        return EmojiParser.getNextUnicodeCandidate(string.toCharArray(), 0) != None
    
    @staticmethod
    def isOnlyEmojis(string: str) -> bool:
        """
        Tests if a given String only contains emojis.
        
        Args:
            string (str): The string to test
            
        Returns:
            bool: True if the string only contains emojis, False otherwise
        """
        return string != None and EmojiParser.removeAllEmojis(string) == ""
    
    @staticmethod
    def isEmoji(sequence: typing.Sequence[typing.Any]) -> "EmojiTrie.Matches":
        """
        Checks if sequence of chars contain an emoji.
        
        Args:
            sequence (Sequence): Sequence of char that may contain emoji in full or partially.
            
        Returns:
            EmojiTrie.Matches: 
                Matches.EXACTLY if char sequence in its entirety is an emoji
                Matches.POSSIBLY if char sequence matches prefix of an emoji
                Matches.IMPOSSIBLE if char sequence matches no emoji or prefix of an emoji
        """
        return self.EMOJI_TRIE.isEmoji(sequence)
    
    @staticmethod
    def getAllTags() -> typing.List[str]:
        """
        Returns all the tags in the database
        
        Returns:
            list: A list of all tags
        """
        return list(self.EMOJIS_BY_TAG.keys())