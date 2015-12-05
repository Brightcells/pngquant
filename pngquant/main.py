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
        self.command_str = ur'{quant_file} --quality={min_quality}-{max_quality} --force - < {tmp_file}'
        self.quant_file = ''
        self.min_quality = 65
        self.max_quality = 80
        self.ndeep = 100
        self.ndigits = 4
        self.tmp_file = '/tmp/quant.tmp.png'
        self.command_line = self.set_command_line()

    def config(self, quant_file=None, min_quality=None, max_quality=None, ndeep=None, ndigits=None, tmp_file=None):
        """
        Config Set

        :param quant_file: pngquant exec file
        :param min_quality: Min Quality
        :param max_quality: Max Quality
        :param ndeep: Compress Times
        :param ndigits: float precision
        :param tmp_file:
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

        :param filename: file to judge
        :return:
        """
        return os.path.exists(filename)

    def open_file(self, filename):
        """
        Open File and Get Data

        :param filename: file to open and get data
        :return:
        """
        with open(filename, 'r') as f:
            return f.read()

    def save_tmp_file(self, data):
        """
        Save Data as Tmp File

        :param data: data to save
        :return:
        """
        with open(self.tmp_file, 'w') as f:
            f.write(data)

    def copy_tmp_file(self, dst):
        """
        Copy Tmp File to DST

        :param dst: tmp image copy to
        :return:
        """
        if self.file_exists(self.tmp_file):
            shutil.copyfile(self.tmp_file, dst)

    def delete_tmp_file(self):
        """
        Delete Tmp File

        :return:
        """
        if self.file_exists(self.tmp_file):
            os.remove(self.tmp_file)

    def compress_proportion(self, origin_data, compressed_data, ndigits=None):
        """
        Calculate Compress Proportion

        :param origin_data:
        :param compressed_data:
        :param ndigits: float precision
        :return:
        """
        origin_len, compressed_len = len(origin_data), len(compressed_data)
        return round((origin_len - compressed_len) / origin_len, ndigits or self.ndigits)

    def quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):
        """
        Compress Image by Pass Image Data

        :param data: image data
        :param dst: tmp image copy to
        :param ndeep: Compress Times
        :param ndigits: float precision
        :param delete: whether delete tmp image
        :return:
        """
        # Check Whether Data Exists
        if not data:
            raise ValueError(u'Lost Of Data')
        # Save Data As tmp_file
        self.save_tmp_file(data)
        # Assign Value Origin_data as Data
        # & Ndeep as Pass or Default
        # & Compressed as Empty
        origin_data, ndeep, compressed_data = data, ndeep or self.ndeep, ''
        # Exec Compressed Process Until
        # Ndeep become Zero or Compressed Isn't Smaller than Earlier
        while ndeep and (len(compressed_data) < len(origin_data)):
            ndeep -= 1
            # Or for First Compress
            origin_data = compressed_data or origin_data
            # Read image from stdin and send result to stdout.
            compressed_data = subprocess.check_output(self.command_line, shell=True)
            # Save Compressed Data As tmp_file
            self.save_tmp_file(compressed_data)
        # Judge and Copy tmp_file
        if dst:
            self.copy_tmp_file(dst)
        # Judge and Delete tmp_file
        if delete:
            self.delete_tmp_file()
        return self.compress_proportion(data, compressed_data, ndigits), compressed_data

    def quant_image(self, image=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True):
        """
        Compress Image by Pass Image Path

        :param image: image path
        :param dst:
        :param ndeep: Compress Times
        :param ndigits: float precision
        :param override: whether override origin image
        :param delete: whether delete tmp image
        :return:
        """
        # Check Whether Image Exists
        if not self.file_exists(image):
            raise ValueError(u'Lost Of Image')
        # Compress Image by Call function quant_data
        # dst should pass image when override origin image
        return self.quant_data(self.open_file(image), dst=dst or (image if override else None), ndeep=ndeep, ndigits=ndigits, delete=delete)


# For backwards compatibility
_global_instance = PngQuant()
config = _global_instance.config
quant_data = _global_instance.quant_data
quant_image = _global_instance.quant_image
