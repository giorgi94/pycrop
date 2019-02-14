# PyCrop

1. What it does
2. functions
    1. Contain
    2. Cover
3. Installation

## What it does
Methods to manipulate images

## Functions

### 1.Cover
- params:
    - path:str - image absolute path
    - size:list - output image size (width:int, height:int)
    - point:list - point from where image is cropped and resized
    - savepath:str - image destination path
    - quality:int - output image quality (from 0 to 100%)
- returns:
    - (resize status, output image path):tuple

Based on size, it will crop evenly distributed rectagle from point coordinates (in percentage).

### 2.Contain
- params:
    - path:str - image absolute path
    - size:list - output image size (width:int, height:int)
    - savepath:str - image destination path
    - quality:int - output image quality (from 0 to 100%)
- returns:
    - (resize status, output image path):tuple 

Function will fit source image in rectagle which has same dimensions as size.

## Installation

To install the package by `pip` run following command

```sh
$ pip install pycrop
```

or

```sh
$ pip install git+https://github.com/giorgi94/pycrop.git
```
