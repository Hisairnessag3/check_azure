import requests
import json

# === Replace these with your actual values ===
subscription_key = "YOUR_COMPUTER_VISION_KEY"
endpoint = "YOUR_COMPUTER_VISION_ENDPOINT"  # e.g. "https://<region>.api.cognitive.microsoft.com/"
image_url = "https://upload.wikimedia.org/wikipedia/commons/9/99/Black_and_white_portrait_of_a_man.jpg"

# Computer Vision Analyze API URL
analyze_url = f"{endpoint}/vision/v3.2/analyze"

# Parameters for what we want to analyze
params = {
    "visualFeatures": "Description,Faces"
}

# Headers and body
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json"
}
data = {
    "url": image_url
}

# Make request
response = requests.post(analyze_url, headers=headers, params=params, json=data)
response.raise_for_status()
analysis = response.json()

# Print caption
captions = analysis.get("description", {}).get("captions", [])
if captions:
    print(f"Caption: {captions[0]['text']} (Confidence: {captions[0]['confidence']:.2f})")
else:
    print("No caption found.")

# Print face info
faces = analysis.get("faces", [])
if faces:
    print("\nFaces Detected:")
    for face in faces:
        print(f"- Age: {face['age']}, Gender: {face['gender']}, Position: {face['faceRectangle']}")
else:
    print("\nNo faces detected.")
