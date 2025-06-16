import requests

# Replace with your Azure endpoint and key
endpoint = ""
subscription_key = ""

# A valid image URL (JPEG)
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Fronalpstock_big.jpg/800px-Fronalpstock_big.jpg"

# Endpoint for image analysis
url = endpoint + "vision/v3.2/analyze"

headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json"
}

params = {
    "visualFeatures": "Categories"
}

data = {
    "url": image_url
}

try:
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        print("✅ Endpoint is active and responded successfully.")
        print("response:",response.json())
    else:
        print(f"⚠️ Endpoint responded with status code {response.status_code}")
        print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Failed to connect to endpoint:", e)
