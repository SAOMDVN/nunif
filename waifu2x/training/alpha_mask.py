import random
from io import BytesIO
from PIL import Image, ImageEnhance
from torchvision.transforms import functional as TF
import torch
from os import path

def GenAlphaMask(image, grayscale, bg_color, darken):
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

def GenColorMask(image, grayscale, bg_color, darken):
    background_color = bg_color

    source = image
    alpha = source.getchannel("A")

    if darken:
        enhancer = ImageEnhance.Brightness(source)
        source = enhancer.enhance(float(darken))

    flat = alpha.point(lambda p: 255 if p > 0 else 0)
    background = Image.new("RGB", source.size, background_color)
    color = Image.composite(source, background, alpha)
    mask = Image.composite(source, background, flat)

    if grayscale:
        color = color.convert("L")
        mask = mask.convert("L")

    return color.convert("RGB"), mask.convert("RGB")

def GenMask(image, use_color=False, grayscale=False, bg_color=(255,255,255), darken=0.):
    if use_color:
        return GenColorMask(image, grayscale, bg_color, darken)
    else:
        return GenAlphaMask(image, grayscale, bg_color, darken)