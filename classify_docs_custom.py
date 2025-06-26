import requests
import time
import json
import os

API_KEY = ""
ENDPOINT = ""
IMAGE_PATH = ""  # ← Change this

headers_binary = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/octet-stream"
}

def read_image_bytes(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found at: {path}")
    with open(path, "rb") as f:
        return f.read()

def extract_text(image_data):
    url = f"{ENDPOINT}/vision/v3.2/read/analyze"
    response = requests.post(url, headers=headers_binary, data=image_data)
    if response.status_code != 202:
        return None, f"Failed OCR submit: {response.text}"
    operation_url = response.headers["Operation-Location"]

    for _ in range(10):
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": API_KEY})
        data = result.json()
        if data.get("status") == "succeeded":
            lines = []
            for page in data["analyzeResult"]["readResults"]:
                for line in page["lines"]:
                    lines.append(line["text"])
            return lines, None
        time.sleep(1)
    return None, "OCR polling timed out."

def get_tags(image_data):
    url = f"{ENDPOINT}/vision/v3.2/tag"
    response = requests.post(url, headers=headers_binary, data=image_data)
    if response.status_code == 200:
        tags = [t["name"] for t in response.json().get("tags", [])]
        return tags
    return []

def describe_image(image_data):
    url = f"{ENDPOINT}/vision/v3.2/describe"
    response = requests.post(url, headers=headers_binary, data=image_data)
    if response.status_code == 200:
        return response.json()["description"]["captions"][0]["text"]
    return "No description."

def classify_document(tags, text_lines):
    text = " ".join(text_lines).lower()
    if "invoice" in text or "amount" in text or "total" in text:
        return "Invoice"
    if "resume" in text or "curriculum vitae" in text:
        return "Resume"
    if "meeting" in text or "agenda" in text:
        return "Meeting Notes"
    if any(tag in tags for tag in ["receipt", "document", "paper"]):
        return "Receipt"
    return "Uncategorized"

def main():
    try:
        image_data = read_image_bytes(IMAGE_PATH)
    except Exception as e:
        print("❌", e)
        return

    print("🧾 Extracting text from image...")
    lines, err = extract_text(image_data)
    if err:
        print("❌", err)
        return

    print("\n📝 Extracted Text:")
    for line in lines:
        print("  ", line)

    print("\n🏷️ Getting tags...")
    tags = get_tags(image_data)
    print("  Tags:", tags)

    print("\n🖼️ Getting description...")
    description = describe_image(image_data)
    print("  Description:", description)

    doc_type = classify_document(tags, lines)
    print(f"\n📂 Classified as: {doc_type}")
    print(f"📦 Routing document to: ./docs/{doc_type.lower()}")

if __name__ == "__main__":
    main()
