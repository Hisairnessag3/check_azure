from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os

# === Replace with your actual key and endpoint ===
subscription_key = "YOUR_COMPUTER_VISION_KEY"
endpoint = "YOUR_COMPUTER_VISION_ENDPOINT"

# Sample image URL (can also be a local file)
image_url = "https://upload.wikimedia.org/wikipedia/commons/9/99/Black_and_white_portrait_of_a_man.jpg"

# Authenticate client
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Analyze image with description and face detection
features = [VisualFeatureTypes.description, VisualFeatureTypes.faces]
analysis = client.analyze_image(image_url, visual_features=features)

# Caption output
if analysis.description and analysis.description.captions:
    caption = analysis.description.captions[0]
    print(f"Caption: {caption.text} (Confidence: {caption.confidence:.2f})")
else:
    print("No caption found.")

# Face detection output
if analysis.faces:
    print("\nFaces Detected:")
    for face in analysis.faces:
        print(f"- Age: {face.age}, Gender: {face.gender}, Position: {face.face_rectangle}")
else:
    print("\nNo faces detected.")
