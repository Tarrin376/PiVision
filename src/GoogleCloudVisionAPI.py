import requests
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import base64
from io import BytesIO


class GoogleCloudVisionAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://vision.googleapis.com/v1/images:annotate"

    def request_ocr(self, image):
        # JSON request payload
        payload = {
            "requests": [{
                "image": {
                    "content": image
                },
                "features": [{
                    "type": "TEXT_DETECTION"
                }]
            }]
        }
        
        # Send POST request to the Google Cloud Vision API
        url = f"{self.api_url}?key={self.api_key}"
        response = requests.post(url, json=payload)
        
        # If the image failed to be read, raise error
        if response.status_code != 200 or response.json().get("error"):
            raise Exception("Failed to read image.")
        
        # Text found in the image
        result = response.json()["responses"][0]
        
        # If no text was found in the image, raise error
        if not result:
            raise Exception("No readable text found!")
        
        result = result["textAnnotations"][0]
        # Highlight the area where the text in the image was found
        self.highlight_image_text(result, image)
        # Return the text found in the image
        return result["description"]
    
    def highlight_image_text(self, result, image):
        # Get the coordinates of the rectangle that surrounds the found text
        coord = pd.DataFrame(result["boundingPoly"]["vertices"])
        # Get the bottom left corner of the rectangle
        x_min, y_min = np.min(coord["x"]), np.min(coord["y"])
        # Get the bottom right corner of the rectangle
        x_max, y_max = np.max(coord["x"]), np.max(coord["y"])
        
        # Decode the image and create a new Image object to draw rectangle on
        decoded_image = base64.b64decode(image)
        image_stream = BytesIO(decoded_image)
        highlighted_image = Image.open(image_stream)
        
        # Draw a green rectangle around the area where text was found
        draw = ImageDraw.Draw(highlighted_image)
        draw.rectangle((x_min, y_min, x_max, y_max), outline="red", width=4)
        
        # Save the image to the 'static' folder to be read by the web app
        highlighted_image.save("./src/static/image.jpg", format="JPEG")
        
        
        