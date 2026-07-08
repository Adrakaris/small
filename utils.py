import pygame 

def scale_to_new_size(image:pygame.Surface, new_width:int|None=None, new_height:int|None=None) -> pygame.Surface:
    """
    Scales a surface to the given new width or height.

    If one of width or height is not provided, that dimension will be scaled using the same aspect ratio as the input image
    """

    if new_width is None and new_height is None:
        raise ValueError("One of width or height must be specified")

    orig_width, orig_height = image.get_size()

    # both values are provided
    if new_width is not None and new_height is not None:
        return pygame.transform.scale(image, (new_width, new_height))

    # only height is provided
    if new_width is None and new_height is not None:
        ratio = new_height / orig_height
        new_width = int(orig_width * ratio)
    elif new_width is not None and new_height is None:
        ratio = new_width / orig_width
        new_height = int(orig_height * ratio)

    return pygame.transform.scale(image, (new_width, new_height))  # type:ignore
