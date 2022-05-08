import os.path

from django.conf import settings


def sponsor_filesanitize(fileattr, sponsor):
    f = getattr(sponsor, fileattr)
    if not f:
        return None

    absolutePath = settings.MEDIA_ROOT / f.name

    newname = sponsor.contact.companyName + absolutePath.suffix

    return (absolutePath, newname)
