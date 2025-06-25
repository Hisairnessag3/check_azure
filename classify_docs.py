import requests
import time
import json

API_KEY = ""
ENDPOINT = ""

IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/0/0c/ReceiptSwiss.jpg"

headers = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json"
}
json_body = {"url": IMAGE_URL}

def extract_text():
    url = f"{ENDPOINT}/vision/v3.2/read/analyze"
    response = requests.post(url, headers=headers, json=json_body)
    if response.status_code != 202:
        return None, "Failed to submit OCR"

    operation_url = response.headers.get("Operation-Location")
    for _ in range(10):
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": API_KEY})
        data = result.json()
        if data.get("status") == "succeeded":
            lines = []
            for read_result in data["analyzeResult"]["readResults"]:
                for line in read_result["lines"]:
                    lines.append(line["text"])
            return lines, None
        time.sleep(1)
    return None, "OCR timeout"

def get_tags():
    url = f"{ENDPOINT}/vision/v3.2/tag"
    response = requests.post(url, headers=headers, json=json_body)
    if response.status_code == 200:
        tags = [tag["name"] for tag in response.json().get("tags", [])]
        return tags
    return []

def describe_image():
    url = f"{ENDPOINT}/vision/v3.2/describe"
    response = requests.post(url, headers=headers, json=json_body)
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
    if any(tag in tags for tag in ["receipt", "text", "document"]):
        return "Receipt"
    return "Uncategorized"

def main():
    print("🧾 Extracting text from image...")
    lines, err = extract_text()
    if err:
        print(f"❌ OCR failed: {err}")
        return

    print("\n📝 Extracted Text:")
    for line in lines:
        print("  ", line)

    print("\n🏷️ Getting tags...")
    tags = get_tags()
    print("  Tags:", tags)

    print("\n🖼️ Getting description...")
    description = describe_image()
    print("  Description:", description)

    doc_type = classify_document(tags, lines)
    print(f"\n📂 Classified as: {doc_type}")

    # Simulate routing
    print(f"📦 Routing document to folder: ./docs/{doc_type.lower()}")

if __name__ == "__main__":
    main()
