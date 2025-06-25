import requests
import time
import json

API_KEY = ""
ENDPOINT = ""

headers = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json"
}

image_sources = {
    "analyze_image": "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/waterfall.jpg",
    "describe_image": "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/dice.png",
    "tag_image": "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/pumpkin.jpg",
    "read_ocr": "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/newspaper.jpg",
    "detect_brands": "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/starbucks.jpg"
}

def post_json(endpoint_path, image_key, params=None):
    url = f"{ENDPOINT}{endpoint_path}"
    json_body = {"url": image_sources[image_key]}
    response = requests.post(url, headers=headers, json=json_body, params=params)
    return response

def analyze_image():
    response = post_json("/vision/v3.2/analyze", "analyze_image", {
        "visualFeatures": "Categories,Description,Color,Objects,Faces,ImageType,Brands,Tags",
        "details": "Landmarks",
        "language": "en"
    })
    print_json("Analyze Image", response)

def describe_image():
    response = post_json("/vision/v3.2/describe", "describe_image")
    print_json("Describe Image", response)

def tag_image():
    response = post_json("/vision/v3.2/tag", "tag_image")
    print_json("Tag Image", response)

def detect_domain(domain):
    response = post_json(f"/vision/v3.2/models/{domain}/analyze", f"detect_{domain}")
    print_json(f"Detect Domain - {domain.title()}", response)

def generate_thumbnail():
    url = f"{ENDPOINT}/vision/v3.2/generateThumbnail"
    json_body = {"url": image_sources["generate_thumbnail"]}
    response = requests.post(url, headers=headers, json=json_body, params={
        "width": 100,
        "height": 100,
        "smartCropping": "true"
    })
    print(f"\n=== Generate Thumbnail ===\nThumbnail bytes received: {len(response.content)}")

def area_of_interest():
    response = post_json("/vision/v3.2/areaOfInterest", "area_of_interest")
    print_json("Area of Interest", response)

def read_ocr():
    url = f"{ENDPOINT}/vision/v3.2/read/analyze"
    json_body = {"url": image_sources["read_ocr"]}
    response = requests.post(url, headers=headers, json=json_body)
    if response.status_code != 202:
        print_json("OCR (Read)", response)
        return

    operation_url = response.headers.get("Operation-Location")
    print(f"\n=== OCR: submitted. Polling at {operation_url} ===")
    for _ in range(10):
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": API_KEY})
        data = result.json()
        if data.get("status") in ["succeeded", "failed"]:
            print_json("OCR (Read Result)", result)
            return
        time.sleep(1)
    print("OCR timed out.")

def detect_brands():
    response = post_json("/vision/v3.2/analyze", "detect_brands", {
        "visualFeatures": "Brands"
    })
    print_json("Detect Brands", response)
def print_json(title, response):
    print(f"\n=== {title} ===")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error parsing JSON:", e)
        print(response.text)

if __name__ == "__main__":
    analyze_image()
    describe_image()
    tag_image()
    detect_brands()
    read_ocr()
