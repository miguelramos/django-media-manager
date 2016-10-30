from django.test import TestCase
from django.contrib.auth import get_user_model

from filebrowser.conf import fb_settings

from PIL import Image, ImageDraw
import os


class BaseTestCase(TestCase):
    """
    Base class with user creation, etc
    """
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser('admin',
                                                        'admin@example.com',
                                                        'admin')
        self.client.login(username='admin', password='admin')

        self.img = self.create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(
            fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY, self.image_name
        )
        self.img.save(self.filename, 'JPEG')

        self.working_dir = os.path.join(fb_settings.MEDIA_ROOT,
                                        fb_settings.DIRECTORY)


    def tearDown(self):
        self.client.logout()
        os.remove(self.filename)

    def create_image(self, mode='RGB', size=(800, 600)):
        image = Image.new(mode, size)
        draw = ImageDraw.Draw(image)
        x_bit, y_bit = size[0] // 10, size[1] // 10
        draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), 'red')
        draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), 'red')
        return image
