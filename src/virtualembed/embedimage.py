from io import BytesIO
import urllib.request


class EmbedImage:
    def __init__(self, image_url):
        self.image_url = image_url

    def save_img(self, path):
        req = urllib.request.Request(self.image_url, headers={'User-Agent': "Magic Browser"})
        resource = urllib.request.urlopen(req)
        output = open(path, "wb")
        output.write(resource.read())
        output.close()

    def get_buffer(self):
        req = urllib.request.Request(self.image_url, headers={'User-Agent': "Magic Browser"})
        resource = urllib.request.urlopen(req)
        img_bytes = BytesIO(resource.read())
        return img_bytes
