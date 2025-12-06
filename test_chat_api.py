#!/usr/bin/env python3
"""Test the chat API endpoint"""

import requests
import json
import sys

# Configuration
API_URL = "http://localhost:8000"
EMAIL = "chattest@example.com"
PASSWORD = "Test123!@#"

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{API_URL}/api/v1/auth/login",
        data={
            "username": EMAIL,
            "password": PASSWORD
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    data = response.json()
    print(f"✅ Login successful")
    return data["access_token"]

def test_chat_stream(token):
    """Test the chat streaming endpoint"""
    print("\n💬 Testing chat stream endpoint...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Current-Org": "1"
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Say hello in 5 words"
            }
        ],
        "model": "gemini-2.0-flash",
        "stream": True
    }
    
    print(f"📤 Sending request to: {API_URL}/api/v1/ai/chat/stream")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/ai/chat/stream",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print("\n📨 Streaming response:")
        print("-" * 50)
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print(decoded)
                
                if decoded.startswith("data: "):
                    data = decoded[6:].strip()
                    if data and data != "[DONE]":
                        full_response += data
        
        print("-" * 50)
        print(f"\n✅ Full response: {full_response}")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_non_stream(token):
    """Test the non-streaming chat endpoint"""
    print("\n💬 Testing non-streaming chat endpoint...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Current-Org": "1"
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Say hello in 3 words"
            }
        ],
        "model": "gemini-2.0-flash",
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/ai/chat",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        print(f"✅ Response: {json.dumps(data, indent=2)}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Chat API Tests\n")
    
    # Login
    token = login()
    
    # Test streaming
    stream_success = test_chat_stream(token)
    
    # Test non-streaming
    non_stream_success = test_chat_non_stream(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"  Streaming: {'✅ PASS' if stream_success else '❌ FAIL'}")
    print(f"  Non-streaming: {'✅ PASS' if non_stream_success else '❌ FAIL'}")
    print("=" * 50)
    
    sys.exit(0 if (stream_success and non_stream_success) else 1)
