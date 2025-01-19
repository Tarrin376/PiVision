import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
api_key = os.environ.get("API_KEY")

def test_ocr(image):
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
    
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    response = requests.post(url, json=payload)

    if response.status_code != 200 or response.json().get("error"):
        print("Error occurred.")
    
    print(response.json()["responses"][0]["textAnnotations"][0]["description"])

with open('test_image.jpg', 'rb') as img_file:
    img_data = img_file.read()
    # Convert the image data to base64
    image = base64.b64encode(img_data).decode('utf-8')
    test_ocr(image)