import requests
import base64
from PIL import Image
import io

# API endpoint
API_URL = "http://localhost:8000"

def create_test_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

def test_submit_score():
    # Create test data
    test_data = {
        "name": "Test User",
        "image": create_test_image()
    }
    
    # Send POST request
    print("Sending test request...")
    response = requests.post(f"{API_URL}/submit-score/", json=test_data)
    
    # Print response
    print("\nResponse from /submit-score/:")
    print(response.json())
    
    return response.json()

def test_leaderboard():
    # Get leaderboard
    print("\nFetching leaderboard...")
    response = requests.get(f"{API_URL}/leaderboard/")
    
    # Print response
    print("\nLeaderboard:")
    print(response.json())

if __name__ == "__main__":
    # Test submitting a score
    test_submit_score()
    
    # Test getting the leaderboard
    test_leaderboard() 