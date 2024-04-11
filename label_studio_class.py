# Description: This file contains the class for the label studio object

# detection class
class Det:

    DEFAULT_LABEL = "object"
    DEFAULT_LABEL = "object"

    # constructor
    def __init__(self, name: str, x: float, y: float, w: float, h: float):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h