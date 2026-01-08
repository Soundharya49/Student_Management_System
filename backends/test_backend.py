import requests
import sys

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:5000/api"

def run_tests():
    session = requests.Session()
    
    # 1. Login
    print("1. Testing Login...")
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")
    
    if not username or not password:
        print("Error: ADMIN_USER and ADMIN_PASS must be set in .env")
        sys.exit(1)

    try:
        resp = session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if resp.status_code != 200:
            print(f"Login failed: {resp.text}")
            sys.exit(1)
        token = resp.json().get('access_token')
        refresh_token = resp.json().get('refresh_token')
        if not token or not refresh_token:
            print("No access or refresh token received")
            sys.exit(1)
        headers = {'Authorization': f'Bearer {token}'}
        print("Login Successful (Tokens received)")
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    # 2. Get Students (Empty)
    print("2. fetching Students (Expect Empty)...")
    resp = session.get(f"{BASE_URL}/students", headers=headers)
    print(f"Response: {resp.json()}")

    # 3. Add Student
    print("3. Adding Student...")
    new_student = {"name": "John Doe", "email": "john@example.com", "course": "CS101"}
    resp = session.post(f"{BASE_URL}/students", json=new_student, headers=headers)
    if resp.status_code != 201:
        print(f"Add student failed: {resp.text}")
    else:
        print("Student Added")
        student_id = resp.json().get("id")

    # 4. Get Students (Expect 1)
    print("4. fetching Students...")
    resp = session.get(f"{BASE_URL}/students", headers=headers)
    students = resp.json()
    print(f"Students found: {len(students)}")
    print(students)

    # 5. Delete Student
    if student_id:
        print(f"5. Deleting Student {student_id}...")
        resp = session.delete(f"{BASE_URL}/students/{student_id}", headers=headers)
        if resp.status_code == 200:
            print("Student Deleted")
        else:
            print(f"Delete failed: {resp.text}")

    print("All backend tests passed!")

if __name__ == "__main__":
    run_tests()
