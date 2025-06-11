import requests
import json

def check_computer_vision_service(endpoint, subscription_key):
    """
    Check if Azure Computer Vision service is accessible
    
    Args:
        endpoint (str): Your Azure Computer Vision endpoint URL
        subscription_key (str): Your subscription key
    
    Returns:
        bool: True if service is accessible, False otherwise
    """
    
    # Construct the URL for a simple analyze operation
    analyze_url = f"{endpoint}/vision/v3.2/analyze"
    
    # Headers
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }
    
    # This is Microsoft's sample image URL for testing
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
    
    data = {
        'url': test_image_url
    }
    
    # Parameters for basic analysis
    params = {
        'visualFeatures': 'Categories'
    }
    
    try:
        response = requests.post(analyze_url, headers=headers, params=params, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Computer Vision service is accessible!")
            print(f"Response status: {response.status_code}")
            return True
        else:
            print(f"❌ Service returned status code: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Replace with your actual endpoint and key
    ENDPOINT = "https://your-resource-name.cognitiveservices.azure.com/"
    SUBSCRIPTION_KEY = "your-subscription-key-here"
    
    # Check service availability
    is_accessible = check_computer_vision_service(ENDPOINT, SUBSCRIPTION_KEY)
    
    if is_accessible:
        print("Service is ready to use!")
    else:
        print("Please check your endpoint and subscription key.")