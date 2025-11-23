import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import authenticate

# Test authentication
email = 'admin@example.com'
password = 'admin123'

print(f"Testing authentication for: {email}")
user = authenticate(username=email, password=password)

if user is not None:
    print(f"✓ Authentication SUCCESSFUL")
    print(f"  User: {user.email}")
    print(f"  Active: {user.is_active}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Superadmin: {user.is_superadmin}")
else:
    print(f"✗ Authentication FAILED")
    print(f"  Possible reasons:")
    print(f"    - Wrong password")
    print(f"    - User not active")
    print(f"    - User doesn't exist")

# Also test with wrong password
print("\n" + "="*50)
print("Testing with wrong password...")
user_wrong = authenticate(username=email, password='wrongpass')
print(f"Result: {'FAILED (as expected)' if user_wrong is None else 'UNEXPECTED SUCCESS'}")
