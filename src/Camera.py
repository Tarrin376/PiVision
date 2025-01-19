from picamera import PiCamera, Color
from GoogleCloudVisionAPI import GoogleCloudVisionAPI
import time
import io
import base64
import os
import json
import math


class Camera:
    def __init__(self, lcd_backlight):
        self.lcd_backlight = lcd_backlight
        self.vision_api = GoogleCloudVisionAPI(api_key=os.environ.get("API_KEY"))
        
        # Create PiCamera instance and configure the camera settings
        self.camera = PiCamera()
        self.zoom = 0
    
    def update_zoom(self, joystick_val):
        # The new zoom percentage to be applied
        new_zoom = round(min(1, self.zoom + joystick_val * 0.10), 1)
        
        # If the user has chosen to zoom in
        if new_zoom == 1:
            self.camera.zoom = (new_zoom, new_zoom, 0.01, 0.01)
        else:
            self.camera.zoom = (new_zoom, new_zoom, 1 - new_zoom, 1 - new_zoom)
        
        # Update zoom
        self.zoom = new_zoom
    
    def reset_zoom(self):
        self.zoom = 0
    
    def parse_image(self):
        self.camera.stop_preview()
        
        # Take a picture of the current camera state and covert to a byte stream
        image_stream = io.BytesIO()
        self.camera.capture(image_stream, format="jpeg")
        image_stream.seek(0)
        
        self.lcd_backlight.set_text("Parsing image...")
        
        # Read the image from the byte stream and convert to base64 UTF-8 encoding
        image_data = image_stream.read()
        image = base64.b64encode(image_data).decode('utf-8')
        
        return image
    
    def read_image_text(self, image):
        self.lcd_backlight.set_text("Reading image text...")
        
        # Call the Google Vision API to extract text from the image
        result = self.vision_api.request_ocr(image)
        
        self.lcd_backlight.set_text("Done! Please refresh the app.")
        time.sleep(5)
        self.lcd_backlight.set_text("")
        return result

    def write_image_text(self, text):
        json_data = {'text': text}
        # Bind the text.json file to the "./src/static" directory
        json_path = os.path.join("./src/static", 'text.json')
        
        with open(json_path, 'w') as json_file:
            # Add the image text data to the json file
            json.dump(json_data, json_file)
    
    