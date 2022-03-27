from io import BytesIO
from PIL import Image
import urllib.request


class EmbedImage:
    def __init__(self, image_url):
        self.image_url = image_url

    def get_img(self):
        req = urllib.request.Request(self.image_url, headers={'User-Agent': "your bot 0.1"})
        resource = urllib.request.urlopen(req)
        img = Image.open(BytesIO(resource.read()))
        width, height = img.size
        area = (900, 0, width, height)
        cropped_img = img.crop(area)
        byteIO = BytesIO()
        cropped_img.save(byteIO, format='PNG')
        byteArr = BytesIO(byteIO.getvalue())
        return byteArr

    def save_img(self, path):
        resource = self.get_img()
        output = open(path, "wb")
        output.write(resource.read())
        output.close()

    def get_buffer(self):
        img_bytes = self.get_img()
        return img_bytes
