import os.path
import random
import string

from django.conf import settings


def random_filename_generator(size=16, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


def random_filename_upload(basedir):
    def upload_transform_func(instance, filename):
        fn, ext = os.path.splitext(filename)
        while True:
            newname = random_filename_generator() + ext
            path = os.path.join(basedir, newname)
            if not (settings.MEDIA_ROOT / path).is_file():
                break
        return path

    return upload_transform_func
