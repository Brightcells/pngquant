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

import os
import shutil
import subprocess


class PngQuant(object):
    def __init__(self):
        self.quant_file = ''
        self.tmp_file = '/tmp/quant.tmp.png'
        self.min_quality = 65
        self.max_quality = 80
        self.quant_deep = 100
        self.quant_cmd = r'{quant_file} --quality={min_quality}-{max_quality} --force - < {tmp_file}'.format(
            quant_file=self.quant_file,
            min_quality=self.min_quality,
            max_quality=self.max_quality,
            tmp_file=self.tmp_file,
        )

    def config(self, quant_file=None, min_quality=None, max_quality=None, quant_deep=None, tmp_file=None):
        """
        Config

        :param quant_file: pngquant exec file
        :param min_quality: Min Quality
        :param max_quality: Max Quality
        :param quant_deep:
        :param tmp_file:
        :return:
        """
        self.quant_file = quant_file or self.quant_file
        self.min_quality = min_quality or self.min_quality
        self.max_quality = max_quality or self.max_quality
        self.quant_deep = quant_deep or self.quant_deep
        self.tmp_file = tmp_file or self.tmp_file
        self.quant_cmd = r'{quant_file} --quality={min_quality}-{max_quality} --force - < {tmp_file}'.format(
            quant_file=self.quant_file,
            min_quality=self.min_quality,
            max_quality=self.max_quality,
            tmp_file=self.tmp_file,
        )
        return {
            'quant_file': self.quant_file,
            'min_quality': self.min_quality,
            'max_quality': self.max_quality,
            'quant_deep': self.quant_deep,
            'tmp_file': self.tmp_file,
            'quant_cmd': self.quant_cmd,
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

    def quant_data(self, data=None, dst=None, delete=True):
        """
        Compress Image by Pass Image Data

        :param data: image data
        :param dst: tmp image copy to
        :param delete: whether delete tmp image
        :return:
        """
        # Check Whether Data Exists
        if not data:
            raise ValueError(u'Lost Of Data')
        # Save Data As tmp_file
        self.save_tmp_file(data)
        # Assign Value Deep as Default & Compressed as Empty
        deep, compressed = self.quant_deep, ''
        # Exec Compressed Process Until
        # Deep become Zero or Compressed Isn't Smaller than Earlier
        while deep and (len(compressed) < len(data)):
            deep -= 1
            # Or for First Compress
            data = compressed or data
            # Read image from stdin and send result to stdout.
            compressed = subprocess.check_output(self.quant_cmd, shell=True)
            # Save Compressed Data As tmp_file
            self.save_tmp_file(compressed)
        # Judge and Copy tmp_file
        if dst:
            self.copy_tmp_file(dst)
        # Judge and Delete tmp_file
        if delete:
            self.delete_tmp_file()
        return compressed

    def quant_image(self, image=None, override=True, delete=True):
        """
        Compress Image by Pass Image Path

        :param image: image path
        :param override: whether override origin image
        :param delete: whether delete tmp image
        :return:
        """
        # Check Whether Image Exists
        if not self.file_exists(image):
            raise ValueError(u'Lost Of Image')
        # Compress Image by Call function quant_data
        # dst should pass image when override origin image
        return self.quant_data(self.open_file(image), dst=image if override else None, delete=delete)


# For backwards compatibility
_global_instance = PngQuant()
config = _global_instance.config
quant_data = _global_instance.quant_data
quant_image = _global_instance.quant_image
