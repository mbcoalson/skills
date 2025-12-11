"""
Test SkySpark API access using session cookie

This script tests API access using the skyarc-auth-80 cookie
obtained from browser login.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://mbcx.iconergyco.com"
COOKIE_NAME = "skyarc-auth-80"
COOKIE_VALUE = "web-jE9i5Wx_hyCZVMs_lSGzbEIGHD6WGyK-1GOArQiwkfk-1c6"

# Projects to test
PROJECTS = ["demo", "default", "db", "site"]

def test_api_with_cookie():
    """Test SkySpark API access using session cookie"""
    print("=" * 70)
    print("SkySpark API Cookie Test")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Cookie: {COOKIE_NAME}")
    print()

    # Create session with cookie
    session = requests.Session()
    session.cookies.set(COOKIE_NAME, COOKIE_VALUE)

    # Test each project
    for project in PROJECTS:
        print(f"\n{'=' * 70}")
        print(f"Testing Project: {project}")
        print('=' * 70)

        # Test 1: About endpoint (server info)
        test_endpoint(
            session,
            f"{BASE_URL}/api/{project}/about",
            "Server Info (about)"
        )

        # Test 2: Ops endpoint (available operations)
        test_endpoint(
            session,
            f"{BASE_URL}/api/{project}/ops",
            "Available Operations (ops)"
        )

        # Test 3: Read endpoint (query data)
        test_endpoint(
            session,
            f"{BASE_URL}/api/{project}/read?limit=1",
            "Read Data (limit 1 record)"
        )

    # Summary
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. If you see successful 200 responses above, the cookie works!")
    print("2. Save this cookie for use in n8n HTTP requests")
    print("3. Add header: Cookie: skyarc-auth-80=<cookie-value>")
    print("=" * 70)

def test_endpoint(session, url, description):
    """Test a single endpoint and print results"""
    print(f"\n{description}")
    print(f"URL: {url}")

    try:
        # Try JSON format first
        response = session.get(
            url,
            headers={"Accept": "application/json"},
            timeout=10
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCCESS!")

            # Try to parse as JSON
            try:
                data = response.json()
                print(f"Response (JSON):")
                print(json.dumps(data, indent=2)[:500])
            except:
                # Not JSON, show as text
                print(f"Response (text):")
                print(response.text[:500])

        elif response.status_code == 401:
            print("UNAUTHORIZED - Cookie may be expired or invalid")

        elif response.status_code == 403:
            print("FORBIDDEN - Access denied")

        else:
            print(f"Response preview: {response.text[:200]}")

    except requests.exceptions.Timeout:
        print("ERROR: Request timeout")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_api_with_cookie()
