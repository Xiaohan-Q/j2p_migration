import typing

class EmojiLoader:
    """
    Loads the emojis from a JSON database.

    Attributes:
        data (typing.List[Emoji]): A list of emojis loaded from the JSON database.

    Methods:
        load_emojis(stream: typing.IO) -> typing.List[Emoji]: Loads a JSONArray of emojis from an InputStream, parses it and returns the associated list of Emoji objects.
        build_emoji_from_json(json: typing.Any) -> typing.Optional[Emoji]: Builds an Emoji object from a JSONObject.
    """

    def __init__(self):
        self.data = []

    def load_emojis(self, stream: typing.IO) -> typing.List[Emoji]:
        emojis_json = json.loads(stream.read())
        for emoji in emojis_json:
            emoji_obj = self.build_emoji_from_json(emoji)
            if emoji_obj is not None:
                self.data.append(emoji_obj)
        return self.data

    def build_emoji_from_json(self, json: typing.Any) -> typing.Optional[Emoji]:
        """Builds an Emoji object from a JSONObject."""
        if not json.get('emoji'):
            return None
        emoji = json.get('emoji')
        description = None
        supports_fitzpatrick = False
        aliases = []
        tags = []
        try:
            description = json.get('description', None)
            supports_fitzpatrick = json.get('supports_fitzpatrick', False)
            aliases = json.get('aliases', [])
            tags = json.get('tags', [])
        except KeyError as e:
            print(f'Key error while building emoji from JSON: {e}')
        return Emoji(description, supports_fitzpatrick, aliases, tags, emoji)