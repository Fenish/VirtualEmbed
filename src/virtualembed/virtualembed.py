import json
import base64

from .embedimage import EmbedImage
import urllib.request


class VirtualEmbed:
    def __init__(self, bot_avatar: str = "", title:str="", description:str="", color:str=""):
        self._title = title
        self._description = description
        self._color = color
        self._bot_name = "Clyde"

        self.thumbnail = None
        self.image = None
        self.author_name = None
        self.author_icon = None

        self.bot_avatar = bot_avatar
        self.json = {
            'embed': {
                'type': 'rich',
                'fields': []
            }
        }

    @property
    def bot_name(self):
        return self._bot_name

    @bot_name.setter
    def bot_name(self, new_name):
        self._bot_name = new_name.replace(" ", "%20")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.json["embed"]["title"] = title

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.json["embed"]["color"] = color

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
        self.json["embed"]["description"] = description

    def get_embed_json(self):
        return self.json

    def get_base_url(self):
        return f"https://glitchii.github.io/embedbuilder/?username={self.bot_name}&verified=&avatar={self.bot_avatar}&data="

    def get_embed_as_image(self):
        html_encoded = urllib.parse.quote(str(json.dumps(self.get_embed_json())))
        message_bytes = html_encoded.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        embed_url = urllib.parse.quote(self.get_base_url() + base64_bytes.decode("utf-8"))
        screenshot = f"https://api.screenshotmachine.com?key=09b279&url={embed_url}&device=desktop&dimension=1024x768&format=jpg&selector=body%20%3E%20div%20%3E%20section.side2%20%3E%20div.msgEmbed"
        return EmbedImage(screenshot)

    def add_field(self, name: str, value: str, inline: bool):
        field = {
            "name": name,
            "value": value,
            "inline": inline
        }
        self.get_embed_json()["embed"]["fields"].append(field)

    def set_thumbnail(self, image_url: str):
        thumbnail = {
            "thumbnail": {
                "url": image_url
            }
        }
        self.thumbnail = image_url
        self.get_embed_json()["embed"].update(thumbnail)

    def set_image(self, image_url: str):
        thumbnail = {
            "image": {
                "url": image_url
            }
        }
        self.image = image_url
        self.get_embed_json()["embed"].update(thumbnail)

    def set_author(self, name: str, icon_url: str = None):
        author = {
            "author": {
                "name": name,
                "icon_url": icon_url
            }
        }
        self.author_name = name
        self.author_icon = icon_url
        self.get_embed_json()["embed"].update(author)


def virtualembed_from_embed(embed):
    try:
        import discord
        if isinstance(embed, discord.Embed):
            dc_embed = embed.to_dict()
            virtualembed = VirtualEmbed()
            virtualembed.json = {"embed": dc_embed}
            virtualembed.title = dc_embed.get("title")
            virtualembed.color = dc_embed.get("color")
            virtualembed.description = dc_embed.get("description")
            return virtualembed
        raise ValueError("The parameter must be Discord Embed")
    except ModuleNotFoundError:
        raise ModuleNotFoundError("You have to install discord library for use this function")
