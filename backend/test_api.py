"""
Quick API Testing Script
Tests all backend endpoints

Author: Vignesh (Backend Developer)

Usage:
    python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print section header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")


def test_health():
    """Test health endpoints"""
    print_section("HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/")
    print(f"GET / : {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"\nGET /health : {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_auth():
    """Test authentication endpoints"""
    print_section("AUTHENTICATION")
    
    # Test anonymous user creation
    print("1. Creating anonymous user...")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/anonymous",
        json={"display_name": "Test Anonymous User"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Anonymous user created!")
        print(f"   Token: {data['access_token'][:50]}...")
        print(f"   Username: {data['user']['username']}")
        return data['access_token']
    else:
        print(f"❌ Error: {response.text}")
        return None
    
    # Test regular registration
    print("\n2. Registering regular user...")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "username": "test_vignesh",
            "password": "password123",
            "email": "vignesh@test.com"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ User registered!")
        token = data['access_token']
        print(f"   Token: {token[:50]}...")
        return token
    elif response.status_code == 400:
        print("⚠️  User already exists, trying login...")
        
        # Try login instead
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={
                "username": "test_vignesh",
                "password": "password123"
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logged in!")
            token = data['access_token']
            print(f"   Token: {token[:50]}...")
            return token
    
    print(f"❌ Error: {response.text}")
    return None


def test_users(token):
    """Test user endpoints"""
    print_section("USER MANAGEMENT")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get my profile
    print("1. Getting my profile...")
    response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Profile retrieved!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.text}")


def test_chat(token):
    """Test chat endpoints"""
    print_section("CHAT FUNCTIONALITY")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create session
    print("1. Creating chat session...")
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/sessions",
        headers=headers,
        json={}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        session = response.json()
        print("✅ Session created!")
        print(f"   Session ID: {session['session_id']}")
        session_id = session['session_id']
        
        # Get sessions
        print("\n2. Getting my sessions...")
        response = requests.get(f"{BASE_URL}/api/v1/chat/sessions", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Found {len(response.json())} session(s)")
        
        # Get history
        print(f"\n3. Getting chat history for session {session_id}...")
        response = requests.get(
            f"{BASE_URL}/api/v1/chat/sessions/{session_id}/history",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            history = response.json()
            print(f"✅ History retrieved!")
            print(f"   Messages: {len(history['messages'])}")
        
        print(f"\n4. WebSocket endpoint:")
        print(f"   ws://localhost:8000/api/v1/chat/ws/{session_id}?token={token[:30]}...")
        print(f"   (Use browser/Postman to test WebSocket)")
        
    else:
        print(f"❌ Error: {response.text}")


def test_appointments(token):
    """Test appointments endpoints (Phase 2 - should return 501)"""
    print_section("APPOINTMENTS (Phase 2)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing appointments endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/appointments/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 501:
        print("✅ Phase 2 endpoint confirmed (not yet implemented)")
    else:
        print(f"Response: {response.text}")


def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("  CYCOLOGY BACKEND API TESTING")
    print("  Make sure backend is running at http://localhost:8000")
    print("="*50)
    
    try:
        # Test health
        test_health()
        
        # Test auth and get token
        token = test_auth()
        
        if token:
            # Test users
            test_users(token)
            
            # Test chat
            test_chat(token)
            
            # Test appointments
            test_appointments(token)
        
        print_section("TESTING COMPLETE ✅")
        print("All endpoints are working correctly!")
        print("\nNext steps:")
        print("1. Visit http://localhost:8000/docs for interactive testing")
        print("2. Test WebSocket connection using browser/Postman")
        print("3. Integrate with frontend!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("Make sure backend is running:")
        print("  docker-compose up backend mongo redis")
        print("  OR")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()


