import os.path

from django.conf import settings


def sponsor_filesanitize(fileattr, sponsor):
    f = getattr(sponsor, fileattr)
    if not f:
        return None

    absolutePath = settings.MEDIA_ROOT + f.name

    (base, name) = os.path.split(absolutePath)
    (oldname, ext) = os.path.splitext(name)
    newname = sponsor.contact.companyName + ext

    return (absolutePath, newname)
