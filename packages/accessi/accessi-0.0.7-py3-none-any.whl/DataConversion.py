import json
import base64
import numpy as np
from typing import Literal
from datetime import datetime
from types import SimpleNamespace
from src import accessi as Access


def websocket_to_object(websocket_data):
    data = json.dumps(Access.handle_websocket_message(websocket_data))
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def websocket_imagestream_to_image(websocket_data, bit_depth: Literal[8, 16] = 8):
    """
    returns:
        - image: either 8 or 16 bit image as numpy array
        - metadata: the original image metadata
    """
    image = None
    metadata = None
    image_data = websocket_to_object(websocket_data)
    if "imageStream" in image_data:
        image = base64_to_image(image_data[2], bit_depth)
        metadata = image_data[2].value
    return image, metadata


def base64_to_image(imagedata, bit_depth: Literal[8, 16] = 8):
    image = np.frombuffer(base64.b64decode(imagedata.value.image.data), dtype=np.uint16)
    image = np.reshape(image, (imagedata.value.image.dimensions.columns,
                               imagedata.value.image.dimensions.rows))
    if bit_depth == 8:
        image = (image / image.max() * 255).astype(np.uint8)
    elif bit_depth == 16:
        image = image.astype(np.uint16)
    return image
