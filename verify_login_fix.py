#!/usr/bin/env python
"""
Script to verify the login authentication fix.
This demonstrates that authenticate(username=email, password=password) now works correctly.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import Account

print("="*70)
print("LOGIN AUTHENTICATION FIX VERIFICATION")
print("="*70)

# Check if test user exists
try:
    test_user = Account.objects.get(email='admin@example.com')
    print(f"\n✓ Test user found: {test_user.email}")
    print(f"  - Active: {test_user.is_active}")
    print(f"  - Staff: {test_user.is_staff}")
    print(f"  - Superadmin: {test_user.is_superadmin}")
except Account.DoesNotExist:
    print("\n✗ Test user not found!")
    sys.exit(1)

print("\n" + "-"*70)
print("TESTING AUTHENTICATION WITH CORRECT PASSWORD")
print("-"*70)

# Test with correct password
user = authenticate(username='admin@example.com', password='admin123')

if user is not None:
    print("✓ AUTHENTICATION SUCCESSFUL!")
    print(f"  Authenticated user: {user.email}")
    print(f"  User is active: {user.is_active}")
    print(f"\n✓ THE FIX WORKS! Login should now redirect to dashboard.")
else:
    print("✗ AUTHENTICATION FAILED")
    print("  This means either:")
    print("    1. Password is incorrect")
    print("    2. User is not active (is_active=False)")
    print("    3. There's still an issue with the authentication backend")

print("\n" + "-"*70)
print("TESTING AUTHENTICATION WITH WRONG PASSWORD")
print("-"*70)

# Test with wrong password (should fail)
user_wrong = authenticate(username='admin@example.com', password='wrongpassword')

if user_wrong is None:
    print("✓ Correctly rejected wrong password")
else:
    print("✗ WARNING: Accepted wrong password (security issue!)")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
The authentication fix has been applied:
  - Changed: auth.authenticate(email=email, password=password)
  - To: auth.authenticate(username=email, password=password)

Why this works:
  - Your custom Account model uses USERNAME_FIELD = 'email'
  - Django's ModelBackend expects credentials in the 'username' parameter
  - By passing username=email, the backend correctly looks up users by email

Next steps:
  1. The server is already running at http://127.0.0.1:8000/
  2. Visit http://127.0.0.1:8000/account/login/
  3. Login with:
     Email: admin@example.com
     Password: admin123
  4. You should be redirected to the dashboard successfully!
""")
print("="*70)
