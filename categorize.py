import os
import requests
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Replace with your Azure Computer Vision details
API_KEY = ""
ENDPOINT = ""
# API endpoint
VISION_ANALYZE_URL = AZURE_ENDPOINT + "vision/v3.2/analyze"
HEADERS = {
    'Ocp-Apim-Subscription-Key': AZURE_KEY,
    'Content-Type': 'application/json'
}
PARAMS = {
    'visualFeatures': 'Tags,Description'
}

# Examples
image_urls = [
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/data/house.JPG",
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/data/flower.jpg",
    "https://raw.githubusercontent.com/Hisairnessag3/check_azure/refs/heads/main/data/dog.jpg"
]

output_dir = "categorized_images"
os.makedirs(output_dir, exist_ok=True)


def categorize_and_caption_image(image_url):
    # Analyze the image
    response = requests.post(VISION_ANALYZE_URL, headers=HEADERS, params=PARAMS, json={"url": image_url})
    response.raise_for_status()
    analysis = response.json()

    # Extract the tag with the highest confidence
    tags = analysis.get("tags", [])
    if tags:
        best_tag = max(tags, key=lambda tag: tag.get("confidence", 0.0))
        main_tag = best_tag.get("name", "uncategorized")
        confidence = best_tag.get("confidence", 0.0)
    else:
        main_tag = "uncategorized"
        confidence = 0.0

    # Get caption
    caption = analysis.get("description", {}).get("captions", [{}])[0].get("text", "No caption")

    # Create folder based on main tag
    tag_dir_path = os.path.join(output_dir, main_tag)
    os.makedirs(tag_dir_path, exist_ok=True)

    # Download and save image
    img_name = os.path.basename(urlparse(image_url).path)
    img_path = os.path.join(tag_dir_path, img_name)
    urlretrieve(image_url, img_path)

    # Save caption
    caption_filename = f"{os.path.splitext(img_name)[0]}_caption.txt"
    caption_path = os.path.join(tag_dir_path, caption_filename)
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(f"Caption: {caption}\n")
        f.write(f"Main Tag: {main_tag} (confidence: {confidence:.2f})")

    print(f"[{main_tag}] Saved {img_name} with caption and confidence: {confidence:.2f}")


for url in image_urls:
    try:
        categorize_and_caption_image(url)
    except Exception as e:
        print(f"Failed to process {url}: {e}")
