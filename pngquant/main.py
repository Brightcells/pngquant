# -*- coding: utf-8 -*-

from __future__ import division

import os
import shutil
import subprocess
import tempfile
import uuid
from distutils.spawn import find_executable
# See http://stackoverflow.com/questions/31064981/python3-error-initial-value-must-be-str-or-none
# TypeError: initial_value must be str or None, not bytes.
# The StringIO and cStringIO modules are gone.
# Instead, import the io module and use io.StringIO or io.BytesIO for text and data respectively.
from io import BytesIO

import puremagic


# AttributeError: 'module' object has no attribute 'check_output'
# http://stackoverflow.com/questions/4814970/subprocess-check-output-doesnt-seem-to-exist-python-2-6-5/13160748#13160748
if 'check_output' not in dir(subprocess):  # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get('args')
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


try:
    from PIL import Image
except ImportError:
    import Image


class PngQuant(object):
    def __tmpfile(self):
        return os.path.join(tempfile.gettempdir(), '{0}.quant.tmp.png'.format(uuid.uuid4().hex))

    def __absolute_path(self, path):
        return path and os.path.expanduser(path)

    def set_command_line(self, tmp_file=None):
        """
        Set Quant CMD

        :return:
        """
        return self.command_str.format(
            quant_file=self.quant_file,
            min_quality=self.min_quality,
            max_quality=self.max_quality,
            speed=self.speed,
            tmp_file=tmp_file or self.tmp_file or self.__tmpfile(),
        )

    def __init__(self):
        """
        Config Init

        :return:
        """
        # Pngquant Config
        self.command_str = '{quant_file} --quality={min_quality}-{max_quality} --speed={speed} --force - < {tmp_file}'
        # By default, look for binary pngquant in PATH
        self.quant_file = find_executable('pngquant') or '/usr/bin/pngquant'
        self.min_quality = 65
        self.max_quality = 80
        # Compress Config
        self.ndeep = 100
        self.ndigits = 4
        self.speed = 3
        self.tmp_file = None
        self.command_line = None
        # Error Description
        self.err_data = 'data not found'
        self.err_image = 'image not found'
        self.err_pngquant = 'pngquant not found'

    def config(self, quant_file=None, min_quality=None, max_quality=None, ndeep=None, ndigits=None, tmp_file=None, speed=None):
        """
        Config Set

        :param quant_file: Pngquant Exec File
        :param min_quality: Min Quality
        :param max_quality: Max Quality
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param tmp_file: TMP File Image Save As
        :return:
        """
        self.quant_file = self.__absolute_path(quant_file or self.quant_file)
        self.min_quality = min_quality or self.min_quality
        self.max_quality = max_quality or self.max_quality
        self.ndeep = ndeep or self.ndeep
        self.ndigits = ndigits or self.ndigits
        self.speed = speed or self.speed
        self.tmp_file = self.__absolute_path(tmp_file or self.tmp_file)
        return {
            'quant_file': self.quant_file,
            'min_quality': self.min_quality,
            'max_quality': self.max_quality,
            'ndeep': self.ndeep,
            'speed': self.speed,
            'tmp_file': self.tmp_file,
            'command_line': self.set_command_line(),
        }

    def file_exists(self, filename):
        """
        Whether File Exists

        :param filename: File To Judge
        :return:
        """
        return os.path.exists(filename)

    def open_file(self, filename):
        """
        Open File and Get Data

        :param filename: File To Open and Get Data
        :return:
        """
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
        #
        # https://docs.python.org/3/library/functions.html#open
        # 'r'	open for reading (default)
        # 't'	text mode (default)
        # 'b'	binary mode
        #
        # In text mode (the default, or when 't' is included in the mode argument),
        # the contents of the file are returned as str,
        # the bytes having been first decoded using a platform-dependent encoding or using the specified encoding if given.
        with open(filename, 'rb') as f:
            return f.read()

    def save_tmp_file(self, data, tmp_file=None):
        """
        Save Data As TMP File

        :param data: Data to Save
        :return:
        """
        with open(tmp_file, 'wb') as f:
            f.write(data)

    def copy_tmp_file(self, dst, tmp_file=None):
        """
        Copy TMP File To DST

        :param dst: TMP Image Copy To
        :return:
        """
        if dst and self.file_exists(tmp_file):
            shutil.copyfile(tmp_file, dst)

    def delete_tmp_file(self, delete, tmp_file=None):
        """
        Delete TMP File

        :return:
        """
        if delete and self.file_exists(tmp_file):
            os.remove(tmp_file)

    def compression_ratio(self, origin_len, compressed_len, ndigits=None):
        """
        Calculate Compress Proportion

        :param origin_data:
        :param compressed_data:
        :param ndigits: float precision
        :return:
        """
        return round((origin_len - compressed_len) / origin_len, ndigits or self.ndigits)

    def quant_compress(self, data=None, ndeep=None, tmp_file=None):
        """
        Compress Image Using Pngquant

        :param data:
        :param ndeep:
        :return:
        """
        # Assign Value Origin_data As Data & Compressed_data As Empty
        origin_data, compressed_data = data, ''
        # Calculate Length of Origin_data, Compressed_data
        origin_len, compressed_len = len(origin_data), 0

        # Loop Exec Compressed Process Until Ndeep Become Zero Or Compressed Isn't Smaller Than Earlier
        while ndeep and (compressed_len < origin_len):
            ndeep -= 1
            # Or For First Compress
            origin_data, origin_len = compressed_data or origin_data, compressed_len or origin_len
            # Read Image From 'stdin' And Send Result To 'stdout'.
            #
            # See: https://pngquant.org/
            # --quality min-max
            #   Instructs pngquant to use the least amount of colors required to meet or exceed the max quality.
            #   If conversion results in quality below the min quality the image won't be saved
            #   (if outputting to stdout, 24-bit original will be output) and pngquant will exit with status code 99.
            #
            # See: https://docs.python.org/2/library/subprocess.html#subprocess.check_output
            # If the return code was non-zero it raises a CalledProcessError.
            # The CalledProcessError object will have the return code in the returncode attribute
            # and any output in the output attribute.
            try:
                compressed_data = subprocess.check_output(self.command_line, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError:
                compressed_data = origin_data
            # Save Compressed Data As TMP File
            self.save_tmp_file(compressed_data, tmp_file=tmp_file)
            compressed_len = len(compressed_data)
        return compressed_data, compressed_len

    def pillow_compress(self, data=None, ndeep=None, tmp_file=None):
        """
        Compress Image Using Pillow.Save's Optimize Option

        :param data:
        :param ndeep:
        :return:
        """
        # Assign Value Origin_data As Data & Compressed_data As Empty
        origin_data, compressed_data = data, ''
        # Calculate Length of Origin_data, Compressed_data
        origin_len, compressed_len = len(origin_data), 0

        # Get Image's Format
        fmt = Image.open(BytesIO(origin_data)).format.lower()

        # Loop Exec Compressed Process Until Ndeep Become Zero Or Compressed Isn't Smaller Than Earlier
        while ndeep and (compressed_len < origin_len):
            ndeep -= 1
            # Or For First Compress
            origin_data, origin_len = compressed_data or origin_data, compressed_len or origin_len
            # Pillow Image Save Optimize True
            im, out = Image.open(BytesIO(origin_data)), BytesIO()
            im.save(out, format=fmt, optimize=True, quality=75)
            compressed_data = out.getvalue()
            # Save Compressed Data As TMP File
            self.save_tmp_file(compressed_data, tmp_file=tmp_file)
            compressed_len = len(compressed_data)
        return compressed_data, compressed_len

    def quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):
        """
        Compress Image By Pass Image Data

        :param data: Image Data
        :param dst: TMP Tmage Copy To
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param delete: Whether Delete TMP Image
        :return:
        """
        dst = self.__absolute_path(dst)

        # Check Whether Pngquant Exist
        if not self.file_exists(self.quant_file):
            raise ValueError(self.err_pngquant)

        # Check Whether Data Exist
        if not data:
            raise ValueError(self.err_data)

        # Different path for tmp file
        tmp_file = self.tmp_file or self.__tmpfile()
        self.command_line = self.set_command_line(tmp_file)

        # Save Data As TMP File
        self.save_tmp_file(data, tmp_file=tmp_file)

        # Calculate Length Of Data & Assign Value Ndeep As Pass or Default
        data_len, ndeep = len(data), ndeep or self.ndeep

        # Compress Image Using Pngquant
        # If Not Compressed
        # Then Using Pillow.Save's Optimize Option
        compressed_data, compressed_len = self.quant_compress(data, ndeep, tmp_file=tmp_file)
        if compressed_len >= data_len:
            compressed_data, compressed_len = self.pillow_compress(data, ndeep, tmp_file=tmp_file)

        # Copy And Delete TMP File
        if compressed_len < data_len:
            self.copy_tmp_file(dst, tmp_file=tmp_file)
        self.delete_tmp_file(delete, tmp_file=tmp_file)

        return (self.compression_ratio(data_len, compressed_len, ndigits), compressed_data) if compressed_len < data_len else (0, data)

    def quant_image(self, image=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True):
        """
        Compress Image By Pass Image Path

        :param image: Image Path
        :param dst: Dst Image
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param override: Whether Override Origin Image
        :param delete: Whether Delete TMP Image
        :return:
        """
        image = self.__absolute_path(image)
        dst = self.__absolute_path(dst)

        # Check Whether Pngquant Exist
        if not self.file_exists(self.quant_file):
            raise ValueError(self.err_pngquant)

        # Check Whether Image Exist
        if not self.file_exists(image):
            raise ValueError(self.err_image)

        # Compress Image By Call Function quant_data
        # Dst Should Pass Image When Override Origin Image
        return self.quant_data(self.open_file(image), dst=dst or (override and image), ndeep=ndeep, ndigits=ndigits, delete=delete)

    def quant_dir(self, dir=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True, topdown=True):
        """
        Compress Image Appointed Dir

        :param dir: Appointed Dir
        :param dst: Dst Dir
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param override: Whether Override Origin Image
        :param delete: Whether Delete TMP Image
        :param topdown:
        :return:
        """
        dir = self.__absolute_path(dir)
        dst = self.__absolute_path(dst)

        # Check Whether Pngquant Exist
        if not self.file_exists(self.quant_file):
            raise ValueError(self.err_pngquant)

        results = []
        # Traversal Dir To Compress Image One By One
        for root, dirs, files in os.walk(dir, topdown):
            for name in files:
                filename = os.path.join(root, name)
                # Whether File An Image, If Not, Do Nothing
                if puremagic.what(filename):
                    # Compress Image By Call Function quant_image
                    # Dst Should Pass Dst + Name
                    ratio, data = self.quant_image(filename, dst=dst and os.path.join(dst, name), ndeep=ndeep, ndigits=ndigits, override=override, delete=delete)
                    results.append((filename, ratio, data))
        return results


_global_instance = PngQuant()
config = _global_instance.config
quant_data = _global_instance.quant_data
quant_image = _global_instance.quant_image
quant_dir = _global_instance.quant_dir
