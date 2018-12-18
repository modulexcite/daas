import zipfile
from io import BytesIO
import logging
import hashlib

from . import upload_file
from .mime_type import mime_type, zip_mime_types
from . import classifier


def get_in_memory_zip_of(zip_binary):
    """
    :param zip_binary: Bytes of a zip file.
    :return: An in memory file descriptor for the given binary.
    """
    zip_file = BytesIO()
    zip_file.write(zip_binary)
    new_zip = zipfile.ZipFile(zip_file)
    return new_zip


def upload_files_of(zip_binary):
    zip_file = get_in_memory_zip_of(zip_binary)
    for name in zip_file.namelist():
        content = zip_file.read(name)
        sha1 = hashlib.sha1(content).hexdigest()
        try:
            already_exists, _ = upload_file.upload_file(name, content)
        except classifier.ClassifierError:
            logging.debug('There are no valid processor for file: %s [%s]' % (name, sha1))
        else:
            if already_exists:
                logging.debug('File already uploaded: %s [%s]' % (name, sha1))
            else:
                logging.debug('File uploaded correctly: %s [%s]' % (name, sha1))


def is_zip(binary):
    return mime_type(binary) in zip_mime_types
