"""
Generate a secure secret key for Flask application
Run this script to generate a secure secret key for production
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("🔐 Generated Secure Secret Key:")
    print("-" * 50)
    print(secret_key)
    print("-" * 50)
    print("\n📋 Set this as your SECRET_KEY environment variable in Railway:")
    print(f"SECRET_KEY={secret_key}")
    print("\n⚠️  Keep this key secure and never commit it to version control!")
