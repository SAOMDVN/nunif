import random
from io import BytesIO
from PIL import Image, ImageEnhance
from torchvision.transforms import functional as TF
import torch
from os import path

def StaticGenAlphaMask(image, grayscale=False, bg_color=(255, 255, 255), darken=0.):
    background_color = bg_color

    source = image
    alpha = source.getchannel("A")

    if darken:
        enhancer = ImageEnhance.Brightness(source)
        source = enhancer.enhance(float(darken))

    mask = alpha.convert("L")
    background = Image.new("RGB", source.size, background_color)
    color = Image.composite(source, background, alpha)

    if grayscale:
        color = color.convert("L")

    return color.convert("RGB"), mask.convert("RGB")

class GenAlphaMask():
    def __init__(self, grayscale=False, bg_color=(255, 255, 255), darken=0.):
        self.grayscale = grayscale
        self.background_color = bg_color
        self.darken = darken

    def __call__(self, x, y):
        source = x
        alpha = source.getchannel("A")

        if self.darken:
            enhancer = ImageEnhance.Brightness(source)
            source = enhancer.enhance(float(self.darken))

        mask = alpha.convert("L")
        background = Image.new("RGB", source.size, self.background_color)
        color = Image.composite(source, background, alpha)

        if self.grayscale:
            color = color.convert("L")

        return color.convert("RGB"), mask.convert("RGB")

