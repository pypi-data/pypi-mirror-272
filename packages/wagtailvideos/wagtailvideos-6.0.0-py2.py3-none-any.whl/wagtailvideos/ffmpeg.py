import datetime
import logging
import os
import re
import shutil
import subprocess
import tempfile
from shutil import which

from django.conf import settings
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


def DEVNULL():
    return open(os.devnull, 'r+b')


def installed(path=None):
    return which('ffmpeg', path=path) is not None


def get_duration(file_path):
    if not installed():
        raise RuntimeError('ffmpeg is not installed')

    try:
        show_format = subprocess.check_output(
            ['ffprobe', file_path, '-show_format', '-v', 'quiet'],
            stdin=DEVNULL(), stderr=DEVNULL())
        show_format = show_format.decode("utf-8")
        # show_format comes out in key=value pairs seperated by newlines
        duration = re.findall(r'([duration^=]+)=([^=]+)(?:\n|$)', show_format)[0][1]
        return datetime.timedelta(seconds=float(duration))
    except subprocess.CalledProcessError:
        logger.exception("Getting video duration failed")
        return None


def get_thumbnail(file_path):
    if not installed():
        raise RuntimeError('ffmpeg is not installed')

    file_name = os.path.basename(file_path)
    thumb_extension = getattr(settings, 'WAGTAIL_VIDEOS_THUMBNAIL_EXTENSION', 'jpg').lower()
    thumb_name = '{}_thumb.{}'.format(os.path.splitext(file_name)[0], thumb_extension)

    try:
        output_dir = tempfile.mkdtemp()
        output_file = os.path.join(output_dir, thumb_name)
        try:
            subprocess.check_call([
                'ffmpeg',
                '-v', 'quiet',
                '-itsoffset', '-4',
                '-i', file_path,
                '-update', 'true',
                '-vframes', '1',
                '-an',
                '-vf', 'scale=iw:-1',  # Make thumbnail the size & aspect ratio of the input video
                output_file,
            ], stdin=DEVNULL(), stdout=DEVNULL())
        except subprocess.CalledProcessError:
            return None
        return ContentFile(open(output_file, 'rb').read(), thumb_name)
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)
