from PIL import Image, ImageEnhance

def GenAlphaMask(image, grayscale, bg_color, darken):
    alpha = image.getchannel("A")
    
    if darken > 0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(float(darken))

    background = Image.new("RGB", image.size, bg_color)
    color = Image.composite(image.convert("RGB"), background, alpha)

    if grayscale:
        color = color.convert("L").convert("RGB")

    return color, alpha.convert("RGB")


def GenColorMask(image, grayscale, bg_color, darken):
    alpha = image.getchannel("A")
    
    if darken > 0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(float(darken))

    flat_alpha = alpha.point(lambda p: 255 if p > 0 else 0)

    background = Image.new("RGB", image.size, bg_color)
    color = Image.composite(image.convert("RGB"), background, alpha)
    mask = Image.composite(image.convert("RGB"), background, flat_alpha)

    if grayscale:
        color = color.convert("L").convert("RGB")
        mask = mask.convert("L").convert("RGB")

    return color, mask

def GenMask(image, use_color, grayscale=False, bg_color=(255,255,255), darken=0.):
    if use_color:
        return GenColorMask(image, grayscale, bg_color, darken)
    else:
        return GenAlphaMask(image, grayscale, bg_color, darken)