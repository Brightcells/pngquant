#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 HQM <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import division

import imghdr
import os
import shutil
import subprocess


class PngQuant(object):
    def set_command_line(self):
        """
        Set Quant CMD

        :return:
        """
        return self.command_str.format(
            quant_file=self.quant_file,
            min_quality=self.min_quality,
            max_quality=self.max_quality,
            tmp_file=self.tmp_file,
        )

    def __init__(self):
        """
        Config Init

        :return:
        """
        # Pngquant Config
        self.command_str = ur'{quant_file} --quality={min_quality}-{max_quality} --force - < {tmp_file}'
        self.quant_file = ''
        self.min_quality = 65
        self.max_quality = 80
        # Compress Config
        self.ndeep = 100
        self.ndigits = 4
        self.tmp_file = '/tmp/quant.tmp.png'
        self.command_line = self.set_command_line()
        # Error Description
        self.err_data = u'data not found'
        self.err_image = u'image not found'
        self.err_pngquant = u'pngquant not found'

    def config(self, quant_file=None, min_quality=None, max_quality=None, ndeep=None, ndigits=None, tmp_file=None):
        """
        Config Set

        :param quant_file: Pngquant Exec File
        :param min_quality: Min Quality
        :param max_quality: Max Quality
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param tmp_file: Tmp File Image Save As
        :return:
        """
        self.quant_file = quant_file or self.quant_file
        self.min_quality = min_quality or self.min_quality
        self.max_quality = max_quality or self.max_quality
        self.ndeep = ndeep or self.ndeep
        self.ndigits = ndigits or self.ndigits
        self.tmp_file = tmp_file or self.tmp_file
        self.command_line = self.set_command_line()
        return {
            'quant_file': self.quant_file,
            'min_quality': self.min_quality,
            'max_quality': self.max_quality,
            'ndeep': self.ndeep,
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
        with open(filename, 'r') as f:
            return f.read()

    def save_tmp_file(self, data):
        """
        Save Data As Tmp File

        :param data: Data to Save
        :return:
        """
        with open(self.tmp_file, 'w') as f:
            f.write(data)

    def copy_tmp_file(self, dst):
        """
        Copy Tmp File To DST

        :param dst: Tmp Image Copy To
        :return:
        """
        if dst and self.file_exists(self.tmp_file):
            shutil.copyfile(self.tmp_file, dst)

    def delete_tmp_file(self, delete):
        """
        Delete Tmp File

        :return:
        """
        if delete and self.file_exists(self.tmp_file):
            os.remove(self.tmp_file)

    def compression_ratio(self, origin_len, compressed_len, ndigits=None):
        """
        Calculate Compress Proportion

        :param origin_data:
        :param compressed_data:
        :param ndigits: float precision
        :return:
        """
        return round((origin_len - compressed_len) / origin_len, ndigits or self.ndigits)

    def quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):
        """
        Compress Image By Pass Image Data

        :param data: Image Data
        :param dst: Tmp Tmage Copy To
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param delete: Whether Delete Tmp Image
        :return:
        """
        # Check Whether Pngquant Exist
        if not self.file_exists(self.quant_file):
            raise ValueError(self.err_pngquant)

        # Check Whether Data Exist
        if not data:
            raise ValueError(self.err_data)

        # Save Data As Tmp File
        self.save_tmp_file(data)

        # Assign Value Origin_data As Data & Ndeep As Pass or Default & Compressed_data As Empty
        origin_data, ndeep, compressed_data = data, ndeep or self.ndeep, ''
        # Calculate Length Of Data, Origin_data, Compressed_data
        data_len, origin_len, compressed_len = len(data), len(origin_data), 0

        # Loop Exec Compressed Process Until
        # Ndeep Become Zero Or Compressed Isn't Smaller Than Earlier
        while ndeep and (compressed_len < origin_len):
            ndeep -= 1
            # Or For First Compress
            origin_len = compressed_len or origin_len
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
            except subprocess.CalledProcessError as e:
                # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                compressed_data = origin_data
            # Save Compressed Data As Tmp File
            self.save_tmp_file(compressed_data)
            compressed_len = len(compressed_data)
        else:
            if compressed_len < data_len:
                # Copy Tmp File
                self.copy_tmp_file(dst)
            # Delete Tmp File
            self.delete_tmp_file(delete)

        return (self.compression_ratio(data_len, compressed_len, ndigits), compressed_data) if compressed_len < data_len else (0, data)

    def quant_image(self, image=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True):
        """
        Compress Image By Pass Image Path

        :param image: Image Path
        :param dst: Dst Image
        :param ndeep: Compress Times
        :param ndigits: Float Precision
        :param override: Whether Override Origin Image
        :param delete: Whether Delete Tmp Image
        :return:
        """
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
        :param delete: Whether Delete Tmp Image
        :param topdown:
        :return:
        """
        # Check Whether Pngquant Exist
        if not self.file_exists(self.quant_file):
            raise ValueError(self.err_pngquant)

        results = []
        # Traversal Dir To Compress Image One By One
        for root, dirs, files in os.walk(dir, topdown):
            for name in files:
                filename = os.path.join(root, name)
                print filename
                # Whether File An Image, If Not, Do Nothing
                if imghdr.what(filename):
                    # Compress Image By Call Function quant_image
                    # Dst Should Pass Dst + Name
                    ratio, data = self.quant_image(filename, dst=dst and os.path.join(dst, name), ndeep=ndeep, ndigits=ndigits, override=override, delete=delete)
                    print ratio
                    results.append((filename, ratio, data))
        return results


# For backwards compatibility
_global_instance = PngQuant()
config = _global_instance.config
quant_data = _global_instance.quant_data
quant_image = _global_instance.quant_image
quant_dir = _global_instance.quant_dir
