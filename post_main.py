import hmac
import hashlib
import struct
import time
import base64
import json
import requests
import sys

# =========================================================================
# === 1. CONFIGURATION (VERIFY THESE VALUES) ==============================
# =========================================================================

# The Gist path component (e.g., "Cephei18/0beb7cae7882dd66d289bb524fb9384d").
GIST_PATH = "XXX"

# Fixed user credentials
USER_EMAIL = "gopikachauhan1819@gmail.com"
SOLUTION_LANGUAGE = "python"
SUBMISSION_URL = "https"


# =========================================================================
# === 2. CORE TOTP GENERATION LOGIC =======================================
# =========================================================================

def generate_totp(email):
    """
    Calculates the 10-digit TOTP based on HMAC-SHA-512, X=30, T0=0.
    """
    secret_key = (email + "HENNGECHALLENGE004").encode('ascii') 

    X = 30  # Time step in seconds
    T0 = 0  # Initial Unix Time
    current_time = int(time.time())
    
    # Calculate Time Counter T: (Current Time - T0) / X
    T = int((current_time - T0) / X)
    
    # T must be converted into an 8-byte big-endian integer
    T_bytes = struct.pack('>Q', T)

    # Generate HMAC-SHA-512 Hash (64 bytes long)
    hash_result = hmac.new(secret_key, T_bytes, hashlib.sha512).digest()
    
    # Dynamic Truncation (RFC 4226)
    offset = hash_result[-1] & 0x0F
    truncated_hash = hash_result[offset:offset + 4]
    
    # Convert 4 bytes to an integer (big-endian) and mask sign bit
    otp_value = struct.unpack('>I', truncated_hash)[0] & 0x7FFFFFFF
    
    # Calculate the 10-Digit OTP (Modulo 10^10)
    password = otp_value % 10**10
    
    # Format the password as a 10-digit string with leading zeros
    return f"{password:010}"

def prepare_submission(email, gist_path, lang):
    """
    Generates the TOTP, prepares the headers, and the JSON payload.
    """
    # 1. Generate the TOTP password
    totp = generate_totp(email)

    # 2. Prepare Basic Authentication Header
    auth_string = f"{email}:{totp}"
    encoded_auth = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    auth_header = f"Basic {encoded_auth}"

    # 3. Prepare JSON Payload (Fixed Gist URL construction)
    json_payload = {
        "github_url": f"https://gist.github.com/{gist_path}",
        "contact_email": email,
        "solution_language": lang
    }

    return auth_header, json_payload, totp

def submit_challenge():
    """
    Executes the entire challenge submission process.
    """
    # Prepare the authentication and payload using the GIST_PATH
    auth_header, json_payload, totp = prepare_submission(USER_EMAIL, GIST_PATH, SOLUTION_LANGUAGE)
    
    print("-" * 60)
    print("AUTOMATED MISSION 3 SUBMISSION")
    print("-" * 60)
    print(f"Time of Calculation: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} (Local Time)")
    print(f"Generated TOTP: {totp}")
    print(f"Target URL: {SUBMISSION_URL}")
    print(f"Payload: {json.dumps(json_payload)}")
    print("-" * 60)

    # Set up the headers for the HTTP POST request
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header
    }

    # Execute the POST request
    try:
        print("Sending POST request...")
        response = requests.post(SUBMISSION_URL, headers=headers, json=json_payload, timeout=10)
        
        print("-" * 60)
        print(f"HTTP Status Code: {response.status_code}")
        
        # Print the response body
        try:
            response_json = response.json()
            print(f"Response Body: {json.dumps(response_json, indent=4)}")
        except requests.exceptions.JSONDecodeError:
            print(f"Response Body (Raw): {response.text}")

        if response.status_code == 200:
            print("\nMISSION 3 ACHIEVED SUCCESSFULLY!")
            print("Server returned HTTP 200 OK. Look for the 'Congratulations' message.")
        else:
            print("\nSUBMISSION FAILED. The server returned an error status.")
            print("If Status is 401 (Unauthorized), the TOTP may have expired or the Gist/Email is invalid.")

    except requests.exceptions.RequestException as e:
        print(f"\nFATAL ERROR: Failed to connect or receive response. Exception: {e}", file=sys.stderr)


if __name__ == "__main__":
    submit_challenge()