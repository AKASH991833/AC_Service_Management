"""
Test Script - Submit test data to check admin panel
"""
import requests
import json
import os

# Set encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

API_BASE = 'http://localhost:5000/api'
API_KEY = 'ansh_aircool_secure_api_key_2026_change_in_production'

headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': API_KEY
}

print("=" * 60)
print("TESTING: Submitting Test Data")
print("=" * 60)

# Test 1: Submit Service Request
print("\n1. Submitting Service Request...")
service_request_data = {
    "name": "Rajesh Kumar",
    "phone": "9876543210",
    "email": "rajesh@example.com",
    "address": "123 MG Road, Andheri West, Mumbai - 400058",
    "serviceType": "installation",
    "acType": "Split",
    "preferredDate": "2026-03-10",
    "timeSlot": "morning",
    "message": "Need installation for 1.5 ton split AC in living room"
}

try:
    response = requests.post(f'{API_BASE}/service-request', 
                           json=service_request_data, 
                           headers=headers)
    result = response.json()
    
    if response.status_code == 201:
        print("   [SUCCESS] Service Request Submitted!")
        print(f"   Request ID: {result['data']['requestId']}")
    else:
        print(f"   [FAILED] {result.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   [ERROR] {str(e)}")

# Test 2: Submit Contact Form
print("\n2. Submitting Contact Form...")
contact_data = {
    "name": "Priya Sharma",
    "phone": "9123456789",
    "email": "priya@example.com",
    "address": "456 Linking Road, Bandra, Mumbai",
    "serviceType": "repair",
    "acType": "Window",
    "message": "My window AC is making strange noise. Need urgent repair."
}

try:
    response = requests.post(f'{API_BASE}/contact', 
                           json=contact_data, 
                           headers=headers)
    result = response.json()
    
    if response.status_code == 201:
        print("   [SUCCESS] Contact Form Submitted!")
        print(f"   Message ID: {result['data']['messageId']}")
    else:
        print(f"   [FAILED] {result.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   [ERROR] {str(e)}")

# Test 3: Submit Another Service Request
print("\n3. Submitting Another Service Request...")
service_request_data2 = {
    "name": "Amit Patel",
    "phone": "9988776655",
    "email": "amit@example.com",
    "address": "789 Carter Road, Bandra West, Mumbai - 400050",
    "serviceType": "gas",
    "acType": "Split",
    "preferredDate": "2026-03-12",
    "timeSlot": "afternoon",
    "message": "AC gas leak issue. Need gas refill urgently."
}

try:
    response = requests.post(f'{API_BASE}/service-request', 
                           json=service_request_data2, 
                           headers=headers)
    result = response.json()
    
    if response.status_code == 201:
        print("   [SUCCESS] Service Request Submitted!")
        print(f"   Request ID: {result['data']['requestId']}")
    else:
        print(f"   [FAILED] {result.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   [ERROR] {str(e)}")

# Test 4: Submit Another Contact Form
print("\n4. Submitting Another Contact Form...")
contact_data2 = {
    "name": "Sneha Desai",
    "phone": "9765432100",
    "email": "sneha@example.com",
    "address": "321 SV Road, Dadar, Mumbai",
    "serviceType": "amc",
    "acType": "Split",
    "message": "Interested in AMC plan for 2 split ACs."
}

try:
    response = requests.post(f'{API_BASE}/contact', 
                           json=contact_data2, 
                           headers=headers)
    result = response.json()
    
    if response.status_code == 201:
        print("   [SUCCESS] Contact Form Submitted!")
        print(f"   Message ID: {result['data']['messageId']}")
    else:
        print(f"   [FAILED] {result.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   [ERROR] {str(e)}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nTest data submitted successfully!")
print("\nNow check Admin Panel:")
print("   URL: http://localhost:5500/admin/index.html")
print("   Username: admin")
print("   Password: admin123")
print("\nYou should see:")
print("   - 2 Service Requests")
print("   - 2 Contact Messages")
print("=" * 60)
