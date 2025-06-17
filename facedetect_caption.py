import requests



# === Replace these with your actual values ===
subscription_key = ""
endpoint = ""


images = ["https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Fronalpstock_big.jpg/800px-Fronalpstock_big.jpg",
          "https://upload.wikimedia.org/wikipedia/commons/f/f4/Bulgarian_national_football_team.JPG",
          "https://upload.wikimedia.org/wikipedia/commons/4/46/2023_MMA_IVE.jpg"]
analyze_url = f"{endpoint}/vision/v3.2/analyze"
params = {"visualFeatures": "Description,Faces"}
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json"
}
idx = 1
for image in images:
    data = {"url": image}
    print("image "+str(idx))
    response = requests.post(analyze_url, headers=headers, params=params, json=data)
    response.raise_for_status()  # Will raise an error if status != 200

    analysis = response.json()

    # Caption
    captions = analysis.get("description", {}).get("captions", [])
    if captions:
        print(f"Caption: {captions[0]['text']} (Confidence: {captions[0]['confidence']:.2f})")
    else:
        print("No caption found.")

    # Faces
    faces = analysis.get("faces", [])
    if faces:
        print("\nFaces Detected:")
        for face in faces:
            face_rect = face.get('faceRectangle', {})
            print(f"Position: {face_rect}")
    else:
        print("\nNo faces detected.")
    idx +=1
