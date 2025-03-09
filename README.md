# Pngquant
Pngquant is a command-line utility and a library for lossy compression of PNG images.

And This Library Is A Python Wrapper Of Pngquant

* [Lossy PNG compressor — pngquant command and libimagequant library](https://github.com/pornel/pngquant)

## Installation
* Install Pngquant
  * https://pngquant.org/
  * [pngquant 2.0 for ubuntu 12.04 not available](http://askubuntu.com/questions/469171/pngquant-2-0-for-ubuntu-12-04-not-available)

* Install Python Wrapper Of Pngquant

  ```shell
  pip install pngquant
  ```

## Usage
```python
import pngquant

pngquant.config('~/pngquant/pngquant')
pngquant.quant_image('~/pngquant/pngquant/pngquant.png')
```

## Method
```python
def config(self, quant_file=None, min_quality=None, max_quality=None, ndeep=None, ndigits=None, tmp_file=None, speed=None):

def quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):

def quant_image(self, image=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True):

def quant_dir(self, dir=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True, topdown=True):
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Brightcells/pngquant&type=Date)](https://star-history.com/#Brightcells/pngquant&Date)
