# Pngquant
A Python Wrapper of pngquant

* [Lossy PNG compressor — pngquant command and libimagequant library](https://github.com/pornel/pngquant)

## Installation
Install Pngquant First. See https://pngquant.org/
```
pip install pngquant
```

## Usage
```
import pngquant

pngquant.config('~/pngquant/pngquant')
pngquant.quant_image('~/pngquant/pngquant/pngquant.png')
```

## Method
```
def config(self, quant_file=None, min_quality=None, max_quality=None, ndeep=None, ndigits=None, tmp_file=None):

def quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):

def quant_image(self, image=None, dst=None, ndeep=None, ndigits=None, override=True, delete=True):
```
