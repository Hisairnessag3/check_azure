import requests
import time

# Replace with your actual values
endpoint = ""
subscription_key = ""

# Use full endpoint URL for OCR and Object Detection
ocr_url = endpoint + "vision/v3.2/read/analyze"
analyze_url = endpoint + "vision/v3.2/analyze?visualFeatures=Objects"

# List of image URLs or local paths (can be local files or URLs)
image_urls = [
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/v.jpg",
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/building.png",
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/toy.jpg"
]

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-Type': 'application/json'
}

def run_ocr(image_url):
    response = requests.post(ocr_url, headers=headers, json={"url": image_url})
    if response.status_code != 202:
        print("OCR request failed:", response.json())
        return

    operation_url = response.headers["Operation-Location"]

    # Poll for result
    while True:
        result = requests.get(operation_url, headers={'Ocp-Apim-Subscription-Key': subscription_key})
        result_json = result.json()
        if result_json.get("status") == "succeeded":
            print("🔍 OCR Result:")
            for read_result in result_json["analyzeResult"]["readResults"]:
                for line in read_result["lines"]:
                    print(line["text"])
            break
        elif result_json.get("status") == "failed":
            print("OCR failed.")
            break
        time.sleep(1)

def run_object_detection(image_url):
    response = requests.post(analyze_url, headers=headers, json={"url": image_url})
    if response.status_code != 200:
        print("Object detection failed:", response.json())
        return

    result = response.json()
    print("📦 Object Detection:")
    for obj in result.get("objects", []):
        print(f"{obj['object']} ({obj['confidence']*100:.1f}%)")

# Run OCR and Object Detection on each image
for url in image_urls:
    print("\n=== Processing:", url)
    run_ocr(url)
    run_object_detection(url)
