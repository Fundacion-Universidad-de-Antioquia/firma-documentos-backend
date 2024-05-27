import base64
import io
from PIL import Image

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
    

def base64_to_image(base64_data):
    decoded_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(decoded_data))

    # Save image to file in public folder, the name is the CC
    image.save("public/.png", "PNG")

    return image